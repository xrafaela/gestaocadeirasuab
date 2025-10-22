/**
 * Sistema de Planejamento de Estudos - UAB LEI
 * Frontend JavaScript Application
 */

// ==================== CONFIGURAÇÃO E ESTADO GLOBAL ====================
const API_URL = "http://localhost:5000/api";
let currentState = {
  disciplinas: [],
  calendario: {},
  tarefas: [],
  sessoes: [],
  dashboard: {},
  semanaAtual: 1,
  timer: {
    minutes: 25,
    seconds: 0,
    isRunning: false,
    isPaused: false,
    type: "study", // 'study' or 'break'
    interval: null,
    totalSeconds: 1500, // 25 minutes
    currentSeconds: 1500,
    startTimestamp: null, // Timestamp de quando o timer foi iniciado
    pausedAt: null, // Tempo restante quando pausado
  },
};

// ==================== INICIALIZAÇÃO ====================
document.addEventListener("DOMContentLoaded", () => {
  console.log("🚀 Iniciando aplicação...");

  initializeNavigation();
  initializeModals();
  initializeTimer();
  loadInitialData();
  initializePageVisibility();
  requestNotificationPermission();

  // Atualizar dashboard a cada 5 minutos
  setInterval(loadDashboard, 300000);
});

// Solicitar permissão para notificações
function requestNotificationPermission() {
  if ("Notification" in window && Notification.permission === "default") {
    Notification.requestPermission().then((permission) => {
      if (permission === "granted") {
        console.log("✅ Permissão para notificações concedida");
      }
    });
  }
}

// Detectar quando a aba volta a ficar ativa
function initializePageVisibility() {
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden && currentState.timer.isRunning) {
      // Recalcular o tempo restante quando a página volta a ficar visível
      const elapsedSeconds = Math.floor(
        (Date.now() - currentState.timer.startTimestamp) / 1000,
      );
      const remainingSeconds = currentState.timer.totalSeconds - elapsedSeconds;

      if (remainingSeconds <= 0) {
        // Timer já deveria ter terminado
        currentState.timer.currentSeconds = 0;
        updateTimerDisplay();
        timerComplete();
      } else {
        currentState.timer.currentSeconds = remainingSeconds;
        updateTimerDisplay();
      }

      console.log(`⏱️ Timer atualizado: ${remainingSeconds}s restantes`);
    }
  });
}

// ==================== NAVEGAÇÃO ====================
function initializeNavigation() {
  const navItems = document.querySelectorAll(".nav-item");

  navItems.forEach((item) => {
    item.addEventListener("click", () => {
      const pageName = item.getAttribute("data-page");
      navigateToPage(pageName);

      // Atualizar nav ativo
      navItems.forEach((nav) => nav.classList.remove("active"));
      item.classList.add("active");
    });
  });
}

function navigateToPage(pageName) {
  // Esconder todas as páginas
  document.querySelectorAll(".page").forEach((page) => {
    page.classList.remove("active");
  });

  // Mostrar página selecionada
  const targetPage = document.getElementById(`page-${pageName}`);
  if (targetPage) {
    targetPage.classList.add("active");

    // Carregar dados específicos da página
    loadPageData(pageName);
  }
}

function loadPageData(pageName) {
  switch (pageName) {
    case "dashboard":
      loadDashboard();
      break;
    case "calendario":
      loadCalendario();
      break;
    case "disciplinas":
      loadDisciplinas();
      break;
    case "tarefas":
      loadTarefas();
      break;
    case "estatisticas":
      loadEstatisticas();
      break;
    case "agents":
      // Página de agentes Copilot - carregamento automático via HTML
      break;
  }
}

// ==================== CARREGAMENTO INICIAL DE DADOS ====================
async function loadInitialData() {
  showLoading();

  try {
    await Promise.all([
      loadDashboard(),
      loadDisciplinas(),
      inicializarTarefasAutomaticas(),
    ]);

    showToast("Dados carregados com sucesso!", "success");
  } catch (error) {
    console.error("Erro ao carregar dados:", error);
    showToast("Erro ao carregar dados", "error");
  } finally {
    hideLoading();
  }
}

// ==================== DASHBOARD ====================
async function loadDashboard() {
  try {
    const response = await fetch(`${API_URL}/dashboard`);
    const data = await response.json();
    currentState.dashboard = data;

    renderDashboard(data);
  } catch (error) {
    console.error("Erro ao carregar dashboard:", error);
  }
}

function renderDashboard(data) {
  // Horas estudadas hoje
  document.getElementById("horas-hoje").textContent =
    `${data.horas_estudadas_hoje}h`;
  const progressHoje = (data.horas_estudadas_hoje / data.meta_diaria) * 100;
  document.getElementById("progress-hoje").style.width =
    `${Math.min(progressHoje, 100)}%`;

  // Horas estudadas esta semana
  document.getElementById("horas-semana").textContent =
    `${data.horas_estudadas_semana}h`;
  const progressSemana =
    (data.horas_estudadas_semana / data.meta_semanal) * 100;
  document.getElementById("progress-semana").style.width =
    `${Math.min(progressSemana, 100)}%`;

  // Semana atual
  document.getElementById("semana-atual").textContent =
    `Semana ${data.semana_atual}`;

  // Tarefas pendentes
  const totalPendentes = data.tarefas_proximas.length;
  document.getElementById("tarefas-pendentes").textContent = totalPendentes;

  // Tarefas urgentes (próximos 3 dias)
  const hoje = new Date();
  const urgentes = data.tarefas_proximas.filter((t) => {
    const dataEntrega = new Date(t.data_entrega);
    const diff = (dataEntrega - hoje) / (1000 * 60 * 60 * 24);
    return diff <= 3;
  });

  const badgeUrgentes = document.getElementById("tarefas-urgentes");
  badgeUrgentes.textContent = `${urgentes.length} Urgentes`;

  // Atualizar tooltip do badge de urgentes
  if (urgentes.length > 0) {
    const urgentesInfo = urgentes
      .map(t => {
        const dataEntrega = new Date(t.data_entrega);
        const diff = Math.ceil((dataEntrega - hoje) / (1000 * 60 * 60 * 24));
        const diasTexto = diff === 0 ? 'HOJE' : diff === 1 ? 'AMANHÃ' : `em ${diff} dias`;
        return `• ${t.titulo} - ${diasTexto}`;
      })
      .join('\n');
    badgeUrgentes.title = `⚠️ TAREFAS URGENTES (próximos 3 dias):\n${urgentesInfo}\n\nClique para ver detalhes`;
    badgeUrgentes.classList.add('badge-danger');
    badgeUrgentes.classList.remove('badge-warning');
  } else {
    badgeUrgentes.title = 'Nenhuma tarefa urgente nos próximos 3 dias';
    badgeUrgentes.classList.remove('badge-danger');
    badgeUrgentes.classList.add('badge-warning');
  }

  // Atualizar tooltip do card com informações das tarefas
  const cardTarefasPendentes = document.getElementById("card-tarefas-pendentes");
  if (cardTarefasPendentes) {
    if (totalPendentes > 0) {
      const tarefasInfo = data.tarefas_proximas
        .slice(0, 3)
        .map(t => `• ${t.titulo} (${formatDate(t.data_entrega)})`)
        .join('\n');
      const maisInfo = totalPendentes > 3 ? `\n... e mais ${totalPendentes - 3} tarefa(s)` : '';
      cardTarefasPendentes.title = `Tarefas Pendentes (próximos 7 dias):\n${tarefasInfo}${maisInfo}\n\nClique para ver todas`;
      cardTarefasPendentes.classList.add('has-pending');
    } else {
      cardTarefasPendentes.title = 'Nenhuma tarefa pendente nos próximos 7 dias';
      cardTarefasPendentes.classList.remove('has-pending');
    }
  }

  // Meta semanal
  document.getElementById("meta-semanal").textContent = `${data.meta_semanal}h`;
  document.getElementById("meta-diaria").textContent = `${data.meta_diaria}h`;

  // Próximos e-fólios
  renderProximosEfolios(data.proximos_efolios);

  // Progresso por disciplina
  renderProgressoDisciplinas(data.progresso_disciplinas);
}

function renderProximosEfolios(efolios) {
  const container = document.getElementById("proximos-efolios");

  if (efolios.length === 0) {
    container.innerHTML =
      '<p style="text-align: center; color: var(--text-secondary);">Nenhum e-fólio próximo</p>';
    return;
  }

  container.innerHTML = efolios
    .map(
      (ef) => `
        <div class="efolio-item">
            <div class="efolio-info">
                <h4>${ef.tipo}</h4>
                <p>${ef.disciplina}</p>
            </div>
            <div class="efolio-meta">
                <span class="efolio-semana">Semana ${ef.semana}</span>
                <div class="efolio-data">${ef.data}</div>
            </div>
        </div>
    `,
    )
    .join("");
}

function renderProgressoDisciplinas(progresso) {
  const container = document.getElementById("progresso-disciplinas");

  const entries = Object.entries(progresso);
  if (entries.length === 0) {
    container.innerHTML =
      '<p style="text-align: center; color: var(--text-secondary);">Nenhum progresso registrado ainda</p>';
    return;
  }

  container.innerHTML = entries
    .map(
      ([sigla, disc]) => `
        <div class="progress-item">
            <div class="progress-color" style="background: ${disc.cor};"></div>
            <div class="progress-details">
                <div class="progress-header">
                    <h4>${disc.nome}</h4>
                    <span class="progress-percent">${Math.round(disc.progresso)}%</span>
                </div>
                <div class="progress-bar-large">
                    <div class="progress-fill" style="width: ${disc.progresso}%; background: ${disc.cor};"></div>
                </div>
            </div>
        </div>
    `,
    )
    .join("");
}

// ==================== CALENDÁRIO ====================
async function loadCalendario() {
  try {
    const response = await fetch(`${API_URL}/calendario`);
    const data = await response.json();
    currentState.calendario = data;
    currentState.semanaAtual = data.semana_atual || 1;

    renderCalendario(data);
    renderPlanoTrabalho(currentState.semanaAtual);
  } catch (error) {
    console.error("Erro ao carregar calendário:", error);
  }
}

function renderCalendario(data) {
  const container = document.getElementById("calendario-grid");
  const diasSemana = [
    "segunda",
    "terca",
    "quarta",
    "quinta",
    "sexta",
    "sabado",
    "domingo",
  ];
  const diasNomes = [
    "Segunda-feira",
    "Terça-feira",
    "Quarta-feira",
    "Quinta-feira",
    "Sexta-feira",
    "Sábado",
    "Domingo",
  ];

  container.innerHTML = diasSemana
    .map((dia, index) => {
      const diaData = data.calendario_semanal[dia];
      if (!diaData) return "";

      return `
            <div class="dia-card">
                <div class="dia-header">
                    <div class="dia-nome">${diasNomes[index]}</div>
                    <div class="dia-horario">${diaData.horario}</div>
                </div>
                <div class="dia-slots">
                    ${diaData.distribuicao.map((slot) => renderSlot(slot)).join("")}
                </div>
            </div>
        `;
    })
    .join("");
}

