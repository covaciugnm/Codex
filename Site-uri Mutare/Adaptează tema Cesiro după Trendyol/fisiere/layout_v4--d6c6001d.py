from pathlib import Path
import re
o=Path(__file__).parent;p=o/'build_v4.py';s=p.read_text(encoding='utf-8')
def para(prefix,new):
    global s
    found=re.findall(r"p\('"+re.escape(prefix)+r"[^\n]*\)",s)
    assert len(found)==1,(prefix,len(found))
    s=s.replace(found[0],('p('+repr(new)+')') if new else '')
para('Comunicare de testat:', '')
para('Maparea documentară a temei', 'Fiecare rând și câmp sursă are destinație: utilizare, normalizare, revizuire sau arhivare justificată. Se păstrează originalul, sursa, data, regula, aprobarea și versiunea. Arhiva brută poate preceda îmbogățirea; se publică numai loturi eligibile.')
para('Preț unitar:', 'Preț unitar = preț final / cantitate netă normalizată × unitate de referință. Se afișează pe card, fișă și coș în lei/l, lei/kg ori lei/bucată unde este relevant; la pachete mixte nu se inventează unități înșelătoare. Exemple de test: 50 lei/5 l =10 lei/l; 25 lei/50 buc. =0,50 lei/buc. Aplicabilitatea legală se confirmă pe piață. [L12]')
para('ADR03 verifică invalidarea', 'ADR03 verifică invalidarea cacheului și actualizarea E5. Totalul se validează în motor și orice schimbare cere reconfirmare. Datele inițiale sunt serializate sigur, în aceeași limbă/monedă pentru Jinja și React. Fiecare insulă deține propria zonă DOM; storefront.js/shop.js nu dublează handlerii. Testele verifică evenimentele duble și hidratarea.')
para('Bază propusă:', 'Bază propusă: Radix, Tailwind, TanStack Query unde este necesar, React Hook Form și Zod. Python repetă validarea critică. Tokenurile și componentele adminului sunt reutilizabile numai fără dependență de permisiuni administrative.')
para('Suport: ultimele', 'Suport: ultimele două versiuni stabile Chrome, Edge, Firefox, Safari și Samsung Internet; iOS/Android reprezentative. Îmbunătățiri progresive cu fallback și economisire de date. Prefetch doar pentru pagini publice sigure, fără efecte comerciale ori date personale.')
p.write_text(s,encoding='utf-8')
print('Paginare corectată')
