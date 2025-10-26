#!/usr/bin/env python3
"""
Script para extrair planos de trabalho dos PDFs das disciplinas
e atualizar o arquivo disciplinas.json
"""

import json
import re
import os
from pathlib import Path

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    print("PyPDF2 não está instalado. Tentando instalar...")
    import subprocess
    subprocess.check_call(["pip", "install", "PyPDF2"])
    import PyPDF2
    PDF_AVAILABLE = True


def extract_text_from_pdf(pdf_path):
    """Extrai texto de um PDF"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        print(f"Erro ao ler PDF {pdf_path}: {e}")
        return ""


def extract_plano_trabalho(text, disciplina_nome):
    """Extrai o plano de trabalho do texto do PDF"""
    plano = {
        "semanas": [],
        "topicos_detalhados": []
    }

    # Procurar por tópicos com tabelas de semanas
    # Padrão: 7.X. Tópico N: Nome do Tópico
    topico_pattern = r"7\.(\d+)\.\s*Tópico\s+(\d+):\s*([^\n]+)"
    topicos = re.finditer(topico_pattern, text, re.IGNORECASE)

    topicos_encontrados = []
    for match in topicos:
        secao = match.group(1)
        numero = match.group(2)
        titulo = match.group(3).strip()
        posicao = match.end()
        topicos_encontrados.append({
            "secao": secao,
            "numero": numero,
            "titulo": titulo,
            "posicao": posicao
        })

    if not topicos_encontrados:
        print(f"  ⚠️  Nenhum tópico encontrado para {disciplina_nome}")
        return None

    # Para cada tópico, extrair as semanas
    for i, topico in enumerate(topicos_encontrados):
        # Determinar onde termina este tópico (início do próximo ou fim do texto)
        inicio = topico["posicao"]
        fim = topicos_encontrados[i + 1]["posicao"] if i + 1 < len(topicos_encontrados) else len(text)

        topico_text = text[inicio:fim]

        # Procurar por linhas de semana
        # Padrão: número semana data atividade
        # Exemplo: 1 06 de outubro de 2025 Apresentação e leitura PUC.
        semana_pattern = r"(\d+)\s+(\d+\s+de\s+\w+\s+de\s+\d{4})\s+([^\n]+)"
        semanas = re.findall(semana_pattern, topico_text)

        for semana_num, data, atividade in semanas:
            # Limpar atividade
            atividade = atividade.strip()
            # Remover caracteres especiais e múltiplos espaços
            atividade = re.sub(r'\s+', ' ', atividade)
            # Limitar tamanho
            if len(atividade) > 250:
                atividade = atividade[:247] + "..."

            plano["semanas"].append({
                "numero": int(semana_num),
                "data": data.strip(),
                "topico": topico["titulo"],
                "topico_numero": int(topico["numero"]),
                "atividades": atividade
            })

    # Ordenar por número de semana
    plano["semanas"].sort(key=lambda x: x["numero"])

    return plano if plano["semanas"] else None


def process_disciplinas():
    """Processa todas as disciplinas e extrai planos de trabalho"""
    
    # Caminhos
    base_path = Path("/home/igorcostas/Documentos/LEI")
    json_path = base_path / "study-planner/data/disciplinas.json"
    
    # Carregar disciplinas.json
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Mapeamento de pastas das disciplinas
    disciplinas_folders = {
        "FBD": "Fundamento de Base de Dados",
        "LC": "Linguagens e Computaçao",
        "PO": "Programaçao por Objetos",
        "SR": "Sistemas em rede",
        "AC": "Arquitectura de Computadores",
        "SC": "Sistemas Computacionais",
        "EPE": "Ética e Práticas de Engenharia"
    }
    
    # Processar cada disciplina
    for disciplina in data["disciplinas"]:
        sigla = disciplina["sigla"]
        nome = disciplina["nome"]
        
        print(f"\n📚 Processando: {nome} ({sigla})")
        
        if sigla not in disciplinas_folders:
            print(f"  ⚠️  Pasta não mapeada para {sigla}")
            continue
        
        folder_name = disciplinas_folders[sigla]
        folder_path = base_path / folder_name
        
        # Procurar PDF do plano
        pdf_files = list(folder_path.glob("*[Pp]lano*.pdf"))
        
        if not pdf_files:
            print(f"  ⚠️  PDF não encontrado em {folder_path}")
            continue
        
        pdf_path = pdf_files[0]
        print(f"  📄 Lendo: {pdf_path.name}")
        
        # Extrair texto
        text = extract_text_from_pdf(pdf_path)
        
        if not text:
            print(f"  ❌ Falha ao extrair texto")
            continue
        
        # Extrair plano de trabalho
        plano = extract_plano_trabalho(text, nome)
        
        if plano:
            disciplina["plano_trabalho"] = plano
            print(f"  ✅ Plano extraído: {len(plano['semanas'])} semanas")
        else:
            print(f"  ⚠️  Plano não encontrado no PDF")
    
    # Salvar JSON atualizado
    backup_path = json_path.with_suffix('.json.backup')
    
    # Fazer backup
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Backup salvo em: {backup_path}")
    
    # Salvar atualizado
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Arquivo atualizado: {json_path}")
    
    return data


def main():
    """Função principal"""
    print("=" * 60)
    print("EXTRAÇÃO DE PLANOS DE TRABALHO DOS PDFs")
    print("=" * 60)
    
    try:
        data = process_disciplinas()
        
        print("\n" + "=" * 60)
        print("RESUMO")
        print("=" * 60)
        
        for disc in data["disciplinas"]:
            if "plano_trabalho" in disc:
                print(f"✅ {disc['sigla']}: {len(disc['plano_trabalho']['semanas'])} semanas")
            else:
                print(f"⚠️  {disc['sigla']}: Sem plano de trabalho")
        
        print("\n✨ Processo concluído!")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

