// Seleciona todas as abas
const tabs = document.querySelectorAll('.tab');
const container = document.querySelector('.container');

// Adiciona evento de clique a cada aba
tabs.forEach(tab => {
  tab.addEventListener('click', function() {
    // Remove a classe 'active' de todas as abas
    tabs.forEach(tab => tab.classList.remove('active'));
    
    // Adiciona a classe 'active' na aba clicada
    this.classList.add('active');
    
    // Conecta visualmente a aba ativa com o contêiner
    container.classList.add('active');
  });
});
