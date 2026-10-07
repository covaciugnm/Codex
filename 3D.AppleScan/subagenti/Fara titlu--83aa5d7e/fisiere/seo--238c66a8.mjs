import { createHash } from 'node:crypto';
import { locales, normalizeLocale } from './config.mjs';

export const publicRoutes = Object.freeze(['/', '/objects', '/measure', '/spaces', '/uses', '/people', '/technology', '/documentation', '/about']);
const prefixes = { '/': 'hero', '/objects': 'object', '/measure': 'measure', '/spaces': 'spaces', '/uses': 'uses', '/people': 'people', '/technology': 'tech', '/documentation': 'docs', '/about': 'about' };
const navigation = { '/': 'nav.home', '/objects': 'nav.objects', '/measure': 'nav.measure', '/spaces': 'nav.spaces', '/uses': 'nav.uses', '/people': 'nav.people', '/technology': 'nav.technology', '/documentation': 'nav.documentation', '/about': 'nav.about' };
export const escapeHtml = value => String(value ?? '').replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));

export function publicOrigin(value = process.env.PUBLIC_BASE_URL || 'https://3dscan.eva-org.com') {
  const parsed = new URL(value);
  if (!['https:', 'http:'].includes(parsed.protocol) || parsed.username || parsed.password || parsed.search || parsed.hash || parsed.pathname !== '/') throw new Error('PUBLIC_BASE_URL must be an HTTP(S) origin without credentials, path, query or fragment');
  return parsed.origin;
}

export function pageUrl(origin, route, locale) {
  if (!publicRoutes.includes(route)) throw new Error('Unknown public route');
  const url = new URL(route, origin);
  url.searchParams.set('lang', normalizeLocale(locale));
  return url.href;
}

function translator(bundle) {
  return key => {
    const value = bundle.messages[key];
    if (typeof value !== 'string') return '';
    return value.replace(/\{\{(\w+)\}\}/g, (_, name) => String(bundle.variables[name] ?? ''));
  };
}

export function pageMetadata(bundle, route, origin) {
  const locale = normalizeLocale(bundle.locale);
  const t = translator(bundle);
  const prefix = prefixes[route];
  const product = String(bundle.variables.product || 'EVA-3dScan');
  const heading = t(`${prefix}.title`) || t(navigation[route]) || product;
  const intro = route === '/' ? t('campaign.heroIntro') || t('hero.description') || t('meta.description') : t(`${prefix}.intro`) || t('meta.description');
  const title = t(`${prefix}.metaTitle`) || (route === '/' ? t('meta.title') || heading : `${heading} · ${product}`);
  const description = t(`${prefix}.metaDescription`) || intro;
  const status = t('status.development') || 'App in development';
  const canonical = pageUrl(origin, route, locale);
  const structuredData = {
    '@context': 'https://schema.org', '@type': 'SoftwareApplication', '@id': `${origin}/#software`,
    name: product, applicationCategory: 'UtilitiesApplication', operatingSystem: 'iOS', inLanguage: locale,
    creativeWorkStatus: status, description: `${description} ${status}`.trim(), url: pageUrl(origin, '/', locale),
  };
  return { locale, heading, intro, title, description, product, status, canonical, structuredData };
}

function article(title, text, id = '') {
  return `<article${id ? ` id="${escapeHtml(id)}"` : ''}><h2>${escapeHtml(title)}</h2><p>${escapeHtml(text)}</p></article>`;
}

