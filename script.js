document.addEventListener('DOMContentLoaded', () => {
  // Selecteer alle content behalve header/nav (die wil je altijd zichtbaar)
  const fadeElements = document.querySelectorAll(
    'main > div, section, img, h1, h2, h3, p, footer, iframe'
  );

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        // Element komt in beeld → fade-in
        entry.target.classList.add('visible');
      } else {
        // Element gaat uit beeld → fade-out
        entry.target.classList.remove('visible');
      }
    });
  }, { threshold: 0.2 });

  fadeElements.forEach(el => {
    el.classList.add('fade-in');
    observer.observe(el);
  });
});


