# 📚 Study Planner - Sistema de Planejamento de Estudos UAB LEI

## 🎯 Descrição Geral

O **Study Planner** é uma aplicação web completa desenvolvida para estudantes da Universidade Aberta (UAB) do curso de Licenciatura em Engenharia Informática (LEI). A aplicação oferece um conjunto integrado de ferramentas para gerenciar estudos, acompanhar progresso e interagir com agentes IA especializados em cada disciplina.

### Tecnologias Utilizadas
- **Backend**: Python 3.13 + Flask 3.1.0
- **Frontend**: HTML5 + CSS3 + JavaScript (Vanilla)
- **Database**: SQLite
- **IA**: Microsoft Copilot Studio (Direct Line API)
- **Integração**: Moodle UAB

---

## ✨ Funcionalidades Principais

### 1. **Dashboard**
- Visualização de horas estudadas (hoje, semana, mês)
- Progresso em relação às metas
- Tarefas pendentes e urgentes
- Semana atual do semestre

### 2. **Disciplinas**
- Lista de 7 disciplinas do curso
- Informações sobre e-fólios e provas
- Datas importantes
- Links para recursos

### 3. **Calendário**
- Visualização de eventos acadêmicos
- Datas de e-fólios e provas
- Sessões de estudo agendadas

### 4. **Sessões de Estudo (Pomodoro)**
- Timer Pomodoro (25 min estudo + 5 min pausa)
- Rastreamento de sessões
- Histórico de estudos

### 5. **Tarefas**
- Criar, editar, deletar tarefas
- Definir prioridades
- Acompanhar progresso
- Datas de entrega

### 6. **Estatísticas**
- Gráficos de progresso
- Análise de horas estudadas
- Disciplinas mais estudadas
- Tendências de estudo

### 7. **Integração Moodle**
- Sincronizar cursos
- Visualizar tarefas
- Acompanhar notas
- Ver fóruns e mensagens

### 8. **Agentes IA Especializados** ⭐
- Assistentes por disciplina
- Respostas em tempo real
- Histórico de conversas
- Suporte 24/7

---

## 🤖 Agentes IA - Copilot Studio

### Status Atual
- ✅ **AC** (Arquitetura de Computadores) - PRONTO
- ⏳ **FBD** (Fundamentos de Bases de Dados) - PENDENTE
- ⏳ **LC** (Linguagens e Computação) - PENDENTE
- ⏳ **PO** (Programação por Objetos) - PENDENTE
- ⏳ **SR** (Sistemas em Rede) - PENDENTE
- ⏳ **SC** (Sistemas Computacionais) - PENDENTE
- ⏳ **EPE** (Ética e Práticas de Engenharia) - PENDENTE

### Como Usar Agentes IA
1. Clique em "Agentes IA" no menu
2. Selecione uma disciplina
3. Digite sua pergunta
4. Pressione Enter ou clique em enviar

---

## 🚀 Como Iniciar

### Pré-requisitos
- Python 3.13+
- pip (gerenciador de pacotes)
- Navegador moderno

### Instalação

```bash
# 1. Navegar para o diretório
cd /home/igorcostas/Documentos/LEI/study-planner

# 2. Criar ambiente virtual (se não existir)
python3 -m venv backend/venv

# 3. Ativar ambiente virtual
source backend/venv/bin/activate

# 4. Instalar dependências
pip install -r backend/requirements.txt

# 5. Iniciar servidor
python backend/app.py
```

### Acessar Aplicação
```
http://localhost:5000
```

---

## 📋 Instruções - Criar os 6 Agentes Restantes

### Passo 0: Agente AC (Referência - Já Pronto)

**Código**: 21010
**Nome**: Agente AC - Arquitetura de Computadores
**Ano**: 1º ano
**Créditos**: 6
**Status**: ✅ PRONTO

