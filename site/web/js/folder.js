// Seleciona todas as abas
const tabs = document.querySelectorAll('.tab');
container = document.querySelector('.lines-container');

// Adiciona evento de clique a cada aba
tabs.forEach(tab => {
  tab.addEventListener('click', function() {

    // Remove a classe 'active' de todas as abas
    tabs.forEach(tab => tab.classList.remove('active'));
    
    // Adiciona a classe 'active' na aba clicada
    this.classList.add('active');
    
    // // Conecta visualmente a aba ativa com o contêiner
    // container.classList.add('active');

    // Remove a classe 'visible' dos containers das linhas
    document.querySelectorAll('.lines-container').forEach(container => {
      container.classList.remove('visible')
      container.classList.add('hidden')
    });

    // Faz aparecer o conteúdo
    switch(this.id) {
      case 'files':
        container = document.querySelector('.files');
        break;
      case 'plans':
        container = document.querySelector('.plans');
        break;
      case 'legends':
        container = document.querySelector('.legends');
    } 
    container.classList.add('visible');
    container.classList.add('hidden')
  });
});
