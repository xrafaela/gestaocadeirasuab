@echo off
REM ============================================================
REM Sistema de Planejamento de Estudos UAB LEI
REM Script de Inicialização para Windows
REM ============================================================

cls
echo ==========================================
echo   🎓 Sistema de Estudos UAB LEI v2.0
echo ==========================================
echo.

REM Verificar se está no diretório correto
if not exist "backend\app.py" (
    echo ❌ ERRO: Execute este script a partir da pasta study-planner
    pause
    exit /b 1
)

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo.
    echo 📥 Instale o Python 3.12 ou superior:
    echo    https://www.python.org/downloads/
    echo.
    echo ⚠️  IMPORTANTE: Marque "Add Python to PATH" durante a instalação
    pause
    exit /b 1
)

echo ✅ Python encontrado
python --version

REM Criar ambiente virtual se não existir
if not exist "backend\venv" (
    echo.
    echo 📦 Criando ambiente virtual Python...
    python -m venv backend\venv
    echo ✅ Ambiente virtual criado
)

REM Ativar ambiente virtual
echo.
echo 🔧 Ativando ambiente virtual...
call backend\venv\Scripts\activate.bat

REM Instalar/Atualizar dependências
echo.
echo 📥 Instalando/Atualizando dependências...
echo    (Isso pode levar alguns minutos na primeira vez)
echo.

python -m pip install --upgrade pip --quiet
pip install Flask==3.0.0 Flask-CORS==4.0.0 Werkzeug==3.0.1 pytz==2024.1 --quiet
pip install requests==2.32.3 beautifulsoup4==4.12.3 selenium==4.16.0 webdriver-manager==4.0.2 --quiet
pip install PyPDF2==3.0.1 pdfplumber==0.10.3 --quiet
pip install python-dotenv==1.0.1 schedule==1.2.1 pillow==10.4.0 sqlalchemy==2.0.35 APScheduler==3.10.4 --quiet

echo ✅ Todas as dependências instaladas

REM Criar diretórios de dados
if not exist "data\moodle\materials" mkdir data\moodle\materials
if not exist "data\ai" mkdir data\ai

REM Verificar se a porta 5000 está em uso
netstat -ano | findstr :5000 >nul 2>&1
if not errorlevel 1 (
    echo.
    echo ⚠️  Porta 5000 já está em uso
    echo    Tentando liberar a porta...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000') do (
        taskkill /PID %%a /F >nul 2>&1
    )
    timeout /t 2 /nobreak >nul
)

REM Iniciar backend
echo.
echo 🚀 Iniciando servidor backend...
cd backend
start /B python app.py > ..\backend.log 2>&1
cd ..

REM Aguardar servidor iniciar
echo ⏳ Aguardando servidor iniciar...
timeout /t 3 /nobreak >nul

REM Verificar se o servidor está rodando
for /L %%i in (1,1,10) do (
    curl -s http://localhost:5000/ >nul 2>&1
    if not errorlevel 1 (
        echo ✅ Backend iniciado com sucesso!
        goto :server_started
    )
    timeout /t 1 /nobreak >nul
)

echo ❌ Timeout ao iniciar servidor
echo    Verifique o arquivo backend.log para mais detalhes
pause
exit /b 1

:server_started

REM Abrir navegador
echo.
echo 🌐 Abrindo aplicação no navegador...
start http://localhost:5000

REM Informações finais
echo.
echo ==========================================
echo   ✨ Sistema Iniciado com Sucesso!
echo ==========================================
echo.
echo 📱 Acesso:
echo    🌐 URL: http://localhost:5000
echo    📊 API: http://localhost:5000/api
echo.
echo 📋 Comandos Úteis:
echo    🛑 Parar servidor: Pressione Ctrl+C
echo    📄 Ver logs: type backend.log
echo.
echo ⚠️  IMPORTANTE:
echo    Mantenha esta janela aberta enquanto usa o sistema
echo    Para parar o servidor, pressione Ctrl+C
echo.
echo ==========================================
echo.
echo Pressione Ctrl+C para parar o servidor...
echo.

REM Manter o script rodando
:loop
timeout /t 30 /nobreak >nul
curl -s http://localhost:5000/ >nul 2>&1
if errorlevel 1 (
    echo.
    echo ⚠️  Servidor parou inesperadamente
    pause
    exit /b 1
)
goto :loop

