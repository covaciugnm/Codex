import json,re,unicodedata,collections
from pathlib import Path
B=Path(__file__).resolve().parent
def norm(s):return re.sub(r'[^A-Z0-9]+',' ',unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().upper()).strip()
def readjl(p):return [json.loads(l) for l in p.read_text(encoding='utf-8').splitlines() if l.strip()]
def writejl(p,rs):p.write_text(''.join(json.dumps(r,ensure_ascii=False,default=str)+'\n' for r in rs),encoding='utf-8')
p=B/'cnp_candidati_neconfirmati.jsonl';raw=readjl(p);keep=[]
for r in raw:
 tokens=set(norm(r['nume_dosar']).split())
 if r['cnp_in_document']==1 or tokens<=set(norm(r['context']).split()):
  r['regula_selectie']='Un singur CNP valid in documentul care mentioneaza numele sau numele complet in vecinatatea CNP. Ramane neconfirmat.';keep.append(r)
archive=B/'Coocurente documente multipersoana - CNP neatribuite.jsonl'
if not archive.exists():p.rename(archive)
writejl(p,keep)
bygroup=collections.defaultdict(list)
for r in keep:bygroup[r['dosar']].append(r)
records=readjl(B/'audit_persoane.jsonl')
for r in records:r['cnp_candidati_neconfirmati']=bygroup.get(r['dosar'],[])
writejl(B/'audit_persoane.jsonl',records)
issues=readjl(B/'probleme_si_probe.jsonl');new=[];replacement={}
for r in issues:
 if r['tip']=='CNP candidat in continut disponibil':
  candidates=bygroup.get(r['dosar'],[])
  old=r['constatare'];n=len({x['cnp_candidat'] for x in candidates})
  detail=f'{n} CNP-uri candidate au context apropiat de nume sau apar singure in document. Necesita verificarea titularului si paginii; nu se atribuie automat.' if n else 'Coocurentele nume/CNP din documente multipersoana nu au context suficient pentru o candidatura individuala. Nu se atribuie niciun CNP.'
  replacement[old]=detail;r['constatare']=detail
  if not n:r['tip']='CNP mentionat doar in documente multipersoana';r['certitudine']='insuficient_pentru_atribuire'
 new.append(r)
writejl(B/'probleme_si_probe.jsonl',new)
for folder in ['dosare','directoare']:
 for p in (B/folder).glob('*.txt'):
  t=p.read_text(encoding='utf-8')
  for old,fresh in replacement.items():t=t.replace(old,fresh)
  p.write_text(t,encoding='utf-8')
s=json.loads((B/'sumar_audit.json').read_text(encoding='utf-8'));s['cnp_candidates_records']=len(keep);s['groups_with_cnp_candidates']=len(bygroup);s['raw_document_cooccurrences_not_identity_assignments']=len(raw);s['cnp_candidate_filter']='Nume complet in vecinatate sau un singur CNP in document cu numele mentionat; confirmare manuala obligatorie.';s['issues_by_type']=dict(collections.Counter(r['tip'] for r in new));(B/'sumar_audit.json').write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding='utf-8')
(B/'Sumar audit.txt').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n\nIdentitati confirmate suplimentar: identitati_confirmate_auditor.json; Mariana Burian: Mariana Burian - identitate confirmata.json.\n\nNumele folderului nu confirma titularul tuturor documentelor. Statutul CNP de completat din numele folderului este raportat separat de identitatile confirmate vizual in audit.\n',encoding='utf-8')
print({'coocurente_documente_multipersoana':len(raw),'candidati_cu_context':len(keep),'dosare_cu_candidati':len(bygroup)})
