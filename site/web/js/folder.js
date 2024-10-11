// Seleciona todas as abas
function update_itens_count(count) {
  document.querySelector('.sub-text').innerText = count + ' ítem(s)'
}

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
        lines_count = document.querySelectorAll('.files .row').length;
        break;
      case 'plans':
        container = document.querySelector('.plans');
        lines_count = document.querySelectorAll('.plans .row').length;
        break;
      case 'legends':
        container = document.querySelector('.legends');
        lines_count = document.querySelectorAll('.legends .row').length;
    }
    // document.querySelector('.sub-text').innerText = lines_count + ' ítem(s)'
    update_itens_count(lines_count)
    container.classList.add('visible');
    container.classList.add('hidden')
  });
});
