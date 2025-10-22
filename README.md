# 🎓 Sistema de Estudos UAB LEI v2.0

Sistema completo e inteligente de gerenciamento de estudos com integração Moodle, Assistente IA e sincronização automática de pastas para estudantes da Universidade Aberta de Portugal - Licenciatura em Engenharia Informática.

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

---

## 📋 O que é o Study Planner?

O **Study Planner** é uma plataforma web completa desenvolvida para otimizar o processo de aprendizagem de estudantes da UAB LEI. Combina:

- 📊 **Gestão inteligente de tempo** com técnica Pomodoro
- 🏫 **Sincronização automática** com Moodle UAB
- 🤖 **Assistente IA** para dúvidas e planejamento
- 📁 **Sincronização de pastas** locais com o sistema
- 📈 **Análise detalhada** de progresso e produtividade
- 🔔 **Notificações em tempo real** de eventos importantes

---

## ✨ Funcionalidades Principais

### 📊 Dashboard e Gestão Completa
- ✅ **Visão geral de estatísticas** - horas estudadas, disciplinas, progresso
- ✅ **Monitoramento de metas** - diárias, semanais e por disciplina
- ✅ **Progresso em tempo real** - atualização automática de dados
- ✅ **Calendário semanal interativo** - visualização de eventos e tarefas
- ✅ **Gerenciamento de tarefas** - criação, edição, conclusão de tarefas
- ✅ **Gestão de e-fólios** - acompanhamento de avaliações contínuas
- ✅ **Histórico de sessões** - registro completo de todas as sessões de estudo

### ⏱️ Timer Pomodoro Avançado
- ✅ **Técnica Pomodoro completa** - 25min estudo + 5min pausa + 15min pausa longa
- ✅ **Registro automático** de todas as sessões de estudo
- ✅ **Contabilização por disciplina** - horas estudadas em cada matéria
- ✅ **Estatísticas detalhadas** - gráficos de produtividade e tendências
- ✅ **Sincronização com banco de dados** - persistência de dados
- ✅ **Notificações sonoras** - alertas de fim de sessão
- ✅ **Pausa automática** quando a aba perde foco

### 🏫 Integração Completa com Moodle UAB
- ✅ **Login automático** - autenticação segura no portal Moodle
- ✅ **Buscar disciplinas** - lista completa de cursos matriculados
- ✅ **Sincronizar tarefas** - importação automática de e-fólios e prazos
- ✅ **Baixar materiais** - PDFs e recursos das disciplinas
- ✅ **Sincronizar calendário** - eventos e datas importantes
- ✅ **Ler fóruns** - acesso a discussões e posts importantes
- ✅ **Verificar notas** - acompanhamento de avaliações em tempo real
- ✅ **Notificações** - alertas de novos materiais e mensagens
- ✅ **Sincronização programada** - atualização automática em intervalos

### 🤖 Assistente IA Inteligente (OpenAI/OpenRouter)
- ✅ **Chat interativo** - tire dúvidas sobre qualquer matéria
- ✅ **Resumir PDFs** - geração automática de resumos concisos
- ✅ **Explicações didáticas** - conceitos complexos simplificados
- ✅ **Sínteses de aulas** - resumos estruturados de conteúdo
- ✅ **Geração de flashcards** - criação automática de cartões de estudo
- ✅ **Planos de estudo personalizados** - rotinas adaptadas ao seu ritmo
- ✅ **Análise de fóruns** - identificação de posts importantes
- ✅ **Suporte a múltiplas APIs** - OpenAI e OpenRouter

### 📁 Sincronização de Pastas (Folder Sync)
- ✅ **Monitoramento automático** de pastas locais
- ✅ **Sincronização bidirecional** de arquivos
- ✅ **Detecção de mudanças** em tempo real
- ✅ **Organização automática** de materiais por disciplina
- ✅ **Backup automático** de arquivos importantes

### 📈 Dashboard Aprimorado
- ✅ **Materiais novos** - últimos recursos do Moodle
- ✅ **Próximas tarefas** - prazos sincronizados
- ✅ **Posts importantes** - fóruns prioritários
- ✅ **Status de sincronização** - informações em tempo real
- ✅ **Chat IA integrado** - assistente sempre disponível
- ✅ **Gráficos de produtividade** - visualização de tendências