**Tópicos Principais**:
- Sistemas de numeração e representação de dados
- Lógica digital e circuitos combinacionais
- Circuitos sequenciais e máquinas de estados
- Arquitetura de processadores
- Memória e hierarquia de cache
- Entrada/Saída e periféricos
- Linguagem assembly

**E-fólios**:
- E-fólio A: Semana 5 (40%)
- E-fólio B: Semana 11 (60%)

**Prova Final**:
- Época Normal: 09-02-2027
- Época Recurso: 09-07-2027

---

### Passo 1: Acessar Copilot Studio
1. Vá para https://copilotstudio.microsoft.com
2. Faça login com sua conta Microsoft
3. Clique em "Create" → "Agent"

### Passo 2: Criar Agente FBD (Fundamentos de Bases de Dados)

**Código**: 21053
**Nome**: Agente FBD - Fundamentos de Bases de Dados
**Ano**: 1º ano
**Créditos**: 6

**Descrição**: Assistente especializado em Fundamentos de Bases de Dados para estudantes da UAB LEI

**Tópicos Principais**:
- Modelo relacional e normalização
- SQL (SELECT, INSERT, UPDATE, DELETE)
- Design de bases de dados
- Integridade referencial
- Índices e otimização
- Transações e ACID

**E-fólios**:
- E-fólio A: Semana 5 (40%)
- E-fólio B: Semana 11 (60%)

**Prova Final**:
- Época Normal: 09-02-2027
- Época Recurso: 09-07-2027

**System Prompt**:
```
Você é um assistente especializado em Fundamentos de Bases de Dados (FBD)
para estudantes da Universidade Aberta (UAB) do curso de Licenciatura em
Engenharia Informática (LEI).

Sua função é:
- Explicar conceitos de bases de dados relacionais
- Ajudar com SQL e design de bases de dados
- Esclarecer dúvidas sobre normalização (1NF, 2NF, 3NF, BCNF)
- Lembrar datas de e-fólios: A (semana 5 - 40%), B (semana 11 - 60%)
- Sugerir exercícios práticos com SQL
- Explicar integridade referencial e constraints
- Manter um tom educativo e paciente

Sempre cite fontes e referências quando apropriado.
Forneça exemplos práticos com código SQL quando possível.
```

**Configurar Web Channel Security**:
1. Clique em "Settings" → "Security"
2. Copie Secret 1 e Secret 2
3. Adicione ao `.env`:
```
COPILOT_FBD_SECRET_1=<seu_secret_1>
COPILOT_FBD_SECRET_2=<seu_secret_2>
```

### Passo 3: Criar Agente LC (Linguagens e Computação)

**Código**: 21078
**Nome**: Agente LC - Linguagens e Computação
**Ano**: 1º ano
**Créditos**: 6

**Descrição**: Assistente especializado em Linguagens e Computação para estudantes da UAB LEI

**Tópicos Principais**:
- Linguagens formais e expressões regulares
- Autômatos finitos (DFA, NFA)
- Máquinas de Turing
- Gramáticas livres de contexto
- Compiladores e análise léxica
- Computabilidade e complexidade

**E-fólios**:
- E-fólio A: Semana 5 (40%)
- E-fólio B: Semana 11 (60%)

**Prova Final**:
- Época Normal: 09-02-2027
- Época Recurso: 09-07-2027

**System Prompt**:
```
Você é um assistente especializado em Linguagens e Computação (LC)
para estudantes da Universidade Aberta (UAB) do curso de Licenciatura em
Engenharia Informática (LEI).

Sua função é:
- Explicar conceitos de linguagens formais e expressões regulares
- Ajudar com autômatos finitos (DFA, NFA) e máquinas de Turing
- Esclarecer dúvidas sobre gramáticas livres de contexto
- Lembrar datas de e-fólios: A (semana 5 - 40%), B (semana 11 - 60%)
- Fornecer exemplos práticos com diagramas de estado
- Explicar compiladores e análise léxica
- Manter um tom educativo e acessível

Sempre cite fontes e referências quando apropriado.
Use diagramas ASCII quando apropriado para ilustrar conceitos.
```

