# 📚 Tutorial Completo - Study Planner UAB LEI

## Índice
1. [Primeiros Passos](#primeiros-passos)
2. [Dashboard](#dashboard)
3. [Calendário](#calendário)
4. [Disciplinas](#disciplinas)
5. [Timer Pomodoro](#timer-pomodoro)
6. [Tarefas](#tarefas)
7. [Moodle](#moodle)
8. [Agentes IA](#agentes-ia)
9. [Estatísticas](#estatísticas)

---

## Primeiros Passos

### Instalação e Inicialização

**Linux/Mac:**
```bash
cd Documentos/LEI/study-planner
./start.sh
```

**Windows:**
```bash
cd study-planner
.\venv\Scripts\Activate.ps1
python backend/app.py
```

A aplicação abrirá em `http://localhost:5000`

### Setup Inicial

Na primeira vez que acessar, você verá um **Setup Wizard** com 4 passos:

1. **Informações Básicas** - Nome, Curso, Ano
2. **Selecionar Disciplinas** - Escolha as disciplinas a monitorar
3. **Disponibilidade** - Horas/dia e dias de estudo
4. **Calendário** - Preview do seu calendário de estudos

---

## Dashboard

O Dashboard é sua página inicial com visão geral dos estudos.

### Estatísticas Principais

- **Horas Estudadas Hoje** - Progresso diário com meta
- **Horas Estudadas esta Semana** - Progresso semanal
- **Semana Atual** - Número da semana letiva
- **Tarefas Pendentes** - Quantidade de tarefas não concluídas

### Próximos e-Fólios

Lista dos e-fólios com prazos próximos. Clique para ver detalhes.

### Progresso por Disciplina

Gráfico de barras mostrando horas estudadas em cada disciplina.

---

## Calendário

Visualize seu horário semanal de estudos.

### Plano de Trabalho

Mostra as atividades recomendadas para cada semana de cada disciplina.

### Horário Semanal

Grade com distribuição de horas por disciplina:
- **Segunda a Sexta** - Horários de estudo
- **Cores** - Cada cor representa uma disciplina
- **Clique** - Para ver detalhes da atividade

### Navegação

Use os botões ◀ ▶ para navegar entre semanas.

---

## Disciplinas

Gerencie suas disciplinas e acompanhe o progresso.

### Visualizar Disciplinas

As disciplinas são agrupadas por ano:
- **1º Ano** - Disciplinas do primeiro ano
- **2º Ano** - Disciplinas do segundo ano

### Informações da Disciplina

Clique em uma disciplina para ver:
- **Tópicos** - Conteúdos a estudar
- **e-Fólios** - Avaliações contínuas
- **Sessões Síncronas** - Aulas ao vivo
- **Materiais** - PDFs e recursos
- **Histórico de Sessões** - Pomodoros realizados

### Ações

- **Sincronizar Materiais** - Baixar recursos do Moodle
- **Ver Histórico** - Sessões de estudo realizadas
- **Editar** - Modificar informações da disciplina

---

## Timer Pomodoro

Técnica de gestão de tempo: 25min estudo + 5min pausa.

### Como Usar

1. Selecione a disciplina
2. Digite o tópico/atividade (opcional)
3. Clique em **Iniciar**
4. Estude por 25 minutos
5. Faça pausa de 5 minutos
6. Após 4 pomodoros, pausa de 15-30 minutos

### Funcionalidades

- **Iniciar/Pausar** - Controlar o timer
- **Reiniciar** - Resetar para 25 minutos
- **Popup** - Abrir timer em janela flutuante
- **Notificações** - Alertas sonoros ao terminar

### Estatísticas

- **Pomodoros Hoje** - Quantidade realizada
- **Sequência** - Dias consecutivos estudando

---

## Tarefas

Gerencie e-fólios, trabalhos e atividades.

### Criar Tarefa

1. Clique em **+ Nova Tarefa**
2. Preencha os campos:
   - Disciplina
   - Título
   - Descrição
   - Tipo (Geral, e-Fólio, Sessão Síncrona, Projeto, Fórum)
   - Data de Entrega
   - Prioridade (Baixa, Média, Alta)
3. Clique em **Salvar**

### Filtrar Tarefas

- **Todas** - Todas as tarefas
- **Pendentes** - Não concluídas
- **Concluídas** - Finalizadas
- **e-Fólios** - Avaliações contínuas
- **Sessões Síncronas** - Aulas ao vivo
- **Atividades Formativas** - Fóruns

### Marcar Concluída

Clique no checkbox para marcar tarefa como concluída.

---

## Moodle

Integração com a plataforma Moodle UAB.

### Acessar Moodle

Clique em **Abrir Moodle UAB** para acessar a plataforma.

### Links Rápidos

- **Painel Principal** - Visão geral das disciplinas
- **Calendário** - Eventos e prazos
- **Mensagens** - Comunicação com tutores
- **Notas** - Consultar avaliações

### Disciplinas

Acesso rápido às disciplinas com botão **Abrir no Moodle**.

---

## Agentes IA

Assistentes especializados por disciplina.

### Usar Agente

1. Clique na aba **Agentes IA**
2. Selecione uma disciplina na lista
3. Digite sua pergunta
4. Clique em **Enviar** ou pressione Enter

### Funcionalidades

- **Chat Interativo** - Tire dúvidas sobre a matéria
- **Histórico** - Tópicos recentes
- **Limpar** - Resetar conversa

### Exemplos de Perguntas

- "Explique polimorfismo em POO"
- "Como funciona o modelo relacional?"
- "Qual é a diferença entre TCP e UDP?"

---

## Estatísticas

Análise detalhada do seu desempenho.

### Gráficos

- **Horas por Disciplina** - Distribuição de tempo
- **Horas de Estudo Diário** - Tendência semanal

### Conquistas

Desbloqueie achievements:
- ⭐ Primeira Semana
- 🔥 7 dias consecutivos
- 🏅 21 horas em 1 semana
- 👑 Todas as tarefas em dia

---

## Dicas e Boas Práticas

### Produtividade

1. **Use o Timer Pomodoro** - Melhora foco e concentração
2. **Estude regularmente** - Consistência é chave
3. **Faça pausas** - Previne fadiga mental
4. **Revise estatísticas** - Acompanhe seu progresso

### Organização

1. **Configure disciplinas** - Customize seu currículo
2. **Crie pastas locais** - Organize materiais
3. **Sincronize Moodle** - Nunca perca prazos
4. **Planeje com antecedência** - Use o calendário

### Estudo Eficaz

1. **Comece cedo** - Não deixe para última hora
2. **Divida em tópicos** - Estude por partes
3. **Use flashcards** - Revise conceitos
4. **Pratique exercícios** - Reforce aprendizado

---

## Troubleshooting

### Problema: Aplicação não inicia

**Solução:**
```bash
# Verificar se porta 5000 está em uso
lsof -ti:5000

# Matar processo
kill -9 $(lsof -ti:5000)

# Reiniciar
./start.sh
```

### Problema: Dados não carregam

**Solução:**
```bash
# Limpar cache do navegador (Ctrl+Shift+Delete)
# Recarregar página (Ctrl+F5)
# Reiniciar servidor
./restart.sh
```

### Problema: Timer não funciona

**Solução:**
- Verificar se JavaScript está habilitado
- Limpar cache do navegador
- Testar em outro navegador

---

## Suporte

- **Issues:** GitHub Issues
- **Documentação:** README.md
- **Logs:** backend.log

**Bons estudos! 🎓✨**

