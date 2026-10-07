import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import { DEFAULT_LANGUAGE, LANGUAGES, type Language } from '../types';
import bg from './locales/bg.json';
import de from './locales/de.json';
import el from './locales/el.json';
import en from './locales/en.json';
import hu from './locales/hu.json';
import ro from './locales/ro.json';

const STORAGE_KEY = 'dracula.admin.lang';

export const resources = {
  ro: { translation: ro },
  en: { translation: en },
  de: { translation: de },
  hu: { translation: hu },
  bg: { translation: bg },
  el: { translation: el },
} as const;

function detectLanguage(): Language {
  try {
    const stored = localStorage.getItem(STORAGE_KEY) as Language | null;
    if (stored && (LANGUAGES as readonly string[]).includes(stored)) return stored;
  } catch {
    /* storage indisponibil */
  }
  /* Deliberat NU ne mai luam dupa `navigator.language`. Magazinul e romanesc si
     administrat din Romania, dar browserele sunt de regula pe en-US — de aceea
     adminul se deschidea in engleza ("Identity", "Placed", "Revenue", ora "02:43 PM").
     Limba implicita e romana; alegerea explicita a utilizatorului, salvata in
     localStorage, are in continuare prioritate (verificata mai sus). */
  return DEFAULT_LANGUAGE;
}

void i18n.use(initReactI18next).init({
  resources,
  lng: detectLanguage(),
  fallbackLng: DEFAULT_LANGUAGE,
  supportedLngs: LANGUAGES as unknown as string[],
  interpolation: { escapeValue: false },
});

export function setLanguage(lang: Language): void {
  void i18n.changeLanguage(lang);
  try {
    localStorage.setItem(STORAGE_KEY, lang);
  } catch {
    /* storage indisponibil */
  }
  document.documentElement.lang = lang;
}

export default i18n;
