#!/bin/bash

# ============================================================
# Sistema de Planejamento de Estudos UAB LEI
# Versão 2.0 - Com Integração Moodle e IA
# ============================================================

clear
echo "=========================================="
echo "  🎓 Sistema de Estudos UAB LEI v2.0"
echo "=========================================="
echo ""
echo "✨ Funcionalidades:"
echo "  📊 Dashboard e Estatísticas"
echo "  📅 Calendário e Timer Pomodoro"
echo "  📝 Gerenciamento de Tarefas"
echo "  🏫 Integração Moodle UAB"
echo "  🤖 Assistente IA"
echo ""
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
    echo "💡 Instale: sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"

# Criar ambiente virtual se não existir
if [ ! -d "backend/venv" ]; then
    echo ""
    echo "📦 Criando ambiente virtual Python..."
    python3 -m venv backend/venv
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao criar ambiente virtual"
        echo "💡 Instale: sudo apt install python3-venv"
        exit 1
    fi
    echo "✅ Ambiente virtual criado"
fi

# Ativar ambiente virtual e instalar dependências
echo ""
echo "📥 Instalando/Atualizando dependências..."
echo "   (Isso pode levar alguns minutos na primeira vez)"
echo ""

backend/venv/bin/pip install -q --upgrade pip

# Instalar dependências básicas
backend/venv/bin/pip install -q Flask==3.0.0 Flask-CORS==4.0.0 \
    Werkzeug==3.0.1 pytz==2024.1

# Instalar dependências do Moodle (sem lxml para Python 3.13)
echo "   📚 Instalando módulos Moodle..."
backend/venv/bin/pip install -q requests==2.32.3 beautifulsoup4==4.12.3 \
    selenium==4.16.0 webdriver-manager==4.0.2

# Instalar dependências de PDF
echo "   📄 Instalando processadores de PDF..."
backend/venv/bin/pip install -q PyPDF2==3.0.1 pdfplumber==0.10.3

# Instalar dependências de IA (OpenRouter + Gemini)
echo "   🤖 Instalando módulos de IA..."
backend/venv/bin/pip install -q openai==1.52.0 httpx==0.27.2 tiktoken==0.7.0 2>/dev/null || \
    echo "   ⚠️  Módulos IA opcionais não instalados"

# Instalar utilitários
echo "   🔧 Instalando utilitários..."
backend/venv/bin/pip install -q python-dotenv==1.0.1 schedule==1.2.1 \
    pillow==10.4.0 sqlalchemy==2.0.35 APScheduler==3.10.4

if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências"
    exit 1
fi

echo "✅ Todas as dependências instaladas"

# Criar diretórios de dados
echo ""
echo "📁 Criando estrutura de diretórios..."
mkdir -p data/moodle/materials
mkdir -p data/ai
echo "✅ Diretórios criados"

# Parar servidor anterior se existir
echo ""
echo "🔍 Verificando porta 5000..."
PID=$(lsof -ti:5000 2>/dev/null)
if [ ! -z "$PID" ]; then
    echo "⏹️  Parando servidor anterior (PID: $PID)..."
    kill -9 $PID 2>/dev/null
    sleep 2
fi

# Verificar configurações de API
echo ""
echo "🔑 Verificando configurações..."

if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "⚠️  OPENROUTER_API_KEY não configurada"
    echo "   💡 Para habilitar IA: export OPENROUTER_API_KEY='sk-or-v1-...'"
    echo "   📝 Obtenha em: https://openrouter.ai/keys"
    echo "   🤖 Usando: Google Gemini (gratuito!)"
else
    echo "✅ OPENROUTER_API_KEY configurada"
fi

if [ -z "$MOODLE_USERNAME" ] || [ -z "$MOODLE_PASSWORD" ]; then
    echo "ℹ️  Credenciais Moodle não salvas (login manual necessário)"
else
    echo "✅ Credenciais Moodle configuradas"
fi

# Iniciar backend
echo ""
echo "🚀 Iniciando servidor backend..."
cd backend

# Criar arquivo de log se não existir
touch ../backend.log

# Iniciar servidor em background
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
        echo "💡 Verifique os logs: tail -f backend.log"
        exit 1
    fi
    sleep 1
done

# Verificar módulos disponíveis
echo ""
echo "📊 Verificando módulos disponíveis..."
sleep 1

