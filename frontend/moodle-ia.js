// ============================================================
// MÓDULO MOODLE
// ============================================================

const MoodleModule = {
    isLoggedIn: false,
    currentCourses: [],
    notifications: [],

    init() {
        this.setupEventListeners();
        this.checkStatus();
    },

    setupEventListeners() {
        // Login form
        const loginForm = document.getElementById('moodle-login-form');
        if (loginForm) {
            loginForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.login();
            });
        }

        // Sync button
        const syncBtn = document.getElementById('btn-sync-all');
        if (syncBtn) {
            syncBtn.addEventListener('click', () => this.syncAll());
        }

        // Tabs
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tab = e.currentTarget.dataset.tab;
                this.switchTab(tab);
            });
        });
    },

    async checkStatus() {
        try {
            const response = await fetch('http://localhost:5000/api/moodle/status');
            const data = await response.json();

            if (data.logged_in) {
                this.showMainArea();
                this.loadAllData();
            }
        } catch (error) {
            console.error('Erro ao verificar status:', error);
        }
    },

    async login() {
        const username = document.getElementById('moodle-username').value;
        const password = document.getElementById('moodle-password').value;

        showLoading();

        try {
            const response = await fetch('http://localhost:5000/api/moodle/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (data.success) {
                this.isLoggedIn = true;
                showToast('Login realizado com sucesso!', 'success');
                this.showMainArea();
                await this.loadAllData();
            } else {
                showToast('Erro no login: ' + data.error, 'error');
            }
        } catch (error) {
            showToast('Erro ao conectar ao servidor', 'error');
            console.error(error);
        } finally {
            hideLoading();
        }
    },

    showMainArea() {
        document.getElementById('moodle-login-area').style.display = 'none';
        document.getElementById('moodle-main-area').style.display = 'block';
    },

    async loadAllData() {
        await Promise.all([
            this.loadCourses(),
            this.loadNotifications(),
            this.updateSyncStatus()
        ]);
    },

    async loadCourses() {
        try {
            const response = await fetch('http://localhost:5000/api/moodle/courses');
            const data = await response.json();

            if (data.success) {
                this.currentCourses = data.courses;
                this.renderCourses(data.courses);
            }
        } catch (error) {
            console.error('Erro ao carregar disciplinas:', error);
        }
    },

    renderCourses(courses) {
        const container = document.getElementById('moodle-courses-list');
        if (!container) return;

        container.innerHTML = courses.map(course => `
            <div class="course-card" data-course-id="${course.id}">
                <div class="course-icon">
                    <i class="fas fa-book"></i>
                </div>
                <div class="course-info">
                    <h4>${course.name}</h4>
                    <div class="course-actions">
                        <button class="btn btn-sm" onclick="MoodleModule.loadCourseDetails(${course.id})">
                            <i class="fas fa-eye"></i> Ver Detalhes
                        </button>
                        <button class="btn btn-sm" onclick="MoodleModule.loadCourseMaterials(${course.id})">
                            <i class="fas fa-download"></i> Materiais
                        </button>
                    </div>
                </div>
            </div>
        `).join('');

        // Atualizar contador
        document.getElementById('sync-courses-count').textContent = courses.length;
    },

    async loadCourseDetails(courseId) {
        showLoading();
        try {
            // Carregar tarefas
            const assignmentsRes = await fetch(`http://localhost:5000/api/moodle/assignments/${courseId}`);
            const assignmentsData = await assignmentsRes.json();

            // Carregar fóruns
            const forumsRes = await fetch(`http://localhost:5000/api/moodle/forums/${courseId}`);
            const forumsData = await forumsRes.json();

            // Carregar notas
            const gradesRes = await fetch(`http://localhost:5000/api/moodle/grades/${courseId}`);
            const gradesData = await gradesRes.json();

            // Exibir em modal ou seção dedicada
            this.renderCourseDetails({
                assignments: assignmentsData.assignments || [],
                forums: forumsData.forums || [],
                grades: gradesData.grades || {}
            });

        } catch (error) {
            showToast('Erro ao carregar detalhes', 'error');
            console.error(error);
        } finally {
            hideLoading();
        }
    },

    renderCourseDetails(details) {
        // Renderizar tarefas
        const assignmentsList = document.getElementById('moodle-assignments-list');
        if (assignmentsList && details.assignments) {
            assignmentsList.innerHTML = details.assignments.map(assignment => `
                <div class="assignment-item">
                    <div class="assignment-info">
                        <h4>${assignment.name}</h4>
                        <p class="assignment-deadline">
                            <i class="fas fa-clock"></i>
                            ${assignment.deadline || 'Sem prazo definido'}
                        </p>
                    </div>
                    <a href="${assignment.url}" target="_blank" class="btn btn-sm btn-primary">
                        <i class="fas fa-external-link-alt"></i> Abrir
                    </a>
                </div>
            `).join('');
        }

        // Renderizar fóruns
        const forumsList = document.getElementById('moodle-forums-list');
        if (forumsList && details.forums) {
            forumsList.innerHTML = details.forums.map(forum => `
                <div class="forum-item">
                    <div class="forum-icon">
                        <i class="fas fa-comments"></i>
                    </div>
                    <div class="forum-info">
                        <h4>${forum.title}</h4>
                        <p class="forum-author">Por: ${forum.author}</p>
                    </div>
                    <a href="${forum.url}" target="_blank" class="btn btn-sm">
                        <i class="fas fa-eye"></i> Ver
                    </a>
                </div>
            `).join('');
        }

        // Renderizar notas
        const gradesList = document.getElementById('moodle-grades-list');
        if (gradesList && details.grades) {
            const gradesHTML = Object.entries(details.grades).map(([item, grade]) => `
                <div class="grade-item">
                    <span class="grade-label">${item}</span>
                    <span class="grade-value">${grade}</span>
                </div>
            `).join('');
            gradesList.innerHTML = gradesHTML || '<p>Nenhuma nota disponível</p>';
        }
    },

    async loadCourseMaterials(courseId) {
        showLoading();
        try {
            const response = await fetch(`http://localhost:5000/api/moodle/materials/${courseId}`);
            const data = await response.json();

            if (data.success) {
                this.renderMaterials(data.materials);
            }
        } catch (error) {
            showToast('Erro ao carregar materiais', 'error');
        } finally {
            hideLoading();
        }
    },

    renderMaterials(materials) {
        const container = document.getElementById('new-materials-list');
        if (!container) return;

        container.innerHTML = materials.map(material => `
            <div class="material-card">
                <div class="material-icon">
                    <i class="fas fa-${material.type === 'pdf' ? 'file-pdf' : 'file'}"></i>
                </div>
                <div class="material-info">
                    <h4>${material.name}</h4>
                    <small>${material.type.toUpperCase()}</small>
                </div>
                <a href="${material.url}" target="_blank" class="btn btn-sm">
                    <i class="fas fa-download"></i> Baixar
                </a>
            </div>
        `).join('');

        document.getElementById('sync-materials-count').textContent = materials.length;
    },

    async loadNotifications() {
        try {
            const response = await fetch('http://localhost:5000/api/moodle/notifications');
            const data = await response.json();

            if (data.success) {
                this.notifications = data.notifications || [];
                this.renderNotifications(this.notifications);
            }
        } catch (error) {
            console.error('Erro ao carregar notificações:', error);
        }
    },

    renderNotifications(notifications) {
        const container = document.getElementById('notifications-list');
        if (!container) return;

        if (notifications.length === 0) {
            container.innerHTML = '<p class="empty-state">Nenhuma notificação nova</p>';
            return;
        }

        container.innerHTML = notifications.map(notif => `
            <div class="notification-item">
                <div class="notification-icon">
                    <i class="fas fa-bell"></i>
                </div>
                <div class="notification-content">
                    <h4>${notif.subject || 'Notificação'}</h4>
                    <p>${notif.message || ''}</p>
                    <small>${notif.time || ''}</small>
                </div>
            </div>
        `).join('');

        document.getElementById('sync-notifications-count').textContent = notifications.length;
    },

    async syncAll() {
        showLoading();
        showToast('Sincronizando dados do Moodle...', 'info');

        try {
            const response = await fetch('http://localhost:5000/api/moodle/sync', {
                method: 'POST'
            });

            const data = await response.json();

            if (data.success) {
                showToast('Sincronização concluída!', 'success');
                await this.loadAllData();
                this.updateSyncStatus();
            } else {
                showToast('Erro na sincronização', 'error');
            }
        } catch (error) {
            showToast('Erro ao sincronizar', 'error');
            console.error(error);
        } finally {
            hideLoading();
        }
    },

    updateSyncStatus() {
        const now = new Date();
        const timeStr = now.toLocaleTimeString('pt-BR', {
            hour: '2-digit',
            minute: '2-digit'
        });

        const lastSyncEl = document.getElementById('last-sync-time');
        if (lastSyncEl) {
            lastSyncEl.textContent = timeStr;
        }
    },

    switchTab(tabName) {
        // Atualizar botões
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Atualizar conteúdo
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`tab-${tabName}`).classList.add('active');

        // Carregar dados se necessário
        if (tabName === 'calendar') {
            this.loadCalendar();
        }
    },

    async loadCalendar() {
        try {
            const response = await fetch('http://localhost:5000/api/moodle/calendar');
            const data = await response.json();

            if (data.success) {
                this.renderCalendar(data.events || []);
            }
        } catch (error) {
            console.error('Erro ao carregar calendário:', error);
        }
    },

    renderCalendar(events) {
        const container = document.getElementById('moodle-calendar');
        if (!container) return;

        if (events.length === 0) {
            container.innerHTML = '<p class="empty-state">Nenhum evento no calendário</p>';
            return;
        }

        container.innerHTML = events.map(event => `
            <div class="calendar-event">
                <div class="event-date">
                    <i class="fas fa-calendar"></i>
                    ${event.date}
                </div>
                <div class="event-info">
                    <h4>${event.title}</h4>
                    <a href="${event.url}" target="_blank">Ver detalhes</a>
                </div>
            </div>
        `).join('');
    }
};

