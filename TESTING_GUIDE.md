# Guia de Testes - Token Endpoint

## 🧪 Teste Rápido (5 minutos)

### 1. Verificar Servidor
```bash
# Terminal 1: Verificar se servidor está rodando
curl http://localhost:5000/api/copilot/agents
# Esperado: Lista de agentes em JSON
```

### 2. Testar Token Endpoint
```bash
# Terminal 2: Obter token
curl http://localhost:5000/api/copilot/AC/token
# Esperado: JSON com token, conversationId, directlineUrl
```

### 3. Testar no Navegador
1. Abra http://localhost:5000
2. Clique em "Agentes IA"
3. Clique em "AC - Arquitetura de Computadores"
4. Aguarde WebChat carregar
5. Digite uma mensagem

## 🔍 Verificação de Erros

### Console do Navegador (F12)
Procure por:
- ✅ "Token obtido:" - Token foi recebido
- ✅ "WebChat inicializado com sucesso" - WebChat carregou
- ❌ "Erro ao obter token" - Problema no backend
- ❌ "Erro ao inicializar WebChat" - Problema no frontend

### Logs do Servidor
Procure por:
- ✅ "✓ Token gerado para AC" - Token gerado com sucesso
- ❌ "❌ Erro ao gerar token: 403" - Problema com secret

## 🐛 Troubleshooting

### Problema: "Erro ao conectar: 403 - ResourceNotFound"

**Causa**: "Require secured access" não está ativado no Copilot Studio

**Solução**:
1. Vá para https://copilotstudio.microsoft.com
2. Abra agente AC
3. Settings > Security > Web channel security
4. Ative "Require secured access"
5. Aguarde até 2 horas
6. Tente novamente

### Problema: WebChat não aparece

**Causa**: Token não foi obtido ou WebChat CDN não carregou

**Solução**:
1. Abra console (F12)
2. Verifique erros de rede
3. Verifique se token foi obtido
4. Recarregue a página (Ctrl+F5)

### Problema: Mensagens não são enviadas

**Causa**: Token expirou ou conexão perdida

**Solução**:
1. Limpe o histórico (botão "Limpar")
2. Selecione o agente novamente
3. Tente enviar mensagem

## ✅ Checklist de Teste

- [ ] Servidor rodando em http://localhost:5000
- [ ] Rota /api/copilot/agents retorna lista
- [ ] Rota /api/copilot/AC/token retorna token
- [ ] Frontend carrega sem erros
- [ ] Aba "Agentes IA" aparece
- [ ] Agente AC está disponível
- [ ] WebChat aparece ao clicar em AC
- [ ] Mensagem é enviada com sucesso
- [ ] Resposta do agente aparece
- [ ] Botão "Limpar" funciona
- [ ] Histórico é mantido

## 📊 Teste de Carga

```bash
# Testar múltiplas requisições de token
for i in {1..10}; do
  curl http://localhost:5000/api/copilot/AC/token
  echo "Requisição $i"
done
```

Esperado: Todos os tokens são gerados com sucesso

## 🔐 Teste de Segurança

1. Abra console (F12)
2. Procure por "secret" no código
3. Esperado: Nenhuma ocorrência de secret no frontend
4. Procure por "token" no código
5. Esperado: Token é usado apenas para conectar ao WebChat

## 📝 Relatório de Teste

Após testar, preencha:

```
Data: ___________
Hora: ___________

Servidor: [ ] OK [ ] Erro
Token: [ ] OK [ ] Erro
Frontend: [ ] OK [ ] Erro
WebChat: [ ] OK [ ] Erro
Mensagens: [ ] OK [ ] Erro

Erros encontrados:
_________________________________
_________________________________

Observações:
_________________________________
_________________________________
```

## 🎯 Próximos Testes

1. Testar com múltiplos agentes
2. Testar renovação de token
3. Testar com conexão lenta
4. Testar em diferentes navegadores
5. Testar em dispositivos móveis