**Configurar Web Channel Security**:
1. Clique em "Settings" → "Security"
2. Copie Secret 1 e Secret 2
3. Adicione ao `.env`:
```
COPILOT_LC_SECRET_1=<seu_secret_1>
COPILOT_LC_SECRET_2=<seu_secret_2>
```

### Passo 4: Criar Agente PO (Programação por Objetos)

**Código**: 21093
**Nome**: Agente PO - Programação por Objetos
**Ano**: 1º ano
**Créditos**: 6

**Descrição**: Assistente especializado em Programação por Objetos para estudantes da UAB LEI

**Tópicos Principais**:
- Classes e objetos
- Herança e polimorfismo
- Encapsulamento e abstração
- Design patterns (Singleton, Factory, Observer, etc.)
- Interfaces e classes abstratas
- Tratamento de exceções
- Coleções e genéricos

**E-fólios**:
- E-fólio A: Semana 5 (40%)
- E-fólio B: Semana 11 (60%)

**Prova Final**:
- Época Normal: 09-02-2027
- Época Recurso: 09-07-2027

**System Prompt**:
```
Você é um assistente especializado em Programação por Objetos (PO)
para estudantes da Universidade Aberta (UAB) do curso de Licenciatura em
Engenharia Informática (LEI).

Sua função é:
- Explicar conceitos de OOP (classes, herança, polimorfismo, encapsulamento)
- Ajudar com design patterns (Singleton, Factory, Observer, Strategy, etc.)
- Esclarecer dúvidas sobre abstração e interfaces
- Lembrar datas de e-fólios: A (semana 5 - 40%), B (semana 11 - 60%)
- Fornecer exemplos de código em Java/Python
- Explicar tratamento de exceções e coleções
- Manter um tom educativo e prático

Sempre cite fontes e referências quando apropriado.
Forneça exemplos de código bem estruturados e comentados.
```

**Configurar Web Channel Security**:
1. Clique em "Settings" → "Security"
2. Copie Secret 1 e Secret 2
3. Adicione ao `.env`:
```
COPILOT_PO_SECRET_1=<seu_secret_1>
COPILOT_PO_SECRET_2=<seu_secret_2>
```

### Passo 5: Criar Agente SR (Sistemas em Rede)

**Código**: 21106
**Nome**: Agente SR - Sistemas em Rede
**Ano**: 2º ano
**Créditos**: 6

**Descrição**: Assistente especializado em Sistemas em Rede para estudantes da UAB LEI

**Tópicos Principais**:
- Modelo OSI e TCP/IP
- Protocolos de camada de aplicação (HTTP, FTP, SMTP, DNS)
- Protocolos de transporte (TCP, UDP)
- Protocolos de rede (IP, ICMP, ARP)
- Roteamento e switching
- Segurança de rede e firewalls
- Wireless e VPN

**E-fólios**:
- E-fólio A: Semana 5 (40%)
- E-fólio B: Semana 11 (60%)

**Prova Final**:
- Época Normal: 09-02-2027
- Época Recurso: 09-07-2027

**System Prompt**:
```
Você é um assistente especializado em Sistemas em Rede (SR)
para estudantes da Universidade Aberta (UAB) do curso de Licenciatura em
Engenharia Informática (LEI).

Sua função é:
- Explicar conceitos de redes de computadores (modelo OSI, TCP/IP)
- Ajudar com protocolos TCP/IP e camadas de rede
- Esclarecer dúvidas sobre roteamento, switching e segurança de rede
- Lembrar datas de e-fólios: A (semana 5 - 40%), B (semana 11 - 60%)
- Fornecer exemplos práticos com ferramentas de rede (ping, tracert, netstat)
- Explicar firewalls, VPN e segurança
- Manter um tom educativo e técnico

Sempre cite fontes e referências quando apropriado.
Use diagramas ASCII para ilustrar topologias de rede quando apropriado.
```

