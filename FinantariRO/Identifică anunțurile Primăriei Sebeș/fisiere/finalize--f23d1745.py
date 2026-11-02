import sqlite3,json,hashlib,csv,gzip,html,re,shutil,sys,time,urllib.parse
from pathlib import Path
BASE=Path(r'D:\Codex\iFLYTEK-audit');O=BASE/'results';R=Path(r'\\192.168.100.169\Comun\00.Roboti\iFLYTEK\archive-repository');C=sqlite3.connect(O/'catalog.sqlite');C.row_factory=sqlite3.Row
P=BASE/'deliverable';P.mkdir(exist_ok=True)
for n in ['00_Raport','01_Inventar','02_Functii_variabile','03_Conectare_API','04_Native_Drivere','05_Comparatii','06_Audit','07_Reproducere']: (P/n).mkdir(exist_ok=True)
def rows(sql,args=()):return [dict(r) for r in C.execute(sql,args)]
def js(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def csvout(path,rs,columns=None):
 it=iter(rs);first=next(it,None)
 if first is None and columns is None:columns=['fara_inregistrari']
 elif columns is None:columns=list(first.keys())
 op=gzip.open if path.suffix=='.gz' else open
 with op(path,'wt',encoding='utf-8-sig',newline='') as f:
  w=csv.writer(f);w.writerow(columns)
  def safe(v):
   s='' if v is None else str(v)
   return "'"+s if s.startswith(('=','+','-','@')) else s
  if first is not None:w.writerow([safe(first.get(k)) for k in columns])
  for r in it:w.writerow([safe(r.get(k)) for k in columns])
def exported(path,sql):
 cur=C.execute(sql);names=[x[0] for x in cur.description];csvout(path,(dict(zip(names,row)) for row in cur),names)
def digest(items):return hashlib.sha256('\n'.join(sorted(items)).encode()).hexdigest()
baseline=json.loads((R/'apk-analysis-2026-11-01/catalog.json').read_text());expected={v['sourceSha256']:v for v in baseline['versions']}
actual=rows('select * from versions');assert len(actual)==14 and set(v['sha256'] for v in actual)==set(expected),'input coverage mismatch'
assert not rows('select * from errors'),'parser errors remain'
for v in actual:
 meta=json.loads(v['metadata']);meta['baseline']=expected[v['sha256']];C.execute('update versions set metadata=? where id=?',(json.dumps(meta),v['id']))
# Metadata values can include credentials. Preserve the names and redacted manifest, not raw values.
C.execute("delete from evidence where category='Manifest' and kind like 'meta-data:%value'")
for row in rows("select rowid,value from evidence where kind in ('const-string','native-string') and (value like '%secret%' or value like '%api%key%' or value like '%token%' or value like '%password%')"):
 s=row['value'];s=re.sub(r'([\"\x27])([A-Za-z0-9+/=_-]{24,})([\"\x27])',lambda m:m[1]+'[REDACTAT sha256='+hashlib.sha256(m[2].encode()).hexdigest()+']'+m[3],s)
 if s!=row['value']:C.execute('update evidence set value=? where rowid=?',(s,row['rowid']))
C.commit()
for row in rows("select rowid,value from evidence where value like '%://%?%'"):
 s=re.sub(r'([?&][^=&#\s]+=)[^&#\s]*',r'\1[REDACTAT]',row['value'])
 if s!=row['value']:C.execute('update evidence set value=? where rowid=?',(s,row['rowid']))
C.commit()
for stage in ['secrets','aot']:
 C.execute("attach database ? as stage",(str(O/(stage+'-staging.sqlite')),))
 tables=[r[0] for r in C.execute("select name from stage.sqlite_master where type='table'")]
 for table in tables:C.execute('drop table if exists main.'+table);C.execute('create table main.'+table+' as select * from stage.'+table)
 C.commit();C.execute('detach database stage')
candidate_fingerprints={r[0] for r in C.execute('select distinct sha256 from key_candidates')}
token_pattern=re.compile(r'[A-Za-z0-9+/_=-]{24,128}')
for row in rows("select rowid,value from evidence where kind in ('const-string','native-string','string-pool')"):
 def mask_candidate(m):
  fp=hashlib.sha256(m[0].encode()).hexdigest()
  return '[CANDIDAT REDACTAT sha256='+fp+']' if fp in candidate_fingerprints else m[0]
 s=token_pattern.sub(mask_candidate,row['value'])
 if s!=row['value']:C.execute('update evidence set value=? where rowid=?',(s,row['rowid']))
C.commit()
# Correct pyelftools default has_dwarf_info(): .eh_frame alone is not debug variable data.
for r in rows('select * from elf_validation'):
 stat=json.loads(C.execute('select stats from artifacts where hash=?',(r['artifact'],)).fetchone()[0]);stat['has_dwarf']=bool(r['has_debug_info']);stat['dwarf_check']='strict (.debug_info/.zdebug_info), excludes unwind-only .eh_frame';C.execute('update artifacts set stats=? where hash=?',(json.dumps(stat),r['artifact']))
validation=json.loads((O/'independent-validation.json').read_text());audits=[]
for a in rows("select * from artifacts where kind='dex'"):
 h=a['hash'];s=json.loads(a['stats']);v=validation.get(h,{});ms=[r[0] for r in C.execute('select signature from methods where artifact=? and defined=1',(h,))];fs=[r[0] for r in C.execute('select signature from fields where artifact=? and defined=1',(h,))]
 checks={'classes':s['classes']==v.get('classes'),'methods':len(ms)==v.get('defined_methods'),'fields':len(fs)==v.get('defined_fields'),'method_signatures':digest(ms)==v.get('method_signature_digest'),'field_signatures':digest(fs)==v.get('field_signature_digest'),'sampled_disassembly':v.get('sampled_code_methods',0)>0,'integrity':s['checksum'] and s['signature']}
 audits.append({'artifact':h,**checks,'pass':all(checks.values()),'sampled_methods':v.get('sampled_code_methods',0),'sampled_instructions':v.get('sampled_instructions',0)})
assert all(a['pass'] for a in audits),'independent validation mismatch'
C.commit()
versions=[];manifests={};dexsets={}
for v in actual:
 b=expected[v['sha256']];mf=json.loads((R/'apk-analysis-2026-11-01'/b['manifest']).read_text());manifests[v['id']]=mf
 arts=rows('select distinct a.* from entries e join artifacts a on a.hash=e.sha256 where e.version=?',(v['id'],));ds=[a for a in arts if a['kind']=='dex'];ns=[a for a in arts if a['kind']=='elf'];dexsets[v['id']]=[a['hash'] for a in ds]
 stat=[json.loads(a['stats']) for a in ds]
 item={'id':v['id'],'package':b['package'],'version':b['version'],'variant':b['variant'],'kind':b['kind'],'sha256':v['sha256'],'bytes':mf['source']['bytes'],'components':len(mf['components']),'dex_unique':len(ds),'defined_methods':sum(s['defined_methods'] for s in stat),'method_ids_including_references':sum(s['method_ids'] for s in stat),'defined_fields':sum(s['defined_fields'] for s in stat),'classes':sum(s['classes'] for s in stat),'debug_variables':sum(s['debug_variables'] for s in stat),'native_libraries':len(ns),'decompilation_status':json.dumps(mf.get('decompilation',{})),'scope':'static; includes third-party SDKs; no runtime validation'}
 versions.append(item)
js(P/'01_Inventar/versions.json',versions);csvout(P/'01_Inventar/versions.csv',versions);exported(P/'01_Inventar/artifacts.csv','select * from artifacts');exported(P/'01_Inventar/version-artifact-map.csv','select * from entries')
# Full machine-readable exports, not truncated to the examples shown in HTML.
for table,folder in [('methods','02_Functii_variabile'),('fields','02_Functii_variabile'),('classes','02_Functii_variabile'),('variables','02_Functii_variabile'),('aot_functions','02_Functii_variabile'),('aot_field_offsets','02_Functii_variabile'),('evidence','03_Conectare_API'),('key_candidates','03_Conectare_API'),('protocol_constants','03_Conectare_API'),('native_symbols','04_Native_Drivere'),('native_dependencies','04_Native_Drivere')]:
 print('EXPORT',table,flush=True);exported(P/folder/(table+'.csv.gz'),'select * from '+table)
native=rows("select distinct e.version,e.component,e.path,e.sha256,a.stats from entries e join artifacts a on a.hash=e.sha256 where a.kind='elf'");csvout(P/'04_Native_Drivere/libraries.csv',native)
endpoints=rows("select distinct artifact,method_idx,offset,kind,value from evidence where category='Endpoint'")
def redact_url(s):
 return re.sub(r'([?&][^=&#\s]+=)[^&#\s]*',r'\1[REDACTAT]',s)
for e in endpoints:e['value']=redact_url(e['value'])
csvout(P/'03_Conectare_API/endpoints.csv',endpoints)
# Adjacent vendor versions, plus all Translate variants versus the original official build.
byvariant={v['variant']:v for v in versions};pairs=[]
bavs=sorted([v for v in versions if v['package']=='com.iflytek.bavvo'],key=lambda v:tuple(map(int,v['version'].split('.'))))
pairs += list(zip(bavs,bavs[1:]));ref=byvariant['iflytranslate-official']
pairs += [(ref,v) for v in versions if v['package']==ref['package'] and v['id']!=ref['id']]
def members(vid):
 out={}
 for h in dexsets[vid]:
  for sig,ch in C.execute('select signature,code_hash from methods where artifact=? and defined=1',(h,)):out.setdefault(sig,set()).add(ch)
 return out
diffs=[];symbolcache={}
with gzip.open(P/'05_Comparatii/method-deltas.jsonl.gz','wt',encoding='utf-8') as df:
 for left,right in pairs:
  print('DIFF',left['variant'],right['variant'],flush=True)
  a=symbolcache.setdefault(left['id'],members(left['id']));b=symbolcache.setdefault(right['id'],members(right['id']));added=set(b)-set(a);removed=set(a)-set(b);changed={s for s in set(a)&set(b) if a[s]!=b[s]}
  ea={(e['component'],e['path']):e['sha256'] for e in manifests[left['id']]['entries']};eb={(e['component'],e['path']):e['sha256'] for e in manifests[right['id']]['entries']}
  # Split filenames can change between XAPK versions; compare logical member paths as well.
  fa={e['path']:e['sha256'] for e in manifests[left['id']]['entries']};fb={e['path']:e['sha256'] for e in manifests[right['id']]['entries']}
  diffs.append({'from':left['variant'],'to':right['variant'],'added_method_signatures':len(added),'removed_method_signatures':len(removed),'changed_raw_instruction_hashes':len(changed),'added_paths':len(set(fb)-set(fa)),'removed_paths':len(set(fa)-set(fb)),'changed_path_hashes':sum(fa[k]!=fb[k] for k in set(fa)&set(fb)),'warning':'raw code hash differences can be index relocation; obfuscated name equality is not semantic equivalence'})
  for status,ss in [('added',added),('removed',removed),('raw_code_changed',changed)]:
   for s in sorted(ss):df.write(json.dumps({'from':left['variant'],'to':right['variant'],'status':status,'signature':s},ensure_ascii=False)+'\n')
csvout(P/'05_Comparatii/version-differences.csv',diffs)
old=sqlite3.connect(BASE/'prior/extracted/catalog-apk.sqlite');oldm={'L'+cl.replace('.','/')+';->'+name+desc.replace(' ','') for cl,name,desc in old.execute('select class_name,name,descriptor from functions')};oldf={'L'+cl.replace('.','/')+';->'+name+':'+typ for cl,name,typ in old.execute('select class_name,name,type_descriptor from fields')};newm=set(members(ref['id']));newf=set()
for h in dexsets[ref['id']]:newf.update(r[0] for r in C.execute('select signature from fields where artifact=? and defined=1',(h,)))
prior={'reference_apk_sha256':ref['sha256'],'prior_archive_sha256':hashlib.sha256((BASE/'prior/13673d6669020433-catalog-apk-sqlite.zip').read_bytes()).hexdigest(),'methods_prior':len(oldm),'methods_current':len(newm),'methods_only_prior':len(oldm-newm),'methods_only_current':len(newm-oldm),'fields_prior':len(oldf),'fields_current':len(newf),'fields_only_prior':len(oldf-newf),'fields_only_current':len(newf-oldf)}
js(P/'05_Comparatii/prior-catalog-comparison.json',prior)
csvout(P/'05_Comparatii/prior-signature-deltas.csv',[{'kind':k,'status':s,'signature':x} for k,a,b in [('method',oldm,newm),('field',oldf,newf)] for s,ss in [('only_prior',a-b),('only_current',b-a)] for x in sorted(ss)])
# Keep manifest evidence, with metadata credentials redacted.
from lxml import etree
for src in (O/'manifests').glob('*.xml'):
 tree=etree.parse(str(src));ns='{http://schemas.android.com/apk/res/android}'
 for el in tree.iter():
  if el.tag=='meta-data' and re.search(r'(?i)key|secret|token|password',el.get(ns+'name','')):
   if el.get(ns+'value') is not None:el.set(ns+'value','[REDACTAT]')
 target=P/'01_Inventar/manifests'/src.name;target.parent.mkdir(exist_ok=True);tree.write(str(target),encoding='utf-8',xml_declaration=True,pretty_print=True)
shutil.copy2(O/'independent-validation.json',P/'06_Audit/independent-validation.json');shutil.copy2(O/'aot-validation.json',P/'06_Audit/aot-validation.json')
csvout(P/'06_Audit/dex-cross-check.csv',audits)
checks=[{'id':'A01','check':'Toate cele 14 containere din inventarul existent, identitate SHA256','status':'PASS','observation':'12 containere vendor + 2 derivate; includ spliturile XAPK'}, {'id':'A02','check':'DEX: integritate, definitii, semnaturi, instructiuni','status':'PASS','observation':str(len(audits))+' DEX unice; definitii si semnaturi comparate integral cu Androguard; instructiuni reverificate prin esantion sistematic'}, {'id':'A03','check':'Comparatie cu vechiul catalog al APK oficial','status':'PASS' if oldm==newm and oldf==newf else 'REVIEW','observation':json.dumps(prior)}, {'id':'A04','check':'Biblioteci native: simboluri/importuri/dependente','status':'PASS','observation':'Toate fisierele .so din intrari; nu echivaleaza cu recuperarea functiilor interne stripate'}, {'id':'A05','check':'Nume de variabile originale','status':'LIMITARE','observation':'Nume disponibile numai daca exista debug_info; registrele si parametrii anonimi nu sunt nume originale'}, {'id':'A06','check':'Flutter AOT: toate versiunile','status':'DESCHIS','observation':'Catalogul AOT existent verificat numai pentru hashul original documentat; celelalte libapp.so au nevoie de recuperare AOT specifica versiunii'}, {'id':'A07','check':'Protocoale si servere validate practic','status':'DESCHIS','observation':'Constatari statice; fara executie APK, autentificare, SMS sau teste de trafic/dispozitiv'}, {'id':'A08','check':'Chei: evidenta fara valori brute','status':'PASS','observation':'Fingerprint, forma si locatie; candidatii pot fi hashuri/identificatori/teste; validitatea nu este confirmata'}, {'id':'A09','check':'Starea decompilarii JADX','status':'INFORMARE','observation':'Snapshot per versiune in versions.csv; cod DEX inventariat independent de succesul reconstructiei Java'}, {'id':'A10','check':'Scor 10/10 pentru recuperare completa','status':'NEACORDAT','observation':'Punctele A06 si A07 raman deschise. Raportul nu certifica sursa originala sau functionalitatea pe dispozitiv.'}]
csvout(P/'06_Audit/checklist-corecturi.csv',checks);js(P/'06_Audit/audit.json',{'date':'2026-11-01','result':'structural static audit passed; complete reverse engineering remains open','checks':checks,'dex':audits,'corrections':[{'issue':'Two derived inputs were still downloading in the shared work directory','fix':'Discarded incomplete input hash; downloaded immutable copies into separate local storage; checked SHA256 against release and inventory; reran all passes'},{'issue':'ELF unwind metadata could be misreported as debug information','fix':'Rechecked every ELF with strict debug_info test, updated artifact metadata; never inferred source locals from eh_frame'}]})
for file in ['audit.py','validate.py','secrets.py','aot.py','finalize.py','query.py']:
 shutil.copy2(BASE/file,P/'07_Reproducere'/file)
for file in ['run.log','run-resume.log','validate.log','validate-resume.log','secrets.log','secrets-resume.log','aot.log']:shutil.copy2(BASE/file,P/'07_Reproducere'/file)
js(P/'07_Reproducere/requirements.json',{'python':sys.version,'packages':{'androguard':'4.1.4','pyelftools':'0.33'},'dex_spec':'https://source.android.com/docs/core/runtime/dex-format','note':'Scripts contain original absolute research paths; adjust ROOT/BASE/OUT for a different machine. No APK execution required.'})
# Human report: compact matrix plus searchable evidence examples. The complete table is in SQLite/CSV.
def table(rs):
 if not rs:return '<p>Nicio înregistrare.</p>'
 cols=list(rs[0]);return '<div class="scroll"><table><thead><tr>'+''.join('<th>'+html.escape(k)+'</th>' for k in cols)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(str(r[k] if r[k] is not None else ''))+'</td>' for k in cols)+'</tr>' for r in rs)+'</tbody></table></div>'
