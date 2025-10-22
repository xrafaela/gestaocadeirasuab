# Configuração com Token Endpoint - Guia Rápido

## 📋 O que foi implementado

A aplicação agora usa **Token Endpoint** em vez de secrets diretos para conectar aos agentes Copilot Studio. Isso é mais seguro e confiável.

## 🔄 Fluxo de Funcionamento

```
1. Usuário clica em um agente (ex: AC)
   ↓
2. Frontend solicita token ao backend
   ↓
3. Backend gera token usando secret (DirectLine API)
   ↓
4. Frontend recebe token
   ↓
5. WebChat conecta ao agente usando token
   ↓
6. Usuário conversa com o agente
   ↓
7. Token expira em 30 minutos (renovação automática)
```

## 🔐 Segurança

- **Secret**: Fica no backend (seguro)
- **Token**: Temporário, expira em 30 minutos
- **Frontend**: Nunca vê o secret, apenas o token

## 📝 Mudanças Realizadas

### Frontend (index.html)

1. **Adicionado WebChat CDN** (linha 2109)
   ```html
   <script src="https://cdn.botframework.com/botframework-webchat/latest/webchat.js"></script>
   ```

2. **Nova função `initializeWebChat()`** (linhas 2236-2300)
   - Obtém token do backend
   - Cria DirectLine com token
   - Renderiza WebChat

3. **Atualizada função `selectAgent()`** (linhas 2195-2234)
   - Agora é async
   - Chama initializeWebChat()

### Backend (app.py)

- Rota `/api/copilot/{agent}/token` - Já existe ✓
- Rota `/api/copilot/{agent}/chat` - Já existe ✓
- Rota `/api/copilot/{agent}/clear` - Já existe ✓

## 🧪 Como Testar

1. Abra http://localhost:5000
2. Clique em "Agentes IA"
3. Clique em um agente (ex: AC)
4. Aguarde o WebChat carregar
5. Digite uma mensagem

## ⚠️ Verificação Necessária no Copilot Studio

1. Vá para https://copilotstudio.microsoft.com
2. Abra seu agente AC
3. Vá para **Settings > Security > Web channel security**
4. Verifique se **"Require secured access"** está **ATIVADO**
5. Se não estiver, ative-o
6. Aguarde até 2 horas para a mudança propagar

## 🐛 Troubleshooting

### Erro: "403 - ResourceNotFound"
- Verifique se "Require secured access" está ativado
- Regenere novos secrets
- Aguarde 2 horas para propagar

### WebChat não aparece
- Abra console (F12) e verifique erros
- Verifique se o token foi obtido
- Verifique a conexão de internet

### Mensagens não são enviadas
- Verifique se o token não expirou
- Tente limpar histórico
- Reinicie a conversa

## 📚 Arquivos Modificados

- `/frontend/index.html` - Adicionado WebChat e funções
- `/backend/app.py` - Sem mudanças (rotas já existem)
- `/backend/copilot_agent.py` - Sem mudanças

## 🎯 Próximas Melhorias (Opcional)

1. Renovação automática de token
2. Persistência de histórico
3. Autenticação de usuário
4. Suporte a anexos
5. Múltiplos agentes simultâneos

## 📞 Suporte

Se encontrar problemas:
1. Verifique o console do navegador (F12)
2. Verifique os logs do servidor
3. Verifique as configurações no Copilot Studio
4. Tente regenerar os secrets

