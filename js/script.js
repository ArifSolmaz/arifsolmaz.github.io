document.addEventListener('DOMContentLoaded', () => {
  let currentLang = localStorage.getItem('language') || 'tr';
  const langToggle = document.getElementById('lang-toggle');

  // Load language content
  function loadLanguage(lang) {
    fetch(`lang/${lang}.json`)
      .then(response => response.json())
      .then(data => {
        document.querySelectorAll('[data-i18n]').forEach(elem => {
          const key = elem.getAttribute('data-i18n');
          elem.textContent = data[key] || elem.textContent;
        });
        document.documentElement.lang = lang;
        langToggle.textContent = lang === 'tr' ? 'EN' : 'TR';
      });
  }

  // Toggle language
  langToggle.addEventListener('click', () => {
    currentLang = currentLang === 'tr' ? 'en' : 'tr';
    localStorage.setItem('language', currentLang);
    loadLanguage(currentLang);
  });

  // Initial load
  loadLanguage(currentLang);
});