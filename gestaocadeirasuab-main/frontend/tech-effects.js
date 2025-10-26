// ==================== TECH THEME - LIGHTWEIGHT EFFECTS ====================

// Efeito de brilho nos cards ao hover (CSS-based, sem JS pesado)
function initCardGlowEffects() {
  const style = document.createElement('style');
  style.textContent = `
    .stat-card, .disciplina-card, .section {
      position: relative;
      overflow: hidden;
    }
    
    .stat-card::after, .disciplina-card::after, .section::after {
      content: '';
      position: absolute;
      top: -50%;
      left: -50%;
      width: 200%;
      height: 200%;
      background: radial-gradient(circle, rgba(0, 212, 255, 0.15) 0%, transparent 50%);
      opacity: 0;
      transition: opacity 0.6s ease;
      pointer-events: none;
    }
    
    .stat-card:hover::after, .disciplina-card:hover::after, .section:hover::after {
      opacity: 1;
    }
  `;
  document.head.appendChild(style);
}

// Efeito de typing no título (executa uma vez, leve)
function initTypingEffect() {
  const titles = document.querySelectorAll('.page-header h1');
  
  titles.forEach(title => {
    const text = title.textContent;
    title.textContent = '';
    title.style.opacity = '1';
    
    let index = 0;
    const speed = 50;
    
    function type() {
      if (index < text.length) {
        title.textContent += text.charAt(index);
        index++;
        setTimeout(type, speed);
      }
    }
    
    // Só executa uma vez quando a página carrega
    if (!title.dataset.typed) {
      type();
      title.dataset.typed = 'true';
    }
  });
}

// Efeito de reveal ao scroll (otimizado com IntersectionObserver)
function initScrollReveal() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        observer.unobserve(entry.target); // Remove observer após revelar
      }
    });
  }, { 
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  });
  
  const elements = document.querySelectorAll('.stat-card, .section, .disciplina-card, .tarefa-categoria');
  elements.forEach(el => {
    if (!el.classList.contains('revealed')) {
      observer.observe(el);
    }
  });
}

// Efeito de código binário no background (muito leve, CSS-based)
function createBinaryBackground() {
  const binaryContainer = document.createElement('div');
  binaryContainer.className = 'binary-bg';
  
  // Apenas 5 colunas de binário (muito leve)
  for (let i = 0; i < 5; i++) {
    const column = document.createElement('div');
    column.className = 'binary-column';
    column.style.left = `${20 + i * 20}%`;
    column.style.animationDelay = `${i * 0.5}s`;
    column.textContent = Math.random().toString(2).substring(2, 12);
    binaryContainer.appendChild(column);
  }
  
  document.body.appendChild(binaryContainer);
}

// Efeito de pulso nos badges (CSS-based)
function initBadgePulse() {
  const badges = document.querySelectorAll('.badge-danger, #tarefas-urgentes');
  badges.forEach(badge => {
    if (badge.textContent.includes('Urgentes') && !badge.textContent.includes('0')) {
      badge.classList.add('pulse-badge');
    }
  });
}

// Efeito de hover suave nos botões (throttled)
let hoverTimeout;
function initButtonHoverEffects() {
  const buttons = document.querySelectorAll('.btn, .nav-item');
  
  buttons.forEach(button => {
    button.addEventListener('mouseenter', function() {
      clearTimeout(hoverTimeout);
      this.classList.add('btn-hover-active');
    });
    
    button.addEventListener('mouseleave', function() {
      hoverTimeout = setTimeout(() => {
        this.classList.remove('btn-hover-active');
      }, 300);
    });
  });
}

// Efeito de loading bar no topo (aparece em transições)
function createLoadingBar() {
  const loadingBar = document.createElement('div');
  loadingBar.className = 'loading-bar';
  loadingBar.id = 'loading-bar';
  document.body.appendChild(loadingBar);
}

