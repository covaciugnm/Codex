from pathlib import Path
import json,hashlib,collections,datetime,re
root=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');out=root/'executie/R8_pregatire/A05'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
prior=out/'Registru_nominal_final_A05.json';d=j(prior);assert h(prior)=='a730481f4fcdffd616287cb96bd5fd6d8df3560dc37955cfb7ac58275954258a'
q={r['criterion']:r for r in j(root/'Coada_reverificari_P01.json')['rows']};by={r['criterion']:r for r in d['rows']}
def extra(i,file,message):
 p=out/file;path=p.relative_to(root).as_posix();digest=h(p);d['proofs'][path]=digest
 by[i]['observations'].append({'layer':'FINAL_QA','observed':message,'proof':{'path':path,'sha256':digest}})
def partial(k,msg):
 rr=by[k];rr['full_criterion_reexecuted']=False;rr['classification']='COMPONENTĂ_REEXECUTATĂ_REST_NEEXECUTAT';rr['verdict']='PARȚIAL_FĂRĂ_VERDICT_INTEGRAL';rr['remaining']=msg;rr['next_exact']=q[k]['next']
k='T330-R2-025';by[k]['observations']=[v for v in by[k]['observations'] if 'Matrice_T40.json' not in str(v)];partial(k,'C-24 cere export comparat prin DIFF-CLASE, MD5 jar/container și toate resursele. Au fost rulate clase explicite, inclusiv TestFefo; nu s-a rerulat exportul integral sau comparația completă de resurse. C-23 / RZ-8.3 sunt cele două criterii despre matrice.');extra(k,'JVM/TestFefo.txt','183 aserțiuni trecute; subset, nu suita completă.')
partial('T163-R2-016','Documentul 1000006 a fost pregătit din buton cu 2 poziții și conturile 607/7588. Readback detaliat al mișcărilor și 0 GL în DR există pe celălalt document 1000004 de concurs; datele celor două nu sunt îmbinate pentru un PASS.')
partial('T163-R2-033','Scanare statică actuală exactă, 11.294 fișiere urmărite, 0 NOI/rc 0. Dovada rulării înaintea fiecărui commit istoric nu rezultă dintr-o relansare curentă.')
partial('T326-R2-019','Două firme cu valori diferite și parametrul registrului probate prin JVM T03. Nu sunt publicate două liste complete pe aceleași produse și stoc în cele două firme.')
partial('T354-R2-003','Seturile testate în originalul T354: 16 seturi distincte, 0 M_StorageOnHand și 0 M_Transaction. C-2 cere toate C-3/C-4/C-7/C-9 pe același set; scenariile scriptului au seturi proprii.')
extra('T329-R2-028','T329_lots_nativ.json','În acest inventar au apărut 2 M_Lot distincte și legate de ASI pe același produs. Readbackul separat gol din Readback_native.json este după alte fixture; aici obiectele sunt nominalizate și confirmă pragul ≥2.')
partial('T354-R2-011','Garda statică actuală 0 NOI, iar pe traseul A s-au acceptat doar GET la mock. Proba complementară B s-a oprit înaintea cazurilor box/front, criteriul cere ambele.')
d['warnings'].append('Pachetele T163 C13 (două documente diferite), C30 (istoric complet), T326 K18 (două liste), T354 C2 (același set), C10 (ambele loturi) și T330 C24 (export întreg) nu sunt tratate ca reexecutări integrale. Matricea T40 este un control documentar separat.')
d['scope_correction']={'superseded_draft':prior.name,'sha256_prior':h(prior),'in_force':'Acest fișier este ediția finală A05 pentru A12/A11.'}
for row in d['rows']:
 if row['classification']=='REEXECUTAT_DOCUMENTAR':
  assert row['criterion'] in {'T329-R2-023','T329-R2-030','T330-R2-024','T330-R2-033'}
 elif row['classification']=='NUMAI_DOCUMENT_ISTORIC':
  row['verdict']='NEEXECUTAT_FĂRĂ_PROBĂ_FUNCȚIONALĂ_ACTUALĂ'
  row['remaining']='Niciun caz curent al acestei ediții nu îndeplinește cerința. Oracolul și propunerea exactă sunt păstrate în source/manual_oracle sau oracle și next_exact.'
for p,dig in d['proofs'].items():assert h(root/p)==dig
keys=sorted(set(r['classification'] for r in d['rows']));d['results_by_kind']={k:[r['criterion'] for r in d['rows'] if r['classification']==k] for k in keys};d['counts']={k:len(v) for k,v in d['results_by_kind'].items()}
d['submitted_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
final=out/'Registru_nominal_final_A05_v2.json'
assert len(d['rows'])==len(by)==sum(d['counts'].values())==135 and len(set(by)^set(r['criterion'] for r in q.values() if r['owner']=='A05' and r['category']=='FIXTURĂ_EXECUTABILĂ'))==0
with final.open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
print(h(final),d['counts'],len(d['proofs']),final.stat().st_size)
