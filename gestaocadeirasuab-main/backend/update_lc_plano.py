#!/usr/bin/env python3
import json

# Plano de trabalho de Linguagens e Computação extraído do PDF
plano_lc = {
    "semanas": [
        {
            "numero": 1,
            "mes": "Outubro",
            "data": "2025-10-06",
            "topico": "Introdução - Leitura do Plano da Unidade Curricular",
            "topico_numero": 1,
            "atividades": [
                "Leia bem o Plano da Unidade Curricular",
                "Coloque as dúvidas que tiver no Fórum de Notícias e Ajuda",
                "Verifique que tem tudo o que é necessário para poder seguir a unidade curricular"
            ]
        },
        {
            "numero": 2,
            "mes": "Outubro",
            "data": "2025-10-13",
            "topico": "Tema 1: Linguagens formais e autómatos",
            "topico_numero": 1,
            "atividades": [
                "Leia o capítulo 1 do livro adotado",
                "Estude as secções 1.2, 1.3 e 1.4 sobre demonstrações lógicas formais",
                "Realize as atividades formativas",
                "Discuta no fórum com os seus colegas"
            ]
        },
        {
            "numero": 3,
            "mes": "Outubro",
            "data": "2025-10-20",
            "topico": "Tema 1: Linguagens formais e autómatos (continuação)",
            "topico_numero": 1,
            "atividades": [
                "Continue o estudo do capítulo 1",
                "Realize as atividades formativas",
                "Discuta no fórum com os seus colegas"
            ]
        },
        {
            "numero": 4,
            "mes": "Outubro",
            "data": "2025-10-27",
            "topico": "Tema 2: Autómatos finitos",
            "topico_numero": 2,
            "atividades": [
                "Leia o capítulo 2 do livro adotado",
                "Estude autómatos finitos deterministas e não-deterministas",
                "Aprenda a converter entre os dois tipos de autómatos",
                "Realize as atividades formativas"
            ]
        },
        {
            "numero": 5,
            "mes": "Novembro",
            "data": "2025-11-03",
            "topico": "Tema 2: Autómatos finitos (continuação)",
            "topico_numero": 2,
            "atividades": [
                "Continue o estudo do capítulo 2",
                "Estude transições-epsilon nos autómatos não deterministas",
                "Realize as atividades formativas",
                "Discuta no fórum com os seus colegas"
            ]
        },
        {
            "numero": 6,
            "mes": "Novembro",
            "data": "2025-11-10",
            "topico": "Tema 3: Linguagens e expressões regulares",
            "topico_numero": 3,
            "atividades": [
                "Leia o capítulo 3 do livro adotado",
                "Estude expressões regulares e operações fundamentais",
                "Aprenda a converter entre expressões regulares e autómatos finitos",
                "Teste ferramentas práticas de expressões regulares"
            ]
        },
        {
            "numero": 7,
            "mes": "Novembro",
            "data": "2025-11-17",
            "topico": "Tema 3: Expressões regulares (continuação)",
            "topico_numero": 3,
            "atividades": [
                "Continue o estudo do capítulo 3",
                "Estude leis dos operadores das expressões regulares",
                "Use o interpretador de expressões regulares online",
                "Realize as atividades formativas"
            ]
        },
        {
            "numero": 8,
            "mes": "Novembro",
            "data": "2025-11-25",
            "topico": "E-Fólio A",
            "topico_numero": 0,
            "atividades": [
                "Realização do E-Fólio A (25 de novembro a 9 de dezembro)",
                "Discuta no fórum as principais dificuldades encontradas"
            ]
        },
        {
            "numero": 9,
            "mes": "Dezembro",
            "data": "2025-12-08",
            "topico": "Tema 4: Linguagens e gramáticas independentes do contexto",
            "topico_numero": 4,
            "atividades": [
                "Leia os capítulos 5 e 6 do livro adotado",
                "Estude gramáticas independentes do contexto",
                "Aprenda sobre árvores sintáticas (parse trees)",
                "Estude autómatos de pilha (PDA)"
            ]
        },
        {
            "numero": 10,
            "mes": "Dezembro",
            "data": "2025-12-15",
            "topico": "Tema 4: Gramáticas e autómatos de pilha (continuação)",
            "topico_numero": 4,
            "atividades": [
                "Continue o estudo dos capítulos 5 e 6",
                "Estude a equivalência entre PDA e CFG",
                "Aprenda sobre autómatos de pilha deterministas",
                "Realize as atividades formativas"
            ]
        },
        {
            "numero": 11,
            "mes": "Dezembro",
            "data": "2025-12-20",
            "topico": "E-Fólio B",
            "topico_numero": 0,
            "atividades": [
                "Realização do E-Fólio B (20 de dezembro)",
                "Entrega do E-Fólio B até 14 de janeiro"
            ]
        },
        {
            "numero": 12,
            "mes": "Dezembro/Janeiro",
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
            "topico": "Preparação para fase final",
            "topico_numero": 0,
            "atividades": [
                "Discuta no fórum as principais dificuldades encontradas",
                "Sugira soluções e prepare-se para a fase seguinte"
            ]
        },
        {
            "numero": 14,
            "mes": "Janeiro",
            "data": "2026-01-12",
            "topico": "Tema 5: Máquinas de Turing",
            "topico_numero": 5,
            "atividades": [
                "Estude o 5º e último tópico: máquinas de Turing",
                "Aprenda sobre o formalismo mais comum que incorpora o conceito de computação",
                "Estude a hierarquia de Chomsky",
                "Realize as atividades formativas"
            ]
        },
        {
            "numero": 15,
            "mes": "Janeiro",
            "data": "2026-01-19",
            "topico": "Revisão e Preparação para P-Fólio/Exame",
            "topico_numero": 5,
            "atividades": [
                "Faça uma revisão da matéria",
                "Prepare-se para o P-Fólio Global/Exame"
            ]
        },
        {
            "numero": 16,
            "mes": "Janeiro",
            "data": "2026-01-26",
            "topico": "P-Fólio Global ou Exame",
            "topico_numero": 0,
            "atividades": [
                "Realização do P-Fólio Global ou Exame"
            ]
        }
    ]
}

# Carregar disciplinas.json
with open('/home/igorcostas/Documentos/LEI/study-planner/data/disciplinas.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Encontrar e atualizar LC
disciplinas = data['disciplinas']
for disc in disciplinas:
    if disc['sigla'] == 'LC':
        disc['plano_trabalho'] = plano_lc
        print(f"✅ Plano de trabalho de {disc['nome']} atualizado com sucesso!")
        print(f"   Total de semanas: {len(plano_lc['semanas'])}")
        break

# Salvar disciplinas.json
with open('/home/igorcostas/Documentos/LEI/study-planner/data/disciplinas.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n✅ disciplinas.json atualizado com sucesso!")

