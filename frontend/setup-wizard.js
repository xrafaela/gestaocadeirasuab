/**
 * Setup Wizard para Primeiro Usuário
 * Gerencia a configuração inicial do Study Planner
 */

let setupState = {
    currentStep: 1,
    nome: '',
    curso: '',
    ano: '',
    disciplinas: [],
    horasDia: 3,
    diasEstudo: ['segunda', 'terca', 'quarta', 'quinta', 'sexta'],
    todasDisciplinas: []
};

// Inicializar setup wizard
function initSetupWizard() {
    const setupWizard = document.getElementById('setup-wizard');
    if (!setupWizard) {
        console.warn('Setup wizard HTML não encontrado');
        return;
    }

    // Verificar se há dados gravados (usuário já ativo)
    const userConfig = localStorage.getItem('userConfig');
    const setupCompleto = localStorage.getItem('setupCompleto');

    // Mostrar wizard apenas se não houver dados gravados
    if (!userConfig && !setupCompleto) {
        setupWizard.style.display = 'flex';
        carregarDisciplinasParaSetup();
    } else {
        // Usuário já tem dados, esconder wizard
        setupWizard.style.display = 'none';
    }
}

// Carregar disciplinas para o setup
async function carregarDisciplinasParaSetup() {
    try {
        const response = await fetch(`${API_URL}/disciplinas`);
        const disciplinas = await response.json();
        setupState.todasDisciplinas = disciplinas;
        renderDisciplinasSetup(disciplinas);
    } catch (error) {
        console.error('Erro ao carregar disciplinas:', error);
    }
}

// Renderizar disciplinas no setup
function renderDisciplinasSetup(disciplinas) {
    const container = document.getElementById('setup-disciplinas-list');
    if (!container) return;

    container.innerHTML = disciplinas.map(d => `
        <label style="background-color: ${d.cor}20; border-left: 4px solid ${d.cor};">
            <input type="checkbox" name="disciplina" value="${d.id}" checked>
            <span>${d.sigla} - ${d.nome}</span>
        </label>
    `).join('');
}

// Navegar para próximo passo
function nextSetupStep(step) {
    // Validar passo atual
    if (!validarPasso(setupState.currentStep)) {
        return;
    }

    // Salvar dados do passo atual
    salvarDadosPasso(setupState.currentStep);

    // Mostrar próximo passo
    document.getElementById(`step-${setupState.currentStep}`).classList.remove('active');
    setupState.currentStep = step;
    document.getElementById(`step-${step}`).classList.add('active');

    // Atualizar progress bar
    atualizarProgressBar();

    // Se for passo 4, gerar calendário
    if (step === 4) {
        gerarCalendarioPreview();
    }
}

// Navegar para passo anterior
function prevSetupStep(step) {
    document.getElementById(`step-${setupState.currentStep}`).classList.remove('active');
    setupState.currentStep = step;
    document.getElementById(`step-${step}`).classList.add('active');
    atualizarProgressBar();
}

// Validar dados do passo
function validarPasso(passo) {
    switch (passo) {
        case 1:
            const nome = document.getElementById('setup-nome').value.trim();
            const curso = document.getElementById('setup-curso').value.trim();
            const ano = document.getElementById('setup-ano').value;

            if (!nome || !curso || !ano) {
                alert('Por favor, preencha todos os campos');
                return false;
            }
            return true;

        case 2:
            const disciplinasChecked = document.querySelectorAll('input[name="disciplina"]:checked');
            if (disciplinasChecked.length === 0) {
                alert('Por favor, selecione pelo menos uma disciplina');
                return false;
            }
            return true;

        case 3:
            const horasDia = document.getElementById('setup-horas-dia').value;
            if (!horasDia || horasDia < 1) {
                alert('Por favor, indique as horas de estudo disponíveis');
                return false;
            }
            return true;

        default:
            return true;
    }
}

// Salvar dados do passo
function salvarDadosPasso(passo) {
    switch (passo) {
        case 1:
            setupState.nome = document.getElementById('setup-nome').value;
            setupState.curso = document.getElementById('setup-curso').value;
            setupState.ano = document.getElementById('setup-ano').value;
            break;

        case 2:
            const disciplinasChecked = document.querySelectorAll('input[name="disciplina"]:checked');
            setupState.disciplinas = Array.from(disciplinasChecked).map(el => el.value);
            break;

        case 3:
            setupState.horasDia = parseInt(document.getElementById('setup-horas-dia').value);
            const diasChecked = document.querySelectorAll('input[name="dia"]:checked');
            setupState.diasEstudo = Array.from(diasChecked).map(el => el.value);
            break;
    }
}

// Atualizar progress bar
function atualizarProgressBar() {
    const progressFill = document.getElementById('setup-progress-fill');
    const progressText = document.getElementById('setup-progress-text');
    const percentual = (setupState.currentStep / 4) * 100;
    progressFill.style.width = percentual + '%';
    progressText.textContent = `Passo ${setupState.currentStep} de 4`;
}

// Gerar preview do calendário
function gerarCalendarioPreview() {
    const container = document.getElementById('setup-calendario-preview');
    if (!container) return;

    const diasSemana = ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo'];
    const diasNomes = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'];

    let html = '<h3>Seu Calendário de Estudos</h3>';
    html += '<p>Horas por dia: <strong>' + setupState.horasDia + 'h</strong></p>';
    html += '<p>Dias de estudo: <strong>' + setupState.diasEstudo.length + ' dias/semana</strong></p>';
    html += '<div style="margin-top: 15px;">';

    diasSemana.forEach((dia, index) => {
        const ativo = setupState.diasEstudo.includes(dia);
        const classe = ativo ? 'ativo' : 'inativo';
        html += `<div style="padding: 8px; margin: 5px 0; background: ${ativo ? '#e8f5e9' : '#f5f5f5'}; border-radius: 5px; border-left: 4px solid ${ativo ? '#4caf50' : '#ccc'};">
            <strong>${diasNomes[index]}</strong>: ${ativo ? setupState.horasDia + 'h de estudo' : 'Sem estudo'}
        </div>`;
    });

    html += '</div>';
    html += '<p style="margin-top: 15px; color: #666; font-size: 14px;">Total semanal: <strong>' + (setupState.horasDia * setupState.diasEstudo.length) + 'h</strong></p>';

    container.innerHTML = html;
}

// Finalizar setup
async function finalizarSetup() {
    salvarDadosPasso(3);

    // Salvar configuração no localStorage
    const config = {
        nome: setupState.nome,
        curso: setupState.curso,
        ano: setupState.ano,
        disciplinas: setupState.disciplinas,
        horasDia: setupState.horasDia,
        diasEstudo: setupState.diasEstudo,
        dataSetup: new Date().toISOString()
    };

    localStorage.setItem('userConfig', JSON.stringify(config));
    localStorage.setItem('setupCompleto', 'true');

    // Fechar wizard
    const setupWizard = document.getElementById('setup-wizard');
    setupWizard.style.display = 'none';

    // Recarregar página
    showToast('✅ Setup concluído! Bem-vindo ao Study Planner!', 'success');
    setTimeout(() => {
        location.reload();
    }, 1500);
}

// Exportar configuração do usuário
function getUserConfig() {
    const config = localStorage.getItem('userConfig');
    return config ? JSON.parse(config) : null;
}

// Resetar setup (para testes)
function resetSetup() {
    localStorage.removeItem('setupCompleto');
    localStorage.removeItem('userConfig');
    location.reload();
}

