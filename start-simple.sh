#!/bin/bash

# ============================================================
# Sistema de Planejamento de Estudos UAB LEI
# Script Simplificado - SEM abertura automática do navegador
# ============================================================

clear
echo "=========================================="
echo "  🎓 Sistema de Estudos UAB LEI v2.0"
echo "=========================================="
echo ""

# Verificar se está no diretório correto
if [ ! -f "backend/app.py" ]; then
    echo "❌ ERRO: Execute este script a partir da pasta study-planner"
    exit 1
fi

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado!"
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"

# Criar ambiente virtual se não existir
if [ ! -d "backend/venv" ]; then
    echo ""
    echo "📦 Criando ambiente virtual Python..."
    python3 -m venv backend/venv
    echo "✅ Ambiente virtual criado"
fi

# Instalar dependências
echo ""
echo "📥 Instalando/Atualizando dependências..."
backend/venv/bin/pip install -q --upgrade pip
backend/venv/bin/pip install -q Flask==3.0.0 Flask-CORS==4.0.0 Werkzeug==3.0.1 pytz==2024.1
backend/venv/bin/pip install -q requests==2.32.3 beautifulsoup4==4.12.3 selenium==4.16.0 webdriver-manager==4.0.2
backend/venv/bin/pip install -q PyPDF2==3.0.1 pdfplumber==0.10.3
backend/venv/bin/pip install -q openai==1.52.0 httpx==0.27.2 tiktoken==0.7.0 2>/dev/null || true
backend/venv/bin/pip install -q python-dotenv==1.0.1 schedule==1.2.1 pillow==10.4.0 sqlalchemy==2.0.35 APScheduler==3.10.4

echo "✅ Todas as dependências instaladas"

# Criar diretórios de dados
mkdir -p data/moodle/materials
mkdir -p data/ai

# Parar servidor anterior se existir
PID=$(lsof -ti:5000 2>/dev/null)
if [ ! -z "$PID" ]; then
    echo ""
    echo "⏹️  Parando servidor anterior (PID: $PID)..."
    kill -9 $PID 2>/dev/null
    sleep 2
fi

# Iniciar backend
echo ""
echo "🚀 Iniciando servidor backend..."
cd backend
touch ../backend.log
nohup ./venv/bin/python app.py > ../backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > ../.backend.pid
cd ..

# Aguardar servidor iniciar
echo "⏳ Aguardando servidor iniciar..."
for i in {1..10}; do
    if curl -s http://localhost:5000/ > /dev/null 2>&1; then
        echo "✅ Backend iniciado com sucesso! (PID: $BACKEND_PID)"
        break
    fi
    if [ $i -eq 10 ]; then
        echo "❌ Timeout ao iniciar servidor"
        exit 1
    fi
    sleep 1
done

# Informações finais
echo ""
echo "=========================================="
echo "  ✨ Sistema Iniciado com Sucesso!"
echo "=========================================="
echo ""
echo "📱 Acesso:"
echo "   🌐 Abra no navegador: http://localhost:5000"
echo "   📊 API: http://localhost:5000/api"
echo ""
echo "📋 Comandos Úteis:"
echo "   🛑 Parar servidor: kill $BACKEND_PID"
echo "   📄 Ver logs: tail -f backend.log"
echo ""
echo "⚠️  IMPORTANTE:"
echo "   Abra MANUALMENTE no navegador: http://localhost:5000"
echo "   (Isso evita múltiplas abas)"
echo ""
echo "=========================================="
echo ""
echo "Pressione Ctrl+C para parar o servidor..."
echo ""

# Função de limpeza ao sair
cleanup() {
    echo ""
    echo "⏹️  Parando servidor..."
    kill $BACKEND_PID 2>/dev/null
    rm -f .backend.pid
    echo "✅ Servidor parado com sucesso"
    echo "👋 Até logo!"
    exit 0
}

# Capturar sinais de interrupção
trap cleanup INT TERM

# Monitorar processo
while kill -0 $BACKEND_PID 2>/dev/null; do
    sleep 30
done

echo ""
echo "⚠️  Servidor parou inesperadamente"
exit 1

