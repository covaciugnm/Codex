import json,hashlib,pathlib,datetime
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
E=R/'executie'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
rub=read(R/'A11_rubrica_control.json')
base=read(R/'A11_verdict_plan.json')
d=E/'delta/2026-11-02T15-00-35-559Z'
def emit(z,p,exp,blocked,metrics,issues):
 assert h(p)==exp
 dd=read(p)
 cs=[{'id':q['id'],'score':(0 if q['id'] in blocked else 0.2),'reason':blocked.get(q['id'],'Plan parent déjà accepté: contrôle inchangé et non affecté, ou explicité dans le supplément.')} for c in rub['criteria'] for q in c['plan_subchecks']]
 for x in cs:
  if x['id'] not in blocked: x['reason']='Cerința planului semnat rămâne satisfăcută în domeniul suplimentului; nu se reevaluează execuția.'
 v={'schema':'A11-gate-addendum-v1','reviewer':'A11','time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'subject':str(p.relative_to(R)).replace(chr(92),'/'),'hash_sha256':h(p),'base_plan':base['artifact_hash'],'decision':'RESPINS_REPLANIFICARE','scope':'Poartă de plan, independentă; fără execuție suplimentară. Planul inițial rămâne nemodificat.','checked_inputs':metrics,'scores':cs,'earned':50-len(blocked),'out_of':50,'plan_score':(50-len(blocked))/5,'open_blockers':['HB04','HB09'],'fixes':issues,'implementation_score':None}
 out=E/('A11_gate_'+z+'_R1.json');out.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(z,h(out),v['plan_score'])
p=d/'Addendum_plan.json'
dp=read(p);ex=read(d/'Inventar_P01_supplement.json');orig=read(R/'Inventar_P01.json')
changed={x['technical'] for x in ex['rows'] if x['in_individual_review']}-{x['technical'] for x in orig['rows'] if x['in_individual_review']}
assert changed=={'T352'}
assert {x['technical'] for x in orig['rows'] if x['in_individual_review']} <= {x['technical'] for x in ex['rows'] if x['in_individual_review']}
assert all(h(d/f['name'])==f['sha256'] for f in dp['sources'])
emit('delta_P01',p,'df4b2681f4fba1f03b599652930ebaec70830133549d56c7f588ce6528bcca2a',{
'QC01-P2':'Titularul material T366/A05 lipsește; T352 A12 auditor task ≠ A06 titular de zonă; coexecutori diferă de inventar fără dispoziție.',
'QC02-P2':'Nu există mapare nominală criterii originale T352/T366 la un control, pipeline și probă; atribuiri A02/A09 fără flux concret.',
'QC02-P4':'Cantități suplimentare furnizor în bucăți/procent, modificare AI și funcții rapide nu apar în teste.',
'QC02-P5':'T366 are doar verificarea stării «montat», fără criteriul pe rând/per produs + confirmare.',
'QC04-P2':'Nu există oracle specifice procent/bucăți/rotunjire și modificări rapide/AI în condiții neautorizate sau ambigue.',
'QC06-P3':'Nu există handoff bilateral backend WMS/inventar T366; titularii din inventarul T352/A01/A05/A07 trebuie să aibă o decizie explicită.',
'QC09-P1':'Pentru T366 lipsesc probă, caz pozitiv/negativ, rezultat de linie versus întregul document și identitatea cabinetului instalat.',
'QC10-P1':'Șablonul 36 A12 este referit, însă lipsește legarea semantică a fiecărei cerințe suplimentare la rezultat/dovadă.'},
{'matching_files':len(dp['sources']),'before':[len(orig['rows']),sum(x['in_individual_review'] for x in orig['rows'])],'after':[len(ex['rows']),sum(x['in_individual_review'] for x in ex['rows'])],'added':list(changed),'removed':[],'frozen_rows_added_or_changed':[{'id':x['technical'],'index':x['registry_index'],'title':x['title'],'requirement_quote':x['requirements'],'business_owner':x['owner'],'secondaries':x['secondary'],'delivery':x['declared_delivery']} for x in ex['rows'] if x['technical'] in ('T352','T366')]},
['T352: declinați fiecare cerință sursă din /rows/962 în oracle număr/procent, responsabil autorizat, stoc fizic versus supliment furnizor/ETA, AI și funcții rapide confirmate/persistate; includeți cote/rotunjire și neaplicarea unei modificări respinse.','T366: repartizați A12→A05, indicați tabele/procese și stări, operația rând 1 versus rând 2, 0/negativ/anulare/retry/document fără validare globală. Verificați 60048769789 și calea raportului r57 pe cabinet precis; eticheta «montat» nu închide cerința.','Mapare de titular/control/flux/artefact și decizie pentru toți titularii declarați / propuși; păstrați rezultatul celor trei taskuri active ca delta administrativă.'])
p=E/'A09/A09_addendum_android.json';android=read(p);m=read(E/'A09/android_source_manifest.json');src=pathlib.Path(m['source_root']);rows=m['files'];bad=[]
for x in rows:
 if 'sha256' in x:
  raw=(src/x['path']).read_bytes()
  if hashlib.sha256(raw).hexdigest()!=x['sha256'] or hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\x00'+raw).hexdigest()!=x['blob']:bad.append(x['path'])
assert not bad and h(pathlib.Path(m['apk']['copy']))==m['apk']['sha256']
emit('android',p,'182f638890c9642e26524ac6e00f3a266530217d30492cee604ca5b534dba081',{
'QC01-P3':'181/199 surse materializate; 18 fără dispoziție explicită, inclusiv parametrii Gradle și reguli ProGuard pentru build reproductibil.',
'QC02-P2':'Liste distincte de AND01–06 față de taskuri/controale/fluxuri semnate; lipsesc muchiile per AND.',
'QC04-P3':'Răspunsul pierdut trebuie separat de commitul real; lipsește corelarea client/API/document/DB pe operație.',
'QC05-P2':'Lipsește oracol cantitativ pentru documente/mișcări, aceeași cheie și un act nou legitim. MockWebServer nu probează efect ERP.',
'QC06-P3':'Sunt indicate roluri, dar nu furnizor/consumator cu dovadă solicitată pentru granița AND–A01/A05/A09/A10/A12.',
'QC09-P1':'Lipsesc legături la comenzi/module de reproducere, artefact individual per AND și alternativa verificabilă dacă AVD lipsește.',
'QC10-P1':'Lipsesc matricea individuală de trasabilitate și șablonul dovezii AND individuale.'},
{'manifest_sha256':h(E/'A09/android_source_manifest.json'),'declared_and_matching_android_sha':m['sha'],'tracked':len(rows),'git_blob_and_sha256_independently_checked':sum('sha256' in x for x in rows),'not_materialized':[x['path'] for x in rows if 'sha256' not in x],'apk_sha256_recomputed':h(pathlib.Path(m['apk']['copy'])),'adb_devices_at_snapshot':m['adb_inventory'],'and_ids':[c['id'] for c in android['controls']]},
['Mappați individual AND→titular principal/perechi de interfață→task/motiv N/A→control/flux părinte→comandă/modul→oracol și fișier probator. Includeți acceptul A01/A05/A09/A10/A12 la predare.','Dispuneți cele 18 fișiere în afara copiei, inclusiv build.gradle.kts, settings.gradle.kts, gradle.properties, app/proguard-rules.pro și tools/proba_emulator.sh. Înregistrați materializarea prin blob înainte de build sau limita exactă, păstrând sha original și fără chei private.','AND03/04: problemă înainte versus după commit; aceeași cheie→0/1 mișcări, altă trimitere comercial legitimă→1 nouă, actor/firma schimbată→0 efect în străinătate. Instrumentați ID/DB/terminal real separat de mock, rollback și cleanup.','Păstrați separat semnarea pachetului, reproducibilitatea sursă→APK și hardware fizic/AVD; indisponibilitatea este NEEXECUTAT.'])

