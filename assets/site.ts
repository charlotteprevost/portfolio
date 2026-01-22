type Lang = 'en' | 'fr';

function $all(selector: string): NodeListOf<HTMLElement> {
  return document.querySelectorAll(selector) as NodeListOf<HTMLElement>;
}

function setLang(next: Lang) {
  const fr = $all('.lang-fr');
  const en = $all('.lang-en');

  const showFR = next === 'fr';
  fr.forEach((el) => (el.style.display = showFR ? '' : 'none'));
  en.forEach((el) => (el.style.display = showFR ? 'none' : ''));

  document.documentElement.lang = showFR ? 'fr' : 'en';
  try {
    localStorage.setItem('portfolio_lang', showFR ? 'fr' : 'en');
  } catch {
    // ignore
  }
}

// Expose for inline onclick handlers (kept intentionally minimal)
(window as unknown as { toggleLanguage: () => void }).toggleLanguage = function toggleLanguage() {
  const current = (document.documentElement.lang === 'fr' ? 'fr' : 'en') as Lang;
  setLang(current === 'fr' ? 'en' : 'fr');
};

function init() {
  const y = String(new Date().getFullYear());
  const year = document.getElementById('year');
  const yearFr = document.getElementById('year-fr');
  if (year) year.textContent = y;
  if (yearFr) yearFr.textContent = y;

  let saved: string | null = 'en';
  try {
    saved = localStorage.getItem('portfolio_lang');
  } catch {
    saved = 'en';
  }
  setLang(saved === 'fr' ? 'fr' : 'en');
}

init();