# Verificar Moodle
if curl -s http://localhost:5000/api/moodle/status | grep -q "available"; then
    echo "✅ Módulo Moodle: Disponível"
else
    echo "⚠️  Módulo Moodle: Indisponível"
fi

# Verificar IA
if curl -s http://localhost:5000/api/ai/status | grep -q "available"; then
    echo "✅ Módulo IA: Disponível"
else
    echo "⚠️  Módulo IA: Indisponível"
fi

# Preparar frontend
echo ""
echo "🌐 Preparando frontend..."

# Abrir frontend no navegador (apenas uma vez)
FRONTEND_PATH="file://$(pwd)/frontend/index.html"

echo "🌐 Abrindo aplicação no navegador..."

# Verificar se há navegador aberto e abrir apenas uma aba
BROWSER_OPENED=false

# Tentar abrir com xdg-open (Linux)
if command -v xdg-open > /dev/null; then
    xdg-open "$FRONTEND_PATH" 2>/dev/null &
    BROWSER_OPENED=true
    sleep 3
fi

# Se xdg-open não funcionou, tentar firefox
if [ "$BROWSER_OPENED" = false ] && command -v firefox > /dev/null; then
    firefox "$FRONTEND_PATH" 2>/dev/null &
    BROWSER_OPENED=true
    sleep 3
fi

# Se ainda não abriu, tentar google-chrome
if [ "$BROWSER_OPENED" = false ] && command -v google-chrome > /dev/null; then
    google-chrome "$FRONTEND_PATH" 2>/dev/null &
    BROWSER_OPENED=true
    sleep 3
fi

# Se ainda não abriu, tentar chromium
if [ "$BROWSER_OPENED" = false ] && command -v chromium-browser > /dev/null; then
    chromium-browser "$FRONTEND_PATH" 2>/dev/null &
    BROWSER_OPENED=true
    sleep 3
fi

# Se nenhum navegador foi aberto
if [ "$BROWSER_OPENED" = false ]; then
    echo "⚠️  Navegador não detectado automaticamente"
    echo "   Abra manualmente: $FRONTEND_PATH"
fi

# Informações finais
echo ""
echo "=========================================="
echo "  ✨ Sistema Iniciado com Sucesso!"
echo "=========================================="
echo ""
echo "📱 Acesso:"
echo "   Frontend: $FRONTEND_PATH"
echo "   API: http://localhost:5000"
echo ""
echo "📚 Funcionalidades Disponíveis:"
echo "   📊 Dashboard - Visão geral de estudos"
echo "   📅 Calendário - Planejamento semanal"
echo "   📝 Tarefas - Gerenciamento de atividades"
echo "   ⏱️  Timer - Pomodoro para foco"
echo "   📈 Estatísticas - Análise de desempenho"
echo "   🏫 Moodle - Sincronização UAB"
echo "   🤖 IA - Assistente inteligente"
echo "   💬 Chat Flutuante - Botão roxo no canto inferior direito"
echo ""
echo "🔧 Configurações Opcionais:"
echo "   export OPENROUTER_API_KEY='sk-or-v1-...'  # Habilitar IA (Gemini)"
echo "   export MOODLE_USERNAME='...'     # Auto-login Moodle"
echo "   export MOODLE_PASSWORD='...'     # Auto-login Moodle"
echo ""
echo "📋 Comandos Úteis:"
echo "   🛑 Parar servidor: kill $BACKEND_PID"
echo "   📄 Ver logs: tail -f backend.log"
echo "   🔄 Reiniciar: ./restart.sh"
echo ""
echo "💡 Dicas:"
echo "   • Clique no botão ROXO 🤖 no canto para usar o Chat IA"
echo "   • Use o Timer Pomodoro para sessões focadas"
echo "   • Sincronize o Moodle para importar tarefas"
echo "   • Use a IA para resumir PDFs e tirar dúvidas"
echo "   • Acompanhe seu progresso no Dashboard"
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
echo "📊 Monitorando sistema..."
echo ""

# Esperar indefinidamente
while kill -0 $BACKEND_PID 2>/dev/null; do
    sleep 30
done

echo ""
echo "⚠️  Servidor parou inesperadamente"
echo "💡 Verifique os logs: cat backend.log"
exit 1
ENDOFFILE </dev/null