function renderSlot(slot) {
  if (slot.tipo === "pausa") {
    return `
            <div class="slot-item slot-pausa" style="border-left-color: #e2e8f0;">
                <div class="slot-time">${slot.inicio} - ${slot.fim}</div>
                <div class="slot-disciplina">
                    <strong>☕ Pausa</strong>
                    <span>Descanso e intervalo</span>
                </div>
            </div>
        `;
  }

  const disciplina = currentState.disciplinas.find(
    (d) => d.sigla === slot.disciplina,
  );
  const cor = disciplina ? disciplina.cor : "#667eea";
  const tipo = slot.tipo === "projeto" ? " (Projeto)" : "";

  let nome = slot.disciplina;
  if (slot.disciplina === "REVISAO") {
    nome = "Revisão Geral";
  } else if (slot.disciplina === "E_FOLIOS") {
    nome = "Preparação e-Fólios";
  } else if (disciplina) {
    nome = disciplina.nome;
  }

  return `
        <div class="slot-item" style="border-left-color: ${cor};">
            <div class="slot-time">${slot.inicio} - ${slot.fim}</div>
            <div class="slot-disciplina">
                <strong>${nome}${tipo}</strong>
                <span>${slot.disciplina}</span>
            </div>
        </div>
    `;
}

// ==================== PLANO DE TRABALHO ====================
function renderPlanoTrabalho(semana) {
  const container = document.getElementById("plano-trabalho-grid");
  const semanaNumero = document.getElementById("semana-numero");

  if (semanaNumero) {
    semanaNumero.textContent = semana;
  }

  // Coletar todas as atividades da semana de todas as disciplinas
  const atividadesSemana = [];

  currentState.disciplinas.forEach(disciplina => {
    if (disciplina.plano_trabalho && disciplina.plano_trabalho.semanas) {
      const atividades = disciplina.plano_trabalho.semanas.filter(s => s.numero === semana);
      atividades.forEach(atividade => {
        atividadesSemana.push({
          ...atividade,
          disciplina: disciplina.sigla,
          disciplinaNome: disciplina.nome,
          cor: disciplina.cor
        });
      });
    }
  });

  if (atividadesSemana.length === 0) {
    container.innerHTML = `
      <div class="plano-empty">
        <i class="fas fa-calendar-times"></i>
        <p>Nenhuma atividade planejada para esta semana</p>
      </div>
    `;
    return;
  }

  // Ordenar por data
  atividadesSemana.sort((a, b) => {
    const dateA = parsePortugueseDate(a.data);
    const dateB = parsePortugueseDate(b.data);
    return dateA - dateB;
  });

  container.innerHTML = atividadesSemana.map(atividade => `
    <div class="plano-item" style="border-left-color: ${atividade.cor}">
      <div class="plano-header">
        <div class="plano-disciplina">
          <span class="plano-disciplina-badge" style="background-color: ${atividade.cor}"></span>
          ${atividade.disciplina}
        </div>
        <div class="plano-data">
          <i class="fas fa-calendar-day"></i>
          ${atividade.data}
        </div>
      </div>
      <div class="plano-topico">
        <i class="fas fa-book-open"></i>
        ${atividade.topico}
      </div>
      <div class="plano-atividades">
        ${atividade.atividades}
      </div>
    </div>
  `).join('');
}

function mudarSemana(direcao) {
  currentState.semanaAtual += direcao;

  // Limitar entre 1 e 14 semanas
  if (currentState.semanaAtual < 1) {
    currentState.semanaAtual = 1;
  } else if (currentState.semanaAtual > 14) {
    currentState.semanaAtual = 14;
  }

  renderPlanoTrabalho(currentState.semanaAtual);
}

function parsePortugueseDate(dateStr) {
  // Converte "06 de outubro de 2025" para Date
  const meses = {
    'janeiro': 0, 'fevereiro': 1, 'março': 2, 'abril': 3,
    'maio': 4, 'junho': 5, 'julho': 6, 'agosto': 7,
    'setembro': 8, 'outubro': 9, 'novembro': 10, 'dezembro': 11
  };

  const parts = dateStr.toLowerCase().split(' de ');
  if (parts.length === 3) {
    const dia = parseInt(parts[0]);
    const mes = meses[parts[1]];
    const ano = parseInt(parts[2]);
    return new Date(ano, mes, dia);
  }
  return new Date();
}

// ==================== DISCIPLINAS ====================
async function loadDisciplinas() {
  try {
    const response = await fetch(`${API_URL}/disciplinas`);
    const data = await response.json();
    currentState.disciplinas = data;

    await renderDisciplinas(data);
    populateDisciplinaSelects(data);
  } catch (error) {
    console.error("Erro ao carregar disciplinas:", error);
  }
}

async function renderDisciplinas(disciplinas) {
  const container = document.getElementById("disciplinas-list");

  // Buscar todas as sessões de uma vez
  const sessoesPromises = disciplinas.map(async (disc) => {
    try {
      const response = await fetch(
        `${API_URL}/sessoes?disciplina_id=${disc.id}`,
      );
      if (response.ok) {
        const sessoes = await response.json();
        return { disciplinaId: disc.id, sessoes };
      }
    } catch (error) {
      console.error(`Erro ao buscar sessões para ${disc.id}:`, error);
    }
    return { disciplinaId: disc.id, sessoes: [] };
  });

  const sessoesResults = await Promise.all(sessoesPromises);
  const sessoesMap = {};
  sessoesResults.forEach((result) => {
    sessoesMap[result.disciplinaId] = result.sessoes;
  });

  // Buscar todas as tarefas para calcular progresso de AFs
  let todasTarefas = [];
  try {
    const response = await fetch(`${API_URL}/tarefas`);
    if (response.ok) {
      todasTarefas = await response.json();
    }
  } catch (error) {
    console.error("Erro ao buscar tarefas:", error);
  }

  // Criar mapa de AFs por disciplina
  const afsMap = {};
  disciplinas.forEach(disc => {
    const afs = todasTarefas.filter(t => t.disciplina_id === disc.id && t.tipo === 'forum');
    const afsConcluidas = afs.filter(t => t.concluida);
    afsMap[disc.id] = {
      total: afs.length,
      concluidas: afsConcluidas.length,
      progresso: afs.length > 0 ? (afsConcluidas.length / afs.length) * 100 : 0
    };
  });

  // Agrupar disciplinas por ano
  const disciplinasPorAno = {
    "1º ano": disciplinas.filter((d) => d.ano === "1º ano"),
    "2º ano": disciplinas.filter((d) => d.ano === "2º ano"),
  };

  let html = "";

  // Criar HTML para cada ano
  Object.entries(disciplinasPorAno).forEach(([ano, discs], anoIndex) => {
    if (discs.length === 0) return;

    html += `
      <div class="year-section" data-year="${ano}" style="animation-delay: ${anoIndex * 0.2}s;">
        <div class="year-header">
          <div class="year-badge">
            <span class="year-number">${ano.split("º")[0]}</span>
            <span class="year-label">ANO</span>
          </div>
          <h2 class="year-title">${ano}</h2>
          <div class="year-stats">
            <span class="year-stat">
              <i class="fas fa-book"></i>
              ${discs.length} Disciplinas
            </span>
            <span class="year-stat">
              <i class="fas fa-award"></i>
              ${discs.reduce((sum, d) => sum + d.creditos, 0)} ECTS
            </span>
          </div>
        </div>
        <div class="disciplinas-grid-modern">
    `;

    discs.forEach((disc, index) => {
      const totalTopicos = disc.topicos ? disc.topicos.length : 0;
      const efolios = disc.e_folios
        ? disc.e_folios.length
        : disc.avaliacoes
          ? disc.avaliacoes.length
          : 0;

      // Usar progresso do backend (sincronizado com Dashboard)
      const progresso = disc.progresso || 0;

      // Obter informações de sessões e AFs
      const sessoesDisciplina = sessoesMap[disc.id] || [];
      const totalPomodoros = sessoesDisciplina.length;
      const afsInfo = afsMap[disc.id] || { total: 0, concluidas: 0, progresso: 0 };

      html += `
        <div class="disciplina-card-modern"
             data-disciplina-id="${disc.id}"
             onclick="showDisciplinaModal('${disc.id}')"
             style="--disc-color: ${disc.cor};
                    --disc-index: ${index};
                    --disc-total: ${discs.length};
                    animation-delay: ${index * 0.1 + anoIndex * 0.3}s;">

          <div class="card-glow" style="background: ${disc.cor};"></div>
          <div class="card-shine"></div>

          <div class="card-header-modern">
            <div class="sigla-badge" style="background: ${disc.cor};">
              <span class="sigla-text">${disc.sigla}</span>
              <div class="sigla-particles"></div>
            </div>
            <div class="creditos-badge">
              ${disc.creditos} <span>ECTS</span>
            </div>
          </div>

          <div class="card-body-modern">
            <h3 class="disciplina-nome-modern">${disc.nome}</h3>

            ${
              progresso > 0
                ? `
            <div class="progresso-wrapper">
              <div class="progresso-label">
                <span>Progresso de Estudo</span>
                <span class="progresso-percent">${Math.round(progresso)}%</span>
              </div>
              <div class="progresso-bar-outer">
                <div class="progresso-bar-inner" style="width: ${progresso}%; background: ${disc.cor};">
                  <div class="progresso-shimmer"></div>
                </div>
              </div>
            </div>
            `
                : ""
            }

            <div class="stats-grid-modern">
              <div class="stat-item-modern">
                <div class="stat-icon" style="background: ${disc.cor}20; color: ${disc.cor};">
                  <i class="fas fa-book-open"></i>
                </div>
                <div class="stat-content">
                  <span class="stat-value">${totalTopicos}</span>
                  <span class="stat-label">Tópicos</span>
                </div>
              </div>

              <div class="stat-item-modern">
                <div class="stat-icon" style="background: ${disc.cor}20; color: ${disc.cor};">
                  <i class="fas fa-clipboard-list"></i>
                </div>
                <div class="stat-content">
                  <span class="stat-value">${efolios}</span>
                  <span class="stat-label">Avaliações</span>
                </div>
              </div>

              ${
                totalPomodoros > 0
                  ? `
              <div class="stat-item-modern highlight">
                <div class="stat-icon" style="background: linear-gradient(135deg, #48bb78, #38a169); color: white;">
                  <i class="fas fa-fire"></i>
                </div>
                <div class="stat-content">
                  <span class="stat-value">${totalPomodoros}</span>
                  <span class="stat-label">Pomodoros</span>
                </div>
                <div class="stat-pulse"></div>
              </div>
              `
                  : ""
              }

              ${
                afsInfo.total > 0
                  ? `
              <div class="stat-item-modern ${afsInfo.concluidas === afsInfo.total ? 'highlight' : ''}">
                <div class="stat-icon" style="background: ${afsInfo.concluidas === afsInfo.total ? 'linear-gradient(135deg, #48bb78, #38a169)' : disc.cor + '20'}; color: ${afsInfo.concluidas === afsInfo.total ? 'white' : disc.cor};">
                  <i class="fas fa-comments"></i>
                </div>
                <div class="stat-content">
                  <span class="stat-value">${afsInfo.concluidas}/${afsInfo.total}</span>
                  <span class="stat-label">AFs</span>
                </div>
                ${afsInfo.concluidas === afsInfo.total ? '<div class="stat-pulse"></div>' : ''}
              </div>
              `
                  : ""
              }
            </div>

            ${
              sessoesDisciplina.length > 0 && sessoesDisciplina[0].topico
                ? `
            <div class="last-session">
              <i class="fas fa-history"></i>
              <span>Último estudo: <strong>${sessoesDisciplina[0].topico}</strong></span>
            </div>
            `
                : ""
            }
          </div>

          <div class="card-footer-modern">
            <button class="btn-action-modern" onclick="event.stopPropagation(); window.location.href='admin-folders.html';">
              <i class="fas fa-sync"></i>
              <span>Sincronizar</span>
            </button>
            <button class="btn-action-modern primary" onclick="event.stopPropagation(); showDisciplinaModal('${disc.id}');">
              <i class="fas fa-arrow-right"></i>
              <span>Ver Detalhes</span>
            </button>
          </div>

          <div class="card-corners">
            <span class="corner top-left"></span>
            <span class="corner top-right"></span>
            <span class="corner bottom-left"></span>
            <span class="corner bottom-right"></span>
          </div>
        </div>
      `;
    });

    html += `
        </div>
      </div>
    `;
  });

  container.innerHTML = html;

  // Aplicar animações e efeitos após renderização
  setTimeout(() => {
    initModernDisciplinasEffects();
  }, 100);
}

