#!/usr/bin/env python3
import json

# Plano de trabalho de Arquitetura de Computadores extraído do PDF
plano_ac = {
    "semanas": [
        {
            "numero": 1,
            "mes": "Outubro",
            "data": "2025-10-06",
            "topico": "Bloco I - Introdução",
            "topico_numero": 1,
            "atividades": [
                "Explore o espaço, leia os documentos",
                "Coloque as suas dúvidas de funcionamento da unidade curricular no fórum Central",
                "Na 5ª-feira participe na sessão síncrona de abertura às 21h (09-10-2025)",
                "Pode adiantar-se desde já no estudo da matéria"
            ]
        },
        {
            "numero": 2,
            "mes": "Outubro",
            "data": "2025-10-13",
            "topico": "Capítulo 1",
            "topico_numero": 1,
            "atividades": [
                "Ler Capítulo 1",
                "Realizar Atividades Formativas"
            ]
        },
        {
            "numero": 3,
            "mes": "Outubro",
            "data": "2025-10-20",
            "topico": "Bloco II - Componentes Digitais Básicos",
            "topico_numero": 2,
            "atividades": [
                "Indique ao professor até final desta 3ª semana a sua opção de avaliação",
                "Utilize o recurso 'Decisão sobre a Avaliação'",
                "Ler Capítulo 2",
                "Realizar Atividades Formativas"
            ]
        },
        {
            "numero": 4,
            "mes": "Outubro",
            "data": "2025-10-27",
            "topico": "Capítulos 4 e continuação",
            "topico_numero": 2,
            "atividades": [
                "Até ao final do dia 27-10-2025, escolher a modalidade de avaliação",
                "Realizar Atividade Formativa",
                "Ler Capítulo 4",
                "Realizar Atividades Formativas"
            ]
        },
        {
            "numero": 5,
            "mes": "Novembro",
            "data": "2025-11-03",
            "topico": "Capítulos 5 e 6",
            "topico_numero": 2,
            "atividades": [
                "Ler o capítulo 5",
                "Realizar Atividades Formativas",
                "Ler o capítulo 6"
            ]
        },
        {
            "numero": 6,
            "mes": "Novembro",
            "data": "2025-11-10",
            "topico": "Capítulo 7 e E-Fólio A",
            "topico_numero": 3,
            "atividades": [
                "Realizar Atividades Formativas",
                "Ler o capítulo 7",
                "Realizar Atividades Formativas",
                "Na 5ª-feira participe na sessão síncrona do e-fólio A, às 21h (13-11-2025)",
                "Final da semana, divulgação do enunciado do e-fólio A (14-11-2025)"
            ]
        },
        {
            "numero": 7,
            "mes": "Novembro",
            "data": "2025-11-17",
            "topico": "Resolução do E-fólio A",
            "topico_numero": 3,
            "atividades": [
                "Resolução do E-fólio A"
            ]
        },
        {
            "numero": 8,
            "mes": "Novembro",
            "data": "2025-11-24",
            "topico": "Bloco III - Organização Básica do Computador",
            "topico_numero": 4,
            "atividades": [
                "Envio do E-fólio A para correção",
                "Ler capítulo 9",
                "Realizar Atividade formativa",
                "Indicação da classificação do E-fólio A",
                "Ler capítulo 10"
            ]
        },
        {
            "numero": 9,
            "mes": "Dezembro",
            "data": "2025-12-02",
            "topico": "Bloco III - Organização Básica do Computador (continuação)",
            "topico_numero": 4,
            "atividades": [
                "Abertura do Bloco III - Organização Básica do Computador",
                "Ler capítulo 9",
                "Realizar Atividade formativa",
                "Indicação da classificação do E-fólio A",
                "Ler capítulo 10"
            ]
        },
        {
            "numero": 10,
            "mes": "Dezembro",
            "data": "2025-12-09",
            "topico": "Atividades Formativas",
            "topico_numero": 4,
            "atividades": [
                "Realizar Atividades formativas",
                "Realizar Atividades formativas 11",
                "Realizar Atividades formativas"
            ]
        },
        {
            "numero": 11,
            "mes": "Dezembro",
            "data": "2025-12-15",
            "topico": "E-Fólio B",
            "topico_numero": 5,
            "atividades": [
                "Terminar o estudo do módulo 3",
                "Na 5ª-feira participe na sessão síncrona do e-fólio B, às 21h (18-12-2025)",
                "Na 6ª-feira, divulgação do enunciado do e-fólio B (19-12-2025)",
                "Realização do e-fólio B"
            ]
        },
        {
            "numero": 12,
            "mes": "Dezembro",
            "data": "2025-12-22",
            "topico": "Pausa letiva - Período de Natal",
            "topico_numero": 0,
            "atividades": ["Pausa letiva"]
        },
        {
            "numero": 13,
            "mes": "Janeiro",
            "data": "2026-01-05",
            "topico": "Realização do E-fólio B",
            "topico_numero": 5,
            "atividades": [
                "Realização do e-fólio B"
            ]
        },
        {
            "numero": 14,
            "mes": "Janeiro",
            "data": "2026-01-12",
            "topico": "Envio do E-fólio B",
            "topico_numero": 5,
            "atividades": [
                "Envio do E-fólio B ao professor"
            ]
        },
        {
            "numero": 15,
            "mes": "Janeiro",
            "data": "2026-01-19",
            "topico": "Classificação do E-fólio B",
            "topico_numero": 5,
            "atividades": [
                "Indicação da classificação do E-fólio B",
                "Na 4ª-feira, participe na sessão síncrona das provas, às 21h (22-01-2026)"
            ]
        },
        {
            "numero": 16,
            "mes": "Janeiro",
            "data": "2026-01-26",
            "topico": "Provas (E-Fólio Global ou Exame)",
            "topico_numero": 0,
            "atividades": [
                "Provas (E-Fólio Global ou Exame)"
            ]
        }
    ]
}

# Carregar disciplinas.json
with open('/home/igorcostas/Documentos/LEI/study-planner/data/disciplinas.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Encontrar e atualizar AC
disciplinas = data['disciplinas']
for disc in disciplinas:
    if disc['sigla'] == 'AC':
        disc['plano_trabalho'] = plano_ac
        print(f"✅ Plano de trabalho de {disc['nome']} atualizado com sucesso!")
        print(f"   Total de semanas: {len(plano_ac['semanas'])}")
        break

# Salvar disciplinas.json
with open('/home/igorcostas/Documentos/LEI/study-planner/data/disciplinas.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n✅ disciplinas.json atualizado com sucesso!")

