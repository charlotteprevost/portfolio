// Generated from assets/site.ts (kept in sync manually).
function $all(selector) {
  return document.querySelectorAll(selector);
}
function setLang(next) {
  var fr = $all('.lang-fr');
  var en = $all('.lang-en');
  var showFR = next === 'fr';
  fr.forEach(function (el) { return (el.style.display = showFR ? '' : 'none'); });
  en.forEach(function (el) { return (el.style.display = showFR ? 'none' : ''); });
  document.documentElement.lang = showFR ? 'fr' : 'en';
  try {
    localStorage.setItem('portfolio_lang', showFR ? 'fr' : 'en');
  }
  catch (_a) {
    // ignore
  }
}
window.toggleLanguage = function toggleLanguage() {
  var current = document.documentElement.lang === 'fr' ? 'fr' : 'en';
  setLang(current === 'fr' ? 'en' : 'fr');
};
function init() {
  var y = String(new Date().getFullYear());
  var year = document.getElementById('year');
  var yearFr = document.getElementById('year-fr');
  if (year)
    year.textContent = y;
  if (yearFr)
    yearFr.textContent = y;
  var saved = 'en';
  try {
    saved = localStorage.getItem('portfolio_lang');
  }
  catch (_a) {
    saved = 'en';
  }
  setLang(saved === 'fr' ? 'fr' : 'en');
}
init();

