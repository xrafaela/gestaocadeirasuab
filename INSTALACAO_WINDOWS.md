# 🪟 Instalação no Windows - Study Planner UAB LEI

Guia completo para instalar e executar o Sistema de Planejamento de Estudos no Windows.

---

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Instalação do Python](#instalação-do-python)
3. [Instalação do Git](#instalação-do-git)
4. [Download do Projeto](#download-do-projeto)
5. [Configuração do Ambiente](#configuração-do-ambiente)
6. [Executar o Sistema](#executar-o-sistema)
7. [Solução de Problemas](#solução-de-problemas)

---

## 📦 Pré-requisitos

- **Windows 10 ou superior**
- **Conexão com a internet**
- **Pelo menos 500 MB de espaço livre**

---

## 🐍 Instalação do Python

### Passo 1: Download do Python

1. Acesse: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Clique em **"Download Python 3.12.x"** (versão mais recente)
3. Aguarde o download do instalador

### Passo 2: Instalar Python

1. Execute o arquivo baixado (`python-3.12.x-amd64.exe`)
2. ⚠️ **IMPORTANTE**: Marque a opção **"Add Python to PATH"**
3. Clique em **"Install Now"**
4. Aguarde a instalação concluir
5. Clique em **"Close"**

### Passo 3: Verificar Instalação

1. Abra o **Prompt de Comando** (CMD):
   - Pressione `Win + R`
   - Digite `cmd` e pressione Enter

2. Digite o comando:
   ```cmd
   python --version
   ```

3. Deve aparecer algo como:
   ```
   Python 3.12.x
   ```

✅ Se aparecer a versão, o Python está instalado corretamente!

---

## 🔧 Instalação do Git

### Passo 1: Download do Git

1. Acesse: [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. O download deve iniciar automaticamente
3. Aguarde o download do instalador

### Passo 2: Instalar Git

1. Execute o arquivo baixado (`Git-2.x.x-64-bit.exe`)
2. Clique em **"Next"** em todas as telas (configurações padrão)
3. Aguarde a instalação concluir
4. Clique em **"Finish"**

### Passo 3: Verificar Instalação

1. Abra um novo **Prompt de Comando** (CMD)
2. Digite o comando:
   ```cmd
   git --version
   ```

3. Deve aparecer algo como:
   ```
   git version 2.x.x
   ```

✅ Se aparecer a versão, o Git está instalado corretamente!

---

## 📥 Download do Projeto

### Opção 1: Clonar com Git (Recomendado)

1. Abra o **Prompt de Comando** (CMD)

2. Navegue até a pasta onde deseja instalar:
   ```cmd
   cd C:\Users\SeuUsuario\Documents
   ```

3. Clone o repositório:
   ```cmd
   git clone https://github.com/seu-usuario/study-planner.git
   ```

4. Entre na pasta do projeto:
   ```cmd
   cd study-planner
   ```

### Opção 2: Download ZIP

1. Acesse: [https://github.com/seu-usuario/study-planner](https://github.com/seu-usuario/study-planner)
2. Clique no botão verde **"Code"**
3. Clique em **"Download ZIP"**
4. Extraia o arquivo ZIP em uma pasta de sua preferência
5. Abra o **Prompt de Comando** e navegue até a pasta:
   ```cmd
   cd C:\Users\SeuUsuario\Documents\study-planner
   ```

---

## ⚙️ Configuração do Ambiente

### Passo 1: Criar Ambiente Virtual

No Prompt de Comando, dentro da pasta do projeto:

```cmd
python -m venv backend\venv
```

### Passo 2: Ativar Ambiente Virtual

```cmd
backend\venv\Scripts\activate
```

Você verá `(venv)` no início da linha do prompt.

### Passo 3: Instalar Dependências

```cmd
pip install --upgrade pip
pip install Flask==3.0.0 Flask-CORS==4.0.0 Werkzeug==3.0.1 pytz==2024.1
pip install requests==2.32.3 beautifulsoup4==4.12.3 selenium==4.16.0 webdriver-manager==4.0.2
pip install PyPDF2==3.0.1 pdfplumber==0.10.3
pip install python-dotenv==1.0.1 schedule==1.2.1 pillow==10.4.0 sqlalchemy==2.0.35 APScheduler==3.10.4
```

Aguarde a instalação de todas as dependências (pode levar alguns minutos).

---

## 🚀 Executar o Sistema

### Método 1: Script Automático (Recomendado)

1. Execute o script de inicialização:
   ```cmd
   start-windows.bat
   ```

2. O navegador abrirá automaticamente em `http://localhost:5000`

### Método 2: Manual

1. Ative o ambiente virtual (se ainda não estiver ativo):
   ```cmd
   backend\venv\Scripts\activate
   ```

2. Entre na pasta backend:
   ```cmd
   cd backend
   ```

3. Execute o servidor:
   ```cmd
   python app.py
   ```

4. Abra o navegador e acesse:
   ```
   http://localhost:5000
   ```

---

## 🛑 Parar o Sistema

### Se usou o script automático:
- Pressione `Ctrl + C` no Prompt de Comando
- Digite `S` e pressione Enter

### Se executou manualmente:
- Pressione `Ctrl + C` no Prompt de Comando

---

## 🔧 Solução de Problemas

### ❌ Erro: "python não é reconhecido como comando"

**Solução:**
1. Reinstale o Python
2. Marque a opção **"Add Python to PATH"**
3. Reinicie o computador

### ❌ Erro: "pip não é reconhecido como comando"

**Solução:**
```cmd
python -m pip install --upgrade pip
```

### ❌ Erro: "Porta 5000 já está em uso"

**Solução:**
1. Abra o **Gerenciador de Tarefas** (Ctrl + Shift + Esc)
2. Procure por processos Python
3. Finalize o processo
4. Tente executar novamente

Ou use este comando:
```cmd
netstat -ano | findstr :5000
taskkill /PID <numero_do_pid> /F
```

### ❌ Erro: "ModuleNotFoundError: No module named 'flask'"

**Solução:**
1. Certifique-se de que o ambiente virtual está ativado
2. Reinstale as dependências:
   ```cmd
   pip install -r requirements.txt
   ```

### ❌ O navegador não abre automaticamente

**Solução:**
- Abra manualmente o navegador
- Acesse: `http://localhost:5000`

### ❌ Página não carrega / Erro 404

**Solução:**
1. Verifique se o servidor está rodando
2. Verifique se está acessando `http://localhost:5000` (não `https`)
3. Limpe o cache do navegador (Ctrl + Shift + Delete)

---

## 📱 Acessar de Outros Dispositivos

Para acessar o sistema de outros dispositivos na mesma rede:

1. Descubra seu IP local:
   ```cmd
   ipconfig
   ```
   Procure por "Endereço IPv4" (ex: 192.168.1.100)

2. No outro dispositivo, acesse:
   ```
   http://192.168.1.100:5000
   ```

---

## 🔄 Atualizar o Sistema

Se você clonou com Git:

```cmd
git pull origin master
pip install --upgrade -r requirements.txt
```

---

## 📞 Suporte

Se encontrar problemas:

1. Verifique a seção [Solução de Problemas](#solução-de-problemas)
2. Consulte o arquivo `README.md`
3. Abra uma issue no GitHub

---

## 🎓 Próximos Passos

Após a instalação:

1. ✅ Configure seu perfil de estudos
2. ✅ Adicione suas disciplinas
3. ✅ Configure seu horário de estudos
4. ✅ Comece a usar o Pomodoro Timer
5. ✅ Acompanhe seu progresso

---

## 📚 Recursos Adicionais

- [Tutorial Completo de Uso](TUTORIAL_COMPLETO.md)
- [Como Sincronizar Pastas](TUTORIAL_SINCRONIZACAO_PASTAS.md)
- [README Principal](README.md)

---

**Desenvolvido para estudantes da UAB - Licenciatura em Engenharia Informática** 🎓

