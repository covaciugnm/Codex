import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './app/App';
import { setLanguages } from './types/common';
import './styles/global.css';
import i18n from './i18n';

const container = document.getElementById('root');
if (!container) throw new Error('#root lipsește din index.html');

async function boot() {
  try { const response = await fetch('/api/public/brand'); if(response.ok) {const brand=await response.json(); if(Array.isArray(brand.languages)&&brand.languages.length)setLanguages(brand.languages);} } catch { /* auth error screen remains available */ }
try {
  const response=await fetch('/api/dracula/admin-content');
  if(response.ok) {
    const labels=await response.json() as Record<string,Record<string,string>>;
    for(const [key,values] of Object.entries(labels))
      for(const [lang,value] of Object.entries(values))i18n.addResource(lang,'translation',key,value);
  }
} catch { /* Bundled fallback when offline. */ }
createRoot(container!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
}
void boot();
