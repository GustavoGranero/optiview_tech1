// script.js
document.addEventListener("DOMContentLoaded", function() {
    const loader = document.getElementById("loader");
    const content = document.getElementById("content");
  
    function showLoader() {
      loader.style.display = "flex";
      content.classList.remove("loaded");
    }
  
    function hideLoader() {
      loader.style.display = "none";
      content.classList.add("loaded");
    }
  
    // Simula um carregamento inicial
    setTimeout(hideLoader, 700);
  
    const links = document.querySelectorAll(".link");
    links.forEach(link => {
      link.addEventListener("click", function(e) {
        e.preventDefault();
        showLoader();
        setTimeout(() => {
          window.location.href = this.href;
        }, 1000); // Simula um tempo de carregamento
      });
    });
  });
  