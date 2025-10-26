#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sistema de Planejamento de Estudos - UAB LEI
Backend Flask API
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sistema de Planejamento de Estudos - UAB LEI
Backend Flask API
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Acessar as variáveis
openai_api_key = os.environ.get("OPENAI_API_KEY")
moodle_username = os.environ.get("MOODLE_USERNAME")
moodle_password = os.environ.get("MOODLE_PASSWORD")

# Usar as variáveis
print(f"Chave OpenAI: {openai_api_key}")

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from datetime import datetime, timedelta
import pytz
import json
import os
from pathlib import Path
import sqlite3
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

try:
    from moodle_integration import MoodleUAB, quick_sync

    MOODLE_AVAILABLE = True
except ImportError:
    MOODLE_AVAILABLE = False
    print("⚠️ Módulo Moodle não disponível")

try:
    from ai_assistant import AIAssistant

    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("⚠️ Módulo IA não disponível")

try:
    from folder_sync import FolderSyncManager

    FOLDER_SYNC_AVAILABLE = True
except ImportError:
    FOLDER_SYNC_AVAILABLE = False
    print("⚠️ Módulo Folder Sync não disponível")

try:
    from copilot_agent import CopilotAgent

    COPILOT_AVAILABLE = True
except ImportError:
    COPILOT_AVAILABLE = False
    print("⚠️ Módulo Copilot Studio não disponível")

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "estudos.db"

moodle_client = None
ai_assistant = None
folder_sync_manager = None
copilot_agents = {
    'AC': None,  # Arquitetura de Computadores
    'FBD': None, # Fundamentos de Bases de Dados
    'LC': None,  # Linguagens e Computação
    'PO': None,  # Programação por Objetos
    'SR': None,  # Sistemas em Rede
    'SC': None,  # Sistemas Computacionais
    'EPE': None  # Ética e Práticas de Engenharia
}


def init_db():
    """Inicializa o banco de dados SQLite"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessoes_estudo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disciplina_id TEXT NOT NULL,
            data DATE NOT NULL,
            hora_inicio TIME NOT NULL,
            hora_fim TIME,
            duracao_minutos INTEGER,
            topico TEXT,
            notas TEXT,
            concluido BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progresso_topicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disciplina_id TEXT NOT NULL,
            topico_numero INTEGER NOT NULL,
            progresso_percentual INTEGER DEFAULT 0,
            ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(disciplina_id, topico_numero)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disciplina_id TEXT NOT NULL,
            titulo TEXT NOT NULL,
            descricao TEXT,
            tipo TEXT,
            data_entrega DATE,
            prioridade INTEGER DEFAULT 2,
            concluida BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metas_diarias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data DATE NOT NULL UNIQUE,
            meta_horas REAL DEFAULT 3.0,
            horas_estudadas REAL DEFAULT 0.0,
            disciplinas_estudadas TEXT,
            notas TEXT
        )
    """)

    conn.commit()
    conn.close()