// Função para inicializar efeitos modernos nas disciplinas
function initModernDisciplinasEffects() {
  const cards = document.querySelectorAll(".disciplina-card-modern");

  cards.forEach((card, index) => {
    // Efeito 3D no hover
    card.addEventListener("mousemove", (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      const rotateX = (y - centerY) / 10;
      const rotateY = (centerX - x) / 10;

      card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.05)`;

      // Mover o brilho
      const shine = card.querySelector(".card-shine");
      if (shine) {
        shine.style.left = `${x}px`;
        shine.style.top = `${y}px`;
      }
    });

    card.addEventListener("mouseleave", () => {
      card.style.transform =
        "perspective(1000px) rotateX(0) rotateY(0) scale(1)";
    });

    // Adicionar partículas ao badge
    const siglaParticles = card.querySelector(".sigla-particles");
    if (siglaParticles) {
      for (let i = 0; i < 5; i++) {
        const particle = document.createElement("div");
        particle.className = "particle";
        particle.style.animationDelay = `${i * 0.2}s`;
        siglaParticles.appendChild(particle);
      }
    }

    // Animação de entrada com observer
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1 },
    );

    observer.observe(card);
  });

  // Efeito parallax nos year headers
  const yearSections = document.querySelectorAll(".year-section");
  window.addEventListener("scroll", () => {
    yearSections.forEach((section) => {
      const rect = section.getBoundingClientRect();
      const scrollPercent =
        (window.innerHeight - rect.top) / window.innerHeight;

      if (scrollPercent > 0 && scrollPercent < 1) {
        const header = section.querySelector(".year-header");
        if (header) {
          header.style.transform = `translateY(${scrollPercent * -20}px)`;
        }
      }
    });
  });

  // Adicionar efeito de hover nos stats
  document.querySelectorAll(".stat-item-modern").forEach((stat) => {
    stat.addEventListener("mouseenter", function () {
      this.style.transform = "translateY(-5px) scale(1.05)";
    });

    stat.addEventListener("mouseleave", function () {
      this.style.transform = "translateY(0) scale(1)";
    });
  });
}

async function showDisciplinaModal(disciplinaId) {
  const disciplina = currentState.disciplinas.find(
    (d) => d.id === disciplinaId,
  );
  if (!disciplina) return;

  const modal = document.getElementById("modal-disciplina");
  const modalBody = document.getElementById("modal-disciplina-body");
  const modalNome = document.getElementById("modal-disciplina-nome");

  modalNome.textContent = disciplina.nome;

  // Buscar sessões de estudo para esta disciplina
  let sessoesDisciplina = [];
  try {
    const response = await fetch(
      `${API_URL}/sessoes?disciplina_id=${disciplinaId}`,
    );
    if (response.ok) {
      sessoesDisciplina = await response.json();
    }
  } catch (error) {
    console.error("Erro ao buscar sessões:", error);
  }

  // Buscar tarefas da disciplina (incluindo AFs)
  let tarefasDisciplina = [];
  try {
    const response = await fetch(`${API_URL}/tarefas`);
    if (response.ok) {
      const todasTarefas = await response.json();
      tarefasDisciplina = todasTarefas.filter(t => t.disciplina_id === disciplinaId);
    }
  } catch (error) {
    console.error("Erro ao buscar tarefas:", error);
  }

  // Buscar arquivos/materiais da disciplina do banco de dados
  let materiaisDB = [];
  try {
    const response = await fetch(`${API_URL}/folders/files/${disciplinaId}`);
    if (response.ok) {
      const data = await response.json();
      if (data.success) {
        materiaisDB = data.files;
      }
    }
  } catch (error) {
    console.error("Erro ao buscar materiais:", error);
  }

  // Calcular estatísticas gerais
  const totalPomodoros = sessoesDisciplina.length;
  const totalMinutos = totalPomodoros * 25;
  const totalHoras = Math.floor(totalMinutos / 60);
  const minutosRestantes = totalMinutos % 60;

  // Obter tópicos únicos estudados
  const topicosEstudados = [
    ...new Set(sessoesDisciplina.filter((s) => s.topico).map((s) => s.topico)),
  ];

  let html = `
        <div style="margin-bottom: 2rem;">
            <span class="badge" style="background: ${disciplina.cor}; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 1rem;">
                ${disciplina.sigla}
            </span>
            <p style="margin-top: 1rem; color: var(--text-secondary);">
                ${disciplina.creditos} ECTS • ${disciplina.tipo}
            </p>
        </div>

        <!-- Resumo de Pomodoros -->
        ${
          totalPomodoros > 0
            ? `
            <div style="background: var(--bg-tertiary);
                        border: 1px solid var(--border-color);
                        border-radius: 12px;
                        padding: 1.25rem;
                        margin-bottom: 2rem;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem;">
                    <div style="text-align: center;">
                        <i class="fas fa-clock" style="color: var(--success-color); font-size: 1.5rem;"></i>
                        <h4 style="color: var(--primary-color); margin: 0.5rem 0 0.25rem; font-size: 1.5rem;">${totalPomodoros}</h4>
                        <p style="color: var(--text-secondary); font-size: 0.85rem;">Pomodoro${totalPomodoros > 1 ? "s" : ""} Realizado${totalPomodoros > 1 ? "s" : ""}</p>
                    </div>
                    <div style="text-align: center;">
                        <i class="fas fa-hourglass-half" style="color: var(--success-color); font-size: 1.5rem;"></i>
                        <h4 style="color: var(--primary-color); margin: 0.5rem 0 0.25rem; font-size: 1.5rem;">${totalHoras}h ${minutosRestantes}min</h4>
                        <p style="color: var(--text-secondary); font-size: 0.85rem;">Tempo Total Estudado</p>
                    </div>
                    <div style="text-align: center;">
                        <i class="fas fa-book-open" style="color: var(--success-color); font-size: 1.5rem;"></i>
                        <h4 style="color: var(--primary-color); margin: 0.5rem 0 0.25rem; font-size: 1.5rem;">${topicosEstudados.length}</h4>
                        <p style="color: var(--text-secondary); font-size: 0.85rem;">Tópicos Diferentes</p>
                    </div>
                </div>
                ${
                  sessoesDisciplina.length > 0
                    ? `
                    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border-color);">
                        <p style="color: var(--text-primary); font-size: 0.85rem; display: flex; align-items: center; gap: 0.5rem;">
                            <i class="fas fa-history" style="color: var(--success-color);"></i>
                            <span>
                                Última sessão: <strong>${sessoesDisciplina[0].topico || "Estudo geral"}</strong>
                                em ${new Date(
                                  sessoesDisciplina[0].data,
                                ).toLocaleDateString("pt-BR", {
                                  day: "2-digit",
                                  month: "2-digit",
                                  year: "numeric",
                                })}
                            </span>
                        </p>
                    </div>
                `
                    : ""
                }
                <div style="margin-top: 1rem; text-align: center;">
                    <button onclick="showAllPomodoros('${disciplinaId}')"
                            style="padding: 0.5rem 1rem;
                                   background: var(--success-color);
                                   color: white;
                                   border: none;
                                   border-radius: 8px;
                                   cursor: pointer;
                                   font-size: 0.9rem;
                                   transition: all 0.3s ease;">
                        <i class="fas fa-list"></i> Ver Todos os Pomodoros
                    </button>
                </div>
            </div>
        `
            : `
            <div style="background: var(--bg-tertiary);
                        border: 1px solid var(--border-color);
                        border-radius: 12px;
                        padding: 1.5rem;
                        margin-bottom: 2rem;
                        text-align: center;">
                <i class="fas fa-info-circle" style="color: var(--text-secondary); font-size: 2rem; margin-bottom: 1rem;"></i>
                <p style="color: var(--text-primary); margin-bottom: 1rem;">Ainda não há sessões de estudo registradas para esta disciplina</p>
                <p style="color: var(--text-secondary); font-size: 0.85rem;">Use o Timer Pomodoro para registrar suas sessões de estudo!</p>
            </div>
        `
        }
    `;

  // Tópicos
  if (disciplina.topicos && disciplina.topicos.length > 0) {
    html +=
      '<h3 style="margin-bottom: 1rem;"><i class="fas fa-list"></i> Tópicos</h3>';
    html += '<div style="display: grid; gap: 1rem; margin-bottom: 2rem;">';
    disciplina.topicos.forEach((topico) => {
      // Filtrar sessões relacionadas a este tópico
      const sessoesTopico = sessoesDisciplina.filter(
        (s) =>
          s.topico &&
          (s.topico.toLowerCase().includes(topico.titulo.toLowerCase()) ||
            s.topico.toLowerCase().includes(`tópico ${topico.numero}`) ||
            s.topico.toLowerCase().includes(`topico ${topico.numero}`)),
      );

      html += `
                <div style="padding: 1rem; background: var(--bg-tertiary); border-radius: 8px; border-left: 4px solid ${disciplina.cor};">
                    <strong style="color: var(--text-primary);">Tópico ${topico.numero}: ${topico.titulo}</strong>
                    <p style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 0.5rem;">
                        Semanas ${topico.semanas.join(", ")} • ${topico.carga_horaria}h
                    </p>
                    ${
                      topico.atividades
                        ? `
                        <ul style="margin-top: 0.5rem; font-size: 0.9rem; color: var(--text-secondary);">
                            ${topico.atividades.map((at) => `<li>${at}</li>`).join("")}
                        </ul>
                    `
                        : ""
                    }
                    ${
                      sessoesTopico.length > 0
                        ? `
                        <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border-color);">
                            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                                <i class="fas fa-clock" style="color: var(--success-color);"></i>
                                <strong style="color: var(--success-color);">${sessoesTopico.length} Pomodoro${sessoesTopico.length > 1 ? "s" : ""} realizado${sessoesTopico.length > 1 ? "s" : ""}</strong>
                            </div>
                            <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                                ${sessoesTopico
                                  .slice(0, 3)
                                  .map((s) => {
                                    const data = new Date(s.data);
                                    const dataFormatada =
                                      data.toLocaleDateString("pt-BR", {
                                        day: "2-digit",
                                        month: "2-digit",
                                      });
                                    return `
                                    <div style="padding: 0.5rem; background: var(--bg-elevated); border-radius: 6px; font-size: 0.85rem; border-left: 2px solid var(--success-color);">
                                        <div style="display: flex; justify-content: space-between; align-items: center;">
                                            <span style="color: var(--text-primary); font-weight: 500;">
                                                ${s.topico || "Sessão de estudo"}
                                            </span>
                                            <span style="color: var(--text-secondary); font-size: 0.8rem;">
                                                ${dataFormatada} às ${s.hora_inicio}
                                            </span>
                                        </div>
                                        ${s.notas ? `<p style="color: var(--text-secondary); margin-top: 0.25rem; font-size: 0.8rem;">${s.notas}</p>` : ""}
                                    </div>
                                  `;
                                  })
                                  .join("")}
                                ${
                                  sessoesTopico.length > 3
                                    ? `
                                    <p style="text-align: center; color: var(--text-secondary); font-size: 0.85rem; margin-top: 0.5rem;">
                                        + ${sessoesTopico.length - 3} pomodoro${sessoesTopico.length - 3 > 1 ? "s" : ""} anterior${sessoesTopico.length - 3 > 1 ? "es" : ""}
                                    </p>
                                `
                                    : ""
                                }
                            </div>
                        </div>
                    `
                        : `
                        <div style="margin-top: 1rem; padding: 0.5rem; background: var(--bg-elevated); border-radius: 6px; font-size: 0.85rem; color: var(--text-secondary); text-align: center;">
                            <i class="fas fa-info-circle"></i> Nenhum Pomodoro registrado ainda
                        </div>
                    `
                    }
                </div>
            `;
    });
    html += "</div>";
  }

  // Plano de Trabalho
  if (disciplina.plano_trabalho && disciplina.plano_trabalho.semanas && disciplina.plano_trabalho.semanas.length > 0) {
    html += `
      <h3 style="margin-bottom: 1rem;">
        <i class="fas fa-calendar-check"></i> Plano de Trabalho
        <span style="float: right; font-size: 0.85rem; color: var(--text-secondary);">
          ${disciplina.plano_trabalho.semanas.length} semanas
        </span>
      </h3>
      <div style="display: grid; gap: 0.75rem; margin-bottom: 2rem;">
    `;

    disciplina.plano_trabalho.semanas.forEach((semana) => {
      html += `
        <div style="padding: 1rem;
                    background: var(--bg-tertiary);
                    border-radius: 8px;
                    border-left: 4px solid ${disciplina.cor};
                    transition: all 0.3s ease;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <strong style="color: var(--primary-color);">
              <i class="fas fa-calendar-week"></i> Semana ${semana.numero}
            </strong>
            <span style="color: var(--text-secondary); font-size: 0.85rem;">
              <i class="fas fa-calendar-day"></i> ${semana.data}
            </span>
          </div>
          <div style="color: var(--secondary-color); font-size: 0.9rem; margin-bottom: 0.5rem;">
            <i class="fas fa-book-open"></i> ${semana.topico}
          </div>
          <p style="color: var(--text-primary); font-size: 0.9rem; line-height: 1.5; padding-left: 1rem; border-left: 2px solid var(--border-color);">
            ${semana.atividades}
          </p>
        </div>
      `;
    });

    html += "</div>";
  }

  // e-Fólios
  if (disciplina.e_folios && disciplina.e_folios.length > 0) {
    html +=
      '<h3 style="margin-bottom: 1rem;"><i class="fas fa-clipboard-list"></i> e-Fólios</h3>';
    html += '<div style="display: grid; gap: 1rem; margin-bottom: 2rem;">';
    disciplina.e_folios.forEach((ef) => {
      html += `
                <div style="padding: 1rem; background: var(--bg-tertiary); border-radius: 8px; border-left: 4px solid var(--secondary-color);">
                    <strong style="color: var(--text-primary);">${ef.tipo}</strong>
                    <p style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 0.5rem;">
                        Semana ${ef.semana} • ${ef.data || ef.data_inicio} • Peso: ${ef.peso}%
                    </p>
                    ${ef.descricao ? `<p style="color: var(--text-primary); font-size: 0.9rem; margin-top: 0.5rem;">${ef.descricao}</p>` : ""}
                </div>
            `;
    });
    html += "</div>";
  }

  // Sessões Síncronas
  if (disciplina.sessoes_sincronas && disciplina.sessoes_sincronas.length > 0) {
    html +=
      '<h3 style="margin-bottom: 1rem;"><i class="fas fa-video"></i> Sessões Síncronas</h3>';
    html += '<div style="display: grid; gap: 1rem; margin-bottom: 2rem;">';
    disciplina.sessoes_sincronas.forEach((ss) => {
      html += `
                <div style="padding: 1rem; background: var(--bg-tertiary); border-radius: 8px; border-left: 4px solid var(--warning-color);">
                    <strong style="color: var(--text-primary);">${ss.dia_semana}, ${ss.data}</strong>
                    <p style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 0.5rem;">
                        Horário: ${ss.horario}
                    </p>
                </div>
            `;
    });
    html += "</div>";
  }

  // Atividades Formativas (AFs)
  const afs = tarefasDisciplina.filter(t => t.tipo === 'forum');
  if (afs.length > 0) {
    const afsConcluidas = afs.filter(t => t.concluida);
    const afsPendentes = afs.filter(t => !t.concluida);
    const progressoAFs = afs.length > 0 ? Math.round((afsConcluidas.length / afs.length) * 100) : 0;

    html += `
      <h3 style="margin-bottom: 1rem; color: var(--text-primary);">
        <i class="fas fa-comments"></i> Atividades Formativas (AF)
        <span style="float: right; font-size: 0.85rem; color: ${progressoAFs === 100 ? 'var(--success-color)' : 'var(--text-secondary)'};">
          ${afsConcluidas.length}/${afs.length} concluídas (${progressoAFs}%)
        </span>
      </h3>
      <div style="display: grid; gap: 1rem; margin-bottom: 2rem;">
    `;

    afs.forEach((af) => {
      const statusColor = af.concluida ? 'var(--success-color)' : 'var(--error-color)';
      const statusIcon = af.concluida ? 'fa-check-circle' : 'fa-clock';
      const statusText = af.concluida ? 'Concluída' : 'Pendente';
      const bgColor = af.concluida ? 'var(--bg-elevated)' : 'var(--bg-elevated)';

      html += `
        <div style="padding: 1rem; background: ${bgColor}; border-radius: 8px; border-left: 4px solid ${statusColor};">
          <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
            <strong style="color: var(--text-primary);">${af.titulo}</strong>
            <span style="display: inline-flex; align-items: center; gap: 0.25rem; padding: 0.25rem 0.75rem; background: ${statusColor}; color: white; border-radius: 12px; font-size: 0.75rem; font-weight: 600;">
              <i class="fas ${statusIcon}"></i> ${statusText}
            </span>
          </div>
          ${af.descricao ? `<p style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 0.5rem;">${af.descricao}</p>` : ''}
          ${af.data_entrega ? `
            <p style="color: var(--text-secondary); font-size: 0.85rem; margin-top: 0.5rem;">
              <i class="fas fa-calendar"></i> Entrega: ${formatDate(af.data_entrega)}
            </p>
          ` : ''}
        </div>
      `;
    });

    html += "</div>";
  }

  // Materiais - Priorizar materiais do banco de dados
  // Filtrar arquivos temporários
  const materiaisFiltrados = materiaisDB.filter((arquivo) => {
    const extensoesTemporarias = [
      ".crdownload",
      ".tmp",
      ".temp",
      ".download",
      ".part",
    ];
    return !extensoesTemporarias.includes(arquivo.tipo);
  });

  if (materiaisFiltrados.length > 0) {
    const totalTamanho = materiaisFiltrados.reduce(
      (acc, f) => acc + f.tamanho,
      0,
    );
    html +=
      '<h3 style="margin-bottom: 1rem; color: var(--text-primary);"><i class="fas fa-folder-open"></i> Materiais Sincronizados</h3>';
    html += `
      <div style="background: var(--bg-tertiary);
                  padding: 1rem;
                  border-radius: 8px;
                  border: 1px solid var(--border-color);
                  margin-bottom: 1rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
          <p style="color: var(--text-primary); font-size: 0.85rem; margin: 0;">
            <i class="fas fa-info-circle" style="color: var(--primary-color);"></i>
            <strong>${materiaisFiltrados.length}</strong> arquivos sincronizados
          </p>
          <p style="color: var(--text-secondary); font-size: 0.85rem; margin: 0;">
            <i class="fas fa-hdd" style="color: var(--primary-color);"></i>
            ${formatFileSize(totalTamanho)}
          </p>
        </div>
        <button onclick="resyncDisciplinaMaterials('${disciplinaId}', '${disciplina.nome}')"
                style="width: 100%;
                       padding: 0.5rem;
                       background: var(--primary-color);
                       color: white;
                       border: none;
                       border-radius: 6px;
                       cursor: pointer;
                       font-size: 0.85rem;
                       transition: all 0.3s ease;"
                onmouseover="this.style.transform='translateY(-1px)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.2)';"
                onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
          <i class="fas fa-sync"></i> Resincronizar Arquivos
        </button>
      </div>
    `;
    html +=
      '<div style="display: grid; gap: 0.5rem;" id="materiais-list-${disciplinaId}">';

    materiaisFiltrados.forEach((arquivo) => {
      const tamanho = formatFileSize(arquivo.tamanho);
      const data = new Date(arquivo.data_modificacao);
      const dataFormatada = data.toLocaleDateString("pt-BR", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
      });

      // Ícone baseado no tipo de arquivo
      let icone = "fa-file";
      if (arquivo.tipo === ".pdf") icone = "fa-file-pdf";
      else if ([".doc", ".docx"].includes(arquivo.tipo)) icone = "fa-file-word";
      else if ([".xls", ".xlsx"].includes(arquivo.tipo))
        icone = "fa-file-excel";
      else if ([".ppt", ".pptx"].includes(arquivo.tipo))
        icone = "fa-file-powerpoint";
      else if ([".jpg", ".jpeg", ".png", ".gif"].includes(arquivo.tipo))
        icone = "fa-file-image";
      else if ([".zip", ".rar", ".7z"].includes(arquivo.tipo))
        icone = "fa-file-archive";
      else if ([".mp4", ".avi", ".mov"].includes(arquivo.tipo))
        icone = "fa-file-video";

      const caminhoEncoded = arquivo.caminho_completo.replace(/\//g, "|");

      html += `
        <div style="padding: 0.75rem;
                    background: white;
                    border-radius: 6px;
                    border: 1px solid #e2e8f0;
                    cursor: pointer;
                    transition: all 0.3s ease;"
             onmouseover="this.style.boxShadow='0 2px 8px rgba(0,0,0,0.1)'; this.style.transform='translateX(2px)';"
             onmouseout="this.style.boxShadow='none'; this.style.transform='translateX(0)';"
             onclick="openLocalFile('${caminhoEncoded}')">
          <div style="display: flex; align-items: center; gap: 0.75rem;">
            <i class="fas ${icone}" style="color: ${disciplina.cor}; font-size: 1.5rem;"></i>
            <div style="flex: 1;">
              <div style="font-weight: 500; color: #2d3748; margin-bottom: 0.25rem;">
                ${arquivo.nome_arquivo}
              </div>
              <div style="font-size: 0.75rem; color: #a0aec0;">
                ${tamanho} • ${dataFormatada}
              </div>
            </div>
            <i class="fas fa-external-link-alt" style="color: #a0aec0;"></i>
          </div>
        </div>
      `;
    });

    html += "</div></div>";
  } else if (disciplina.materiais && disciplina.materiais.length > 0) {
    // Fallback para materiais estáticos se não houver sincronização
    html +=
      '<h3 style="margin-bottom: 1rem;"><i class="fas fa-file-pdf"></i> Materiais</h3>';
    html +=
      '<div style="background: #fff5e6; padding: 1rem; border-radius: 8px; border-left: 4px solid #f6ad55; margin-bottom: 1rem;">';
    html +=
      '<p style="color: #c05621; font-size: 0.85rem; margin-bottom: 0.5rem;"><i class="fas fa-exclamation-triangle"></i> Configure a sincronização de pasta para acesso direto aos arquivos</p>';
    html += "</div>";
    html += '<ul style="list-style: none; padding: 0;">';
    disciplina.materiais.forEach((mat) => {
      html += `<li style="padding: 0.5rem 0;"><i class="fas fa-file"></i> ${mat}</li>`;
    });
    html += "</ul>";
  } else {
    html += `
      <div style="background: #f7fafc; padding: 2rem; border-radius: 8px; text-align: center; margin-top: 1rem;">
        <i class="fas fa-folder-open" style="font-size: 3rem; color: #cbd5e0; margin-bottom: 1rem;"></i>
        <p style="color: #718096; margin-bottom: 0.5rem;">Nenhum material sincronizado</p>
        <p style="color: #a0aec0; font-size: 0.85rem;">
          Configure a sincronização de pasta em
          <a href="#" onclick="window.location.href='admin-folders.html'; return false;" style="color: ${disciplina.cor}; text-decoration: underline;">
            Sincronizar Arquivos
          </a>
        </p>
      </div>
    `;
  }

  modalBody.innerHTML = html;
  modal.classList.add("active");
}

// Função para mostrar todos os Pomodoros de uma disciplina
async function showAllPomodoros(disciplinaId) {
  const disciplina = currentState.disciplinas.find(
    (d) => d.id === disciplinaId,
  );
  if (!disciplina) return;

  // Buscar todas as sessões desta disciplina
  let sessoes = [];
  try {
    const response = await fetch(
      `${API_URL}/sessoes?disciplina_id=${disciplinaId}`,
    );
    if (response.ok) {
      sessoes = await response.json();
    }
  } catch (error) {
    console.error("Erro ao buscar sessões:", error);
    return;
  }

  // Agrupar sessões por tópico
  const sessoesPorTopico = {};
  const sessoesGerais = [];

  sessoes.forEach((sessao) => {
    if (sessao.topico) {
      if (!sessoesPorTopico[sessao.topico]) {
        sessoesPorTopico[sessao.topico] = [];
      }
      sessoesPorTopico[sessao.topico].push(sessao);
    } else {
      sessoesGerais.push(sessao);
    }
  });

  // Calcular estatísticas
  const totalSessoes = sessoes.length;
  const totalMinutos = totalSessoes * 25;
  const totalHoras = Math.floor(totalMinutos / 60);
  const minutosRestantes = totalMinutos % 60;

  // Criar HTML para o modal
  let html = `
    <div style="max-height: 70vh; overflow-y: auto;">
      <div style="background: linear-gradient(135deg, #48bb78, #38a169);
                  color: white;
                  padding: 1.5rem;
                  border-radius: 12px;
                  margin-bottom: 2rem;">
        <h2 style="margin-bottom: 1rem;">
          <i class="fas fa-clock"></i> Histórico de Pomodoros - ${disciplina.nome}
        </h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 1rem;">
          <div style="text-align: center;">
            <h3 style="font-size: 2rem; margin: 0;">${totalSessoes}</h3>
            <p style="opacity: 0.9; font-size: 0.9rem;">Total de Sessões</p>
          </div>
          <div style="text-align: center;">
            <h3 style="font-size: 2rem; margin: 0;">${totalHoras}h ${minutosRestantes}min</h3>
            <p style="opacity: 0.9; font-size: 0.9rem;">Tempo Total</p>
          </div>
          <div style="text-align: center;">
            <h3 style="font-size: 2rem; margin: 0;">${Object.keys(sessoesPorTopico).length}</h3>
            <p style="opacity: 0.9; font-size: 0.9rem;">Tópicos Estudados</p>
          </div>
        </div>
      </div>
  `;

  // Listar sessões por tópico
  if (Object.keys(sessoesPorTopico).length > 0) {
    html +=
      '<h3 style="margin-bottom: 1rem;"><i class="fas fa-layer-group"></i> Sessões por Tópico</h3>';

    for (const [topico, sessoesList] of Object.entries(sessoesPorTopico)) {
      const totalTopico = sessoesList.length;
      html += `
        <div style="background: #f7fafc;
                    border-left: 4px solid ${disciplina.cor};
                    padding: 1rem;
                    margin-bottom: 1rem;
                    border-radius: 8px;">
          <h4 style="color: ${disciplina.cor}; margin-bottom: 0.5rem;">
            ${topico}
            <span style="float: right;
                         background: ${disciplina.cor};
                         color: white;
                         padding: 0.25rem 0.75rem;
                         border-radius: 12px;
                         font-size: 0.85rem;">
              ${totalTopico} sessão(ões)
            </span>
          </h4>
          <div style="display: grid; gap: 0.5rem; margin-top: 1rem;">
      `;

      sessoesList.slice(0, 5).forEach((sessao) => {
        const data = new Date(sessao.data);
        const dataFormatada = data.toLocaleDateString("pt-BR", {
          day: "2-digit",
          month: "2-digit",
          year: "numeric",
        });

        html += `
          <div style="padding: 0.75rem;
                      background: white;
                      border-radius: 6px;
                      display: flex;
                      justify-content: space-between;
                      align-items: center;">
            <div>
              <i class="fas fa-check-circle" style="color: #48bb78; margin-right: 0.5rem;"></i>
              <span style="color: #4a5568;">${sessao.duracao_minutos} minutos</span>
              ${sessao.notas ? `<p style="color: #718096; font-size: 0.85rem; margin-top: 0.25rem; margin-left: 1.5rem;">${sessao.notas}</p>` : ""}
            </div>
            <span style="color: #a0aec0; font-size: 0.85rem;">
              ${dataFormatada} • ${sessao.hora_inicio}
            </span>
          </div>
        `;
      });

      if (sessoesList.length > 5) {
        html += `
          <p style="text-align: center; color: #718096; font-size: 0.85rem; margin-top: 0.5rem;">
            + ${sessoesList.length - 5} sessão(ões) adicional(is)
          </p>
        `;
      }

      html += "</div></div>";
    }
  }

  // Listar sessões gerais (sem tópico específico)
  if (sessoesGerais.length > 0) {
    html += `
      <h3 style="margin-bottom: 1rem; margin-top: 2rem;">
        <i class="fas fa-book"></i> Sessões de Estudo Geral
      </h3>
      <div style="display: grid; gap: 0.5rem;">
    `;

    sessoesGerais.forEach((sessao) => {
      const data = new Date(sessao.data);
      const dataFormatada = data.toLocaleDateString("pt-BR");

      html += `
        <div style="padding: 0.75rem;
                    background: #f7fafc;
                    border-radius: 6px;
                    display: flex;
                    justify-content: space-between;">
          <span>
            <i class="fas fa-clock" style="color: #48bb78;"></i>
            ${sessao.duracao_minutos} minutos
          </span>
          <span style="color: #718096; font-size: 0.85rem;">
            ${dataFormatada} • ${sessao.hora_inicio}
          </span>
        </div>
      `;
    });

    html += "</div>";
  }

  if (sessoes.length === 0) {
    html += `
      <div style="text-align: center; padding: 3rem;">
        <i class="fas fa-info-circle" style="font-size: 3rem; color: #a0aec0; margin-bottom: 1rem;"></i>
        <p style="color: #718096;">Ainda não há sessões de Pomodoro registradas para esta disciplina.</p>
        <p style="color: #a0aec0; font-size: 0.9rem; margin-top: 0.5rem;">
          Use o Timer Pomodoro para começar a registrar suas sessões de estudo!
        </p>
      </div>
    `;
  }

  html += "</div>";

  // Criar e mostrar o modal
  const existingModal = document.getElementById("modal-pomodoros");
  if (existingModal) {
    existingModal.remove();
  }

  const modal = document.createElement("div");
  modal.id = "modal-pomodoros";
  modal.className = "modal active";
  modal.innerHTML = `
    <div class="modal-content" style="max-width: 800px;">
      <div class="modal-header">
        <h2>Histórico Completo de Pomodoros</h2>
        <button class="modal-close" onclick="this.closest('.modal').remove()">&times;</button>
      </div>
      <div class="modal-body">
        ${html}
      </div>
    </div>
  `;

  document.body.appendChild(modal);

  // Fechar modal ao clicar fora
  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.remove();
    }
  });
}

// Exportar para o escopo global
window.showAllPomodoros = showAllPomodoros;

// Função para formatar tamanho de arquivo
function formatFileSize(bytes) {
  if (bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB", "TB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + " " + sizes[i];
}

// Função para abrir arquivo local
async function openLocalFile(encodedPath) {
  try {
    const response = await fetch(`${API_URL}/folders/open/${encodedPath}`);
    const data = await response.json();

    if (data.success) {
      showToast("📂 Arquivo aberto no aplicativo padrão", "success");
    } else {
      showToast(`❌ Erro ao abrir arquivo: ${data.error}`, "error");
    }
  } catch (error) {
    console.error("Erro ao abrir arquivo:", error);
    showToast("❌ Erro ao abrir arquivo", "error");
  }
}

// Função para resincronizar materiais de uma disciplina
async function resyncDisciplinaMaterials(disciplinaId, disciplinaNome) {
  try {
    showToast(`🔄 Sincronizando materiais de ${disciplinaNome}...`, "info");

    const response = await fetch(`${API_URL}/folders/scan/${disciplinaId}`, {
      method: "POST",
    });

    const data = await response.json();

    if (data.success) {
      showToast(
        `✅ ${data.files_indexed} arquivo(s) sincronizado(s) com sucesso!`,
        "success",
      );

      // Reabrir o modal para mostrar os arquivos atualizados
      await showDisciplinaModal(disciplinaId);
    } else {
      showToast(`❌ Erro ao sincronizar: ${data.error}`, "error");
    }
  } catch (error) {
    console.error("Erro ao resincronizar materiais:", error);
    showToast("❌ Erro ao sincronizar materiais", "error");
  }
}

// Exportar funções para o escopo global
window.openLocalFile = openLocalFile;
window.formatFileSize = formatFileSize;
window.resyncDisciplinaMaterials = resyncDisciplinaMaterials;

function populateDisciplinaSelects(disciplinas) {
  const selects = ["tarefa-disciplina", "timer-disciplina"];

  selects.forEach((selectId) => {
    const select = document.getElementById(selectId);
    if (select) {
      const currentValue = select.value;
      select.innerHTML =
        '<option value="">Selecione...</option>' +
        disciplinas
          .map((d) => `<option value="${d.id}">${d.sigla} - ${d.nome}</option>`)
          .join("");
      if (currentValue) select.value = currentValue;
    }
  });
}

// ==================== TAREFAS ====================
async function loadTarefas(filter = "todas") {
  try {
    let url = `${API_URL}/tarefas`;
    if (filter === "pendentes") url += "?concluida=false";
    if (filter === "concluidas") url += "?concluida=true";

    const response = await fetch(url);
    let tarefas = await response.json();

    // Filtrar por tipo se necessário
    if (
      filter !== "todas" &&
      filter !== "pendentes" &&
      filter !== "concluidas"
    ) {
      tarefas = tarefas.filter((t) => t.tipo === filter);
    }

    currentState.tarefas = tarefas;
    renderTarefas(tarefas);
  } catch (error) {
    console.error("Erro ao carregar tarefas:", error);
  }
}

function renderTarefas(tarefas) {
  const container = document.getElementById("tarefas-list");

  if (tarefas.length === 0) {
    container.innerHTML =
      '<p style="text-align: center; color: var(--text-secondary); padding: 2rem;">Nenhuma tarefa encontrada</p>';
    return;
  }

  // Verificar se estamos mostrando apenas pendentes OU apenas concluídas
  const apenasPendentes = tarefas.every(t => !t.concluida);
  const apenasConcluidas = tarefas.every(t => t.concluida);

  if ((apenasPendentes || apenasConcluidas) && tarefas.length > 0) {
    // Agrupar tarefas por categoria
    const categorias = {
      'sessao-sincrona': {
        titulo: '📹 Sessões Síncronas',
        icon: 'fas fa-video',
        tarefas: []
      },
      'e-folio': {
        titulo: '📝 e-Fólios',
        icon: 'fas fa-clipboard-check',
        tarefas: []
      },
      'forum': {
        titulo: '💬 Atividades Formativas (AF)',
        icon: 'fas fa-comments',
        tarefas: []
      },
      'outras': {
        titulo: '📋 Outras Tarefas',
        icon: 'fas fa-tasks',
        tarefas: []
      }
    };

    // Classificar tarefas por categoria
    tarefas.forEach(tarefa => {
      if (tarefa.tipo === 'sessao-sincrona') {
        categorias['sessao-sincrona'].tarefas.push(tarefa);
      } else if (tarefa.tipo === 'e-folio') {
        categorias['e-folio'].tarefas.push(tarefa);
      } else if (tarefa.tipo === 'forum') {
        categorias['forum'].tarefas.push(tarefa);
      } else {
        categorias['outras'].tarefas.push(tarefa);
      }
    });

    // Ordenar tarefas dentro de cada categoria por data
    Object.values(categorias).forEach(cat => {
      cat.tarefas.sort((a, b) => {
        if (a.data_entrega && b.data_entrega) {
          return new Date(a.data_entrega) - new Date(b.data_entrega);
        }
        return b.prioridade - a.prioridade;
      });
    });

    // Renderizar por categorias
    let html = '';
    Object.entries(categorias).forEach(([key, cat]) => {
      if (cat.tarefas.length > 0) {
        html += `
          <div class="tarefas-categoria">
            <h3 class="categoria-titulo">
              <i class="${cat.icon}"></i>
              ${cat.titulo}
              <span class="categoria-count">${cat.tarefas.length}</span>
            </h3>
            <div class="categoria-tarefas">
              ${cat.tarefas.map(tarefa => renderTarefaItem(tarefa)).join('')}
            </div>
          </div>
        `;
      }
    });

    container.innerHTML = html;
  } else {
    // Renderização normal (todas ou concluídas)
    tarefas.sort((a, b) => {
      if (a.concluida !== b.concluida) return a.concluida ? 1 : -1;
      if (a.data_entrega && b.data_entrega) {
        const dateA = new Date(a.data_entrega);
        const dateB = new Date(b.data_entrega);
        if (dateA - dateB !== 0) return dateA - dateB;
      }
      return b.prioridade - a.prioridade;
    });

    container.innerHTML = tarefas.map(tarefa => renderTarefaItem(tarefa)).join("");
  }
}

function renderTarefaItem(tarefa) {
  const disciplina = currentState.disciplinas.find(
    (d) => d.id === tarefa.disciplina_id,
  );
  const discNome = disciplina ? disciplina.sigla : "N/A";
  const tipoIcon = getTipoIcon(tarefa.tipo);

  return `
    <div class="tarefa-item prioridade-${tarefa.prioridade} ${tarefa.concluida ? "concluida" : ""}">
        <input type="checkbox" class="tarefa-check" ${tarefa.concluida ? "checked" : ""}
               onchange="toggleTarefa(${tarefa.id}, this.checked)">
        <div class="tarefa-content">
            <div class="tarefa-titulo">${tarefa.titulo}</div>
            ${tarefa.descricao ? `<div class="tarefa-descricao">${tarefa.descricao}</div>` : ""}
            <div class="tarefa-meta">
                <span><i class="fas fa-book"></i> ${discNome}</span>
                ${tarefa.tipo ? `<span><i class="${tipoIcon}"></i> ${tarefa.tipo}</span>` : ""}
                ${tarefa.data_entrega ? `<span><i class="fas fa-calendar"></i> ${formatDate(tarefa.data_entrega)}</span>` : ""}
            </div>
        </div>
        <div class="tarefa-actions">
            <button class="btn-icon" onclick="editTarefa(${tarefa.id})" title="Editar">
                <i class="fas fa-edit"></i>
            </button>
            <button class="btn-icon" onclick="deleteTarefa(${tarefa.id})" title="Excluir">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    </div>
  `;
}

function getTipoIcon(tipo) {
  const icons = {
    "e-folio": "fas fa-clipboard-check",
    "sessao-sincrona": "fas fa-video",
    projeto: "fas fa-project-diagram",
    forum: "fas fa-comments",
    geral: "fas fa-tasks",
  };
  return icons[tipo] || "fas fa-tasks";
}

async function toggleTarefa(tarefaId, concluida) {
  try {
    // Buscar a tarefa atual para pegar todos os campos
    const tarefa = currentState.tarefas.find((t) => t.id === tarefaId);
    if (!tarefa) {
      showToast("Tarefa não encontrada", "error");
      return;
    }

    // Enviar todos os campos necessários
    await fetch(`${API_URL}/tarefas/${tarefaId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        titulo: tarefa.titulo,
        descricao: tarefa.descricao || "",
        data_entrega: tarefa.data_entrega || null,
        prioridade: tarefa.prioridade || 2,
        concluida: concluida,
      }),
    });

    showToast(concluida ? "Tarefa concluída!" : "Tarefa reaberta", "success");
    loadTarefas();
    loadDashboard();
  } catch (error) {
    console.error("Erro ao atualizar tarefa:", error);
    showToast("Erro ao atualizar tarefa", "error");
  }
}

