#!/usr/bin/env python3
import json
import PyPDF2
import re

# Extrair texto do PDF
pdf_path = "/home/igorcostas/Documentos/LEI/Sistemas Computacionais/Plano da Unidade Curricular _ PlataformAbERTA.pdf"

try:
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

    # Procurar pela seção "Outubro"
    outubro_start = text.find("Outubro O que se espera")
    if outubro_start != -1:
        plano_text = text[outubro_start:outubro_start+15000]
        print("=== PLANO DE TRABALHO - OUTUBRO ===\n")
        print(plano_text)
    else:
        print("Seção 'Outubro' não encontrada")
        # Procurar por "7.1. Primeiro mês"
        primeiro_mes = text.find("7.1. Primeiro mês")
        if primeiro_mes != -1:
            print("\n=== PRIMEIRO MÊS ===\n")
            print(text[primeiro_mes:primeiro_mes+10000])

except Exception as e:
    print(f"Erro ao extrair PDF: {e}")