// ============================================================
// MÓDULO IA
// ============================================================

const IAModule = {
    isConfigured: false,
    chatHistory: [],
    currentFlashcards: [],
    currentFlashcardIndex: 0,

    init() {
        this.checkStatus();
        this.setupEventListeners();
    },

    setupEventListeners() {
        // Chat
        const sendBtn = document.getElementById('btn-send-chat');
        if (sendBtn) {
            sendBtn.addEventListener('click', () => this.sendChatMessage());
        }

        const chatInput = document.getElementById('chat-input');
        if (chatInput) {
            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendChatMessage();
                }
            });
        }

        // Suggestions
        document.querySelectorAll('.suggestion-chip').forEach(chip => {
            chip.addEventListener('click', (e) => {
                const suggestion = e.currentTarget.dataset.suggestion;
                document.getElementById('chat-input').value = suggestion;
                this.sendChatMessage();
            });
        });

        // Resumir PDF
        const summarizeBtn = document.getElementById('btn-summarize-pdf');
        if (summarizeBtn) {
            summarizeBtn.addEventListener('click', () => this.summarizePDF());
        }

        // Explicar conceito
        const explainBtn = document.getElementById('btn-explain-concept');
        if (explainBtn) {
            explainBtn.addEventListener('click', () => this.explainConcept());
        }

        // Criar flashcards
        const flashcardsBtn = document.getElementById('btn-create-flashcards');
        if (flashcardsBtn) {
            flashcardsBtn.addEventListener('click', () => this.createFlashcards());
        }

        // Plano de estudos
        const studyPlanBtn = document.getElementById('btn-create-study-plan');
        if (studyPlanBtn) {
            studyPlanBtn.addEventListener('click', () => this.createStudyPlan());
        }

        // Tabs IA
        document.querySelectorAll('.ia-tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tab = e.currentTarget.dataset.iaTab;
                this.switchTab(tab);
            });
        });

        // Navegação de flashcards
        const prevBtn = document.getElementById('btn-prev-flashcard');
        const nextBtn = document.getElementById('btn-next-flashcard');
        if (prevBtn) prevBtn.addEventListener('click', () => this.prevFlashcard());
        if (nextBtn) nextBtn.addEventListener('click', () => this.nextFlashcard());
    },

    async checkStatus() {
        try {
            const response = await fetch('http://localhost:5000/api/ai/status');
            const data = await response.json();

            const statusCheck = document.getElementById('ia-status-check');
            const mainArea = document.getElementById('ia-main-area');
            const configArea = document.getElementById('ia-config-area');
            const statusMessage = document.getElementById('ia-status-message');

            if (data.available && data.configured) {
                this.isConfigured = true;
                statusCheck.style.display = 'none';
                mainArea.style.display = 'block';
                configArea.style.display = 'none';
            } else if (data.available && !data.configured) {
                statusMessage.textContent = 'Assistente disponível mas não configurado';
                setTimeout(() => {
                    statusCheck.style.display = 'none';
                    configArea.style.display = 'block';
                }, 2000);
            } else {
                statusMessage.textContent = 'Módulo IA não disponível';
                setTimeout(() => {
                    statusCheck.style.display = 'none';
                    configArea.style.display = 'block';
                }, 2000);
            }
        } catch (error) {
            console.error('Erro ao verificar status da IA:', error);
            document.getElementById('ia-status-message').textContent = 'Erro ao conectar';
        }
    },

    async sendChatMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();

        if (!message) return;

        // Adicionar mensagem do usuário
        this.addChatMessage(message, 'user');
        input.value = '';

        // Contexto
        const disciplineSelect = document.getElementById('chat-context-discipline');
        const context = disciplineSelect ? {
            disciplina: disciplineSelect.value
        } : null;

        showLoading();

        try {
            const response = await fetch('http://localhost:5000/api/ai/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message, context })
            });

            const data = await response.json();

            if (data.success) {
                this.addChatMessage(data.response, 'bot');
            } else {
                this.addChatMessage('Erro: ' + data.response, 'bot');
            }
        } catch (error) {
            this.addChatMessage('Erro ao conectar com o assistente', 'bot');
            console.error(error);
        } finally {
            hideLoading();
        }
    },

    addChatMessage(text, sender) {
        const messagesContainer = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${sender}`;

        const time = new Date().toLocaleTimeString('pt-BR', {
            hour: '2-digit',
            minute: '2-digit'
        });

        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-${sender === 'user' ? 'user' : 'robot'}"></i>
            </div>
            <div class="message-content">
                <p>${text}</p>
                <small class="message-time">${time}</small>
            </div>
        `;

        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    },

    async summarizePDF() {
        const fileInput = document.getElementById('pdf-file-input');
        const style = document.getElementById('summary-style').value;

        if (!fileInput.files || !fileInput.files[0]) {
            showToast('Selecione um arquivo PDF', 'warning');
            return;
        }

        showLoading();
        showToast('Resumindo PDF... Isso pode levar alguns segundos', 'info');

        try {
            // Simular upload e processamento
            // Em produção, você precisaria fazer upload do arquivo primeiro
            const file = fileInput.files[0];
            const pdfPath = `/tmp/${file.name}`;

            const response = await fetch('http://localhost:5000/api/ai/summarize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ pdf_path: pdfPath, style })
            });

            const data = await response.json();

            if (data.success) {
                document.getElementById('summary-content').textContent = data.summary;
                document.getElementById('summary-result').style.display = 'block';
                showToast('Resumo gerado com sucesso!', 'success');
            } else {
                showToast('Erro: ' + data.error, 'error');
            }
        } catch (error) {
            showToast('Erro ao gerar resumo', 'error');
            console.error(error);
        } finally {
            hideLoading();
        }
    },

    async explainConcept() {
        const concept = document.getElementById('concept-input').value.trim();
        const level = document.getElementById('explanation-level').value;

        if (!concept) {
            showToast('Digite um conceito para explicar', 'warning');
            return;
        }

        showLoading();

        try {
            const response = await fetch('http://localhost:5000/api/ai/explain', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ concept, level })
            });

            const data = await response.json();

            if (data.success) {
                document.getElementById('explanation-content').innerHTML =
                    data.explanation.replace(/\n/g, '<br>');
                document.getElementById('explanation-result').style.display = 'block';
                showToast('Conceito explicado!', 'success');
            } else {
                showToast('Erro: ' + data.explanation, 'error');
            }
        } catch (error) {
            showToast('Erro ao explicar conceito', 'error');
            console.error(error);
        } finally {
            hideLoading();
        }
    },

    async createFlashcards() {
        const fileInput = document.getElementById('flashcards-pdf-input');
        const numCards = document.getElementById('num-flashcards').value;

        if (!fileInput.files || !fileInput.files[0]) {
            showToast('Selecione um arquivo PDF', 'warning');
            return;
        }

        showLoading();
        showToast('Criando flashcards... Aguarde', 'info');

        try {
            const file = fileInput.files[0];
            const pdfPath = `/tmp/${file.name}`;

            const response = await fetch('http://localhost:5000/api/ai/flashcards', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ pdf_path: pdfPath, num_cards: parseInt(numCards) })
            });

            const data = await response.json();

            if (data.success) {
                this.currentFlashcards = data.flashcards;
                this.currentFlashcardIndex = 0;
                this.renderFlashcard();
                document.getElementById('flashcards-result').style.display = 'block';
                showToast(`${data.count} flashcards criados!`, 'success');
            } else {
                showToast('Erro: ' + data.error, 'error');
            }
        } catch (error) {
            showToast('Erro ao criar flashcards', 'error');
            console.error(error);
        } finally {
            hideLoading();
        }
    },

    renderFlashcard() {
        if (this.currentFlashcards.length === 0) return;

        const card = this.currentFlashcards[this.currentFlashcardIndex];
        const container = document.getElementById('flashcards-list');

        container.innerHTML = `
            <div class="flashcard" onclick="this.classList.toggle('flipped')">
                <div class="flashcard-front">
                    <h4>Pergunta:</h4>
                    <p>${card.frente}</p>
                    <small>Clique para ver a resposta</small>
                </div>
                <div class="flashcard-back">
                    <h4>Resposta:</h4>
                    <p>${card.verso}</p>
                </div>
            </div>
        `;

        document.getElementById('flashcard-counter').textContent =
            `${this.currentFlashcardIndex + 1} / ${this.currentFlashcards.length}`;
    },

    prevFlashcard() {
        if (this.currentFlashcardIndex > 0) {
            this.currentFlashcardIndex--;
            this.renderFlashcard();
        }
    },

    nextFlashcard() {
        if (this.currentFlashcardIndex < this.currentFlashcards.length - 1) {
            this.currentFlashcardIndex++;
            this.renderFlashcard();
        }
    },

    async createStudyPlan() {
        const weeks = document.getElementById('study-plan-weeks').value;

        // Pegar disciplinas selecionadas
        const selectedDisciplines = [];
        document.querySelectorAll('#study-plan-disciplines input:checked').forEach(input => {
            selectedDisciplines.push({ name: input.value });
        });

        if (selectedDisciplines.length === 0) {
            showToast('Selecione pelo menos uma disciplina', 'warning');
            return;
        }

        showLoading();

        try {
            const response = await fetch('http://localhost:5000/api/ai/study-plan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    courses: selectedDisciplines,
                    weeks: parseInt(weeks)
                })
            });

            const data = await response.json();

            if (data.success) {
                document.getElementById('study-plan-content').innerHTML =
                    data.plan.replace(/\n/g, '<br>');
                document.getElementById('study-plan-result').style.display = 'block';
                showToast('Plano de estudos criado!', 'success');
            } else {
                showToast('Erro: ' + data.error, 'error');
            }
        } catch (error) {
            showToast('Erro ao criar plano', 'error');
            console.error(error);
        } finally {
            hideLoading();
        }
    },

    switchTab(tabName) {
        // Atualizar botões
        document.querySelectorAll('.ia-tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-ia-tab="${tabName}"]`).classList.add('active');

        // Atualizar conteúdo
        document.querySelectorAll('.ia-tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`ia-tab-${tabName}`).classList.add('active');
    }
};

// ============================================================
// INICIALIZAÇÃO
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
    // Inicializar módulos quando a página Moodle ou IA for aberta
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.target.id === 'page-moodle' &&
                mutation.target.classList.contains('active')) {
                MoodleModule.init();
            }
            if (mutation.target.id === 'page-ia' &&
                mutation.target.classList.contains('active')) {
                IAModule.init();
            }
        });
    });

    const moodlePage = document.getElementById('page-moodle');
    const iaPage = document.getElementById('page-ia');

    if (moodlePage) {
        observer.observe(moodlePage, { attributes: true, attributeFilter: ['class'] });
    }
    if (iaPage) {
        observer.observe(iaPage, { attributes: true, attributeFilter: ['class'] });
    }
});

// Exportar módulos
window.MoodleModule = MoodleModule;
window.IAModule = IAModule;
