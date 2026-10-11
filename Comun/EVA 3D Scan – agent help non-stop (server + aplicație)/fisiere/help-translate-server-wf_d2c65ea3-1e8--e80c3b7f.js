export const meta = {
  name: 'help-translate-server',
  description: 'Translate EVA 3D Scan server help content RO into 6 languages',
  phases: [{ title: 'Translate' }],
}
const LANGS = [
  ['en', 'English'], ['de', 'German (Hochdeutsch, Sie-Form wie in der App, korrekte Umlaute ä ö ü ß)'], ['fr', 'French (typographie française, espaces insécables U+00A0 avant ; : ? ! et dans « »)'],
  ['es', 'Spanish (neutral, tú as in the app)'], ['hu', 'Hungarian'], ['bg', 'Bulgarian (Cyrillic)'],
]
const prompt = (code, name) => `You are a professional translator. Translate the help content of the website EVA 3D Scan from Romanian into ${name}. Work only via: ssh -o BatchMode=yes saga-server@192.168.100.151 '<cmd>'. Do NOT touch git or any repo file.

Source: ~/work/helpwriter-tmp/ro-server.json (schema eva.help.server-content/1). Output: ~/work/helpwriter-tmp/out/${code}.json (mkdir -p), same JSON structure and keys exactly, "locale": "${code}". Translate every value of sections, topics.*.title/summary/slides.*.title/body and tips.*.*.what/does. Keep \\n paragraph breaks, keep the placeholder {label} unchanged, keep numbers, units, file formats, URLs (https://3dscan.eva-org.com/ajutor/), API routes, HTTP headers, error codes (e.g. invalid_email) and keyboard key names unchanged except the usual localized key names (e.g. Leertaste, Entrée only if natural; arrows). Product names stay: EVA 3D Scan, EVA-3dScan, EVA, EVA Print, App Store, LiDAR.

Terminology (MANDATORY, consistent): use this glossary from Site/docs/HELP_ARHITECTURA.md §5.3 in ~/work/3dscan-helpwriter (read it: sed -n 310,337p Site/docs/HELP_ARHITECTURA.md). Quoted UI labels („…” in Romanian) MUST be replaced by the real label the site shows in ${name}: look them up in ~/work/3dscan-helpwriter via git show origin/main:Site/content/locales/${code}.json (public SPA labels; compare with ro.json same keys), git show origin/main:Site/db/site-i18n/${code}.json (account/library pages, keys site.*), and git show origin/main:Site/db/app-i18n/${code}.json (app terms like Library/Help). For help-widget labels not in those files (e.g. „Ce e asta?”, „Ce face”, „Mai mult în ajutor”, „Apăsare lungă = ajutor”, „Tasta ? deschide ajutorul”, „Deschide în portal”, „Copiază linkul”, „Filă nouă”, „Deschide linkul”, „Link copiat”, „În pregătire”, „Atinge un element ca să afli ce face”, „Anulează”, „Redă”, „Pauză”, „Înapoi”, „Înainte”) translate naturally and use the glossary where given; use typographic quotes of ${name}.

Hard rules (validated by machine): plain text only — no < > characters, no ** __ backticks or ](, no line starting with "# ", "- ", "* ", "+ ", "> "; no tabs or invisible/bidi/zero-width chars (U+00A0 and U+202F allowed); no URLs other than https://3dscan.eva-org.com/...; no email addresses. Length limits: title ≤ 120, summary ≤ 400, slide body ≤ 1200, what ≤ 300, does ≤ 600 characters. Natural, clear, second person, the same meaning — do not add or drop facts.

Then validate: build a test dir: rm -rf ~/work/helpwriter-tmp/v-${code} && cp -r ~/work/helpwriter-tmp/t ~/work/helpwriter-tmp/v-${code} && for l in ro en de fr es hu bg; do cp ~/work/helpwriter-tmp/out/${code}.json ~/work/helpwriter-tmp/v-${code}/server/$l.json; sed -i "s/\\"locale\\": \\"${code}\\"/\\"locale\\": \\"$l\\"/" ~/work/helpwriter-tmp/v-${code}/server/$l.json; done; cd ~/work/helpwriter-tmp && node validate.mjs v-${code}  — must print errors: 0 (ignore the "sedilă" rule, it only applies to ro). Fix and repeat until 0. Write files by creating them locally in your scratchpad and piping via ssh stdin (cat > file), using UTF-8.

Final message: one line "OK ${code} <n strings> errors 0" or the remaining problem.`
const res = await parallel(LANGS.map(([c, n]) => () => agent(prompt(c, n), { label: 'translate:' + c, phase: 'Translate' })))
return res
