#!/usr/bin/env python3
"""
Script para testar se o progresso está sincronizado entre Dashboard e Disciplinas
"""
import json
import sys
sys.path.insert(0, '.')
from app import app, get_db_connection, load_disciplinas

def test_progresso_sync():
    with app.app_context():
        print("=" * 80)
        print("TESTE DE SINCRONIZAÇÃO DE PROGRESSO")
        print("=" * 80)
        
        # Carregar dados
        data = load_disciplinas()
        conn = get_db_connection()
        
        # Teste 1: Verificar cálculo de progresso para cada disciplina
        print("\n1. CÁLCULO DE PROGRESSO POR DISCIPLINA:")
        print("-" * 80)
        
        for disc in data["disciplinas"]:
            disc_id = disc["id"]
            sigla = disc["sigla"]
            nome = disc["nome"]
            creditos = disc.get("creditos", 6)
            
            # Sessões de estudo
            sessoes = conn.execute(
                "SELECT COUNT(*) as total FROM sessoes_estudo WHERE disciplina_id = ?",
                (disc_id,)
            ).fetchone()
            total_sessoes = sessoes["total"] or 0
            total_minutos = total_sessoes * 25
            
            # Progresso de tempo
            progresso_tempo = min((total_minutos / (creditos * 26 * 60)) * 100, 100) if total_minutos > 0 else 0
            
            # AFs
            afs = conn.execute(
                """SELECT COUNT(*) as total, SUM(CASE WHEN concluida = 1 THEN 1 ELSE 0 END) as concluidas
                   FROM tarefas WHERE disciplina_id = ? AND tipo = 'forum'""",
                (disc_id,)
            ).fetchone()
            total_afs = afs["total"] or 0
            afs_concluidas = afs["concluidas"] or 0
            progresso_afs = (afs_concluidas / total_afs * 100) if total_afs > 0 else 0
            
            # Progresso final
            if total_afs > 0:
                progresso_final = (progresso_tempo * 0.7) + (progresso_afs * 0.3)
            else:
                progresso_final = progresso_tempo
            
            print(f"\n{sigla} - {nome}")
            print(f"  Sessões: {total_sessoes} ({total_minutos} min)")
            print(f"  Progresso Tempo: {progresso_tempo:.2f}%")
            print(f"  AFs: {afs_concluidas}/{total_afs} ({progresso_afs:.2f}%)")
            print(f"  Progresso Final: {progresso_final:.2f}%")
        
        # Teste 2: Comparar com endpoint /api/dashboard
        print("\n\n2. COMPARAÇÃO COM ENDPOINT /api/dashboard:")
        print("-" * 80)
        
        with app.test_client() as client:
            response = client.get('/api/dashboard')
            dashboard_data = response.get_json()
            
            print("\nProgresso do Dashboard:")
            for sigla, disc_info in dashboard_data["progresso_disciplinas"].items():
                print(f"  {sigla}: {disc_info['progresso']:.2f}%")
        
        conn.close()
        print("\n" + "=" * 80)
        print("✅ TESTE CONCLUÍDO")
        print("=" * 80)

if __name__ == "__main__":
    test_progresso_sync()

