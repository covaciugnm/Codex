import json,re,html,hashlib,sys,collections
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote
B=Path(__file__).resolve().parent
def readlines(p):return [json.loads(l) for l in p.read_text(encoding='utf-8').splitlines() if l.strip()]
def writejl(p,rs):p.write_text(''.join(json.dumps(r,ensure_ascii=False,default=str)+'\n' for r in rs),encoding='utf-8')
records=readlines(B/'audit_persoane.jsonl');issues=readlines(B/'probleme_si_probe.jsonl');dirs=readlines(B/'audit_fiecare_folder.jsonl');files=readlines(B/'audit_fiecare_fisier.jsonl')
confirmed=json.loads((B/'identitati_confirmate_auditor.json').read_text(encoding='utf-8'))
mariana=json.loads((B/'Mariana Burian - identitate confirmata.json').read_text(encoding='utf-8'))
confirmed.insert(0,{'dosar':'BURIAN MARIANA SIMONA - CNP de completat','titular':mariana['nume_confirmat'],'cnp':mariana['cnp_confirmat'],'serie':'AX','numar':'512258','emitere':'2013-03-20','valabil_pana':'2023-12-07','sursa':mariana['surse'][0]['path'],'pagina':1,'verificare':mariana['verificare'],'observatie':'Confirmare suplimentara in raportul Revisal/CIM. CI gasita are termen trecut; nu confirma un CI actual.'})
for d in confirmed:
 issue={'dosar':d['dosar'],'tip':'CNP si CI confirmate vizual in sursa externa','certitudine':'confirmat_vizual_auditor','constatare':f"{d['titular']}: CNP {d['cnp']}, CI {d['serie']}{d['numar']}, emitere {d['emitere']}, termen {d['valabil_pana']}. {d['observatie']} Originalele si registrul istoric nu au fost modificate.",'probe':[d['sursa']],'prioritate':1}
 issues.append(issue)
 for r in records:
  if r['dosar']==d['dosar']:r.setdefault('identitate_confirmata_in_audit',[]).append(d)
  
 # Add the verified finding at the beginning of the corresponding source-group file.
 fn=re.sub(r'[<>:"/\\|?*]','_',d['dosar'])+'.txt';p=B/'dosare'/fn
 if p.exists():p.write_text('CONSTATARЕ CONFIRMATA\n'+issue['constatare']+'\nSursa: '+d['sursa']+'\n\n'+p.read_text(encoding='utf-8'),encoding='utf-8')

# Candidate file links from the external identity archive, without identity assignment.
root=Path(r'Z:\2019\SCANARI\Copii Buletine')
import unicodedata
def norm(s):return re.sub(r'[^A-Z0-9]+',' ',unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().upper()).strip()
external=list(root.iterdir());candidates=[]
for r in records:
 if r['tip_grupare']!='persoana' or r['cnp_din_dosar']:continue
 tokens=norm(r['dosar'].split(' - ')[0]).split()
 if len(tokens)<2:continue
 for p in external:
  pt=set(norm(p.stem).split())
  if tokens[0] in pt and set(tokens[1:])&pt:
   c={'dosar':r['dosar'],'sursa':str(p),'statut':'CANDIDAT DUPA NUMELE FISIERULUI - identitatea si CNP trebuie verificate in continut'};candidates.append(c);r.setdefault('surse_externe_candidat',[]).append(c)
writejl(B/'surse_CI_externe_de_verificat.jsonl',candidates);writejl(B/'audit_persoane.jsonl',records);writejl(B/'probleme_si_probe.jsonl',issues)

