#!/usr/bin/env python3
"""
Script para extrair planos de trabalho dos PDFs restantes
"""

import json
import re
from pathlib import Path

try:
    import PyPDF2
except ImportError:
    print("❌ PyPDF2 não está instalado. Instalando...")
    import subprocess
    subprocess.check_call(["pip", "install", "PyPDF2"])
    import PyPDF2


def extract_plano_from_pdf(pdf_path):
    """Extrai o plano de trabalho de um PDF"""
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"❌ Erro ao ler {pdf_path}: {e}")
        return ""


def parse_plano_trabalho(text):
    """Extrai semanas do texto do plano de trabalho"""
    semanas = []
    
    # Padrão para encontrar linhas com semanas
    # Procura por padrões como "1", "2", "3" seguido de data
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        # Procura por padrões de semana
        if re.search(r'^\s*\d+\s+\d{1,2}\s+de\s+\w+', line):
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                try:
                    semana_num = int(parts[0].strip())
                    data = parts[1].strip()
                    
                    # Pega a atividade (próximas linhas)
                    atividade = ""
                    if len(parts) > 2:
                        atividade = parts[2].strip()
                    
                    semanas.append({
                        "numero": semana_num,
                        "data": data,
                        "topico": "Tópico",
                        "atividades": atividade
                    })
                except:
                    pass
    
    return semanas


def create_generic_plano(num_semanas=14):
    """Cria um plano genérico para disciplinas sem PDF estruturado"""
    semanas = []
    meses = ["outubro", "novembro", "dezembro", "janeiro"]
    dias_inicio = [6, 13, 20, 27, 3, 10, 17, 24, 1, 8, 15, 5, 12, 19]
    
    for i in range(num_semanas):
        mes_idx = i // 4
        dia = dias_inicio[i] if i < len(dias_inicio) else 6 + (i % 4) * 7
        mes = meses[mes_idx] if mes_idx < len(meses) else "janeiro"
        ano = 2025 if mes_idx < 3 else 2026
        
        semanas.append({
            "numero": i + 1,
            "data": f"{dia:02d} de {mes} de {ano}",
            "topico": f"Tópico {(i // 2) + 1}",
            "atividades": f"Semana {i + 1}: Estudo e atividades formativas"
        })
    
    return {"semanas": semanas}


def main():
    json_path = Path("/home/igorcostas/Documentos/LEI/study-planner/data/disciplinas.json")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Mapeamento de disciplinas para PDFs
    pdf_paths = {
        "AC": "/home/igorcostas/Documentos/LEI/Arquitectura de Computadores/Plano da Unidade Curricular _ PlataformAbERTA.pdf",
        "SC": "/home/igorcostas/Documentos/LEI/Sistemas Computacionais/Plano da Unidade Curricular _ PlataformAbERTA.pdf",
        "LC": "/home/igorcostas/Documentos/LEI/Linguagens e Computaçao/Plano da Unidade Curricular _ linguagens da computaçao.pdf",
        "EPE": "/home/igorcostas/Documentos/LEI/Ética e Práticas de Engenharia/Plano da Unidade Curricular _ PlataformAbERTA.pdf",
    }
    
    print("=" * 60)
    print("EXTRAINDO PLANOS DE TRABALHO RESTANTES")
    print("=" * 60)
    
    for disc in data["disciplinas"]:
        sigla = disc["sigla"]
        
        if sigla not in pdf_paths:
            continue
        
        if "plano_trabalho" in disc:
            print(f"⏭️  {sigla}: Já possui plano de trabalho")
            continue
        
        pdf_path = pdf_paths[sigla]
        
        if not Path(pdf_path).exists():
            print(f"⚠️  {sigla}: PDF não encontrado em {pdf_path}")
            # Criar plano genérico
            disc["plano_trabalho"] = create_generic_plano()
            print(f"✅ {sigla}: Plano genérico criado (14 semanas)")
            continue
        
        print(f"📖 {sigla}: Extraindo de {Path(pdf_path).name}...")
        text = extract_plano_from_pdf(pdf_path)
        
        if text:
            semanas = parse_plano_trabalho(text)
            if semanas and len(semanas) > 0:
                disc["plano_trabalho"] = {"semanas": semanas}
                print(f"✅ {sigla}: {len(semanas)} semanas extraídas")
            else:
                # Se não conseguir extrair, criar genérico
                disc["plano_trabalho"] = create_generic_plano()
                print(f"⚠️  {sigla}: Usando plano genérico (14 semanas)")
        else:
            disc["plano_trabalho"] = create_generic_plano()
            print(f"⚠️  {sigla}: Usando plano genérico (14 semanas)")
    
    # Fazer backup
    backup_path = json_path.with_suffix('.json.backup3')
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Backup salvo em: {backup_path}")
    
    # Salvar atualizado
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Arquivo atualizado: {json_path}")
    
    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO FINAL")
    print("=" * 60)
    for disc in data["disciplinas"]:
        if "plano_trabalho" in disc:
            semanas = len(disc['plano_trabalho']['semanas'])
            print(f"✅ {disc['sigla']:5} - {semanas:2} semanas")
        else:
            print(f"❌ {disc['sigla']:5} - Sem plano")


if __name__ == "__main__":
    main()
    print("\n✨ Processo concluído!")

