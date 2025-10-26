#!/bin/bash

# Script de Reinicialização Rápida
# Sistema de Planejamento de Estudos UAB LEI

echo "🔄 Reiniciando servidor..."
echo ""

# Matar processo na porta 5000
echo "⏹️  Parando servidor anterior..."
PID=$(lsof -ti:5000 2>/dev/null)
if [ ! -z "$PID" ]; then
    kill -9 $PID 2>/dev/null
    echo "✅ Servidor parado (PID: $PID)"
else
    echo "ℹ️  Nenhum servidor rodando"
fi

# Limpar PID file
rm -f .backend.pid

# Aguardar um momento
sleep 2

# Iniciar servidor novamente
echo ""
echo "🚀 Iniciando servidor..."
cd backend
nohup ./venv/bin/python app.py > ../backend.log 2>&1 &
NEW_PID=$!
echo $NEW_PID > ../.backend.pid
cd ..

echo "✅ Servidor iniciado (PID: $NEW_PID)"
echo ""
echo "⏳ Aguardando 3 segundos..."
sleep 3

# Verificar se está funcionando
if curl -s http://localhost:5000/ > /dev/null 2>&1; then
    echo "✅ Servidor funcionando!"
    echo "🌐 API: http://localhost:5000"
    echo "🌐 Frontend: file://$(pwd)/frontend/index.html"
else
    echo "❌ Servidor não respondeu"
    echo "💡 Verifique: cat backend.log"
fi

echo ""
echo "📄 Ver logs: tail -f backend.log"
echo "🛑 Parar: kill $NEW_PID"
echo ""
