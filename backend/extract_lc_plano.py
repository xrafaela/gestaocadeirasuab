#!/usr/bin/env python3
import PyPDF2

pdf_path = "/home/igorcostas/Documentos/LEI/Linguagens e Computaçao/Plano da Unidade Curricular _ linguagens da computaçao.pdf"

try:
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
    
    # Procurar pela seção "Plano de Trabalho"
    plano_start = text.find("Plano de Trabalho")
    if plano_start != -1:
        plano_text = text[plano_start:plano_start+20000]
        print("=== PLANO DE TRABALHO ===\n")
        print(plano_text)
    else:
        print("Seção 'Plano de Trabalho' não encontrada")
        # Procurar por "Semana"
        semana_start = text.find("Semana")
        if semana_start != -1:
            print("\n=== PRIMEIRAS SEMANAS ===\n")
            print(text[semana_start:semana_start+10000])
    
except Exception as e:
    print(f"Erro ao extrair PDF: {e}")

