# 🎓 Gestão de Cadeiras UAB

Sistema de gestão de disciplinas para estudantes da Universidade Aberta de Portugal (UAB) - Licenciatura em Engenharia Informática (LEI).

## 📋 Descrição

Este projeto é um sistema completo de planejamento e gestão de estudos para alunos da UAB LEI, integrando:

- 📊 Dashboard com estatísticas de progresso
- 📅 Calendário de estudos semanal
- 📝 Gerenciamento de tarefas e e-fólios
- ⏱️ Timer Pomodoro para sessões focadas
- 🏫 Integração com Moodle UAB
- 🤖 Assistentes IA para tirar dúvidas
- 📁 Sincronização de materiais de estudo
- 📈 Análise de desempenho e estatísticas

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.8+
- Git
- Navegador moderno (Chrome, Firefox, Edge)

### Instalação

```bash
# Clonar repositório
git clone https://github.com/igorcostas/gestao-cadeiras-uab.git
cd gestao-cadeiras-uab

# Executar script de inicialização
./start.sh
```

### Uso

1. Acesse `http://localhost:5000` no navegador
2. Complete o Setup Wizard na primeira vez
3. Configure suas disciplinas e disponibilidade
4. Comece a estudar!

## 📚 Funcionalidades

### Dashboard
- Visão geral do progresso
- Horas estudadas (hoje/semana)
- Próximos e-fólios
- Progresso por disciplina

### Calendário
- Plano de trabalho semanal
- Distribuição de horas por disciplina
- Atividades recomendadas

### Disciplinas
- Visualização de tópicos
- Materiais de estudo
- Sessões síncronas
- Histórico de pomodoros

### Timer Pomodoro
- 25 minutos de estudo
- 5 minutos de pausa
- Notificações automáticas
- Histórico de sessões

### Tarefas
- Criar e gerenciar tarefas
- Filtrar por tipo (e-Fólio, Sessão Síncrona, etc)
- Marcar como concluída
- Priorização

### Moodle
- Integração com UAB
- Sincronização de materiais
- Acesso rápido a disciplinas

### IA
- Chat com assistentes especializados
- Tirar dúvidas sobre matérias
- Resumir PDFs
- Explicar conceitos

### Estatísticas
- Gráficos de horas por disciplina
- Análise de padrões de estudo
- Conquistas e achievements

## 📁 Estrutura do Projeto

```
gestao-cadeiras-uab/
├── backend/
│   ├── app.py                 # API Flask
│   ├── moodle_integration.py  # Integração Moodle
│   ├── ai_assistant.py        # Assistentes IA
│   ├── folder_sync.py         # Sincronização de pastas
│   └── requirements.txt       # Dependências Python
├── frontend/
│   ├── index.html             # Interface principal
│   ├── app.js                 # Lógica da aplicação
│   ├── styles.css             # Estilos
│   ├── setup-wizard.html      # Setup inicial
│   └── setup-wizard.js        # Lógica do setup
├── data/
│   ├── disciplinas.json       # Configuração de disciplinas
│   └── estudos.db             # Banco de dados SQLite
├── README.md                  # Este arquivo
├── TUTORIAL_COMPLETO.md       # Guia completo de uso
├── start.sh                   # Script de inicialização
└── restart.sh                 # Script de reinicialização
```

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
# Moodle
MOODLE_USERNAME=seu_usuario
MOODLE_PASSWORD=sua_senha

# IA (OpenRouter)
OPENROUTER_API_KEY=sk-or-v1-...

# Sincronização
SYNC_FOLDERS='["/caminho/para/pasta1", "/caminho/para/pasta2"]'
SYNC_INTERVAL=300
```

## 📖 Documentação

- [Tutorial Completo](TUTORIAL_COMPLETO.md) - Guia detalhado de todas as funcionalidades
- [README.md](README.md) - Instruções de instalação e configuração

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Igor Costas**
- GitHub: [@igorcostas](https://github.com/igorcostas)
- Email: igorhenriquecosta1@gmail.com

## 🙏 Agradecimentos

- Universidade Aberta de Portugal (UAB)
- Comunidade de estudantes LEI
- Contribuidores e testadores

## 📞 Suporte

Para reportar bugs ou sugerir melhorias, abra uma [Issue](https://github.com/igorcostas/gestao-cadeiras-uab/issues).

---

**Bons estudos! 🎓✨**