**Configurar Web Channel Security**:
1. Clique em "Settings" → "Security"
2. Copie Secret 1 e Secret 2
3. Adicione ao `.env`:
```
COPILOT_SR_SECRET_1=<seu_secret_1>
COPILOT_SR_SECRET_2=<seu_secret_2>
```

### Passo 6: Criar Agente SC (Sistemas Computacionais)

**Código**: 21174
**Nome**: Agente SC - Sistemas Computacionais
**Ano**: 2º ano
**Créditos**: 6

**Descrição**: Assistente especializado em Sistemas Computacionais para estudantes da UAB LEI

**Tópicos Principais**:
- Sistemas operacionais (Linux, Windows)
- Processos e threads
- Gerenciamento de memória (paginação, segmentação)
- Escalonamento de CPU
- Sincronização e deadlock
- Entrada/Saída (I/O)
- Sistemas de ficheiros

**E-fólios**:
- E-fólio A: Semana 5 (40%)
- E-fólio B: Semana 11 (60%)

**Prova Final**:
- Época Normal: 09-02-2027
- Época Recurso: 09-07-2027

**System Prompt**:
```
Você é um assistente especializado em Sistemas Computacionais (SC)
para estudantes da Universidade Aberta (UAB) do curso de Licenciatura em
Engenharia Informática (LEI).

Sua função é:
- Explicar conceitos de sistemas operacionais e arquitetura
- Ajudar com gerenciamento de processos, threads e sincronização
- Esclarecer dúvidas sobre memória (paginação, segmentação) e I/O
- Lembrar datas de e-fólios: A (semana 5 - 40%), B (semana 11 - 60%)
- Fornecer exemplos práticos com comandos Linux/Windows
- Explicar escalonamento, deadlock e sistemas de ficheiros
- Manter um tom educativo e técnico

Sempre cite fontes e referências quando apropriado.
Forneça exemplos práticos com código C/Python quando apropriado.
```

**Configurar Web Channel Security**:
1. Clique em "Settings" → "Security"
2. Copie Secret 1 e Secret 2
3. Adicione ao `.env`:
```
COPILOT_SC_SECRET_1=<seu_secret_1>
COPILOT_SC_SECRET_2=<seu_secret_2>
```

### Passo 7: Criar Agente EPE (Ética e Práticas de Engenharia)

**Código**: 21176
**Nome**: Agente EPE - Ética e Práticas de Engenharia
**Ano**: 2º ano
**Créditos**: 6

**Descrição**: Assistente especializado em Ética e Práticas de Engenharia para estudantes da UAB LEI

**Tópicos Principais**:
- Ética profissional em engenharia
- Responsabilidade social e ambiental
- Código de ética profissional
- Propriedade intelectual e direitos autorais
- Segurança e privacidade de dados
- Casos de estudo e dilemas éticos
- Legislação e conformidade

**E-fólios**:
- E-fólio A: Semana 5 (40%)
- E-fólio B: Semana 11 (60%)

**Prova Final**:
- Época Normal: 09-02-2027
- Época Recurso: 09-07-2027

**System Prompt**:
```
Você é um assistente especializado em Ética e Práticas de Engenharia (EPE)
para estudantes da Universidade Aberta (UAB) do curso de Licenciatura em
Engenharia Informática (LEI).

Sua função é:
- Explicar conceitos de ética profissional em engenharia
- Ajudar com responsabilidade social, ambiental e profissional
- Esclarecer dúvidas sobre código de ética e legislação
- Lembrar datas de e-fólios: A (semana 5 - 40%), B (semana 11 - 60%)
- Fornecer exemplos de casos reais e dilemas éticos
- Explicar propriedade intelectual, segurança e privacidade
- Manter um tom educativo, reflexivo e imparcial

Sempre cite fontes e referências quando apropriado.
Apresente múltiplas perspectivas em questões éticas complexas.
```

