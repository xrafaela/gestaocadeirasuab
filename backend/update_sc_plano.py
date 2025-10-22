#!/usr/bin/env python3
import json

# Plano de trabalho de Sistemas Computacionais extraído do PDF
plano_sc = {
    "semanas": [
        {
            "numero": 1,
            "mes": "Outubro",
            "data": "2025-10-01",
            "topico": "Módulo 1: Componentes e paradigmas computacionais, desempenho",
            "topico_numero": 1,
            "atividades": [
                "Consulte as indicações dadas na sala de aula virtual relativamente ao Módulo 1",
                "Estude os conteúdos fornecidos sobre Componentes e paradigmas computacionais, desempenho",
                "Troque ideias com os seus colegas no fórum",
                "Realize a Atividade Formativa 1 (AF1)",
                "Contacte com os seus colegas no Fórum do Módulo 1"
            ]
        },
        {
            "numero": 2,
            "mes": "Outubro",
            "data": "2025-10-08",
            "topico": "Desempenho computacional",
            "topico_numero": 1,
            "atividades": [
                "Aprofunde o estudo dos conteúdos indicados sobre o tema 'Desempenho computacional'",
                "Realize a Atividade Formativa 2 (AF2)",
                "Confronte as suas respostas com as dos seus colegas"
            ]
        },
        {
            "numero": 3,
            "mes": "Outubro",
            "data": "2025-10-15",
            "topico": "Decisão sobre Avaliação e Módulo 2: Estados e máquinas de estados",
            "topico_numero": 2,
            "atividades": [
                "Indique na plataforma até final desta 3ª semana a sua opção de avaliação: Avaliação Contínua ou Exame Final",
                "Responda ao questionário 'Decisão sobre a Avaliação'",
                "Comece por consultar as indicações dadas na sala de aula virtual relativamente ao Módulo 2",
                "Estude os conteúdos fornecidos sobre Estados e máquinas de estados"
            ]
        },
        {
            "numero": 4,
            "mes": "Outubro",
            "data": "2025-10-22",
            "topico": "Módulo 2: Estados e máquinas de estados (continuação)",
            "topico_numero": 2,
            "atividades": [
                "Aprofunde e consolide as aprendizagens realizadas sobre o Módulo 2",
                "Realize a Atividade Formativa 3 (AF3)",
                "Contacte com os seus colegas no Fórum: Apresente o seu ponto de vista, explicite o que fez"
            ]
        },
        {
            "numero": 5,
            "mes": "Novembro",
            "data": "2025-11-01",
            "topico": "E-Fólio A",
            "topico_numero": 3,
            "atividades": [
                "Disponibilização do enunciado do E-Fólio A (3 de novembro)",
                "Os estudantes em avaliação contínua devem realizar, nesta semana, o E-Fólio A"
            ]
        },
        {
            "numero": 6,
            "mes": "Novembro",
            "data": "2025-11-08",
            "topico": "Módulo 3: Níveis de abstração e comunicação entre camadas",
            "topico_numero": 3,
            "atividades": [
                "Comece por consultar as indicações dadas na sala de aula virtual relativamente ao Módulo 3",
                "Estude os conteúdos fornecidos sobre Níveis de abstração e comunicação entre camadas",
                "Realize a Atividade Formativa 4 (AF4)",
                "Contacte com os seus colegas no Fórum do Módulo 3"
            ]
        },
        {
            "numero": 7,
            "mes": "Novembro",
            "data": "2025-11-15",
            "topico": "Módulo 3: Níveis de abstração (continuação)",
            "topico_numero": 3,
            "atividades": [
                "Aprofunde o estudo dos conteúdos sobre o Módulo 3",
                "Realize a Atividade Formativa 5 (AF5)",
                "Confronte as suas respostas com as dos seus colegas"
            ]
        },
        {
            "numero": 8,
            "mes": "Novembro",
            "data": "2025-11-22",
            "topico": "Módulo 4: Paralelismo",
            "topico_numero": 4,
            "atividades": [
                "Comece por consultar as indicações dadas na sala de aula virtual relativamente ao Módulo 4",
                "Estude os conteúdos fornecidos sobre Paralelismo",
                "Troque ideias com os seus colegas no fórum"
            ]
        },
        {
            "numero": 9,
            "mes": "Dezembro",
            "data": "2025-12-01",
            "topico": "Módulo 4: Paralelismo (continuação)",
            "topico_numero": 4,
            "atividades": [
                "Estude os conteúdos fornecidos",
                "Realize a Atividade Formativa 6 (AF6)",
                "Contacte com os seus colegas no Fórum do Módulo 4"
            ]
        },
        {
            "numero": 10,
            "mes": "Dezembro",
            "data": "2025-12-08",
            "topico": "Módulo 5: Introdução à Administração de Sistemas",
            "topico_numero": 5,
            "atividades": [
                "Comece por consultar as indicações dadas na sala de aula virtual relativamente ao Módulo 5",
                "Estude os conteúdos fornecidos sobre Introdução à Administração de Sistemas",
                "Troque ideias com os seus colegas no fórum"
            ]
        },
        {
            "numero": 11,
            "mes": "Dezembro",
            "data": "2025-12-15",
            "topico": "Módulo 5: Administração de Sistemas (continuação)",
            "topico_numero": 5,
            "atividades": [
                "Estude os conteúdos fornecidos",
                "Realize a Atividade Formativa 7 (AF7)",
                "Aprofunde e consolide as aprendizagens realizadas sobre o Módulo 5"
            ]
        },
        {
            "numero": 12,
            "mes": "Dezembro",
            "data": "2025-12-22",
            "topico": "PAUSA LETIVA",
            "topico_numero": 0,
            "atividades": ["Pausa letiva - Início a 22 de dezembro de 2025"]
        },
        {
            "numero": 13,
            "mes": "Dezembro/Janeiro",
            "data": "2025-12-29",
            "topico": "PAUSA LETIVA",
            "topico_numero": 0,
            "atividades": ["Pausa letiva - até 4 de janeiro de 2026"]
        },
        {
            "numero": 14,
            "mes": "Janeiro",
            "data": "2026-01-05",
            "topico": "E-Fólio B",
            "topico_numero": 0,
            "atividades": [
                "Disponibilização do enunciado do E-Fólio B (5 de janeiro)",
                "Os estudantes em avaliação contínua devem realizar, nesta semana, o E-Fólio B"
            ]
        },
        {
            "numero": 15,
            "mes": "Janeiro",
            "data": "2026-01-12",
            "topico": "Avaliação do E-Fólio B",
            "topico_numero": 0,
            "atividades": ["Disponibilização da avaliação do E-Fólio B"]
        },
        {
            "numero": 16,
            "mes": "Janeiro",
            "data": "2026-01-19",
            "topico": "PREPARAÇÃO PARA PROVA FINAL",
            "topico_numero": 0,
            "atividades": ["Preparação para prova final"]
        }
    ]
}

# Carregar disciplinas.json
with open('/home/igorcostas/Documentos/LEI/study-planner/data/disciplinas.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Encontrar e atualizar SC
disciplinas = data['disciplinas']
for disc in disciplinas:
    if disc['sigla'] == 'SC':
        disc['plano_trabalho'] = plano_sc
        print(f"✅ Plano de trabalho de {disc['nome']} atualizado com sucesso!")
        print(f"   Total de semanas: {len(plano_sc['semanas'])}")
        break

# Salvar disciplinas.json
with open('/home/igorcostas/Documentos/LEI/study-planner/data/disciplinas.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n✅ disciplinas.json atualizado com sucesso!")