# One human-readable record for each physical directory, including empty ones.
(B/'directoare').mkdir(exist_ok=True)
byparent=collections.defaultdict(list)
for f in files:byparent[str(Path(f['path']).parent).casefold()].append(f)
tab=[]
for i,d in enumerate(dirs,1):
 slug=f'{i:04d}-'+hashlib.sha256(d['folder'].encode('utf-8')).hexdigest()[:12]+'.txt';d['fisa_audit']='directoare/'+slug
 direct=byparent[d['folder'].casefold()]
 lines=[d['folder'],f"Fisiere directe: {d['fisiere_directe']}; inclusiv subdosare: {d['fisiere_inclusiv_subdosare']}",f"Dosar gol in instantaneu: {d['gol']}",'Nu se deduce obligativitatea vreunui act din faptul ca o categorie este goala.','\nFISIERE DIRECTE SI ACOPERIRE:']
 for f in direct:lines += [f['path'],f"Tipuri indicate de nume (neconfirmate): {f['tipuri_indicate_de_nume']}",f"Continut: {f['acoperire_continut']}",f"Amprenta: {f['sha256']} | {f['baza_amprentei']}",'']
 lines.append('\nCONSTATARI LA NIVELUL PERSOANEI/GRUPARII:')
 for x in issues:
  if x['dosar']==d['grupare']:lines += [x['tip']+' | '+x['certitudine'],x['constatare']]+x['probe']+['']
 (B/d['fisa_audit']).write_text('\n'.join(lines),encoding='utf-8')
 tab.append('<tr><td><a href="'+d['fisa_audit']+'">'+html.escape(d['folder'])+'</a></td><td>'+str(d['fisiere_directe'])+'</td><td>'+str(d['fisiere_inclusiv_subdosare'])+'</td><td>'+('DA' if d['gol'] else 'NU')+'</td></tr>')
writejl(B/'audit_fiecare_folder.jsonl',dirs)
style='<style>body{font:15px system-ui;margin:32px;color:#163044}input{font:inherit;padding:12px;width:80%}table{width:100%;border-collapse:collapse;margin-top:24px}td,th{padding:10px;text-align:left;border-bottom:1px solid #ddd;vertical-align:top}th{background:#edf2f5}a{color:#16567d}</style>'
(B/'Audit fiecare director.html').write_text('<!doctype html><meta charset="utf-8"><title>Audit fiecare director</title>'+style+'<h1>Audit fiecare director</h1><p>'+str(len(dirs))+' directoare cu fisa individuala. Inventar la momentul instantaneului. Procesul de completare continua; continuturile inca necitite nu sunt declarate acte lipsa.</p><input id="q" placeholder="Filtreaza calea"><table><thead><tr><th>Director si fisa audit</th><th>Fisiere directe</th><th>Cu subdosare</th><th>Gol</th></tr></thead><tbody>'+''.join(tab)+'</tbody></table><script>const rows=[...document.querySelectorAll("tbody tr")];q.oninput=()=>{const s=q.value.toLowerCase();for(const r of rows)r.hidden=!r.textContent.toLowerCase().includes(s)}</script>',encoding='utf-8')

# Visible verified findings are separate from candidates in the main report.
p=B/'Audit dosare.html';t=p.read_text(encoding='utf-8');insert='<h2>Identitati confirmate in audit</h2><ul>'+''.join('<li>'+html.escape(d['titular'])+' — CNP '+d['cnp']+' — <a href="'+html.escape(Path(d['sursa']).as_uri())+'">CI sursa</a>; termen '+d['valabil_pana']+'</li>' for d in confirmed)+'</ul><p><a href="Audit fiecare director.html">Deschide toate cele '+str(len(dirs))+' de fise de directoare</a></p>'
t=t.replace('<input id="q"',insert+'<input id="q"');p.write_text(t,encoding='utf-8')
summary=json.loads((B/'sumar_audit.json').read_text(encoding='utf-8'));summary.update(verified_additional_identity_records=len(confirmed),external_CI_filename_candidates=len(candidates),directory_records=len(dirs),group_records=len(records),file_records=len(files),issues=len(issues),issues_by_type=dict(collections.Counter(i['tip'] for i in issues)))
(B/'sumar_audit.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')

class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  if tag=='a':self.links += [v for k,v in attrs if k=='href']
bad=[];links=0
for report in ['Audit dosare.html','Audit fiecare director.html']:
 parser=Links();parser.feed((B/report).read_text(encoding='utf-8'))
 for href in parser.links:
  links+=1
  if not href.startswith(('file:','http:','https:')) and not (B/unquote(href)).is_file():bad.append({'report':report,'href':href})
checks={'groups_expected':len(records),'group_txt_files':len(list((B/'dosare').glob('*.txt'))),'directories_expected':len(dirs),'directory_txt_files':len(list((B/'directoare').glob('*.txt'))),'file_records':len(files),'files_in_snapshot':len(json.loads((B/'instantaneu_fizic.json').read_text(encoding='utf-8'))['files']),'html_links_checked':links,'broken_local_report_links':bad,'confirmed_identity_source_files_exist':all(Path(d['sursa']).is_file() for d in confirmed),'mariana_verified_note_exists':(B/'Mariana Burian - identitate confirmata.json').is_file()}
(B/'Verificare livrabile.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(checks,ensure_ascii=False,indent=2))
