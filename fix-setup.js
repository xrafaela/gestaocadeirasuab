// Script para marcar setup como completo
console.log('=== MARCANDO SETUP COMO COMPLETO ===');

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

console.log('✅ Setup marcado como completo!');
console.log('📊 Dados salvos:', config);
console.log('🔄 Recarregue a página (F5) para aplicar as mudanças');

alert('✅ Setup marcado como completo!\n\n🔄 Pressione F5 para recarregar a página.');