categories=rows('select category,count(*) records from evidence group by category order by category');samples=[]
for cat in [r['category'] for r in categories if r['category']!='Manifest']:
 samples+=rows('''select e.category,e.artifact,e.method_idx,e.offset,e.kind,e.value,coalesce(m.signature,'[pool/native/asset]') as caller from evidence e left join methods m on m.artifact=e.artifact and m.idx=e.method_idx where e.category=? group by e.kind,e.value order by case when m.signature like '%/example/%' then 0 when m.signature like '%/iflytek/%' then 1 else 2 end,e.kind desc limit 160''',(cat,))
summary=[{k:v[k] for k in ['variant','version','kind','classes','defined_methods','defined_fields','debug_variables','native_libraries']} for v in versions]
stats={'containers':len(versions),'unique_dex':len(audits),'unique_elf':C.execute("select count(*) from artifacts where kind='elf'").fetchone()[0],'defined_methods_per_unique_dex':C.execute('select count(*) from methods where defined=1').fetchone()[0],'defined_fields_per_unique_dex':C.execute('select count(*) from fields where defined=1').fetchone()[0],'evidence_rows':C.execute('select count(*) from evidence').fetchone()[0],'aot_recovered_functions':C.execute('select count(*) from aot_functions').fetchone()[0]};js(P/'01_Inventar/summary.json',stats)
report='''<!doctype html><html lang="ro"><meta charset="utf-8"><title>iFLYTEK — audit APK</title><style>body{font:15px system-ui;margin:32px;max-width:1600px;color:#172b3a;background:#f6f8fb}h1,h2{color:#173f59}p{max-width:1100px;line-height:1.6}.card{padding:18px;border-radius:12px;background:white;border:1px solid #d6e1e9;margin:18px 0}.open{background:#fff3d8}table{border-collapse:collapse;background:white;width:100%;font-size:12px}td,th{padding:9px;border:1px solid #d8e1e8;text-align:left;vertical-align:top;overflow-wrap:anywhere}th{background:#e6eef5;position:sticky;top:0}.scroll{overflow:auto;max-height:620px}input{width:95%;padding:12px;margin:12px 0}a{color:#075b9c}code{background:#edf1f5;padding:2px}nav a{margin-right:18px}</style><h1>iFLYTEK — catalog și audit APK</h1><p>1 noiembrie 2026 · Analiză statică reproductibilă · Toate cele 14 containere identificate în colecție.</p><nav><a href="#inventar">Inventar</a><a href="#conectare">Conectare și media</a><a href="#comparatii">Comparații</a><a href="#audit">Audit</a><a href="#evidence">Dovezi</a></nav><div class="card open"><b>Rezultat:</b> verificarea structurală DEX este încheiată și verificată cu un al doilea parser. Recuperarea completă a codului Flutter din toate versiunile și validarea pe dispozitive rămân deschise. Nu se acordă 10/10 pentru recuperare completă. Numele originale eliminate la compilare nu pot fi certificate din aceste fișiere.</div>'''
report+='<div class="card"><h2>Ce conține livrarea</h2>'+table([stats])+'''<p><a href="../02_Functii_variabile/catalog.sqlite">Catalog SQLite complet</a> · <a href="../01_Inventar/versions.csv">Inventar CSV</a> · <a href="../03_Conectare_API/endpoints.csv">Endpointuri</a> · <a href="../04_Native_Drivere/libraries.csv">Biblioteci native</a> · <a href="../06_Audit/checklist-corecturi.csv">Checklist audit și corecturi</a></p><p>Fiecare simbol este legat de hashul DEX/ELF; <code>version-artifact-map.csv</code> leagă hashul de versiune, split și cale. CSV-urile comprimate conțin toate rândurile, fără limitarea exemplelor din această pagină. În SQLite, <code>methods.defined=1</code> înseamnă metodă definită; 0 înseamnă referință. <code>fields</code> separă aceleași categorii. <code>variables</code> conține numai informație de depanare reală. Parametrii tipizați sunt în descriptorul metodei; numele p0/p1 generate de un decompilator nu sunt nume originale.</p></div>'''
report+='<h2 id="inventar">Inventar pe versiune</h2>'+table(summary)
report+='''<h2 id="conectare">Interpretarea funcționalităților</h2><div class="card"><p>Bluetooth/BLE: referințele la GATT, dispozitive, înregistrare și redare prin căști/ochelari sunt indexate împreună cu metoda apelantă și offsetul instrucțiunii. WiFi, socketurile, USB/serial și actualizările firmware sunt inventariate separat. O bibliotecă sau un apel dintr-un SDK nu demonstrează că un anumit model de ochelari oferă funcția.</p><p>Audio/video/imagine: catalogul urmărește API-urile Android, pluginurile Flutter, codecurile și bibliotecile native. Pentru a confirma transferul efectiv sunt necesare probe cu dispozitivul: împerechere, negociere, dimensiuni pachete, ordinea mesajelor, sensul fluxului și codecurile folosite. Nu s-au dedus protocoale complete doar din nume de clase.</p><p>Multilingvism: resursele și referințele la traducere, recunoaștere, TTS, locale și limbi sunt dovezi statice. Ele nu confirmă limbi disponibile în cont, pe server, offline sau pentru fiecare dispozitiv. Disponibilitatea românei și autentificarea cu +40 cer verificare separată.</p><p>Servere/API: lista de endpointuri include și adrese SDK, documentație, teste sau șiruri neutilizate; prezența unui URL nu confirmă că este serverul de producție. Cheile candidate sunt descrise prin fingerprint și locație. Valorile nu sunt reproduse și nu au fost folosite. Hashurile și identificatorii pot produce rezultate false pozitive.</p><p>Native/Flutter: simbolurile exportate, importurile și dependențele ELF sunt complete pentru intrările analizate. Funcțiile interne stripate și variabilele locale fără DWARF nu pot fi enumerate ca sursă originală. Catalogul AOT recuperat anterior are proveniență pentru un singur hash libapp.so; adresele sale au fost verificate în segmentele executabile ale bibliotecii originale. Offseturi precum <code>field_f</code> sunt etichete structurale generate, nu nume originale de variabile.</p></div>'''+table(categories)
report+='<h2 id="comparatii">Comparații între versiuni</h2>'+table(diffs)+'<h3>Concordanță cu inventarul anterior</h3>'+table([prior])+'''<p>Diferențele de hash brut al instrucțiunilor pot proveni din schimbarea indicilor din DEX; ele nu sunt automat schimbări de comportament. Diferențele de nume obfuscate pot reflecta redenumire. <a href="../05_Comparatii/method-deltas.jsonl.gz">Lista integrală a diferențelor</a>.</p>'''
report+='<h2 id="audit">Audit, reaudit și lucrări deschise</h2>'+table(checks)+'''<p>Au fost corectate două probleme: fișierele derivate aflate încă în descărcare au fost înlocuite cu copii stabile și verificate SHA256; metadatele ELF pentru unwind au fost separate de informația reală de depanare. Reauditul compară toate semnăturile definite DEX cu Androguard și dezasamblează un eșantion sistematic de metode. Nu reprezintă o examinare manuală a fiecărei funcții sau o certificare de securitate.</p><p>Etapa următoare pentru închiderea auditului complet: recuperare AOT distinctă pentru fiecare hash libapp.so, analiză manuală a fluxurilor de interes, verificare decompilări JADX cu erori, testare pe ochelari/tablete și capturi de trafic autorizate, confirmare limbi și servicii de autentificare. Aceste puncte rămân explicit deschise.</p>'''
report+='<h2 id="evidence">Exemple de dovezi cu apelant și offset</h2><p>Exemple selectate automat pe categorii, maximum 160/categorie. Clasificarea prin termeni necesită revizuire umană. Catalogul complet se află în SQLite și <a href="../03_Conectare_API/evidence.csv.gz">evidence.csv.gz</a>.</p><input id="q" placeholder="Filtrează exemplele: Bluetooth, Gatt, sendMsgCode, Audio, USB…">'+table(samples)+'''<script>const q=document.querySelector('#q'),tb=q.nextElementSibling.querySelector('tbody');q.addEventListener('input',()=>{const s=q.value.toLowerCase();for(const r of tb.rows)r.hidden=!r.textContent.toLowerCase().includes(s)});</script><p>Specificație de referință: <a href="https://source.android.com/docs/core/runtime/dex-format">Android DEX format</a>. Comenzile, versiunile bibliotecilor și jurnalele se află în 07_Reproducere.</p></html>'''
(P/'00_Raport/index.html').write_text(report,encoding='utf-8')
js(P/'02_Functii_variabile/schema.json',rows("select name,sql from sqlite_master where type='table'"))
C.execute('pragma wal_checkpoint(truncate)');C.close();shutil.copy2(O/'catalog.sqlite',P/'02_Functii_variabile/catalog.sqlite')
hashes=[{'path':str(f.relative_to(P)).replace('\\','/'),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in P.rglob('*') if f.is_file() and f.name!='SHA256SUMS.json'];js(P/'SHA256SUMS.json',hashes)
print('DONE',stats,'prior',prior,flush=True)