async function deleteTarefa(tarefaId) {
  if (!confirm("Deseja realmente excluir esta tarefa?")) return;

  try {
    await fetch(`${API_URL}/tarefas/${tarefaId}`, { method: "DELETE" });
    showToast("Tarefa excluída!", "success");
    loadTarefas();
    loadDashboard();
  } catch (error) {
    console.error("Erro ao excluir tarefa:", error);
    showToast("Erro ao excluir tarefa", "error");
  }
}

async function inicializarTarefasAutomaticas() {
  try {
    const response = await fetch(`${API_URL}/inicializar-tarefas`, {
      method: "POST",
    });
    const data = await response.json();
    console.log("✅ Tarefas automáticas inicializadas:", data.tarefas_criadas);
  } catch (error) {
    console.error("Erro ao inicializar tarefas:", error);
  }
}

// Event listeners para filtros de tarefas
document.addEventListener("DOMContentLoaded", () => {
  const filterBtns = document.querySelectorAll(".filter-btn");
  filterBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      filterBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      loadTarefas(btn.getAttribute("data-filter"));
    });
  });

  // Clique no card de tarefas pendentes
  const cardTarefasPendentes = document.getElementById("card-tarefas-pendentes");
  if (cardTarefasPendentes) {
    cardTarefasPendentes.addEventListener("click", () => {
      // Navegar para a página de tarefas
      navigateToPage("tarefas");

      // Aguardar um pouco para a página carregar
      setTimeout(() => {
        // Ativar o filtro de pendentes
        filterBtns.forEach((b) => b.classList.remove("active"));
        const btnPendentes = document.querySelector('.filter-btn[data-filter="pendentes"]');
        if (btnPendentes) {
          btnPendentes.classList.add("active");
          loadTarefas("pendentes");
        }

        // Rolar até a seção de tarefas
        const tarefasSection = document.getElementById("tarefas-page");
        if (tarefasSection) {
          tarefasSection.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      }, 100);
    });
  }

  // Clique no badge de tarefas urgentes
  const badgeUrgentes = document.getElementById("tarefas-urgentes");
  if (badgeUrgentes) {
    badgeUrgentes.addEventListener("click", (e) => {
      e.stopPropagation(); // Evitar que o clique no card seja acionado
      showUrgentTasksModal();
    });
  }

  // Botão nova tarefa
  const btnNovaTarefa = document.getElementById("btn-nova-tarefa");
  if (btnNovaTarefa) {
    btnNovaTarefa.addEventListener("click", () => {
      document.getElementById("modal-nova-tarefa").classList.add("active");
    });
  }

  // Form nova tarefa
  const formNovaTarefa = document.getElementById("form-nova-tarefa");
  if (formNovaTarefa) {
    formNovaTarefa.addEventListener("submit", async (e) => {
      e.preventDefault();

      const tarefa = {
        disciplina_id: document.getElementById("tarefa-disciplina").value,
        titulo: document.getElementById("tarefa-titulo").value,
        descricao: document.getElementById("tarefa-descricao").value,
        tipo: document.getElementById("tarefa-tipo").value,
        data_entrega: document.getElementById("tarefa-data").value,
        prioridade: parseInt(
          document.getElementById("tarefa-prioridade").value,
        ),
      };

      try {
        await fetch(`${API_URL}/tarefas`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(tarefa),
        });

        showToast("Tarefa criada com sucesso!", "success");
        document.getElementById("modal-nova-tarefa").classList.remove("active");
        formNovaTarefa.reset();
        loadTarefas();
        loadDashboard();
      } catch (error) {
        console.error("Erro ao criar tarefa:", error);
        showToast("Erro ao criar tarefa", "error");
      }
    });
  }
});

