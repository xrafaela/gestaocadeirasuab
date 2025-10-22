#!/usr/bin/env python3
"""
Script para testar sincronização final de progresso entre Dashboard e Disciplinas
"""
import json
import sys
sys.path.insert(0, '.')
from app import app

def test_sync_final():
    with app.test_client() as client:
        print("=" * 80)
        print("TESTE FINAL DE SINCRONIZAÇÃO DE PROGRESSO")
        print("=" * 80)
        
        # Obter dados do Dashboard
        print("\n1. CARREGANDO DADOS DO DASHBOARD...")
        dashboard_response = client.get('/api/dashboard')
        dashboard_data = dashboard_response.get_json()
        dashboard_progresso = dashboard_data["progresso_disciplinas"]
        
        print("✅ Dashboard carregado com sucesso")
        
        # Obter dados das Disciplinas
        print("\n2. CARREGANDO DADOS DAS DISCIPLINAS...")
        disciplinas_response = client.get('/api/disciplinas')
        disciplinas_data = disciplinas_response.get_json()
        
        print("✅ Disciplinas carregadas com sucesso")
        
        # Comparar progresso
        print("\n3. COMPARANDO PROGRESSO:")
        print("-" * 80)
        print(f"{'Sigla':<8} {'Dashboard':<15} {'Disciplinas':<15} {'Status':<10}")
        print("-" * 80)
        
        todas_sincronizadas = True
        for disc in disciplinas_data:
            sigla = disc["sigla"]
            disc_progresso = disc.get("progresso", 0)
            dashboard_prog = dashboard_progresso.get(sigla, {}).get("progresso", 0)
            
            # Comparar com tolerância de 0.01% (arredondamento)
            sincronizado = abs(disc_progresso - dashboard_prog) < 0.01
            status = "✅ OK" if sincronizado else "❌ ERRO"
            
            if not sincronizado:
                todas_sincronizadas = False
            
            print(f"{sigla:<8} {dashboard_prog:<15.2f} {disc_progresso:<15.2f} {status:<10}")
        
        print("-" * 80)
        
        if todas_sincronizadas:
            print("\n✅ SUCESSO! Todos os progressos estão sincronizados!")
        else:
            print("\n❌ ERRO! Alguns progressos não estão sincronizados!")
            sys.exit(1)
        
        print("\n" + "=" * 80)
        print("TESTE CONCLUÍDO COM SUCESSO")
        print("=" * 80)

if __name__ == "__main__":
    test_sync_final()