**Configurar Web Channel Security**:
1. Clique em "Settings" → "Security"
2. Copie Secret 1 e Secret 2
3. Adicione ao `.env`:
```
COPILOT_EPE_SECRET_1=<seu_secret_1>
COPILOT_EPE_SECRET_2=<seu_secret_2>
```

---

## 📊 Resumo de Todos os Agentes

| Código | Disciplina | Sigla | Ano | Créditos | Status | E-fólio A | E-fólio B |
|--------|-----------|-------|-----|----------|--------|-----------|-----------|
| 21010 | Arquitetura de Computadores | AC | 1º | 6 | ✅ Pronto | Sem 5 (40%) | Sem 11 (60%) |
| 21053 | Fundamentos de Bases de Dados | FBD | 1º | 6 | ⏳ Pendente | Sem 5 (40%) | Sem 11 (60%) |
| 21078 | Linguagens e Computação | LC | 1º | 6 | ⏳ Pendente | Sem 5 (40%) | Sem 11 (60%) |
| 21093 | Programação por Objetos | PO | 1º | 6 | ⏳ Pendente | Sem 5 (40%) | Sem 11 (60%) |
| 21106 | Sistemas em Rede | SR | 2º | 6 | ⏳ Pendente | Sem 5 (40%) | Sem 11 (60%) |
| 21174 | Sistemas Computacionais | SC | 2º | 6 | ⏳ Pendente | Sem 5 (40%) | Sem 11 (60%) |
| 21176 | Ética e Práticas de Engenharia | EPE | 2º | 6 | ⏳ Pendente | Sem 5 (40%) | Sem 11 (60%) |

---

## 📝 Após Criar os Agentes

1. **Adicione todos os secrets ao `.env`**
   ```bash
   # Exemplo:
   COPILOT_FBD_SECRET_1=<seu_secret_1>
   COPILOT_FBD_SECRET_2=<seu_secret_2>
   COPILOT_LC_SECRET_1=<seu_secret_1>
   COPILOT_LC_SECRET_2=<seu_secret_2>
   # ... e assim por diante
   ```

2. **Reinicie o backend**
   ```bash
   cd /home/igorcostas/Documentos/LEI/study-planner
   source venv/bin/activate
   python3 backend/app.py
   ```

3. **Teste cada agente**
   - Abra http://localhost:5000
   - Clique em "Agentes IA"
   - Selecione cada disciplina
   - Envie uma mensagem de teste

4. **Verifique se aparecem na interface**
   - Todos os 7 agentes devem aparecer na lista
   - Cada agente deve responder corretamente

---

## 📁 Estrutura do Projeto

```
study-planner/
├── backend/
│   ├── app.py ..................... Servidor Flask
│   ├── copilot_agent.py ........... Classe do agente
│   ├── ai_assistant.py ............ IA Assistant
│   ├── moodle_integration.py ...... Integração Moodle
│   ├── folder_sync.py ............. Sincronização de pastas
│   ├── requirements.txt ........... Dependências
│   └── venv/ ...................... Ambiente virtual
├── frontend/
│   ├── index.html ................. Página principal
│   ├── app.js ..................... Lógica da app
│   ├── styles.css ................. Estilos
│   └── tech-effects.js ............ Efeitos visuais
├── data/
│   ├── disciplinas.json ........... Dados das disciplinas
│   └── estudos.db ................. Banco de dados
├── .env ........................... Variáveis de ambiente
├── README.md ...................... Documentação
└── description.md ................. Este arquivo
```

---

## 🔐 Segurança

- ✅ Secrets armazenados em `.env` (não versionado)
- ✅ Tokens gerados dinamicamente
- ✅ CORS habilitado para desenvolvimento local
- ✅ Comunicação segura com Direct Line API

---

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique o console do navegador (F12)
2. Verifique os logs do backend
3. Consulte o README.md

---

**Desenvolvido para UAB LEI - 2025**