// ==================== TIMER POMODORO ====================
function initializeTimer() {
  const btnStart = document.getElementById("timer-start");
  const btnPause = document.getElementById("timer-pause");
  const btnReset = document.getElementById("timer-reset");
  const btnPopup = document.getElementById("timer-popup");

  if (btnStart) {
    btnStart.addEventListener("click", startTimer);
  }

  if (btnPause) {
    btnPause.addEventListener("click", pauseTimer);
  }

  if (btnReset) {
    btnReset.addEventListener("click", resetTimer);
  }

  if (btnPopup) {
    btnPopup.addEventListener("click", openTimerPopup);
  }

  // Adicionar seleção automática de última disciplina estudada
  loadLastStudiedDiscipline();

  updateTimerDisplay();
}

// Carregar última disciplina estudada
async function loadLastStudiedDiscipline() {
  try {
    const response = await fetch(`${API_URL}/sessoes`);
    if (response.ok) {
      const sessoes = await response.json();
      if (sessoes.length > 0) {
        const ultimaDisciplina = sessoes[0].disciplina_id;
        const selectDisciplina = document.getElementById("timer-disciplina");
        if (selectDisciplina && ultimaDisciplina) {
          selectDisciplina.value = ultimaDisciplina;
        }
      }
    }
  } catch (error) {
    console.error("Erro ao carregar última disciplina:", error);
  }
}

