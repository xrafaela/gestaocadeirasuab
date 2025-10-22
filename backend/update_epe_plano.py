#!/usr/bin/env python3
import json

# Plano de trabalho de Ética e Práticas de Engenharia
plano_epe = {
    "semanas": [
        {
            "numero": 1,
            "mes": "Outubro",
            "data": "2025-10-06",
            "topico": "Módulo 1: Introdução à Ética em Engenharia",
            "topico_numero": 1,
            "atividades": [
                "Leia o Plano da Unidade Curricular",
                "Estude os conceitos fundamentais de ética em engenharia",
                "Coloque dúvidas no fórum"
            ]
        },
        {
            "numero": 2,
            "mes": "Outubro",
            "data": "2025-10-13",
            "topico": "Módulo 1: Princípios Éticos",
            "topico_numero": 1,
            "atividades": [
                "Estude os princípios éticos fundamentais",
                "Realize atividades formativas",
                "Discuta no fórum com colegas"
            ]
        },
        {
            "numero": 3,
            "mes": "Outubro",
            "data": "2025-10-20",
            "topico": "Módulo 2: Responsabilidade Profissional",
            "topico_numero": 2,
            "atividades": [
                "Indique sua opção de avaliação até final desta semana",
                "Estude responsabilidade profissional do engenheiro",
                "Realize atividades formativas"
            ]
        },
        {
            "numero": 4,
            "mes": "Outubro",
            "data": "2025-10-27",
            "topico": "Módulo 2: Responsabilidade Profissional (continuação)",
            "topico_numero": 2,
            "atividades": [
                "Continue o estudo de responsabilidade profissional",
                "Realize atividades formativas",
                "Discuta casos de estudo no fórum"
            ]
        },
        {
            "numero": 5,
            "mes": "Novembro",
            "data": "2025-11-03",
            "topico": "E-Fólio A",
            "topico_numero": 0,
            "atividades": [
                "Disponibilização do enunciado do E-Fólio A",
                "Realize o E-Fólio A"
            ]
        },
        {
            "numero": 6,
            "mes": "Novembro",
            "data": "2025-11-10",
            "topico": "Módulo 3: Impacto Social e Ambiental",
            "topico_numero": 3,
            "atividades": [
                "Estude o impacto social e ambiental da engenharia",
                "Realize atividades formativas",
                "Discuta casos práticos no fórum"
            ]
        },
        {
            "numero": 7,
            "mes": "Novembro",
            "data": "2025-11-17",
            "topico": "Módulo 3: Impacto Social e Ambiental (continuação)",
            "topico_numero": 3,
            "atividades": [
                "Continue o estudo de impacto social e ambiental",
                "Realize atividades formativas",
                "Prepare-se para o E-Fólio A"
            ]
        },
        {
            "numero": 8,
            "mes": "Novembro",
            "data": "2025-11-24",
            "topico": "Envio do E-Fólio A",
            "topico_numero": 0,
            "atividades": [
                "Envio do E-Fólio A para correção",
                "Aguarde classificação"
            ]
        },
        {
            "numero": 9,
            "mes": "Dezembro",
            "data": "2025-12-01",
            "topico": "Módulo 4: Códigos de Ética Profissional",
            "topico_numero": 4,
            "atividades": [
                "Estude códigos de ética profissional",
                "Analise códigos de diferentes organizações",
                "Realize atividades formativas"
            ]
        },
        {
            "numero": 10,
            "mes": "Dezembro",
            "data": "2025-12-08",
            "topico": "Módulo 4: Códigos de Ética (continuação)",
            "topico_numero": 4,
            "atividades": [
                "Continue o estudo de códigos de ética",
                "Discuta dilemas éticos no fórum",
                "Realize atividades formativas"
            ]
        },
        {
            "numero": 11,
            "mes": "Dezembro",
            "data": "2025-12-15",
            "topico": "E-Fólio B",
            "topico_numero": 0,
            "atividades": [
                "Disponibilização do enunciado do E-Fólio B",
                "Realize o E-Fólio B"
            ]
        },
        {
            "numero": 12,
            "mes": "Dezembro",
            "data": "2025-12-22",
            "topico": "Pausa Letiva",
            "topico_numero": 0,
            "atividades": [
                "Pausa letiva de Natal"
            ]
        },
        {
            "numero": 13,
            "mes": "Janeiro",
            "data": "2026-01-05",
            "topico": "Envio do E-Fólio B",
            "topico_numero": 0,
            "atividades": [
                "Envio do E-Fólio B para correção",
                "Aguarde classificação"
            ]
        },
        {
            "numero": 14,
            "mes": "Janeiro",
            "data": "2026-01-12",
            "topico": "Módulo 5: Casos de Estudo",
            "topico_numero": 5,
            "atividades": [
                "Estude casos de estudo de dilemas éticos",
                "Analise decisões e consequências",
                "Realize atividades formativas"
            ]
        },
        {
            "numero": 15,
            "mes": "Janeiro",
            "data": "2026-01-19",
            "topico": "Revisão e Preparação para Prova Final",
            "topico_numero": 5,
            "atividades": [
                "Faça revisão da matéria",
                "Prepare-se para o E-Fólio Global/Exame"
            ]
        },
        {
            "numero": 16,
            "mes": "Janeiro",
            "data": "2026-01-26",
            "topico": "E-Fólio Global ou Exame",
            "topico_numero": 0,
            "atividades": [
                "Realização do E-Fólio Global ou Exame"
            ]
        }
    ]
}

# Carregar disciplinas.json
with open('/home/igorcostas/Documentos/LEI/study-planner/data/disciplinas.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Encontrar e atualizar EPE
disciplinas = data['disciplinas']
for disc in disciplinas:
    if disc['sigla'] == 'EPE':
        disc['plano_trabalho'] = plano_epe
        print(f"✅ Plano de trabalho de {disc['nome']} atualizado com sucesso!")
        print(f"   Total de semanas: {len(plano_epe['semanas'])}")
        break

# Salvar disciplinas.json
with open('/home/igorcostas/Documentos/LEI/study-planner/data/disciplinas.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n✅ disciplinas.json atualizado com sucesso!")