function pageContent(bundle, route, meta) {
  const t = translator(bundle);
  const h = escapeHtml;
  const local = path => `${path}?lang=${meta.locale}`;
  const links = publicRoutes.map(path => `<a href="${h(local(path))}"${path === route ? ' aria-current="page"' : ''}>${h(t(navigation[path]) || t(`${prefixes[path]}.title`) || meta.product)}</a>`).join('');
  const languageLinks = locales.map(locale => `<a href="${h(`${route}?lang=${locale}`)}" hreflang="${locale}" lang="${locale}">${locale.toUpperCase()}</a>`).join(' ');
  let sections = '';
  if (route === '/') {
    sections = [['objects', '/objects'], ['live', '/measure'], ['spaces', '/spaces']].map(([id, path]) => `<article><h2><a href="${h(local(path))}">${h(t(`campaign.${id}Title`) || t(navigation[path]))}</a></h2><p>${h(t(`campaign.${id}Text`))}</p></article>`).join('');
    if(t('v2.rolesTitle')) {
      sections = ['object','measure','space'].map((id,i)=>`<article><h2><a href="${h(local(['/objects','/measure','/spaces'][i]))}">${h(t(`v2.${id}Detail`))}</a></h2><p>${h(t('v2.capture'))}: ${h(t(`v2.${id}Input`))}</p><p>${h(t('v2.result'))}: ${h(t(`v2.${id}Result`))}</p><p>${h(t('v2.use'))}: ${h(t(`v2.${id}Use`))}</p></article>`).join('');
      for(const id of ['architect','designer','builder','maker','property','creator']) if(t(`v2.${id}Title`))sections+=article(t(`v2.${id}Title`),t(`v2.${id}Need`)+' '+t(`v2.${id}Deliverable`));
      for(const i of [1,2,3,4]) sections+=article(t(`v2.faq${i}Title`),t(`v2.faq${i}Text`));
      sections+=`<p>${h(t('v2.sampleOnly'))}</p><a href="${h(local('/uses'))}">${h(t('v2.nextCta'))}</a>`;
    } else for (const id of ['input', 'process', 'output']) if (t(`campaign.${id}Title`)) sections += article(t(`campaign.${id}Title`), t(`campaign.${id}Text`));
  } else if (route === '/uses') {
    const ids = Object.keys(bundle.messages).map(key => /^usecase\.([a-z0-9_-]+)\.title$/.exec(key)?.[1]).filter(Boolean).sort();
    sections = ids.map(id => {
      const title = t(`usecase.${id}.title`);
      const description = t(`usecase.${id}.description`);
      return `<article id="usecase-${h(id)}"><h2><a href="${h(`${local('/uses')}#usecase-${id}`)}">${h(title)}</a></h2><p>${h(description)}</p></article>`;
    }).join('');
  } else {
    const prefix = prefixes[route];
    for (const key of Object.keys(bundle.messages)) {
      if (!key.startsWith(`${prefix}.`) || !key.endsWith('Title') || key.endsWith('.metaTitle')) continue;
      const stem = key.slice(0, -5);
      const text = t(`${stem}Text`) || t(`${stem}Description`) || t(`${stem}Note`) || t(`${stem}Intro`);
      if (text) sections += article(t(key), text);
    }
    // Nested content groups support translated people.<section>.title/description.
    for (const key of Object.keys(bundle.messages)) {
      if (!key.startsWith(`${prefix}.`) || !key.endsWith('.title') || key === `${prefix}.title`) continue;
      const stem = key.slice(0, -6);
      const text = t(`${stem}.description`) || t(`${stem}.text`);
      if (text) sections += article(t(key), text);
    }
    if (t(`${prefix}.note`)) sections += `<p class="note">${h(t(`${prefix}.note`))}</p>`;
    if (route === '/documentation') sections += `<p>${h(t('docs.pdfMeta'))}</p><p><a href="/downloads/EVA-3D-Scan-dossier-ro.pdf">${h(t('docs.download'))}</a></p>`;
  }
  return `<a class="skip" href="#main">${h(t('nav.skip'))}</a><header class="site-header"><div class="container header-inner"><a class="brand" href="${h(local('/'))}">${h(meta.product)}</a><nav class="navigation" aria-label="${h(t('nav.menu'))}">${links}</nav></div></header><main id="main" tabindex="-1"><section class="page-heading container"><div class="eyebrow">${h(t(`${prefixes[route]}.eyebrow`))}</div><h1>${h(meta.heading)}</h1><p class="lead">${h(meta.intro)}</p><span class="status-badge">${h(meta.status)}</span></section><section class="container section"><div class="feature-grid">${sections}</div></section></main><footer><div class="container"><p>${h(t('footer.description'))}</p><nav aria-label="${h(t('nav.language'))}">${languageLinks}</nav></div></footer>`;
}