// Abrir timer em popup
function openTimerPopup() {
  const width = 400;
  const height = 650;
  const left = (screen.width - width) / 2;
  const top = (screen.height - height) / 2;

  // Abrir o arquivo HTML do popup
  const popup = window.open(
    "timer-popup.html",
    "timerPopup",
    `width=${width},height=${height},left=${left},top=${top},resizable=no,scrollbars=no,status=no,toolbar=no,menubar=no,location=no,alwaysRaised=yes`,
  );

  if (popup) {
    // Forçar o popup a ficar sempre visível
    popup.focus();

    // Tentar manter o popup sempre no topo (nem sempre funciona em todos os navegadores)
    setInterval(() => {
      if (popup && !popup.closed) {
        popup.focus();
      }
    }, 1000);

    // Salvar referência ao popup
    window.timerPopup = popup;
  }
}

function startTimer() {
  if (currentState.timer.isRunning) return;

  currentState.timer.isRunning = true;
  currentState.timer.isPaused = false;

  // Se estamos retomando de uma pausa, ajustar o timestamp inicial
  if (currentState.timer.pausedAt !== null) {
    // Calcular novo timestamp inicial baseado no tempo que faltava
    currentState.timer.startTimestamp =
      Date.now() -
      (currentState.timer.totalSeconds - currentState.timer.pausedAt) * 1000;
    currentState.timer.pausedAt = null;
  } else {
    // Novo timer - registrar timestamp inicial
    currentState.timer.startTimestamp = Date.now();

    // Atualizar horários de início e fim
    const now = new Date();
    const endTime = new Date(
      now.getTime() + currentState.timer.totalSeconds * 1000,
    );

    document.getElementById("timer-start-time").textContent =
      now.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });
    document.getElementById("timer-end-time").textContent =
      endTime.toLocaleTimeString("pt-BR", {
        hour: "2-digit",
        minute: "2-digit",
      });
  }

  document.getElementById("timer-start").style.display = "none";
  document.getElementById("timer-pause").style.display = "inline-flex";

  currentState.timer.interval = setInterval(() => {
    // Calcular tempo decorrido baseado no timestamp real
    const elapsedSeconds = Math.floor(
      (Date.now() - currentState.timer.startTimestamp) / 1000,
    );
    const remainingSeconds = currentState.timer.totalSeconds - elapsedSeconds;

    console.log(
      "Timer tick: remainingSeconds =",
      remainingSeconds,
      "elapsedSeconds =",
      elapsedSeconds,
    );

    if (remainingSeconds > 0) {
      currentState.timer.currentSeconds = remainingSeconds;
      updateTimerDisplay();
    } else {
      currentState.timer.currentSeconds = 0;
      updateTimerDisplay();
      timerComplete();
    }
  }, 100); // Atualizar mais frequentemente para melhor precisão

  showToast("Timer iniciado!", "success");
}

