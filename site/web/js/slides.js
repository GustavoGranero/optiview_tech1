let slideIndex = 0;
let slides = document.querySelectorAll(".carousel-slide");
let dots = document.querySelectorAll(".dot");
let timer = null;

function showSlides(n) {
  slideIndex = (n + slides.length) % slides.length;
  slides.forEach((slide, index) => {
    slide.style.display = index === slideIndex ? "block" : "none";
    dots[index].classList.toggle("active", index === slideIndex);
  });
  resetTimer();
}

function resetTimer() {
  clearInterval(timer);
  timer = setInterval(() => { showSlides(slideIndex + 1); }, 4000);
}

document.querySelector('.prev').addEventListener('click', () => {
  showSlides(slideIndex - 1);
});

document.querySelector('.next').addEventListener('click', () => {
  showSlides(slideIndex + 1);
});

dots.forEach((dot, index) => {
  dot.addEventListener('click', () => {
    showSlides(index);
  });
});

showSlides(slideIndex);