function showLoadingBar() {
  const bar = document.getElementById('loading-bar');
  if (bar) {
    bar.style.width = '0%';
    bar.style.opacity = '1';
    
    // Animação suave de 0 a 100%
    let width = 0;
    const interval = setInterval(() => {
      width += 10;
      bar.style.width = width + '%';
      
      if (width >= 100) {
        clearInterval(interval);
        setTimeout(() => {
          bar.style.opacity = '0';
        }, 200);
      }
    }, 50);
  }
}

// Efeito de glow nos ícones (apenas CSS, sem JS)
function initIconGlow() {
  const style = document.createElement('style');
  style.textContent = `
    .stat-icon, .nav-brand i {
      transition: filter 0.3s ease;
    }
    
    .stat-icon:hover, .nav-brand:hover i {
      filter: drop-shadow(0 0 10px currentColor);
    }
  `;
  document.head.appendChild(style);
}

// Efeito de tech grid (estático, sem animação pesada)
function createTechGrid() {
  const grid = document.createElement('div');
  grid.className = 'tech-grid';
  document.body.appendChild(grid);
}

// Smooth scroll otimizado
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (href !== '#') {
        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      }
    });
  });
}

// Efeito de foco nos inputs (CSS-based com classe)
function initInputFocusEffects() {
  const inputs = document.querySelectorAll('input, textarea, select');
  
  inputs.forEach(input => {
    input.addEventListener('focus', function() {
      this.parentElement?.classList.add('input-focused');
    });
    
    input.addEventListener('blur', function() {
      this.parentElement?.classList.remove('input-focused');
    });
  });
}

// Contador animado para números (executa uma vez)
function animateCounters() {
  const counters = document.querySelectorAll('.stat-card h3');
  
  counters.forEach(counter => {
    const target = parseInt(counter.textContent);
    if (isNaN(target) || counter.dataset.animated) return;
    
    counter.dataset.animated = 'true';
    let current = 0;
    const increment = target / 30; // 30 frames
    const duration = 1000; // 1 segundo
    const stepTime = duration / 30;
    
    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        counter.textContent = target;
        clearInterval(timer);
      } else {
        counter.textContent = Math.floor(current);
      }
    }, stepTime);
  });
}

// Inicialização otimizada (sem loops infinitos)
document.addEventListener('DOMContentLoaded', () => {
  console.log('🚀 Tech Theme - Lightweight Effects Loading...');

  // Efeitos estáticos (executam uma vez)
  createBinaryBackground();
  createTechGrid();
  createLoadingBar();
  
  // Efeitos CSS-based (sem JS pesado)
  initCardGlowEffects();
  initIconGlow();
  
  // Efeitos com event listeners otimizados
  initButtonHoverEffects();
  initInputFocusEffects();
  initBadgePulse();
  initSmoothScroll();
  
  // Efeitos que executam uma vez
  setTimeout(() => {
    initScrollReveal();
    animateCounters();
  }, 300);
  
  // Typing effect apenas na primeira carga
  if (!sessionStorage.getItem('typingShown')) {
    initTypingEffect();
    sessionStorage.setItem('typingShown', 'true');
  }
  
  // Loading bar em navegação de páginas
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(item => {
    item.addEventListener('click', () => {
      showLoadingBar();
    });
  });
  
  // Re-aplicar scroll reveal apenas quando necessário (otimizado)
  let scrollTimeout;
  const pageObserver = new MutationObserver((mutations) => {
    const hasNewElements = mutations.some(m => 
      Array.from(m.addedNodes).some(node => 
        node.nodeType === 1 && (
          node.classList?.contains('stat-card') ||
          node.classList?.contains('section') ||
          node.classList?.contains('disciplina-card')
        )
      )
    );
    
    if (hasNewElements) {
      clearTimeout(scrollTimeout);
      scrollTimeout = setTimeout(() => {
        initScrollReveal();
        initBadgePulse();
      }, 500);
    }
  });
  
  pageObserver.observe(document.body, {
    childList: true,
    subtree: false // Apenas nível superior
  });
  
  console.log('✅ Tech Theme Effects Loaded!');
});

// Cleanup ao sair da página
window.addEventListener('beforeunload', () => {
  // Limpar observers se necessário
  console.log('🧹 Cleaning up...');
});