function pauseTimer() {
  currentState.timer.isRunning = false;
  currentState.timer.isPaused = true;

  // Salvar o tempo restante quando pausado
  if (currentState.timer.startTimestamp) {
    const elapsedSeconds = Math.floor(
      (Date.now() - currentState.timer.startTimestamp) / 1000,
    );
    currentState.timer.pausedAt = Math.max(
      0,
      currentState.timer.totalSeconds - elapsedSeconds,
    );
    currentState.timer.currentSeconds = currentState.timer.pausedAt;
  }

  clearInterval(currentState.timer.interval);

  document.getElementById("timer-start").style.display = "inline-flex";
  document.getElementById("timer-pause").style.display = "none";

  showToast("Timer pausado", "info");
}

function resetTimer() {
  pauseTimer();

  currentState.timer.currentSeconds = currentState.timer.totalSeconds;
  currentState.timer.isPaused = false;
  currentState.timer.startTimestamp = null;
  currentState.timer.pausedAt = null;

  updateTimerDisplay();
  document.title = "Study Planner"; // Resetar título da página

  // Resetar horários e barra de progresso
  document.getElementById("timer-start-time").textContent = "--:--";
  document.getElementById("timer-end-time").textContent = "--:--";
  const progressBar = document.getElementById("timer-progress-bar");
  if (progressBar) {
    progressBar.style.width = "0%";
  }

  showToast("Timer reiniciado", "info");
}

function timerComplete() {
  pauseTimer();

  playNotificationSound();

  // Resetar timestamp para próxima sessão
  currentState.timer.startTimestamp = null;
  currentState.timer.pausedAt = null;

  // Automaticamente selecionar a disciplina se houver apenas uma
  const selectDisciplina = document.getElementById("timer-disciplina");
  if (
    selectDisciplina &&
    !selectDisciplina.value &&
    currentState.disciplinas.length === 1
  ) {
    selectDisciplina.value = currentState.disciplinas[0].id;
  }

  if (currentState.timer.type === "study") {
    const message = "🎉 Pomodoro completo! Hora da pausa!";
    showToast(message, "success");
    sendBrowserNotification("Pomodoro Completo!", message);

    // Salvar sessão de estudo
    salvarSessaoEstudo();
    // Mudar para pausa (5 minutos)
    currentState.timer.type = "break";
    currentState.timer.totalSeconds = 300; // 5 minutos
    currentState.timer.currentSeconds = 300;
    document.getElementById("timer-label").textContent = "Pausa";
  } else {
    const message = "✅ Pausa terminada! Vamos voltar ao estudo!";
    showToast(message, "success");
    sendBrowserNotification("Pausa Terminada!", message);

    // Mudar para estudo (25 minutos)
    currentState.timer.type = "study";
    currentState.timer.totalSeconds = 1500; // 25 minutos
    currentState.timer.currentSeconds = 1500;
    document.getElementById("timer-label").textContent = "Sessão de Estudo";
  }

  updateTimerDisplay();
}

// Enviar notificação do navegador
function sendBrowserNotification(title, body) {
  if ("Notification" in window && Notification.permission === "granted") {
    try {
      const notification = new Notification(title, {
        body: body,
        icon: "/favicon.ico",
        badge: "/favicon.ico",
        vibrate: [200, 100, 200],
        requireInteraction: false,
        silent: false,
      });

      // Fechar notificação após 10 segundos
      setTimeout(() => notification.close(), 10000);

      // Focar na janela quando clicar na notificação
      notification.onclick = () => {
        window.focus();
        notification.close();
      };
    } catch (error) {
      console.log("Erro ao enviar notificação:", error);
    }
  }
}