def load_disciplinas() -> Dict:
    """Carrega os dados das disciplinas do arquivo JSON"""
    json_path = DATA_DIR / "disciplinas.json"
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_db_connection():
    """Obtém conexão com o banco de dados"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def calcular_semana_atual() -> int:
    """Calcula a semana atual do semestre baseado na data de Lisboa"""
    lisboa_tz = pytz.timezone("Europe/Lisbon")

    data_inicio = lisboa_tz.localize(datetime(2025, 9, 29, 0, 0, 0))

    hoje = datetime.now(lisboa_tz)

    delta = hoje - data_inicio
    semana = delta.days // 7

    semana = max(0, min(semana, 14))

    return semana


def converter_data_portuguesa(data_str: str) -> str:
    """Converte data no formato 'DD mês' para 'YYYY-MM-DD'"""
    meses = {
        "janeiro": 1,
        "fevereiro": 2,
        "março": 3,
        "abril": 4,
        "maio": 5,
        "junho": 6,
        "julho": 7,
        "agosto": 8,
        "setembro": 9,
        "outubro": 10,
        "novembro": 11,
        "dezembro": 12,
    }

    if not data_str or "-" in data_str:
        return data_str

    try:
        partes = data_str.lower().split()
        if len(partes) == 2:
            dia = int(partes[0])
            mes_nome = partes[1]

            if mes_nome in meses:
                mes = meses[mes_nome]
                ano = 2025 if mes >= 9 else 2026

                return f"{ano}-{mes:02d}-{dia:02d}"
    except:
        pass

    return data_str


# ============ INICIALIZAÇÃO DOS AGENTES COPILOT ============

def init_copilot_agents():
    """Inicializa todos os agentes Copilot disponíveis"""
    if not COPILOT_AVAILABLE:
        print("⚠️ Módulo Copilot não disponível")
        return

    for agent_name in copilot_agents.keys():
        try:
            agent = CopilotAgent(agent_name)
            if agent.secret:
                copilot_agents[agent_name] = agent
                print(f"✓ Agente {agent_name} inicializado com sucesso")
            else:
                print(f"⚠️ Secret não encontrado para agente {agent_name}")
        except Exception as e:
            print(f"❌ Erro ao inicializar agente {agent_name}: {str(e)}")

# Chamar na inicialização
init_copilot_agents()


@app.route("/")
def index():
    """Rota principal - serve o frontend"""
    frontend_path = BASE_DIR / "frontend" / "index.html"
    if frontend_path.exists():
        with open(frontend_path, 'r', encoding='utf-8') as f:
            return f.read()

    # Se não encontrar o arquivo, retorna informações da API
    return jsonify(
        {
            "nome": "Sistema de Planejamento de Estudos UAB LEI",
            "versao": "1.0.0",
            "endpoints": {
                "disciplinas": "/api/disciplinas",
                "calendario": "/api/calendario",
                "sessoes": "/api/sessoes",
                "progresso": "/api/progresso",
                "tarefas": "/api/tarefas",
                "dashboard": "/api/dashboard",
            },
        }
    )


@app.route("/<path:filename>")
def serve_static(filename):
    """Serve arquivos estáticos do frontend"""
    frontend_dir = BASE_DIR / "frontend"
    file_path = frontend_dir / filename

    # Verificar se o arquivo existe e está dentro do diretório frontend
    try:
        if file_path.exists() and file_path.is_file():
            if filename.endswith('.css'):
                return send_from_directory(str(frontend_dir), filename, mimetype='text/css')
            elif filename.endswith('.js'):
                return send_from_directory(str(frontend_dir), filename, mimetype='application/javascript')
            elif filename.endswith('.html'):
                return send_from_directory(str(frontend_dir), filename, mimetype='text/html')
            else:
                return send_from_directory(str(frontend_dir), filename)
    except:
        pass

    return jsonify({"error": "Arquivo não encontrado"}), 404


@app.route("/api/disciplinas", methods=["GET"])
def get_disciplinas():
    """Lista todas as disciplinas com progresso"""
    data = load_disciplinas()
    conn = get_db_connection()

    # Adicionar progresso a cada disciplina
    for disc in data["disciplinas"]:
        disc_id = disc["id"]

        # Calcular progresso baseado em tempo de estudo (pomodoros)
        sessoes = conn.execute(
            "SELECT COUNT(*) as total FROM sessoes_estudo WHERE disciplina_id = ?",
            (disc_id,)
        ).fetchone()

        total_sessoes = sessoes["total"] or 0
        total_minutos = total_sessoes * 25
        creditos = disc.get("creditos", 6)

        # Progresso de tempo
        progresso_tempo = min((total_minutos / (creditos * 26 * 60)) * 100, 100) if total_minutos > 0 else 0

        # Calcular progresso de AFs
        afs = conn.execute(
            """SELECT COUNT(*) as total, SUM(CASE WHEN concluida = 1 THEN 1 ELSE 0 END) as concluidas
               FROM tarefas WHERE disciplina_id = ? AND tipo = 'forum'""",
            (disc_id,)
        ).fetchone()

        total_afs = afs["total"] or 0
        afs_concluidas = afs["concluidas"] or 0
        progresso_afs = (afs_concluidas / total_afs * 100) if total_afs > 0 else 0

        # Progresso final
        if total_afs > 0:
            progresso_final = (progresso_tempo * 0.7) + (progresso_afs * 0.3)
        else:
            progresso_final = progresso_tempo

        disc["progresso"] = round(progresso_final, 2)

    conn.close()
    return jsonify(data["disciplinas"])


@app.route("/api/disciplinas/<disciplina_id>", methods=["GET"])
def get_disciplina(disciplina_id):
    """Obtém detalhes de uma disciplina específica"""
    data = load_disciplinas()
    disciplina = next(
        (d for d in data["disciplinas"] if d["id"] == disciplina_id), None
    )
    if disciplina:
        return jsonify(disciplina)
    return jsonify({"error": "Disciplina não encontrada"}), 404


@app.route("/api/calendario", methods=["GET"])
def get_calendario():
    """Retorna o calendário semanal de estudos"""
    data = load_disciplinas()
    semana_atual = calcular_semana_atual()

    return jsonify(
        {
            "semana_atual": semana_atual,
            "calendario_semanal": data["calendario_semanal"],
            "horas_totais_semana": data["horas_totais_semana"],
            "meta_diaria": data["meta_diaria"],
        }
    )


@app.route("/api/calendario/dia/<dia_semana>", methods=["GET"])
def get_calendario_dia(dia_semana):
    """Retorna o calendário de um dia específico"""
    data = load_disciplinas()
    dia_lower = dia_semana.lower()

    if dia_lower not in data["calendario_semanal"]:
        return jsonify({"error": "Dia da semana inválido"}), 400

    calendario_dia = data["calendario_semanal"][dia_lower]
    disciplinas_do_dia = []

    for item in calendario_dia["distribuicao"]:
        if "disciplina" in item and item["disciplina"] not in ["REVISAO", "E_FOLIOS"]:
            disc = next(
                (d for d in data["disciplinas"] if d["sigla"] == item["disciplina"]),
                None,
            )
            if disc:
                disciplinas_do_dia.append(
                    {"disciplina": disc, "horario": f"{item['inicio']} - {item['fim']}"}
                )

    return jsonify(
        {
            "dia": dia_semana,
            "horario_geral": calendario_dia["horario"],
            "distribuicao": calendario_dia["distribuicao"],
            "disciplinas": disciplinas_do_dia,
        }
    )


@app.route("/api/sessoes", methods=["GET", "POST"])
def handle_sessoes():
    """Gerencia sessões de estudo"""
    if request.method == "GET":
        data_inicio = request.args.get("data_inicio")
        data_fim = request.args.get("data_fim")
        disciplina_id = request.args.get("disciplina_id")

        conn = get_db_connection()
        query = "SELECT * FROM sessoes_estudo WHERE 1=1"
        params = []

        if data_inicio:
            query += " AND data >= ?"
            params.append(data_inicio)
        if data_fim:
            query += " AND data <= ?"
            params.append(data_fim)
        if disciplina_id:
            query += " AND disciplina_id = ?"
            params.append(disciplina_id)

        query += " ORDER BY data DESC, hora_inicio DESC"

        sessoes = conn.execute(query, params).fetchall()
        conn.close()

        return jsonify([dict(s) for s in sessoes])

    elif request.method == "POST":
        dados = request.json

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO sessoes_estudo
            (disciplina_id, data, hora_inicio, hora_fim, duracao_minutos, topico, notas, concluido)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                dados.get("disciplina_id"),
                dados.get("data"),
                dados.get("hora_inicio"),
                dados.get("hora_fim"),
                dados.get("duracao_minutos"),
                dados.get("topico"),
                dados.get("notas"),
                dados.get("concluido", False),
            ),
        )

        sessao_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return jsonify({"id": sessao_id, "message": "Sessão criada com sucesso"}), 201


@app.route("/api/sessoes/<int:sessao_id>", methods=["PUT", "DELETE"])
def handle_sessao(sessao_id):
    """Atualiza ou deleta uma sessão específica"""
    conn = get_db_connection()

    if request.method == "PUT":
        dados = request.json
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE sessoes_estudo
            SET hora_fim = ?, duracao_minutos = ?, notas = ?, concluido = ?
            WHERE id = ?
        """,
            (
                dados.get("hora_fim"),
                dados.get("duracao_minutos"),
                dados.get("notas"),
                dados.get("concluido"),
                sessao_id,
            ),
        )

        conn.commit()
        conn.close()

        return jsonify({"message": "Sessão atualizada com sucesso"})

    elif request.method == "DELETE":
        conn.execute("DELETE FROM sessoes_estudo WHERE id = ?", (sessao_id,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Sessão deletada com sucesso"})


@app.route("/api/progresso", methods=["GET"])
def get_progresso():
    """Obtém progresso geral de todas as disciplinas"""
    conn = get_db_connection()
    progresso = conn.execute("""
        SELECT disciplina_id, topico_numero, progresso_percentual, ultima_atualizacao
        FROM progresso_topicos
        ORDER BY disciplina_id, topico_numero
    """).fetchall()
    conn.close()

    return jsonify([dict(p) for p in progresso])


@app.route("/api/progresso/<disciplina_id>/<int:topico_numero>", methods=["PUT"])
def update_progresso(disciplina_id, topico_numero):
    """Atualiza o progresso de um tópico"""
    dados = request.json
    progresso = dados.get("progresso_percentual", 0)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO progresso_topicos (disciplina_id, topico_numero, progresso_percentual)
        VALUES (?, ?, ?)
        ON CONFLICT(disciplina_id, topico_numero)
        DO UPDATE SET progresso_percentual = ?, ultima_atualizacao = CURRENT_TIMESTAMP
    """,
        (disciplina_id, topico_numero, progresso, progresso),
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Progresso atualizado com sucesso"})


@app.route("/api/tarefas", methods=["GET", "POST"])
def handle_tarefas():
    """Gerencia tarefas e atividades"""
    if request.method == "GET":
        conn = get_db_connection()
        concluida = request.args.get("concluida")

        query = "SELECT * FROM tarefas WHERE 1=1"
        params = []

        if concluida is not None:
            query += " AND concluida = ?"
            params.append(1 if concluida.lower() == "true" else 0)

        query += " ORDER BY data_entrega ASC, prioridade DESC"

        tarefas = conn.execute(query, params).fetchall()
        conn.close()

        return jsonify([dict(t) for t in tarefas])

    elif request.method == "POST":
        dados = request.json

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO tarefas
            (disciplina_id, titulo, descricao, tipo, data_entrega, prioridade, concluida)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                dados.get("disciplina_id"),
                dados.get("titulo"),
                dados.get("descricao"),
                dados.get("tipo"),
                dados.get("data_entrega"),
                dados.get("prioridade", 2),
                dados.get("concluida", False),
            ),
        )

        tarefa_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return jsonify({"id": tarefa_id, "message": "Tarefa criada com sucesso"}), 201


@app.route("/api/tarefas/<int:tarefa_id>", methods=["PUT", "DELETE"])
def handle_tarefa(tarefa_id):
    """Atualiza ou deleta uma tarefa"""
    conn = get_db_connection()

    if request.method == "PUT":
        dados = request.json
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE tarefas
            SET titulo = ?, descricao = ?, data_entrega = ?,
                prioridade = ?, concluida = ?
            WHERE id = ?
        """,
            (
                dados.get("titulo"),
                dados.get("descricao"),
                dados.get("data_entrega"),
                dados.get("prioridade"),
                dados.get("concluida"),
                tarefa_id,
            ),
        )

        conn.commit()
        conn.close()

        return jsonify({"message": "Tarefa atualizada com sucesso"})

    elif request.method == "DELETE":
        conn.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Tarefa deletada com sucesso"})


@app.route("/api/dashboard", methods=["GET"])
def get_dashboard():
    """Retorna dados para o dashboard principal"""
    conn = get_db_connection()
    data = load_disciplinas()
    semana_atual = calcular_semana_atual()

    hoje = datetime.now().date()
    inicio_semana = hoje - timedelta(days=hoje.weekday())

    horas_semana = conn.execute(
        """
        SELECT SUM(duracao_minutos) / 60.0 as total
        FROM sessoes_estudo
        WHERE data >= ?
    """,
        (inicio_semana.isoformat(),),
    ).fetchone()

    horas_hoje = conn.execute(
        """
        SELECT SUM(duracao_minutos) / 60.0 as total
        FROM sessoes_estudo
        WHERE data = ?
    """,
        (hoje.isoformat(),),
    ).fetchone()

    proxima_semana = hoje + timedelta(days=7)
    tarefas_proximas = conn.execute(
        """
        SELECT * FROM tarefas
        WHERE data_entrega BETWEEN ? AND ?
        AND concluida = 0
        ORDER BY data_entrega ASC
    """,
        (hoje.isoformat(), proxima_semana.isoformat()),
    ).fetchall()

    proximos_efolios = []
    for disc in data["disciplinas"]:
        if "e_folios" in disc:
            for ef in disc["e_folios"]:
                if ef["semana"] >= semana_atual:
                    proximos_efolios.append(
                        {
                            "disciplina": disc["nome"],
                            "tipo": ef["tipo"],
                            "semana": ef["semana"],
                            "data": ef.get("data", ""),
                            "peso": ef.get("peso", 0),
                        }
                    )

    proximos_efolios.sort(key=lambda x: x["semana"])

    progresso_disciplinas = {}
    for disc in data["disciplinas"]:
        disc_id = disc["id"]

        # Calcular progresso baseado em tempo de estudo (pomodoros)
        sessoes = conn.execute(
            """
            SELECT COUNT(*) as total
            FROM sessoes_estudo
            WHERE disciplina_id = ?
        """,
            (disc_id,),
        ).fetchone()

        total_sessoes = sessoes["total"] or 0
        total_minutos = total_sessoes * 25
        creditos = disc.get("creditos", 6)

        # Progresso de tempo: minutos estudados / (créditos * 26 semanas * 60 minutos)
        progresso_tempo = min((total_minutos / (creditos * 26 * 60)) * 100, 100) if total_minutos > 0 else 0

        # Calcular progresso de AFs (Atividades Formativas)
        afs = conn.execute(
            """
            SELECT COUNT(*) as total, SUM(CASE WHEN concluida = 1 THEN 1 ELSE 0 END) as concluidas
            FROM tarefas
            WHERE disciplina_id = ? AND tipo = 'forum'
        """,
            (disc_id,),
        ).fetchone()

        total_afs = afs["total"] or 0
        afs_concluidas = afs["concluidas"] or 0
        progresso_afs = (afs_concluidas / total_afs * 100) if total_afs > 0 else 0

        # Progresso final: 70% tempo + 30% AFs (se houver AFs)
        if total_afs > 0:
            progresso_final = (progresso_tempo * 0.7) + (progresso_afs * 0.3)
        else:
            progresso_final = progresso_tempo

        progresso_disciplinas[disc["sigla"]] = {
            "nome": disc["nome"],
            "progresso": round(progresso_final, 2),
            "cor": disc["cor"],
        }

    conn.close()

    return jsonify(
        {
            "semana_atual": semana_atual,
            "horas_estudadas_hoje": round(horas_hoje["total"] or 0, 2),
            "horas_estudadas_semana": round(horas_semana["total"] or 0, 2),
            "meta_semanal": data["horas_totais_semana"],
            "meta_diaria": data["meta_diaria"],
            "tarefas_proximas": [dict(t) for t in tarefas_proximas],
            "proximos_efolios": proximos_efolios[:5],
            "progresso_disciplinas": progresso_disciplinas,
        }
    )


@app.route("/api/estatisticas", methods=["GET"])
def get_estatisticas():
    """Retorna estatísticas detalhadas de estudo"""
    conn = get_db_connection()

    data_inicio = (datetime.now() - timedelta(days=30)).date()

    horas_por_disciplina = conn.execute(
        """
        SELECT disciplina_id, SUM(duracao_minutos) / 60.0 as total_horas
        FROM sessoes_estudo
        WHERE data >= ?
        GROUP BY disciplina_id
        ORDER BY total_horas DESC
    """,
        (data_inicio.isoformat(),),
    ).fetchall()

    horas_por_dia = conn.execute(
        """
        SELECT data, SUM(duracao_minutos) / 60.0 as total_horas
        FROM sessoes_estudo
        WHERE data >= ?
        GROUP BY data
        ORDER BY data ASC
    """,
        (data_inicio.isoformat(),),
    ).fetchall()

    conn.close()

    return jsonify(
        {
            "horas_por_disciplina": [dict(h) for h in horas_por_disciplina],
            "horas_por_dia": [dict(h) for h in horas_por_dia],
            "periodo": f"{data_inicio.isoformat()} a {datetime.now().date().isoformat()}",
        }
    )


@app.route("/api/inicializar-tarefas", methods=["POST"])
def inicializar_tarefas():
    """Inicializa tarefas baseadas nos e-fólios do calendário"""
    data = load_disciplinas()
    conn = get_db_connection()
    cursor = conn.cursor()
    lisboa_tz = pytz.timezone("Europe/Lisbon")
    hoje = datetime.now(lisboa_tz).date()

    tarefas_criadas = 0

    for disc in data["disciplinas"]:
        disc_id = disc["id"]

        if "e_folios" in disc:
            for ef in disc["e_folios"]:
                existe = cursor.execute(
                    "SELECT id FROM tarefas WHERE disciplina_id = ? AND titulo LIKE ?",
                    (disc_id, f"%{ef['tipo']}%"),
                ).fetchone()

                if not existe:
                    data_entrega = converter_data_portuguesa(ef.get("data", ""))
                    if data_entrega and data_entrega != "":
                        try:
                            data_tarefa = datetime.strptime(
                                data_entrega, "%Y-%m-%d"
                            ).date()
                            concluida = data_tarefa < hoje
                        except:
                            concluida = False
                    else:
                        concluida = False

                    cursor.execute(
                        """
                        INSERT INTO tarefas
                        (disciplina_id, titulo, descricao, tipo, data_entrega, prioridade, concluida)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                        (
                            disc_id,
                            f"{ef['tipo']} - {disc['sigla']}",
                            ef.get("descricao", ""),
                            "e-folio",
                            data_entrega,
                            3,
                            concluida,
                        ),
                    )
                    tarefas_criadas += 1

        if "sessoes_sincronas" in disc:
            for ss in disc["sessoes_sincronas"]:
                existe = cursor.execute(
                    "SELECT id FROM tarefas WHERE disciplina_id = ? AND titulo LIKE ?",
                    (disc_id, f"%Sessão Síncrona%{ss['data']}%"),
                ).fetchone()

                if not existe:
                    data_entrega = converter_data_portuguesa(ss.get("data", ""))
                    if data_entrega and data_entrega != "":
                        try:
                            data_tarefa = datetime.strptime(
                                data_entrega, "%Y-%m-%d"
                            ).date()
                            concluida = data_tarefa < hoje
                        except:
                            concluida = False
                    else:
                        concluida = False

                    cursor.execute(
                        """
                        INSERT INTO tarefas
                        (disciplina_id, titulo, tipo, data_entrega, prioridade, concluida)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """,
                        (
                            disc_id,
                            f"Sessão Síncrona - {disc['sigla']} - {ss['data']}",
                            "sessao-sincrona",
                            data_entrega,
                            2,
                            concluida,
                        ),
                    )
                    tarefas_criadas += 1

    conn.commit()
    conn.close()

    return jsonify(
        {
            "message": f"{tarefas_criadas} tarefas criadas com sucesso",
            "tarefas_criadas": tarefas_criadas,
        }
    )


@app.route("/api/debug/semana", methods=["GET"])
def debug_semana():
    """Rota de debug para verificar cálculo de semana"""
    lisboa_tz = pytz.timezone("Europe/Lisbon")

    data_inicio = lisboa_tz.localize(datetime(2025, 9, 29, 0, 0, 0))

    hoje = datetime.now(lisboa_tz)

    delta = hoje - data_inicio
    dias_diferenca = delta.days
    semana_calculada = dias_diferenca // 7
    semana_final = max(0, min(semana_calculada, 14))

    return jsonify(
        {
            "data_inicio": data_inicio.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "hoje": hoje.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "dias_diferenca": dias_diferenca,
            "semana_calculada": semana_calculada,
            "semana_final": semana_final,
            "explicacao": {
                "semana_0": "29 setembro - 5 outubro 2025 (apresentação)",
                "semana_1": "6 outubro - 12 outubro 2025 (primeira semana de aulas)",
                "hoje_dia": hoje.day,
                "hoje_mes": hoje.month,
                "hoje_ano": hoje.year,
            },
        }
    )


init_db()


@app.route("/api/moodle/login", methods=["POST"])
def moodle_login():
    """Login no Moodle UAB"""
    global moodle_client

    if not MOODLE_AVAILABLE:
        return jsonify({"success": False, "error": "Módulo Moodle não disponível"}), 503

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "error": "Credenciais não fornecidas"}), 400

    moodle_client = MoodleUAB(username, password)

    if moodle_client.login():
        return jsonify(
            {
                "success": True,
                "message": "Login realizado com sucesso",
                "status": moodle_client.get_sync_status(),
            }
        )
    else:
        return jsonify({"success": False, "error": "Falha no login"}), 401


@app.route("/api/moodle/courses", methods=["GET"])
def moodle_get_courses():
    """Buscar disciplinas matriculadas"""
    global moodle_client

    if not MOODLE_AVAILABLE or not moodle_client or not moodle_client.is_logged_in:
        return jsonify({"success": False, "error": "Não conectado ao Moodle"}), 401

    courses = moodle_client.get_enrolled_courses()
    return jsonify({"success": True, "courses": courses})


@app.route("/api/moodle/assignments/<int:course_id>", methods=["GET"])
def moodle_get_assignments(course_id):
    """Buscar tarefas de uma disciplina"""
    global moodle_client

    if not MOODLE_AVAILABLE or not moodle_client or not moodle_client.is_logged_in:
        return jsonify({"success": False, "error": "Não conectado ao Moodle"}), 401

    assignments = moodle_client.get_course_assignments(course_id)
    return jsonify({"success": True, "assignments": assignments})


@app.route("/api/moodle/materials/<int:course_id>", methods=["GET"])
def moodle_get_materials(course_id):
    """Buscar materiais de uma disciplina"""
    global moodle_client

    if not MOODLE_AVAILABLE or not moodle_client or not moodle_client.is_logged_in:
        return jsonify({"success": False, "error": "Não conectado ao Moodle"}), 401

    materials = moodle_client.get_course_materials(course_id)
    return jsonify({"success": True, "materials": materials})


@app.route("/api/moodle/forums/<int:course_id>", methods=["GET"])
def moodle_get_forums(course_id):
    """Buscar posts de fóruns"""
    global moodle_client

    if not MOODLE_AVAILABLE or not moodle_client or not moodle_client.is_logged_in:
        return jsonify({"success": False, "error": "Não conectado ao Moodle"}), 401

    forums = moodle_client.get_forum_posts(course_id)
    return jsonify({"success": True, "forums": forums})


@app.route("/api/moodle/grades/<int:course_id>", methods=["GET"])
def moodle_get_grades(course_id):
    """Buscar notas de uma disciplina"""
    global moodle_client

    if not MOODLE_AVAILABLE or not moodle_client or not moodle_client.is_logged_in:
        return jsonify({"success": False, "error": "Não conectado ao Moodle"}), 401

    grades = moodle_client.get_grades(course_id)
    return jsonify({"success": True, "grades": grades})


@app.route("/api/moodle/calendar", methods=["GET"])
def moodle_sync_calendar():
    """Sincronizar calendário"""
    global moodle_client

    if not MOODLE_AVAILABLE or not moodle_client or not moodle_client.is_logged_in:
        return jsonify({"success": False, "error": "Não conectado ao Moodle"}), 401

    events = moodle_client.sync_calendar()
    return jsonify({"success": True, "events": events})


@app.route("/api/moodle/notifications", methods=["GET"])
def moodle_get_notifications():
    """Verificar notificações"""
    global moodle_client

    if not MOODLE_AVAILABLE or not moodle_client or not moodle_client.is_logged_in:
        return jsonify({"success": False, "error": "Não conectado ao Moodle"}), 401

    notifications = moodle_client.check_notifications()
    return jsonify({"success": True, "notifications": notifications})


@app.route("/api/moodle/sync", methods=["POST"])
def moodle_full_sync():
    """Sincronização completa"""
    global moodle_client

    if not MOODLE_AVAILABLE or not moodle_client or not moodle_client.is_logged_in:
        return jsonify({"success": False, "error": "Não conectado ao Moodle"}), 401

    courses = moodle_client.get_enrolled_courses()
    calendar = moodle_client.sync_calendar()
    notifications = moodle_client.check_notifications()
    materials = moodle_client.auto_download_new_materials()

    return jsonify(
        {
            "success": True,
            "courses_count": len(courses),
            "calendar_events": len(calendar),
            "notifications_count": len(notifications),
            "materials_downloaded": len(materials),
        }
    )


@app.route("/api/moodle/status", methods=["GET"])
def moodle_status():
    """Status da conexão Moodle"""
    global moodle_client

    if not MOODLE_AVAILABLE:
        return jsonify({"available": False, "error": "Módulo não disponível"})

    if not moodle_client:
        return jsonify({"available": True, "logged_in": False})

    status = moodle_client.get_sync_status()
    return jsonify({"available": True, "logged_in": True, "status": status})


@app.route("/api/ai/status", methods=["GET"])
def ai_status():
    """Verificar status do assistente IA"""
    global ai_assistant

    if not AI_AVAILABLE:
        return jsonify({"available": False, "error": "Módulo IA não disponível"})

    if not ai_assistant:
        ai_assistant = AIAssistant()

    return jsonify({"available": True, "configured": ai_assistant.is_configured()})


@app.route("/api/ai/summarize", methods=["POST"])
def ai_summarize_pdf():
    """Resumir PDF"""
    global ai_assistant

    if not AI_AVAILABLE:
        return jsonify({"success": False, "error": "Módulo IA não disponível"}), 503

    if not ai_assistant:
        ai_assistant = AIAssistant()

    data = request.get_json()
    pdf_path = data.get("pdf_path")
    style = data.get("style", "conciso")

    if not pdf_path:
        return jsonify({"success": False, "error": "Caminho do PDF não fornecido"}), 400

    result = ai_assistant.summarize_pdf(pdf_path, style)
    return jsonify(result)


@app.route("/api/ai/chat", methods=["POST"])
def ai_chat():
    """Chat com IA"""
    global ai_assistant

    if not AI_AVAILABLE:
        return jsonify({"success": False, "response": "Módulo IA não disponível"}), 503

    if not ai_assistant:
        ai_assistant = AIAssistant()

    if not ai_assistant.is_configured():
        return jsonify(
            {
                "success": False,
                "response": "IA não configurada. Por favor, configure OPENROUTER_API_KEY ou OPENAI_API_KEY no arquivo .env",
            }
        ), 503

    data = request.get_json()
    message = data.get("message")
    context = data.get("context")

    if not message:
        return jsonify({"success": False, "response": "Mensagem não fornecida"}), 400

    try:
        response_text = ai_assistant.chat(message, context)
        return jsonify({"success": True, "response": response_text})
    except Exception as e:
        return jsonify({"success": False, "response": f"Erro: {str(e)}"}), 500


@app.route("/api/ai/explain", methods=["POST"])
def ai_explain_concept():
    """Explicar conceito"""
    global ai_assistant

    if not AI_AVAILABLE:
        return jsonify({"success": False, "error": "Módulo IA não disponível"}), 503

    if not ai_assistant:
        ai_assistant = AIAssistant()

    data = request.get_json()
    concept = data.get("concept")
    level = data.get("level", "intermediario")

    if not concept:
        return jsonify({"success": False, "error": "Conceito não fornecido"}), 400

    result = ai_assistant.explain_concept(concept, level)
    return jsonify(result)


@app.route("/api/ai/flashcards", methods=["POST"])
def ai_create_flashcards():
    """Criar flashcards de PDF"""
    global ai_assistant

    if not AI_AVAILABLE:
        return jsonify({"success": False, "error": "Módulo IA não disponível"}), 503

    if not ai_assistant:
        ai_assistant = AIAssistant()

    data = request.get_json()
    pdf_path = data.get("pdf_path")
    num_cards = data.get("num_cards", 10)

    if not pdf_path:
        return jsonify({"success": False, "error": "Caminho do PDF não fornecido"}), 400

    result = ai_assistant.create_flashcards(pdf_path, num_cards)
    return jsonify(result)


@app.route("/api/ai/study-plan", methods=["POST"])
def ai_suggest_study_plan():
    """Sugerir plano de estudos"""
    global ai_assistant

    if not AI_AVAILABLE:
        return jsonify({"success": False, "error": "Módulo IA não disponível"}), 503

    if not ai_assistant:
        ai_assistant = AIAssistant()

    data = request.get_json()
    courses = data.get("courses", [])
    weeks = data.get("weeks", 4)

    result = ai_assistant.suggest_study_plan(courses, weeks)
    return jsonify(result)


@app.route("/api/ai/analyze-forums", methods=["POST"])
def ai_analyze_forums():
    """Analisar posts de fóruns"""
    global ai_assistant

    if not AI_AVAILABLE:
        return jsonify({"success": False, "error": "Módulo IA não disponível"}), 503

    if not ai_assistant:
        ai_assistant = AIAssistant()

    data = request.get_json()
    posts = data.get("posts", [])

    result = ai_assistant.analyze_forum_posts(posts)
    return jsonify(result)


@app.route("/api/ai/clear-conversation", methods=["POST"])
def ai_clear_conversation():
    """Limpar histórico de conversação"""
    global ai_assistant

    if not AI_AVAILABLE:
        return jsonify({"success": False, "error": "Módulo IA não disponível"}), 503

    if not ai_assistant:
        ai_assistant = AIAssistant()

    ai_assistant.clear_conversation()
    return jsonify({"success": True, "message": "Histórico limpo"})


# ==================== FOLDER SYNC ROUTES ====================


@app.route("/api/folders/mappings", methods=["GET"])
def get_folder_mappings():
    """Retorna todos os mapeamentos de pastas"""
    global folder_sync_manager

    if not FOLDER_SYNC_AVAILABLE:
        return jsonify(
            {"success": False, "error": "Módulo Folder Sync não disponível"}
        ), 503

    if not folder_sync_manager:
        folder_sync_manager = FolderSyncManager(DB_PATH)

    try:
        mappings = folder_sync_manager.get_mappings()
        return jsonify({"success": True, "mappings": mappings})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/folders/mappings", methods=["POST"])
def add_folder_mapping():
    """Adiciona um novo mapeamento de pasta"""
    global folder_sync_manager

    if not FOLDER_SYNC_AVAILABLE:
        return jsonify(
            {"success": False, "error": "Módulo Folder Sync não disponível"}
        ), 503

    if not folder_sync_manager:
        folder_sync_manager = FolderSyncManager(DB_PATH)

    data = request.get_json()
    disciplina_id = data.get("disciplina_id")
    disciplina_nome = data.get("disciplina_nome")
    folder_path = data.get("folder_path")

    if not disciplina_id or not folder_path:
        return jsonify({"success": False, "error": "Dados incompletos"}), 400

    try:
        result = folder_sync_manager.add_mapping(
            disciplina_id, disciplina_nome, folder_path
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/folders/mappings/<disciplina_id>", methods=["DELETE"])
def remove_folder_mapping(disciplina_id):
    """Remove um mapeamento de pasta"""
    global folder_sync_manager

    if not FOLDER_SYNC_AVAILABLE:
        return jsonify(
            {"success": False, "error": "Módulo Folder Sync não disponível"}
        ), 503

    if not folder_sync_manager:
        folder_sync_manager = FolderSyncManager(DB_PATH)

    try:
        result = folder_sync_manager.remove_mapping(disciplina_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/folders/scan/<disciplina_id>", methods=["POST"])
def scan_folder(disciplina_id):
    """Escaneia uma pasta de disciplina"""
    global folder_sync_manager

    if not FOLDER_SYNC_AVAILABLE:
        return jsonify(
            {"success": False, "error": "Módulo Folder Sync não disponível"}
        ), 503

    if not folder_sync_manager:
        folder_sync_manager = FolderSyncManager(DB_PATH)

    try:
        # Buscar o caminho da pasta
        conn = get_db_connection()
        mapping = conn.execute(
            """
            SELECT caminho_pasta FROM mapeamento_pastas
            WHERE disciplina_id = ? AND ativo = 1
        """,
            (disciplina_id,),
        ).fetchone()
        conn.close()

        if not mapping:
            return jsonify(
                {"success": False, "error": "Mapeamento não encontrado"}
            ), 404

        result = folder_sync_manager.scan_folder(
            disciplina_id, mapping["caminho_pasta"]
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/folders/files/<disciplina_id>", methods=["GET"])
def get_folder_files(disciplina_id):
    """Retorna arquivos de uma disciplina"""
    global folder_sync_manager

    if not FOLDER_SYNC_AVAILABLE:
        return jsonify(
            {"success": False, "error": "Módulo Folder Sync não disponível"}
        ), 503

    if not folder_sync_manager:
        folder_sync_manager = FolderSyncManager(DB_PATH)

    try:
        files = folder_sync_manager.get_files(disciplina_id)
        return jsonify({"success": True, "files": files})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/folders/open/<path:file_path>", methods=["GET"])
def open_file(file_path):
    """Abre um arquivo local"""
    import subprocess
    import platform

    try:
        # Decodificar o caminho
        file_path = file_path.replace("|", "/")

        # Verificar se o arquivo existe
        if not os.path.exists(file_path):
            return jsonify({"success": False, "error": "Arquivo não encontrado"}), 404

        # Abrir arquivo de acordo com o sistema operacional
        system = platform.system()
        if system == "Windows":
            os.startfile(file_path)
        elif system == "Darwin":  # macOS
            subprocess.run(["open", file_path])
        else:  # Linux
            subprocess.run(["xdg-open", file_path])

        return jsonify({"success": True, "message": "Arquivo aberto"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/folders/stats", methods=["GET"])
def get_folder_stats():
    """Retorna estatísticas de pastas"""
    global folder_sync_manager

    if not FOLDER_SYNC_AVAILABLE:
        return jsonify(
            {"success": False, "error": "Módulo Folder Sync não disponível"}
        ), 503

    if not folder_sync_manager:
        folder_sync_manager = FolderSyncManager(DB_PATH)

    try:
        stats = folder_sync_manager.get_stats()
        return jsonify({"success": True, "stats": stats})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/folders/suggest", methods=["GET"])
def suggest_folders():
    """Sugere pastas baseado nas disciplinas"""
    try:
        data = load_disciplinas()
        suggestions = []

        # Diretórios comuns para procurar
        common_paths = [
            Path.home() / "Documentos",
            Path.home() / "Documents",
            Path.home() / "Desktop",
            Path.home() / "Downloads",
        ]

        for disc in data["disciplinas"]:
            # Procurar por pastas com nome similar
            for base_path in common_paths:
                if not base_path.exists():
                    continue

                # Procurar por nome da disciplina ou sigla
                for item in base_path.iterdir():
                    if item.is_dir():
                        item_name_lower = item.name.lower()
                        disc_nome_lower = disc["nome"].lower()
                        disc_sigla_lower = disc["sigla"].lower()

                        if (
                            disc_sigla_lower in item_name_lower
                            or disc_nome_lower in item_name_lower
                        ):
                            suggestions.append(
                                {
                                    "disciplina_id": disc["id"],
                                    "disciplina_nome": disc["nome"],
                                    "folder_path": str(item),
                                }
                            )
                            break

        return jsonify({"success": True, "suggestions": suggestions})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============ ROTAS DO COPILOT STUDIO ============

@app.route('/api/copilot/agents', methods=['GET'])
def get_copilot_agents():
    """Lista todos os agentes Copilot disponíveis"""
    agents = []
    for name, agent in copilot_agents.items():
        agents.append({
            'name': name,
            'available': agent is not None and agent.secret is not None
        })
    return jsonify(agents)


@app.route('/api/copilot/<agent_name>/chat', methods=['POST'])
def copilot_chat(agent_name):
    """Envia mensagem para um agente Copilot"""
    data = request.json
    message = data.get('message', '')

    if not message:
        return jsonify({'error': 'Mensagem vazia'}), 400

    agent_name = agent_name.upper()
    if agent_name not in copilot_agents:
        return jsonify({'error': f'Agente {agent_name} não encontrado'}), 404

    agent = copilot_agents[agent_name]
    if not agent or not agent.secret:
        return jsonify({'error': f'Agente {agent_name} não configurado'}), 503

    try:
        response = agent.send_message(message)
        if response:
            return jsonify({
                'agent': agent_name,
                'message': message,
                'response': response
            })
        else:
            return jsonify({'error': 'Sem resposta do agente'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/copilot/<agent_name>/token', methods=['GET'])
def get_copilot_token(agent_name):
    """Obtém um token para conectar ao agente"""
    agent_name = agent_name.upper()
    if agent_name not in copilot_agents:
        return jsonify({'error': f'Agente {agent_name} não encontrado'}), 404

    agent = copilot_agents[agent_name]
    if not agent or not agent.secret:
        return jsonify({'error': f'Agente {agent_name} não configurado'}), 503

    try:
        token = agent.get_token()
        if token:
            return jsonify({
                'agent': agent_name,
                'token': token,
                'conversationId': agent.conversation_id,
                'directlineUrl': agent.directline_url
            })
        else:
            return jsonify({'error': 'Erro ao gerar token'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/copilot/<agent_name>/history', methods=['GET'])
def get_copilot_history(agent_name):
    """Obtém o histórico de conversas com um agente"""
    agent_name = agent_name.upper()
    if agent_name not in copilot_agents:
        return jsonify({'error': f'Agente {agent_name} não encontrado'}), 404

    agent = copilot_agents[agent_name]
    if not agent:
        return jsonify({'error': f'Agente {agent_name} não configurado'}), 503

    return jsonify({
        'agent': agent_name,
        'history': agent.get_conversation_history()
    })


@app.route('/api/copilot/<agent_name>/clear', methods=['POST'])
def clear_copilot_history(agent_name):
    """Limpa o histórico de conversas com um agente"""
    agent_name = agent_name.upper()
    if agent_name not in copilot_agents:
        return jsonify({'error': f'Agente {agent_name} não encontrado'}), 404

    agent = copilot_agents[agent_name]
    if not agent:
        return jsonify({'error': f'Agente {agent_name} não configurado'}), 503

    agent.clear_conversation()
    return jsonify({'success': True, 'message': f'Histórico do agente {agent_name} limpo'})


if __name__ == "__main__":
    print("🚀 Iniciando servidor backend...")
    print(f"📂 Diretório de dados: {DATA_DIR}")
    print(f"🗄️  Banco de dados: {DB_PATH}")
    print("🌐 API disponível em: http://localhost:5000")

    if MOODLE_AVAILABLE:
        print("✅ Módulo Moodle disponível")
    else:
        print("⚠️  Módulo Moodle não disponível")

    if AI_AVAILABLE:
        print("✅ Módulo IA disponível")
    else:
        print("⚠️  Módulo IA não disponível")

    if FOLDER_SYNC_AVAILABLE:
        print("✅ Módulo Folder Sync disponível")
        # Inicializar o gerenciador de sincronização de pastas
        folder_sync_manager = FolderSyncManager(DB_PATH)
        print("📁 Gerenciador de pastas inicializado")
    else:
        print("⚠️  Módulo Folder Sync não disponível")

    semana = calcular_semana_atual()
    print(f"📅 Semana atual do semestre: {semana}")

    # Abrir navegador automaticamente
    import threading
    import webbrowser
    import time

    def open_browser():
        time.sleep(2)  # Aguardar o servidor iniciar
        print("🌐 Abrindo navegador...")
        webbrowser.open('http://localhost:5000')

    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()

    app.run(debug=True, host="0.0.0.0", port=5000)