function replaceApp(template, content) {
  const opening = /<div\b[^>]*\bid=["']app["'][^>]*>/i.exec(template);
  if (!opening) throw new Error('Public template is missing #app');
  const divs = /<\/?div\b[^>]*>/gi;
  divs.lastIndex = opening.index + opening[0].length;
  let depth = 1;
  for (let match; (match = divs.exec(template));) {
    depth += /^<\//.test(match[0]) ? -1 : 1;
    if (depth === 0) return template.slice(0, opening.index) + `<div id="app" data-ssr="true">${content}</div>` + template.slice(divs.lastIndex);
  }
  throw new Error('Public template has an unclosed #app');
}

export function renderSeo(template, bundle, route, origin) {
  const meta = pageMetadata(bundle, route, origin);
  const h = escapeHtml;
  // Escaping '<' prevents an edited database value from closing the script element.
  const jsonLd = JSON.stringify(meta.structuredData).replace(/</g, '\\u003c').replace(/\u2028/g, '\\u2028').replace(/\u2029/g, '\\u2029');
  const scriptHash = createHash('sha256').update(jsonLd).digest('base64');
  const alternatives = [...locales.map(locale => [locale, locale]), ['x-default', 'en']].map(([language, locale]) => `<link id="seo-alternate-${language}" rel="alternate" hreflang="${language}" href="${h(pageUrl(origin, route, locale))}">`).join('\n');
  const head = `<title>${h(meta.title)}</title>\n<meta name="description" content="${h(meta.description)}">\n<link id="seo-canonical" rel="canonical" href="${h(meta.canonical)}">\n${alternatives}\n<meta property="og:type" content="website">\n<meta property="og:title" content="${h(meta.title)}">\n<meta property="og:description" content="${h(meta.description)}">\n<meta property="og:url" content="${h(meta.canonical)}">\n<meta property="og:locale" content="${meta.locale}">\n<meta name="twitter:card" content="summary">\n<meta name="twitter:title" content="${h(meta.title)}">\n<meta name="twitter:description" content="${h(meta.description)}">\n<script id="seo-jsonld" type="application/ld+json">${jsonLd}</script>`;
  let html = template.replace(/<title\b[^>]*>[\s\S]*?<\/title>/gi, '')
    .replace(/<meta\b[^>]*(?:name=["'](?:description|twitter:[^"']*)["']|property=["']og:[^"']*["'])[^>]*>/gi, '')
    .replace(/<link\b[^>]*rel=["'](?:canonical|alternate)["'][^>]*>/gi, '')
    .replace(/<script\b[^>]*type=["']application\/ld\+json["'][^>]*>[\s\S]*?<\/script>/gi, '');
  html = html.replace(/<html\b[^>]*>/i, `<html lang="${meta.locale}">`).replace(/<\/head>/i, `${head}\n</head>`);
  html = replaceApp(html, pageContent(bundle, route, meta));
  return { html, scriptHash, locale: meta.locale };
}

export function robots(origin) {
  return `User-agent: *\nAllow: /\nDisallow: /api/auth/\nDisallow: /api/projects\nDisallow: /account\nDisallow: /login\nDisallow: /register\nDisallow: /projects\nSitemap: ${origin}/sitemap.xml\n`;
}

export function sitemap(origin) {
  const entries = publicRoutes.flatMap(route => locales.map(locale => {
    const alternatives = [...locales.map(language => [language, language]), ['x-default', 'en']].map(([language, lang]) => `<xhtml:link rel="alternate" hreflang="${language}" href="${escapeHtml(pageUrl(origin, route, lang))}"/>`).join('');
    return `<url><loc>${escapeHtml(pageUrl(origin, route, locale))}</loc>${alternatives}</url>`;
  }));
  return `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">${entries.join('\n')}</urlset>\n`;
}