function updateTimerDisplay() {
  const minutes = Math.floor(currentState.timer.currentSeconds / 60);
  const seconds = currentState.timer.currentSeconds % 60;

  const display = `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
  document.getElementById("timer-display").textContent = display;

  // Atualizar título da página com o tempo restante
  if (currentState.timer.isRunning) {
    const timerType = currentState.timer.type === "study" ? "📚" : "☕";
    document.title = `${timerType} ${display} - Study Planner`;
  } else if (currentState.timer.isPaused) {
    document.title = `⏸️ ${display} - Study Planner`;
  } else {
    document.title = "Study Planner";
  }

  // Atualizar círculo de progresso
  const progressCircle = document.getElementById("timer-progress-circle");
  const progress =
    currentState.timer.currentSeconds / currentState.timer.totalSeconds;

  // Atualizar barra de progresso verde
  const progressBar = document.getElementById("timer-progress-bar");
  if (progressBar) {
    const progressPercentage =
      ((currentState.timer.totalSeconds - currentState.timer.currentSeconds) /
        currentState.timer.totalSeconds) *
      100;
    progressBar.style.width = `${progressPercentage}%`;
  }
  const dashOffset = 880 - 880 * progress;
  progressCircle.style.strokeDashoffset = dashOffset;
}

async function salvarSessaoEstudo() {
  const disciplinaId = document.getElementById("timer-disciplina").value;
  const topico = document.getElementById("timer-topico").value;

  if (!disciplinaId) return;

  // Usar timezone de Lisboa
  const agora = new Date();
  const lisboaTime = new Date(
    agora.toLocaleString("en-US", { timeZone: "Europe/Lisbon" }),
  );
  const dataHoje = lisboaTime.toISOString().split("T")[0];
  const horaInicio = new Date(lisboaTime.getTime() - 25 * 60 * 1000)
    .toTimeString()
    .split(" ")[0]
    .substring(0, 5);
  const horaFim = lisboaTime.toTimeString().split(" ")[0].substring(0, 5);

  try {
    const response = await fetch(`${API_URL}/sessoes`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        disciplina_id: disciplinaId,
        data: dataHoje,
        hora_inicio: horaInicio,
        hora_fim: horaFim,
        duracao_minutos: 25,
        topico: topico,
        concluido: true,
      }),
    });

    if (response.ok) {
      // Recarregar disciplinas para atualizar contadores
      await loadDisciplinas();

      // Mostrar notificação de sucesso
      showToast(`✅ Sessão salva para ${topico || "estudo"}`, "success");

      // Se estiver na página de disciplinas, atualizar o modal se estiver aberto
      const modalDisciplina = document.getElementById("modal-disciplina");
      if (modalDisciplina && modalDisciplina.classList.contains("active")) {
        const disciplina = currentState.disciplinas.find(
          (d) => d.id === disciplinaId,
        );
        if (disciplina) {
          showDisciplinaModal(disciplinaId);
        }
      }
    }

    // Atualizar contador de pomodoros
    const pomodorosHoje = document.getElementById("pomodoros-hoje");
    const count = parseInt(pomodorosHoje.textContent) || 0;
    pomodorosHoje.textContent = count + 1;
  } catch (error) {
    console.error("Erro ao salvar sessão:", error);
  }
}

function playNotificationSound() {
  // Criar um beep simples usando Web Audio API
  try {
    const audioContext = new (window.AudioContext ||
      window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);

    oscillator.frequency.value = 800;
    oscillator.type = "sine";

    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(
      0.01,
      audioContext.currentTime + 0.5,
    );

    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.5);
  } catch (error) {
    console.log("Não foi possível reproduzir som");
  }
}

// ==================== ESTATÍSTICAS ====================
async function loadEstatisticas() {
  try {
    const response = await fetch(`${API_URL}/estatisticas`);
    const data = await response.json();

    renderChartDisciplinas(data.horas_por_disciplina);
    renderChartDias(data.horas_por_dia);
  } catch (error) {
    console.error("Erro ao carregar estatísticas:", error);
  }
}

function renderChartDisciplinas(dados) {
  const ctx = document.getElementById("chart-disciplinas");
  if (!ctx) return;

  const labels = dados.map((d) => {
    const disc = currentState.disciplinas.find(
      (disc) => disc.id === d.disciplina_id,
    );
    return disc ? disc.sigla : d.disciplina_id;
  });
  const values = dados.map((d) => d.total_horas);
  const colors = dados.map((d) => {
    const disc = currentState.disciplinas.find(
      (disc) => disc.id === d.disciplina_id,
    );
    return disc ? disc.cor : "#667eea";
  });

  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: labels,
      datasets: [
        {
          data: values,
          backgroundColor: colors,
          borderWidth: 2,
          borderColor: "#fff",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          position: "bottom",
          labels: {
            padding: 15,
            font: {
              size: 12,
            },
          },
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              return context.label + ": " + context.parsed.toFixed(1) + "h";
            },
          },
        },
      },
    },
  });
}

function renderChartDias(dados) {
  const ctx = document.getElementById("chart-dias");
  if (!ctx) return;

  const labels = dados.map((d) => formatDate(d.data));
  const values = dados.map((d) => d.total_horas);

  new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Horas de Estudo",
          data: values,
          borderColor: "#667eea",
          backgroundColor: "rgba(102, 126, 234, 0.1)",
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointRadius: 5,
          pointHoverRadius: 7,
          pointBackgroundColor: "#667eea",
          pointBorderColor: "#fff",
          pointBorderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              return context.parsed.y.toFixed(1) + " horas";
            },
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: "#e2e8f0",
          },
          ticks: {
            callback: function (value) {
              return value + "h";
            },
          },
        },
        x: {
          grid: {
            display: false,
          },
        },
      },
    },
  });
}

// ==================== MODAIS ====================
function initializeModals() {
  // Fechar modais ao clicar no botão X ou fora do modal
  document.addEventListener("click", (e) => {
    if (e.target.classList.contains("modal-close")) {
      e.target.closest(".modal").classList.remove("active");
    }
    if (e.target.classList.contains("modal")) {
      e.target.classList.remove("active");
    }
  });

  // Prevenir que cliques dentro do modal-content fechem o modal
  document.querySelectorAll(".modal-content").forEach((content) => {
    content.addEventListener("click", (e) => {
      e.stopPropagation();
    });
  });
}

// ==================== MODAL DE TAREFAS URGENTES ====================
function showUrgentTasksModal() {
  // Buscar tarefas urgentes do estado atual
  fetch(`${API_URL}/dashboard`)
    .then(response => response.json())
    .then(data => {
      const hoje = new Date();
      const urgentes = data.tarefas_proximas.filter((t) => {
        const dataEntrega = new Date(t.data_entrega);
        const diff = (dataEntrega - hoje) / (1000 * 60 * 60 * 24);
        return diff <= 3;
      });

      if (urgentes.length === 0) {
        showToast("Nenhuma tarefa urgente nos próximos 3 dias! 🎉", "success");
        return;
      }

      // Criar modal
      const modal = document.createElement("div");
      modal.className = "modal active";
      modal.innerHTML = `
        <div class="modal-content" style="max-width: 600px;">
          <div class="modal-header">
            <h2>⚠️ Tarefas Urgentes (Próximos 3 dias)</h2>
            <button class="modal-close">&times;</button>
          </div>
          <div class="modal-body">
            <div style="margin-bottom: 1rem; padding: 1rem; background: #fff3cd; border-left: 4px solid #ffc107; border-radius: 8px;">
              <strong>⏰ Atenção!</strong> Estas tarefas vencem nos próximos 3 dias.
            </div>
            ${urgentes.map(t => {
              const dataEntrega = new Date(t.data_entrega);
              const diff = Math.ceil((dataEntrega - hoje) / (1000 * 60 * 60 * 24));
              const diasTexto = diff === 0 ? 'HOJE' : diff === 1 ? 'AMANHÃ' : `em ${diff} dias`;
              const urgenciaClass = diff === 0 ? 'danger' : diff === 1 ? 'warning' : 'info';

              return `
                <div class="tarefa-item" style="margin-bottom: 1rem; border-left: 4px solid ${diff === 0 ? '#dc3545' : diff === 1 ? '#ffc107' : '#17a2b8'};">
                  <div class="tarefa-header">
                    <h3 style="margin: 0; font-size: 1.1rem;">${t.titulo}</h3>
                    <span class="badge badge-${urgenciaClass}" style="font-size: 0.9rem; font-weight: bold;">
                      ${diasTexto.toUpperCase()}
                    </span>
                  </div>
                  <div class="tarefa-info" style="margin-top: 0.5rem;">
                    <span class="badge badge-secondary">${t.tipo || 'Tarefa'}</span>
                    <span style="color: #666; margin-left: 1rem;">
                      📅 ${formatDate(t.data_entrega)}
                    </span>
                  </div>
                  ${t.descricao ? `<p style="margin-top: 0.5rem; color: #666;">${t.descricao}</p>` : ''}
                  <div style="margin-top: 1rem;">
                    <button class="btn btn-sm btn-success" onclick="toggleTarefa(${t.id}, true)">
                      ✓ Marcar como Concluída
                    </button>
                    <button class="btn btn-sm btn-primary" onclick="navigateToPage('tarefas'); document.querySelector('.modal.active')?.remove();">
                      Ver Todas as Tarefas
                    </button>
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        </div>
      `;

      document.body.appendChild(modal);

      // Fechar modal
      modal.querySelector(".modal-close").addEventListener("click", () => {
        modal.remove();
      });

      modal.addEventListener("click", (e) => {
        if (e.target === modal) {
          modal.remove();
        }
      });
    })
    .catch(error => {
      console.error("Erro ao carregar tarefas urgentes:", error);
      showToast("Erro ao carregar tarefas urgentes", "error");
    });
}

// ==================== UTILITÁRIOS ====================
function showLoading() {
  document.getElementById("loading").style.display = "flex";
}

function hideLoading() {
  document.getElementById("loading").style.display = "none";
}

function showToast(message, type = "info") {
  const container = document.getElementById("toast-container");
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;

  const icons = {
    success: "fa-check-circle",
    error: "fa-exclamation-circle",
    warning: "fa-exclamation-triangle",
    info: "fa-info-circle",
  };

  toast.innerHTML = `
        <i class="fas ${icons[type] || icons.info}"></i>
        <span>${message}</span>
    `;

  container.appendChild(toast);

  // Remover após 4 segundos
  setTimeout(() => {
    toast.style.animation = "slideOutRight 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

function formatDate(dateString) {
  if (!dateString) return "";

  // Tratar diferentes formatos de data
  let date;

  // Se for formato "DD mês" (ex: "6 outubro")
  if (
    dateString.includes(" ") &&
    !dateString.includes("-") &&
    !dateString.includes("/")
  ) {
    const meses = {
      janeiro: 0,
      fevereiro: 1,
      março: 2,
      abril: 3,
      maio: 4,
      junho: 5,
      julho: 6,
      agosto: 7,
      setembro: 8,
      outubro: 9,
      novembro: 10,
      dezembro: 11,
    };

    const [dia, mes] = dateString.toLowerCase().split(" ");
    const ano = 2024; // Ano atual do semestre
    const mesNum = meses[mes];

    if (mesNum !== undefined) {
      date = new Date(ano, mesNum, parseInt(dia));
    } else {
      return dateString; // Retorna original se não conseguir parsear
    }
  } else {
    // Formato ISO (YYYY-MM-DD) ou outro
    date = new Date(dateString);
  }

  // Verificar se a data é válida
  if (isNaN(date.getTime())) {
    return dateString; // Retorna original se inválida
  }

  const day = date.getDate().toString().padStart(2, "0");
  const month = (date.getMonth() + 1).toString().padStart(2, "0");
  const year = date.getFullYear();

  return `${day}/${month}/${year}`;
}

function adjustColor(color, percent) {
  // Ajusta a cor (escurece ou clareia)
  const num = parseInt(color.replace("#", ""), 16);
  const amt = Math.round(2.55 * percent);
  const R = (num >> 16) + amt;
  const G = ((num >> 8) & 0x00ff) + amt;
  const B = (num & 0x0000ff) + amt;

  return (
    "#" +
    (
      0x1000000 +
      (R < 255 ? (R < 1 ? 0 : R) : 255) * 0x10000 +
      (G < 255 ? (G < 1 ? 0 : G) : 255) * 0x100 +
      (B < 255 ? (B < 1 ? 0 : B) : 255)
    )
      .toString(16)
      .slice(1)
  );
}

// Exportar funções globais necessárias
window.showDisciplinaModal = showDisciplinaModal;
window.toggleTarefa = toggleTarefa;
window.deleteTarefa = deleteTarefa;
window.editTarefa = function (tarefaId) {
  showToast("Função de edição em desenvolvimento", "info");
};

console.log("✅ Aplicação carregada com sucesso!");