---

## 🚀 Instalação Rápida

### Pré-requisitos

- **Sistema Operacional:** Linux (Ubuntu/Debian recomendado)
- **Python:** 3.8 ou superior
- **Navegador:** Firefox, Chrome ou Chromium
- **Conexão Internet:** Necessária para Moodle e IA
- **Espaço em disco:** ~500MB (incluindo dependências)

### Instalação em 3 Passos

```bash
# 1. Entre na pasta do projeto
cd Documentos/LEI/study-planner

# 2. Execute o script de inicialização
./start.sh

# 3. Pronto! O sistema abrirá automaticamente no navegador
```

O script `start.sh` irá:
- ✅ Criar ambiente virtual Python
- ✅ Instalar todas as dependências automaticamente
- ✅ Configurar estrutura de diretórios
- ✅ Inicializar banco de dados SQLite
- ✅ Iniciar servidor backend Flask
- ✅ Abrir aplicação no navegador (http://localhost:5000)

### Instalação em Windows

#### Pré-requisitos para Windows

1. **Python 3.8+** - Baixe em https://www.python.org/downloads/
   - ⚠️ **IMPORTANTE:** Marque "Add Python to PATH" durante a instalação
   - Verifique a instalação: `python --version`

2. **Git** - Baixe em https://git-scm.com/download/win
   - Instale com as opções padrão

3. **Navegador** - Firefox, Chrome ou Edge

#### Instalação Passo a Passo (Windows)

**Passo 1: Clonar o repositório**
```bash
# Abra o PowerShell ou CMD
git clone https://github.com/igorcostas/study-planner.git
cd study-planner
```

**Passo 2: Criar ambiente virtual**
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# No PowerShell:
.\venv\Scripts\Activate.ps1

# No CMD:
venv\Scripts\activate.bat
```

**Passo 3: Instalar dependências**
```bash
# Navegar para pasta backend
cd backend

# Instalar dependências
pip install -r requirements.txt

# Voltar para pasta raiz
cd ..
```

**Passo 4: Inicializar banco de dados**
```bash
# Criar estrutura de diretórios
mkdir data
mkdir data\moodle
mkdir data\ai

# Inicializar banco de dados (execute Python)
python -c "from backend.app import init_db; init_db()"
```

**Passo 5: Iniciar o servidor**
```bash
# Ativar ambiente virtual (se não estiver ativo)
.\venv\Scripts\Activate.ps1

# Iniciar servidor Flask
python backend/app.py
```

**Passo 6: Acessar a aplicação**
- Abra seu navegador em: `http://localhost:5000`
- A aplicação deve carregar automaticamente

#### Troubleshooting Windows

**Problema: "Python não é reconhecido"**
- Reinstale Python e marque "Add Python to PATH"
- Ou adicione manualmente: `C:\Users\SeuUsuario\AppData\Local\Programs\Python\Python311`

**Problema: "Permissão negada ao ativar venv"**
```bash
# Execute PowerShell como Administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Problema: Porta 5000 em uso**
```bash
# Encontrar processo usando porta 5000
netstat -ano | findstr :5000

# Matar processo (substitua PID)
taskkill /PID <PID> /F

# Ou usar porta diferente
set FLASK_PORT=5001
python backend/app.py
```

**Problema: Módulos não encontrados**
```bash
# Verificar se venv está ativado (deve ter (venv) no prompt)
# Se não, execute:
.\venv\Scripts\Activate.ps1

# Reinstalar dependências
pip install --upgrade pip
pip install -r backend/requirements.txt
```

#### Criar Atalho no Desktop (Windows)

Para facilitar o acesso, crie um arquivo `iniciar.bat`:

```batch
@echo off
cd /d "%~dp0"
.\venv\Scripts\activate.bat
python backend/app.py
pause
```

Salve como `iniciar.bat` na pasta raiz do projeto e clique duas vezes para iniciar.

---

## 📁 Tutorial: Sincronização de Pastas

### O que é Sincronização de Pastas?

A sincronização de pastas permite que o Study Planner monitore automaticamente pastas locais no seu computador e organize os materiais de estudo por disciplina. Qualquer arquivo adicionado às pastas será sincronizado com o sistema.

### Passo 1: Criar Estrutura de Pastas

Crie uma pasta principal para seus estudos e subpastas para cada disciplina:

```
Meus Estudos/
├── Fundamentos de Bases de Dados (FBD)/
│   ├── Aulas/
│   ├── Exercícios/
│   ├── e-Fólios/
│   └── Notas/
├── Programação por Objetos (PO)/
│   ├── Aulas/
│   ├── Projetos/
│   ├── e-Fólios/
│   └── Notas/
├── Arquitetura de Computadores (AC)/
│   ├── Aulas/
│   ├── Exercícios/
│   ├── e-Fólios/
│   └── Notas/
└── Sistemas em Rede (SR)/
    ├── Aulas/
    ├── Projetos/
    ├── e-Fólios/
    └── Notas/
```

### Passo 2: Configurar Sincronização no Study Planner

#### Linux/Mac

1. Abra o arquivo `.env` na pasta raiz do projeto:
```bash
nano .env
```

2. Adicione a configuração de pastas a sincronizar:
```bash
# Sincronização de Pastas
SYNC_FOLDERS='["/home/seu_usuario/Meus Estudos/Fundamentos de Bases de Dados (FBD)", "/home/seu_usuario/Meus Estudos/Programação por Objetos (PO)"]'
SYNC_INTERVAL=300  # Sincronizar a cada 5 minutos
```

3. Salve o arquivo (Ctrl+O, Enter, Ctrl+X)

#### Windows

1. Abra o arquivo `.env` com Bloco de Notas:
```
C:\Users\SeuUsuario\study-planner\.env
```

2. Adicione a configuração:
```
SYNC_FOLDERS='["C:\\Users\\SeuUsuario\\Meus Estudos\\Fundamentos de Bases de Dados (FBD)", "C:\\Users\\SeuUsuario\\Meus Estudos\\Programação por Objetos (PO)"]'
SYNC_INTERVAL=300
```

### Passo 3: Reiniciar o Servidor

```bash
# Linux/Mac
./restart.sh

# Windows
.\venv\Scripts\Activate.ps1
python backend/app.py
```

### Passo 4: Verificar Sincronização

1. Abra o Study Planner em `http://localhost:5000`
2. Vá para a aba "Disciplinas"
3. Clique em uma disciplina para ver os materiais sincronizados
4. Adicione um arquivo à pasta local e aguarde 5 minutos (ou o intervalo configurado)
5. O arquivo deve aparecer automaticamente no sistema

### Dicas de Organização

**Estrutura Recomendada por Disciplina:**

```
Disciplina/
├── 📚 Aulas/
│   ├── Semana 1 - Introdução.pdf
│   ├── Semana 2 - Conceitos Básicos.pdf
│   └── Semana 3 - Aplicações.pdf
├── 📝 Exercícios/
│   ├── Lista 1.pdf
│   ├── Lista 2.pdf
│   └── Soluções/
├── 📋 e-Fólios/
│   ├── e-Fólio A/
│   │   ├── Enunciado.pdf
│   │   ├── Minha Solução.docx
│   │   └── Feedback.pdf
│   └── e-Fólio B/
└── 📌 Notas/
    ├── Resumo Tópico 1.md
    ├── Resumo Tópico 2.md
    └── Flashcards.txt
```

### Sincronização Automática

O sistema sincroniza automaticamente:
- ✅ Novos arquivos adicionados
- ✅ Arquivos modificados
- ✅ Estrutura de pastas
- ✅ Metadados (data de criação, tamanho)

### Troubleshooting

**Problema: Arquivos não sincronizam**
```bash
# Verificar configuração
cat .env | grep SYNC

# Testar sincronização manualmente
python backend/folder_sync.py

# Ver logs
tail -f backend.log
```

**Problema: Permissão negada**
```bash
# Linux/Mac - dar permissões
chmod -R 755 "/caminho/para/pasta"

# Windows - executar como Administrador
```

---

## ⚙️ Configuração

### Configuração Básica (Funciona Imediatamente)

O sistema funciona **sem configuração adicional** com as seguintes funcionalidades:
- ✅ Dashboard completo
- ✅ Calendário semanal
- ✅ Timer Pomodoro
- ✅ Gestão de tarefas
- ✅ Histórico de sessões
- ✅ Estatísticas locais

### Configuração Avançada (Opcional)

#### 1. Habilitar Assistente IA

O sistema suporta **OpenAI** e **OpenRouter**. Escolha uma opção:

**Opção A: OpenAI (GPT-3.5-turbo)**
```bash
# 1. Obtenha sua chave em: https://platform.openai.com/api-keys
# 2. Configure a variável de ambiente:
export OPENAI_API_KEY='sk-sua-chave-aqui'

# 3. Para tornar permanente, adicione ao ~/.bashrc:
echo 'export OPENAI_API_KEY="sk-sua-chave-aqui"' >> ~/.bashrc
source ~/.bashrc

# 4. Reinicie o servidor:
./restart.sh
```

**Opção B: OpenRouter (Alternativa mais barata)**
```bash
# 1. Obtenha sua chave em: https://openrouter.ai/
# 2. Configure a variável de ambiente:
export OPENROUTER_API_KEY='sk-sua-chave-aqui'

# 3. Para tornar permanente:
echo 'export OPENROUTER_API_KEY="sk-sua-chave-aqui"' >> ~/.bashrc
source ~/.bashrc

# 4. Reinicie o servidor:
./restart.sh
```

**Custos:**
- OpenAI GPT-3.5-turbo: ~$0.002 por 1K tokens (~$2-5/mês)
- OpenRouter: Modelos variados, geralmente mais baratos

#### 2. Auto-login no Moodle (Opcional)

```bash
# Configure suas credenciais (use apenas em computador pessoal):
export MOODLE_USERNAME='seu_usuario_uab'
export MOODLE_PASSWORD='sua_senha'

# Para tornar permanente:
echo 'export MOODLE_USERNAME="seu_usuario"' >> ~/.bashrc
echo 'export MOODLE_PASSWORD="sua_senha"' >> ~/.bashrc
source ~/.bashrc

./restart.sh
```

**⚠️ Segurança:** O sistema armazena apenas a sessão temporária, não as credenciais em disco.

#### 3. Sincronização de Pastas (Folder Sync)

```bash
# Configure as pastas a sincronizar no arquivo .env:
SYNC_FOLDERS='["/caminho/pasta1", "/caminho/pasta2"]'
SYNC_INTERVAL=300  # Sincronizar a cada 5 minutos

./restart.sh
```

#### 4. Arquivo .env (Recomendado)

```bash
# Copie o arquivo de exemplo (se existir):
cp .env.example .env

# Edite com suas configurações:
nano .env

# Variáveis disponíveis:
# OPENAI_API_KEY=sk-...
# OPENROUTER_API_KEY=sk-...
# MOODLE_USERNAME=seu_usuario
# MOODLE_PASSWORD=sua_senha
# SYNC_FOLDERS=[...]
# SYNC_INTERVAL=300
```

---

## 📖 Uso Básico

### Primeiro Acesso

1. **Inicie o sistema:**
   ```bash
   ./start.sh
   ```
   A aplicação abrirá automaticamente em `http://localhost:5000`

2. **Explore o Dashboard:**
   - Visualize suas estatísticas de estudo
   - Veja horas estudadas por disciplina
   - Acompanhe progresso semanal
   - Configure suas disciplinas

3. **Conecte ao Moodle (Opcional):**
   - Clique na aba "Moodle"
   - Faça login com credenciais UAB
   - Aguarde sincronização inicial (1-2 minutos)
   - Materiais e tarefas serão importados automaticamente

4. **Use o Assistente IA (Opcional):**
   - Clique na aba "IA Chat"
   - Configure sua API Key (OpenAI ou OpenRouter)
   - Comece a fazer perguntas sobre suas matérias!

5. **Comece a Estudar:**
   - Selecione uma disciplina
   - Clique em "Iniciar Timer"
   - Estude por 25 minutos (Pomodoro)
   - Faça uma pausa de 5 minutos
   - Seu progresso será registrado automaticamente

### Fluxo de Trabalho Diário Recomendado

**🌅 Início do Dia (5 minutos):**
1. Abra o Dashboard
2. Verifique notificações do Moodle
3. Revise tarefas do dia
4. Planeje suas sessões de estudo

**📚 Durante o Estudo (Contínuo):**
1. Use Timer Pomodoro para manter foco
2. Consulte IA para dúvidas conceituais
3. Registre tópicos estudados
4. Faça pausas regulares (5-15 minutos)

**🌙 Fim do Dia (10 minutos):**
1. Revise estatísticas do dia
2. Marque tarefas concluídas
3. Prepare plano para próximo dia
4. Sincronize Moodle (se configurado)

---

## 📱 Funcionalidades Detalhadas

### 🏫 Moodle UAB - Integração Completa

#### Login e Sincronização
- **Login único** - válido por 24 horas
- **Sincronização manual** - clique para atualizar
- **Sincronização automática** - configurável em intervalos
- **Dados locais** - acesso rápido mesmo offline
- **Segurança** - credenciais não são armazenadas

#### Disciplinas Suportadas
```
📚 Programação por Objetos (POO)
📚 Arquitetura de Computadores (AC)
📚 Sistemas Computacionais (SC)
📚 Fundamentos de Base de Dados (FBD)
📚 Sistemas em Rede (SR)
📚 Linguagens da Computação (LC)
📚 Engenharia de Programação (EP)
```

#### Tarefas e Prazos
- ✅ Lista completa de e-fólios com datas
- ✅ Sessões síncronas agendadas
- ✅ Alertas de prazos próximos
- ✅ Status de entrega (entregue/pendente)
- ✅ Notas e feedback dos professores
- ✅ Integração com calendário

#### Materiais e Recursos
- ✅ Download automático de PDFs
- ✅ Organização automática por disciplina
- ✅ Detecção de materiais novos
- ✅ Acesso offline após download
- ✅ Histórico de downloads
- ✅ Sincronização com pastas locais

#### Fóruns e Discussões
- ✅ Leitura de posts de fóruns
- ✅ Identificação de posts importantes
- ✅ Análise IA de discussões
- ✅ Notificações de respostas
- ✅ Histórico de participação

### 🤖 Assistente IA - Suporte Inteligente

#### Chat Interativo
```
Você: "Explique polimorfismo em POO"
IA: "Polimorfismo é a capacidade de um objeto assumir
     múltiplas formas. Em POO, permite que objetos de
     diferentes classes sejam tratados através de uma
     interface comum. Existem dois tipos principais:
     1. Polimorfismo de Compilação (Sobrecarga)
     2. Polimorfismo de Execução (Sobrescrita)
     ..."
```

#### Resumo de PDF
- **Conciso:** 200-300 palavras (resumo rápido)
- **Detalhado:** Resumo completo com exemplos
- **Tópicos:** Lista de conceitos-chave
- **Estruturado:** Seções e subtópicos organizados

#### Flashcards Automáticos
- Geração de 5-20 cards por PDF
- Formato pergunta/resposta
- Navegação interativa
- Revisão espaçada
- Exportação para Anki (em breve)

#### Plano de Estudos Personalizado
- Distribuição inteligente de horas
- Rotina diária personalizada
- Técnicas de estudo recomendadas
- Marcos e objetivos semanais
- Adaptação ao seu ritmo

#### Análise de Conteúdo
- Explicação de conceitos complexos
- Exemplos práticos
- Comparações com conceitos relacionados
- Sugestões de recursos adicionais

---

## 🔧 Comandos Úteis

```bash
# ===== INICIALIZAÇÃO =====
# Iniciar o sistema (primeira vez)
./start.sh

# Reiniciar o servidor
./restart.sh

# ===== GERENCIAMENTO =====
# Parar o servidor
kill $(cat .backend.pid)

# Ver logs em tempo real
tail -f backend.log

# Ver últimas 50 linhas de log
tail -50 backend.log

# ===== BANCO DE DADOS =====
# Limpar banco de dados (CUIDADO: deleta tudo)
./resetar_banco.sh

# Fazer backup do banco
cp data/estudos.db data/estudos_backup_$(date +%Y%m%d_%H%M%S).db

# Restaurar banco de dados
python3 restore_db.py

# ===== SINCRONIZAÇÃO =====
# Sincronizar Moodle manualmente
python3 backend/moodle_sync.py

# Sincronizar pastas locais
python3 backend/folder_sync.py

# ===== TESTES =====
# Testar funcionalidades
python3 backend/test_final_verification.py

# Testar sincronização
python3 backend/test_sync_final.py
```

---

## 📊 Estrutura do Projeto

```
study-planner/
├── backend/
│   ├── app.py                      # API Flask principal (1400+ linhas)
│   ├── moodle_integration.py       # Integração Moodle (785+ linhas)
│   ├── ai_assistant.py             # Assistente IA (181+ linhas)
│   ├── folder_sync.py              # Sincronização de pastas
│   ├── moodle_sync.py              # Script de sincronização
│   ├── extract_*.py                # Scripts de extração de dados
│   ├── update_*.py                 # Scripts de atualização
│   ├── requirements.txt            # Dependências Python
│   ├── tasks.json                  # Tarefas configuradas
│   └── venv/                       # Ambiente virtual Python
│
├── frontend/
│   ├── index.html                  # Interface principal (1761+ linhas)
│   ├── app.js                      # Lógica JavaScript (2687+ linhas)
│   ├── moodle-ia.html              # Interface Moodle/IA
│   ├── moodle-ia.js                # Scripts Moodle/IA
│   ├── chat-bar.html               # Componente chat
│   ├── timer-popup.html            # Popup do timer
│   ├── admin-folders.html          # Gerenciador de pastas
│   ├── tech-effects.js             # Efeitos visuais
│   ├── chat-fix.js                 # Correções de chat
│   └── styles.css                  # Estilos CSS
│
├── data/
│   ├── estudos.db                  # Banco de dados SQLite
│   ├── disciplinas.json            # Configuração de disciplinas
│   ├── moodle/                     # Dados sincronizados do Moodle
│   │   ├── courses.json
│   │   ├── tasks.json
│   │   ├── materials.json
│   │   └── forums.json
│   └── ai/                         # Dados da IA
│       ├── chat_history.json
│       └── study_plans.json
│
├── start.sh                        # Script de inicialização
├── restart.sh                      # Script de reinicialização
├── resetar_banco.sh                # Script de limpeza
├── restore_db.py                   # Restauração de banco
├── dump.sql                        # Dump do banco de dados
├── .env.example                    # Exemplo de configuração
├── README.md                       # Este arquivo
└── backend.log                     # Log de execução
```

---

## 🐛 Troubleshooting

### Problema: Erro ao instalar dependências

**Sintomas:** `error: command 'gcc' failed` ou `ModuleNotFoundError`

**Solução:**
```bash
# Instalar ferramentas de compilação
sudo apt install build-essential python3-dev python3-pip

# Atualizar pip
python3 -m pip install --upgrade pip

# Reinstalar dependências
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Reiniciar
./restart.sh
```

### Problema: Módulo Moodle não disponível

**Sintomas:** `⚠️ Módulo Moodle não disponível` no console

**Solução:**
```bash
source backend/venv/bin/activate
pip install requests beautifulsoup4 selenium webdriver-manager
./restart.sh
```

### Problema: IA não configurada

**Sintomas:** "Assistente IA não configurado" na interface

**Solução:**
```bash
# Opção 1: OpenAI
export OPENAI_API_KEY='sk-sua-chave'

# Opção 2: OpenRouter
export OPENROUTER_API_KEY='sk-sua-chave'

# Verificar se foi configurado
echo $OPENAI_API_KEY

# Reiniciar
./restart.sh
```

### Problema: Porta 5000 em uso

**Sintomas:** `Address already in use` ou `Errno 98`

**Solução:**
```bash
# Encontrar processo usando porta 5000
lsof -ti:5000

# Matar processo
kill -9 $(lsof -ti:5000)

# Ou usar porta diferente
export FLASK_PORT=5001
./start.sh
```

### Problema: Banco de dados corrompido

**Sintomas:** Erro ao acessar dados ou aplicação trava

**Solução:**
```bash
# Fazer backup
cp data/estudos.db data/estudos.db.corrupt

# Restaurar de backup anterior
python3 restore_db.py

# Ou limpar completamente
./resetar_banco.sh
./restart.sh
```

### Problema: Moodle não sincroniza

**Sintomas:** Nenhum dado do Moodle aparece

**Solução:**
```bash
# Verificar credenciais
echo $MOODLE_USERNAME
echo $MOODLE_PASSWORD

# Testar sincronização manualmente
python3 backend/moodle_sync.py

# Ver logs
tail -f backend.log

# Se ainda não funcionar, fazer login novamente
# Limpar dados do Moodle
rm -rf data/moodle/*

# Reiniciar
./restart.sh
```

### Problema: Timer não funciona

**Sintomas:** Timer não inicia ou não conta

**Solução:**
```bash
# Verificar se JavaScript está habilitado no navegador
# Abrir console (F12) e verificar erros

# Limpar cache do navegador
# Ctrl+Shift+Delete (Chrome/Firefox)

# Recarregar página
# Ctrl+F5 (força recarregamento)

# Se persistir, reiniciar servidor
./restart.sh
```

### Problema: Sincronização de pastas não funciona

**Sintomas:** Arquivos não são sincronizados

**Solução:**
```bash
# Verificar configuração
cat .env | grep SYNC

# Testar sincronização manualmente
python3 backend/folder_sync.py

# Ver logs
tail -f backend.log

# Verificar permissões das pastas
ls -la /caminho/pasta/

# Se necessário, dar permissões
chmod -R 755 /caminho/pasta/
```

---

## 📚 Documentação Adicional

- **[Funcionalidades Completas](FUNCIONALIDADES_MOODLE_IA.md)** - Guia detalhado de todas as funcionalidades
- **[Configuração Avançada](.env.example)** - Todas as opções de configuração
- **[API Reference](API_EXAMPLES.md)** - Documentação da API REST
- **[Logs e Debugging](backend.log)** - Arquivo de log da aplicação

---

## 🔒 Segurança e Privacidade

### Proteção de Dados
- ✅ **Credenciais Moodle** - não são armazenadas em disco (apenas sessão temporária)
- ✅ **API Keys** - devem ser configuradas via variáveis de ambiente
- ✅ **Dados locais** - armazenados apenas no seu computador
- ✅ **Sem rastreamento** - nenhum dado enviado para servidores externos (exceto APIs configuradas)
- ✅ **Sessões seguras** - expiram automaticamente após 24 horas
- ✅ **Banco de dados** - SQLite local, sem sincronização em nuvem

### Boas Práticas
- 🔐 Nunca compartilhe suas credenciais Moodle
- 🔐 Guarde sua API Key em local seguro
- 🔐 Use `.env` para configurações sensíveis
- 🔐 Faça backups regulares do banco de dados
- 🔐 Use em computador pessoal quando possível

---

## 🎯 Roadmap e Funcionalidades Futuras

### ✅ Implementado (v2.0)
- [x] Dashboard completo com estatísticas
- [x] Timer Pomodoro com registro automático
- [x] Integração Moodle UAB
- [x] Assistente IA (OpenAI/OpenRouter)
- [x] Sincronização de pastas
- [x] Gestão de tarefas e e-fólios
- [x] Calendário semanal
- [x] Histórico de sessões

### 🔄 Em Desenvolvimento
- [ ] Sincronização automática do Moodle (agendada)
- [ ] Notificações push no desktop
- [ ] Exportação de flashcards (Anki, Quizlet)
- [ ] Integração Google Calendar
- [ ] Modo offline completo
- [ ] Relatórios PDF de progresso

### 🚀 Futuro (v3.0+)
- [ ] App mobile (Android/iOS)
- [ ] Modelo IA local (Ollama)
- [ ] Reconhecimento de voz
- [ ] Correção automática de exercícios
- [ ] Grupos de estudo colaborativos
- [ ] Gamificação com achievements
- [ ] Integração com outras plataformas
- [ ] Análise preditiva de desempenho

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. **Fork o repositório**
   ```bash
   git clone https://github.com/seu-usuario/study-planner.git
   ```

2. **Crie uma branch para sua feature**
   ```bash
   git checkout -b feature/MinhaFeature
   ```

3. **Faça suas mudanças e commit**
   ```bash
   git commit -m 'Adiciona MinhaFeature'
   ```

4. **Push para a branch**
   ```bash
   git push origin feature/MinhaFeature
   ```

5. **Abra um Pull Request**
   - Descreva suas mudanças
   - Explique por que são necessárias
   - Inclua testes se aplicável

### Diretrizes de Contribuição
- Siga o estilo de código existente
- Adicione testes para novas funcionalidades
- Atualize a documentação
- Teste em Linux (Ubuntu/Debian)
- Verifique compatibilidade com Python 3.8+

---

## 📄 Licença

Este projeto é desenvolvido para uso acadêmico na UAB LEI.

**Licença:** MIT (ou conforme especificado no arquivo LICENSE)

---

## 🙏 Agradecimentos

- **UAB Portugal** - Universidade Aberta de Portugal
- **OpenAI** - API de IA e modelos GPT
- **OpenRouter** - Alternativa de IA
- **Comunidade Python** - Bibliotecas e ferramentas
- **Estudantes UAB LEI** - Feedback, sugestões e testes
- **Comunidade Open Source** - Inspiração e suporte

---

## 📞 Suporte e Contato

### Reportar Problemas
- **Issues:** Abra uma issue no GitHub com detalhes do problema
- **Logs:** Inclua saída de `tail -f backend.log`
- **Ambiente:** Especifique SO, versão Python, navegador

### Solicitar Funcionalidades
- Abra uma issue com tag `enhancement`
- Descreva o caso de uso
- Explique como isso ajudaria seus estudos

### Documentação
- Consulte os arquivos `.md` no projeto
- Verifique a seção de Troubleshooting
- Veja exemplos em `API_EXAMPLES.md`

---

## 📊 Status do Projeto

![Status](https://img.shields.io/badge/status-active-success.svg)
![Maintenance](https://img.shields.io/badge/maintained-yes-green.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux-orange.svg)

### Informações do Projeto
- **Última atualização:** Outubro 2025
- **Versão Atual:** 2.0.0
- **Python Mínimo:** 3.8+
- **Plataforma:** Linux (Ubuntu/Debian)
- **Tamanho:** ~500MB (com dependências)
- **Banco de Dados:** SQLite
- **Backend:** Flask 3.1.0
- **Frontend:** HTML5 + JavaScript + CSS3

### Estatísticas
- **Backend:** 1400+ linhas (app.py)
- **Moodle Integration:** 785+ linhas
- **Frontend:** 1761+ linhas (HTML) + 2687+ linhas (JS)
- **Dependências:** 18 pacotes Python
- **Funcionalidades:** 40+ recursos

---

## 🌟 Destaques do Projeto

```
┌─────────────────────────────────────────────────────────┐
│  📊 Dashboard Completo      🎯 Metas e Progresso       │
│  ⏱️  Timer Pomodoro         📅 Calendário Inteligente   │
│  🏫 Integração Moodle       📚 Sync Automático          │
│  🤖 Assistente IA           💡 Resumos e Flashcards    │
│  📝 Gestão de Tarefas       📈 Estatísticas Detalhadas │
│  📁 Sincronização Pastas    🔔 Notificações em Tempo   │
└─────────────────────────────────────────────────────────┘
```

---

## 💡 Dicas para Melhor Aproveitamento

1. **Use o Timer Pomodoro** - Melhora foco e produtividade
2. **Sincronize o Moodle** - Nunca perca prazos importantes
3. **Configure a IA** - Tire dúvidas instantaneamente
4. **Revise estatísticas** - Acompanhe seu progresso
5. **Faça backups** - Proteja seus dados
6. **Customize disciplinas** - Adapte ao seu currículo
7. **Use flashcards** - Revise conceitos importantes
8. **Planeje com antecedência** - Use planos de estudo IA

---

**Desenvolvido com ❤️ para estudantes da UAB LEI**

**Bons estudos! 🎓✨**

---

*Para mais informações, visite: https://moodle.uab.pt*