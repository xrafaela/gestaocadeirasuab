// ============================================================
// CHAT IA - CORRIGIDO
// Sistema UAB LEI v2.0
// ============================================================

(function() {
    'use strict';

    // Elementos DOM
    const chatToggleBtn = document.getElementById('chatToggleBtn');
    const chatWindow = document.getElementById('chatWindow');
    const chatCloseBtn = document.getElementById('chatCloseBtn');
    const chatInput = document.getElementById('chatInput');
    const chatSendBtn = document.getElementById('chatSendBtn');
    const chatMessages = document.getElementById('chatMessages');
    const chatWelcome = document.getElementById('chatWelcome');
    const typingIndicator = document.getElementById('typingIndicator');
    const suggestionChips = document.querySelectorAll('.suggestion-chip');

    // Estado
    let isOpen = false;
    let messageCount = 0;

    // ============================================================
    // FUNÇÕES PRINCIPAIS
    // ============================================================

    // Toggle Chat Window - CORRIGIDO
    function toggleChat(event) {
        if (event) {
            event.preventDefault();
            event.stopPropagation();
        }

        isOpen = !isOpen;

        if (isOpen) {
            chatWindow.classList.add('show');
            chatWindow.style.display = 'flex';
            chatToggleBtn.classList.add('active');
            if (chatInput) {
                setTimeout(() => chatInput.focus(), 100);
            }
        } else {
            chatWindow.classList.remove('show');
            setTimeout(() => {
                chatWindow.style.display = 'none';
            }, 300);
            chatToggleBtn.classList.remove('active');
        }
    }

    // Fechar chat - CORRIGIDO
    function closeChat(event) {
        if (event) {
            event.preventDefault();
            event.stopPropagation();
        }

        if (isOpen) {
            isOpen = false;
            chatWindow.classList.remove('show');
            setTimeout(() => {
                chatWindow.style.display = 'none';
            }, 300);
            chatToggleBtn.classList.remove('active');
        }
    }

    // Adicionar mensagem ao chat
    function addMessage(text, isUser = false) {
        if (!chatMessages) return;

        // Esconder tela de boas-vindas na primeira mensagem
        if (messageCount === 0) {
            if (chatWelcome) chatWelcome.style.display = 'none';
            chatMessages.style.display = 'block';
        }
        messageCount++;

        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${isUser ? 'user' : 'assistant'}`;

        const now = new Date();
        const time = now.toLocaleTimeString('pt-BR', {
            hour: '2-digit',
            minute: '2-digit'
        });

        // Converter quebras de linha para <br>
        const formattedText = text.replace(/\n/g, '<br>');

        messageDiv.innerHTML = `
            <div class="message-bubble">
                <p>${formattedText}</p>
                <div class="message-time">${time}</div>
            </div>
        `;

        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Mostrar indicador de digitação
    function showTyping(show = true) {
        if (!typingIndicator) return;

        if (show) {
            typingIndicator.classList.add('show');
            if (chatMessages) {
                chatMessages.appendChild(typingIndicator);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        } else {
            typingIndicator.classList.remove('show');
        }
    }

    // Enviar mensagem
    async function sendMessage() {
        if (!chatInput) return;

        const message = chatInput.value.trim();
        if (!message) return;

        // Adicionar mensagem do usuário
        addMessage(message, true);
        chatInput.value = '';
        chatInput.style.height = 'auto';

        // Desabilitar entrada enquanto processa
        chatInput.disabled = true;
        if (chatSendBtn) chatSendBtn.disabled = true;
        showTyping(true);

        try {
            const response = await fetch('http://localhost:5000/api/ai/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    context: null
                })
            });

            const data = await response.json();

            showTyping(false);

            if (data.success) {
                addMessage(data.response, false);
            } else {
                addMessage('❌ Erro: ' + (data.response || 'Não foi possível processar sua pergunta.'), false);
            }
        } catch (error) {
            showTyping(false);
            addMessage('❌ Erro de conexão. Verifique se o servidor está rodando (porta 5000).', false);
            console.error('Chat error:', error);
        } finally {
            // Reabilitar entrada
            chatInput.disabled = false;
            if (chatSendBtn) chatSendBtn.disabled = false;
            chatInput.focus();
        }
    }

    // Verificar status da IA
    async function checkIAStatus() {
        try {
            const response = await fetch('http://localhost:5000/api/ai/status');
            const data = await response.json();

            if (!data.configured && messageCount === 0) {
                setTimeout(() => {
                    const warning = document.createElement('div');
                    warning.className = 'chat-error';
                    warning.innerHTML = `
                        ⚠️ IA não configurada.<br>
                        <small>O servidor pode estar reiniciando. Aguarde alguns segundos e tente novamente.</small>
                    `;
                    if (chatMessages) {
                        chatMessages.insertBefore(warning, chatMessages.firstChild);
                    }
                }, 2000);
            } else if (data.configured) {
                console.log('✅ Chat IA configurado e pronto!');
            }
        } catch (error) {
            console.error('Failed to check IA status:', error);
        }
    }

    // ============================================================
    // EVENT LISTENERS
    // ============================================================

    // Botão de abrir/fechar - CORRIGIDO
    if (chatToggleBtn) {
        chatToggleBtn.addEventListener('click', toggleChat);
    }

    // Botão X de fechar - CORRIGIDO
    if (chatCloseBtn) {
        chatCloseBtn.addEventListener('click', closeChat);
    }

    // Auto-resize do textarea
    if (chatInput) {
        chatInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });

        // Enter para enviar (Shift+Enter para nova linha)
        chatInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    }

    // Botão de enviar
    if (chatSendBtn) {
        chatSendBtn.addEventListener('click', sendMessage);
    }

    // Chips de sugestão
    if (suggestionChips) {
        suggestionChips.forEach(chip => {
            chip.addEventListener('click', function() {
                if (chatInput) {
                    chatInput.value = this.dataset.suggestion;
                    sendMessage();
                }
            });
        });
    }

    // Fechar com ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && isOpen) {
            closeChat();
        }
    });

    // ============================================================
    // INICIALIZAÇÃO
    // ============================================================

    // Verificar status da IA ao carregar
    setTimeout(checkIAStatus, 1000);

    // Log de inicialização
    console.log('✅ Chat IA carregado e pronto!');
    console.log('💬 Clique no botão roxo para abrir o chat');

})();
