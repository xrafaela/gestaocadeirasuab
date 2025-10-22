#!/usr/bin/env python3
"""
Teste final de verificação - Sincronização de progresso
"""
import json
import sys
sys.path.insert(0, '.')
from app import app

def test_final_verification():
    with app.test_client() as client:
        print("=" * 80)
        print("TESTE FINAL DE VERIFICAÇÃO")
        print("=" * 80)
        
        # Teste 1: Verificar se /api/disciplinas retorna progresso
        print("\n1. VERIFICANDO ENDPOINT /api/disciplinas...")
        print("-" * 80)
        
        response = client.get('/api/disciplinas')
        if response.status_code != 200:
            print(f"❌ ERRO: Status code {response.status_code}")
            return False
        
        disciplinas = response.get_json()
        print(f"✅ Retornou {len(disciplinas)} disciplinas")
        
        # Verificar se todas têm progresso
        todas_com_progresso = all('progresso' in d for d in disciplinas)
        if todas_com_progresso:
            print("✅ Todas as disciplinas têm campo 'progresso'")
        else:
            print("❌ Algumas disciplinas não têm campo 'progresso'")
            return False
        
        # Teste 2: Verificar se /api/dashboard retorna progresso
        print("\n2. VERIFICANDO ENDPOINT /api/dashboard...")
        print("-" * 80)
        
        response = client.get('/api/dashboard')
        if response.status_code != 200:
            print(f"❌ ERRO: Status code {response.status_code}")
            return False
        
        dashboard = response.get_json()
        print(f"✅ Dashboard carregado com sucesso")
        
        progresso_disciplinas = dashboard.get('progresso_disciplinas', {})
        print(f"✅ Contém progresso de {len(progresso_disciplinas)} disciplinas")
        
        # Teste 3: Comparar sincronização
        print("\n3. COMPARANDO SINCRONIZAÇÃO...")
        print("-" * 80)
        
        todas_sincronizadas = True
        for disc in disciplinas:
            sigla = disc['sigla']
            disc_progresso = disc.get('progresso', 0)
            dashboard_progresso = progresso_disciplinas.get(sigla, {}).get('progresso', 0)
            
            if abs(disc_progresso - dashboard_progresso) < 0.01:
                print(f"✅ {sigla}: {disc_progresso}% == {dashboard_progresso}%")
            else:
                print(f"❌ {sigla}: {disc_progresso}% != {dashboard_progresso}%")
                todas_sincronizadas = False
        
        if not todas_sincronizadas:
            return False
        
        # Teste 4: Verificar estrutura de dados
        print("\n4. VERIFICANDO ESTRUTURA DE DADOS...")
        print("-" * 80)
        
        primeira_disc = disciplinas[0]
        campos_obrigatorios = ['id', 'sigla', 'nome', 'cor', 'creditos', 'progresso']
        
        for campo in campos_obrigatorios:
            if campo in primeira_disc:
                print(f"✅ Campo '{campo}' presente")
            else:
                print(f"❌ Campo '{campo}' ausente")
                return False
        
        print("\n" + "=" * 80)
        print("✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
        print("=" * 80)
        return True

if __name__ == "__main__":
    success = test_final_verification()
    sys.exit(0 if success else 1)

