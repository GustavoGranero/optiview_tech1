document.addEventListener('DOMContentLoaded', function () {
    const video = document.getElementById('myVideo');
    const muteButton = document.getElementById('muteButton');
  
    // Função para verificar se o vídeo está na tela
    function isVideoInView() {
      const rect = video.getBoundingClientRect();
      return rect.top >= 0 && rect.left >= 0 && rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) && rect.right <= (window.innerWidth || document.documentElement.clientWidth);
    }
  
    // Função para controlar a reprodução do vídeo
    function handleVideoPlayback() {
      if (isVideoInView()) {
        video.play();
      } else {
        video.pause();
      }
    }
  
    // Alternar o som do vídeo
    muteButton.addEventListener('click', function () {
      if (video.muted) {
        video.muted = false;
        muteButton.textContent = 'Mute';
      } else {
        video.muted = true;
        muteButton.textContent = 'Unmute';
      }
    });
  
    // Verificar a visibilidade do vídeo ao carregar, rolar e redimensionar a janela
    window.addEventListener('load', handleVideoPlayback);
    window.addEventListener('scroll', handleVideoPlayback);
    window.addEventListener('resize', handleVideoPlayback);
  });
  