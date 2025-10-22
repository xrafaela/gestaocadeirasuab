#!/usr/bin/env python3
"""
Script para adicionar manualmente planos de trabalho para disciplinas
que não puderam ser extraídos automaticamente dos PDFs
"""

import json
from pathlib import Path


def add_manual_planos():
    """Adiciona planos de trabalho manualmente para as disciplinas"""
    
    json_path = Path("/home/igorcostas/Documentos/LEI/study-planner/data/disciplinas.json")
    
    # Carregar disciplinas.json
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Planos de trabalho manuais baseados nas informações fornecidas
    planos_manuais = {
        "PO": {  # Programação por Objetos
            "semanas": [
                {
                    "numero": 1,
                    "data": "06 de outubro de 2025",
                    "topico": "Introdução à POO",
                    "topico_numero": 1,
                    "atividades": "Atividade 1: Preparação para programar em Python. Atividade 1a: Preparação para uso de LLMs. Sessão Síncrona às 22:00"
                },
                {
                    "numero": 2,
                    "data": "13 de outubro de 2025",
                    "topico": "Ambientação à linguagem + problemas da OO",
                    "topico_numero": 2,
                    "atividades": "AF2: Implementar programa Python. Participação ativa no Fórum do Tópico 2"
                },
                {
                    "numero": 3,
                    "data": "20 de outubro de 2025",
                    "topico": "Ambientação à linguagem + problemas da OO",
                    "topico_numero": 2,
                    "atividades": "Continuação AF2. Participação no Fórum"
                },
                {
                    "numero": 4,
                    "data": "27 de outubro de 2025",
                    "topico": "Projeto - Definição e Design",
                    "topico_numero": 3,
                    "atividades": "AF3.1: Definição Projeto + Storyboard + Mockups (com IA) - INÍCIO"
                },
                {
                    "numero": 5,
                    "data": "03 de novembro de 2025",
                    "topico": "Projeto - Definição e Design",
                    "topico_numero": 3,
                    "atividades": "AF3.2: Protótipos Python"
                },
                {
                    "numero": 6,
                    "data": "10 de novembro de 2025",
                    "topico": "Projeto - Definição e Design",
                    "topico_numero": 3,
                    "atividades": "Entrega e-fólio A (Projeto)"
                },
                {
                    "numero": 7,
                    "data": "17 de novembro de 2025",
                    "topico": "Classes e Objetos",
                    "topico_numero": 4,
                    "atividades": "Estudo de Classes e Objetos em Python"
                },
                {
                    "numero": 8,
                    "data": "24 de novembro de 2025",
                    "topico": "Classes e Objetos",
                    "topico_numero": 4,
                    "atividades": "Continuação: Classes e Objetos"
                },
                {
                    "numero": 9,
                    "data": "01 de dezembro de 2025",
                    "topico": "Classes e Objetos",
                    "topico_numero": 4,
                    "atividades": "Aplicação prática de Classes e Objetos"
                },
                {
                    "numero": 10,
                    "data": "08 de dezembro de 2025",
                    "topico": "Herança e Polimorfismo",
                    "topico_numero": 5,
                    "atividades": "Desenvolvimento do projeto final. Entrega e-fólio B"
                },
                {
                    "numero": 11,
                    "data": "15 de dezembro de 2025",
                    "topico": "Herança e Polimorfismo",
                    "topico_numero": 5,
                    "atividades": "Continuação: Herança e Polimorfismo"
                },
                {
                    "numero": 12,
                    "data": "05 de janeiro de 2026",
                    "topico": "Padrões de Design",
                    "topico_numero": 6,
                    "atividades": "Estudo de Padrões de Design"
                },
                {
                    "numero": 13,
                    "data": "12 de janeiro de 2026",
                    "topico": "Padrões de Design",
                    "topico_numero": 6,
                    "atividades": "Aplicação de Padrões de Design"
                },
                {
                    "numero": 14,
                    "data": "19 de janeiro de 2026",
                    "topico": "Padrões de Design",
                    "topico_numero": 6,
                    "atividades": "Revisão e consolidação"
                }
            ]
        },
        "SR": {  # Sistemas em Rede
            "semanas": [
                {
                    "numero": 1,
                    "data": "06 de outubro de 2025",
                    "topico": "Introdução a Redes",
                    "topico_numero": 1,
                    "atividades": "Introdução aos conceitos de redes de computadores"
                },
                {
                    "numero": 2,
                    "data": "13 de outubro de 2025",
                    "topico": "Introdução a Redes",
                    "topico_numero": 1,
                    "atividades": "Arquitetura de redes e protocolos"
                },
                {
                    "numero": 3,
                    "data": "20 de outubro de 2025",
                    "topico": "Introdução a Redes",
                    "topico_numero": 1,
                    "atividades": "Modelo OSI e TCP/IP"
                },
                {
                    "numero": 4,
                    "data": "27 de outubro de 2025",
                    "topico": "Camada de Aplicação",
                    "topico_numero": 2,
                    "atividades": "Protocolos da camada de aplicação. Sessão Síncrona SS 3ª 4 às 21:30"
                },
                {
                    "numero": 5,
                    "data": "03 de novembro de 2025",
                    "topico": "Camada de Aplicação",
                    "topico_numero": 2,
                    "atividades": "HTTP, DNS, FTP"
                },
                {
                    "numero": 6,
                    "data": "10 de novembro de 2025",
                    "topico": "Camada de Aplicação",
                    "topico_numero": 2,
                    "atividades": "Entrega e-fólio A"
                },
                {
                    "numero": 7,
                    "data": "17 de novembro de 2025",
                    "topico": "Camada de Transporte",
                    "topico_numero": 3,
                    "atividades": "TCP e UDP"
                },
                {
                    "numero": 8,
                    "data": "24 de novembro de 2025",
                    "topico": "Camada de Transporte",
                    "topico_numero": 3,
                    "atividades": "Controle de fluxo e congestionamento"
                },
                {
                    "numero": 9,
                    "data": "01 de dezembro de 2025",
                    "topico": "Camada de Rede",
                    "topico_numero": 4,
                    "atividades": "Roteamento e endereçamento IP. Sessão Síncrona SS 3ª 9 às 21:30"
                },
                {
                    "numero": 10,
                    "data": "08 de dezembro de 2025",
                    "topico": "Camada de Rede",
                    "topico_numero": 4,
                    "atividades": "Entrega e-fólio B"
                },
                {
                    "numero": 11,
                    "data": "15 de dezembro de 2025",
                    "topico": "Camada de Rede",
                    "topico_numero": 4,
                    "atividades": "IPv6 e protocolos de roteamento"
                },
                {
                    "numero": 12,
                    "data": "05 de janeiro de 2026",
                    "topico": "Camada de Enlace",
                    "topico_numero": 5,
                    "atividades": "Protocolos de enlace e detecção de erros"
                },
                {
                    "numero": 13,
                    "data": "12 de janeiro de 2026",
                    "topico": "Camada de Enlace",
                    "topico_numero": 5,
                    "atividades": "Ethernet e switches. Sessão Síncrona SS 3ª 13 às 21:30"
                },
                {
                    "numero": 14,
                    "data": "19 de janeiro de 2026",
                    "topico": "Segurança em Redes",
                    "topico_numero": 6,
                    "atividades": "Criptografia e segurança em redes"
                }
            ]
        }
    }
    
    # Adicionar planos manuais
    for disciplina in data["disciplinas"]:
        sigla = disciplina["sigla"]
        if sigla in planos_manuais and "plano_trabalho" not in disciplina:
            disciplina["plano_trabalho"] = planos_manuais[sigla]
            print(f"✅ Adicionado plano manual para {sigla}")
    
    # Fazer backup
    backup_path = json_path.with_suffix('.json.backup2')
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Backup salvo em: {backup_path}")
    
    # Salvar atualizado
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Arquivo atualizado: {json_path}")
    
    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO")
    print("=" * 60)
    for disc in data["disciplinas"]:
        if "plano_trabalho" in disc:
            print(f"✅ {disc['sigla']}: {len(disc['plano_trabalho']['semanas'])} semanas")
        else:
            print(f"⚠️  {disc['sigla']}: Sem plano de trabalho")


if __name__ == "__main__":
    print("=" * 60)
    print("ADICIONANDO PLANOS DE TRABALHO MANUAIS")
    print("=" * 60)
    add_manual_planos()
    print("\n✨ Processo concluído!")

