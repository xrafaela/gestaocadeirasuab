# 🔧 Como Desativar o Setup Wizard

Se o setup wizard continua aparecendo mesmo depois de você já ter configurado o sistema, siga estas instruções:

## 📋 Método 1: Usar a Ferramenta de Debug (RECOMENDADO)

1. Abra o arquivo no navegador:
   ```
   file:///home/igorcostas/Documentos/LEI/study-planner/frontend/marcar-setup-completo.html
   ```

2. Clique no botão **"✅ Marcar Setup Como Completo"**

3. Recarregue a página principal (F5)

4. O setup wizard não deve mais aparecer!

## 📋 Método 2: Console do Navegador

1. Abra a página principal do Study Planner

2. Pressione **F12** para abrir o Console do Navegador

3. Cole este código no console e pressione Enter:
   ```javascript
   const config = {
       nome: 'Igor Costas',
       curso: 'LEI - Licenciatura em Engenharia Informática',
       ano: '1',
       disciplinas: ['AC', 'FBD', 'LC', 'PO', 'SC', 'EPE'],
       horasDia: 4,
       diasEstudo: ['segunda', 'terca', 'quarta', 'quinta', 'sexta'],
       dataSetup: new Date().toISOString()
   };
   localStorage.setItem('userConfig', JSON.stringify(config));
   localStorage.setItem('setupCompleto', 'true');
   alert('Setup marcado como completo! Pressione F5 para recarregar.');
   ```

4. Pressione **F5** para recarregar a página

5. O setup wizard não deve mais aparecer!

## 📋 Método 3: Usar a Função Global

1. Abra a página principal do Study Planner

2. Pressione **F12** para abrir o Console do Navegador

3. Digite no console:
   ```javascript
   markSetupComplete()
   ```

4. Pressione **F5** para recarregar a página

## 🔍 Verificar Status

Para verificar se o setup está marcado como completo:

1. Pressione **F12** no navegador

2. Vá para a aba **Console**

3. Digite:
   ```javascript
   console.log('userConfig:', localStorage.getItem('userConfig'));
   console.log('setupCompleto:', localStorage.getItem('setupCompleto'));
   ```

4. Se ambos mostrarem valores (não `null`), o setup está completo

## 🔄 Resetar Setup (Para Testar)

Se você quiser ver o setup wizard novamente (para testes):

1. Pressione **F12** no navegador

2. No console, digite:
   ```javascript
   localStorage.removeItem('userConfig');
   localStorage.removeItem('setupCompleto');
   location.reload();
   ```

## ❓ Problemas Comuns

### O setup wizard ainda aparece depois de marcar como completo

**Solução:**
- Limpe o cache do navegador (Ctrl+Shift+Delete)
- Feche todas as abas do Study Planner
- Abra novamente

### Os dados não estão sendo salvos

**Solução:**
- Verifique se o navegador permite localStorage
- Verifique se não está em modo anônimo/privado
- Tente outro navegador (Firefox, Chrome)

### Quero ver os dados salvos

**Solução:**
1. Pressione F12
2. Vá para a aba **Application** (Chrome) ou **Storage** (Firefox)
3. Expanda **Local Storage**
4. Clique em `file://` ou `http://localhost:5000`
5. Veja as chaves `userConfig` e `setupCompleto`

## 📞 Suporte

Se nenhum método funcionar:
1. Abra o arquivo `marcar-setup-completo.html`
2. Clique em "Verificar Status"
3. Tire um print da tela
4. Reporte o problema com o print

