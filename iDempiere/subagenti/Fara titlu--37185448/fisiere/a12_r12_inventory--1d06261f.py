import collections, copy, gzip, hashlib, json, pathlib, re, subprocess
from datetime import datetime, timezone

B=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
E=B/'executie'; OUT=E/'R12_plan_delta'; A=OUT/'A12'; A.mkdir(exist_ok=True)
BASE='2fe90ed3f128c33dff7cf9f8674e664a70679390'
HEAD='df85d33c1648ce2b2df130a60a05ef696e2e5480'
UTC=datetime.now(timezone.utc).isoformat()
REPO='/home/saga-server/Documents/EvA-Contab'
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):
    b=p.read_bytes(); return {'path':p.relative_to(B).as_posix(),'sha256':sha(b),'bytes':len(b)}
def save(p,d):
    assert not p.exists(), str(p)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def gz(p,raw):
    assert not p.exists(), str(p)
    p.write_bytes(gzip.compress(raw,mtime=0))
    return dict(ref(p),raw_sha256=sha(raw))
def gzrows(p,rows): return gz(p,('\n'.join(json.dumps(r,ensure_ascii=False,separators=(',',':')) for r in rows)+'\n').encode())
def readgz(p):
    with gzip.open(p,'rt',encoding='utf-8-sig') as f:return [json.loads(l) for l in f]
def tree(commit):
    cmd=['ssh','-o','BatchMode=yes','saga-server@192.168.100.151',f'git -C {REPO} ls-tree -r -z {commit}']
    p=subprocess.run(cmd,capture_output=True,check=True)
    records={}
    for item in p.stdout.split(b'\0'):
        if not item:continue
        meta,path=item.split(b'\t',1); mode,typ,oid=meta.decode().split();name=path.decode('utf-8')
        records[name]={'path':name,'mode':mode,'type':typ,'git_object':oid}
    receipt={'command':cmd,'exit_code':p.returncode,'stdout':gz(A/f'Arbore_{commit[:8]}.nul.gz',p.stdout),'entries':len(records),'stderr':p.stderr.decode('utf-8')}
    return records,receipt

raw=load(OUT/'Inventar_delta_brut.json'); assert raw['base']==BASE and raw['head']==HEAD
source_manifest=load(OUT/'Manifest_sources_lues.json')
old_catalog=readgz(E/'R11_plan_delta/Catalog_Git_integral_per_fisier.jsonl.gz')
old_dispatch=readgz(E/'R11_plan_delta/Dispatch_tehnic_integral.jsonl.gz')
old_by={r['path']:r for r in old_catalog}; dispatch_by={r['path']:r for r in old_dispatch}
controls=load(E/'R11_plan_delta/Manifest_Dispatch_tehnic_integral.json')['controls']
old_tree,old_receipt=tree(BASE);new_tree,new_receipt=tree(HEAD)
assert len(old_tree)==len(old_catalog)==182912
assert all((r['git_object'],r['mode'],r['type'])==(old_tree[r['path']]['git_object'],old_tree[r['path']]['mode'],old_tree[r['path']]['type']) for r in old_catalog)
delta={r['path']:r for r in raw['rows']}; actual_delta={}
for path in sorted(set(old_tree)|set(new_tree)):
    old=old_tree.get(path);new=new_tree.get(path)
    if old!=new:
        actual_delta[path]={'path':path,'status':'A' if old is None else ('D' if new is None else 'M'),'old_oid':old['git_object'] if old else '0'*40,'new_oid':new['git_object'] if new else '0'*40,'old_mode':old['mode'] if old else '000000','new_mode':new['mode'] if new else '000000'}
assert actual_delta==delta, 'Independent trees differ from raw diff'
assert len(new_tree)==183469 and len(delta)==565
assert collections.Counter(r['status'] for r in delta.values())=={'A':557,'M':8}
old_preservation=[]
for r in old_dispatch:
    path=r['path'];b=old_tree[path];n=new_tree[path]
    assert (b['mode'],b['git_object'])==(n['mode'],n['git_object'])
    old_preservation.append({'id':r['id'],'path':path,'base_mode':b['mode'],'head_mode':n['mode'],'base_oid':b['git_object'],'head_oid':n['git_object'],'exact_equal':True,'owner':r['owner'],'peer':r['peer'],'R12_execution_credit':None})
assert len(old_preservation)==6709

sources={}; source_refs={}
for r in source_manifest['rows']:
    p=pathlib.Path(r['local']);data=p.read_bytes()
    assert sha(data)==r['sha256']
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==new_tree[r['path']]['git_object']
    sources[r['path']]=data.decode('utf-8-sig');source_refs[r['path']]=dict(ref(p),git_object=r['new_oid'],source_path=r['path'])
assert len(sources)==27
technical_new=sorted(p for p in delta if pathlib.PurePosixPath(p).suffix in ('.py','.sh'))
assert len(technical_new)==19 and sum(p.startswith('Documentatie/') for p in technical_new)==16
live_dir=E/'delta/2026-11-02T22-49-25-027Z';live=load(live_dir/'00_STATUS_TASKURI.json')
live_comparison=load(live_dir/'Comparatie_ultimul_checkpoint.json')
assert len(live)==996 and sum(r.get('proiect')=='P01' for r in live)==693
assert live_comparison['changes']==[]
live_by={r['id']:(i,r) for i,r in enumerate(live) if r.get('proiect')=='P01'}
old_tasks=load(E/'R11_plan_delta/A12_registru_693_stari_alias_v2.json')['rows']
old_tasks_by={r['technical']:r for r in old_tasks}

def group(path):
    if '/T232-' in path:return 'T232'
    if '/T240-' in path or '/t240/' in path:return 'T240'
    if '/T343-' in path:return 'T343'
    if '/T224-' in path:return 'T224'
    if '/T18-' in path:return 'T225'
    if path=='Documentatie/help/00_DEFECTE_GASITE.md':return 'SHARED_HELP'
    return 'SHARED_REGISTRY'
ROUTING={
 'T232':('A01','A09','A01.C13','A09-C04'),
 'T240':('A08','A09','A09-C25','A01.C13'),
 'T343':('A06','A01','A06-C19','A01.C13'),
 'T224':('A04','A03','A04-C13','A03.CK23'),
 'T225':('A04','A02','A04-C13','A02.C009'),
 'SHARED_HELP':('A08','A09','A09-C25','A01.C13'),
 'SHARED_REGISTRY':('A12','A11',None,None)}
def task_ref(t):
    if t not in live_by:return None
    i,r=live_by[t];prior=old_tasks_by[t];canonical=prior['canonical']
    assert canonical is None or canonical in r['denumire'] or canonical==r.get('cod_capitol')
    return {'technical':t,'canonical':canonical,'title_as_declared':r['denumire'],'state_as_declared':r['stare_generala'],'last_edit_as_declared':r.get('ultima_actualizare'),'exact_finish_date_as_declared':r.get('finalizat_la'),'aliases_from_previous_verified_mapping':prior['alias_declared'],'source':dict(ref(live_dir/'00_STATUS_TASKURI.json'),pointer=f'/{i}'),'in_historic_652':prior['in_R10'],'R12_task_closure_credit':None}

# Individual planning contracts derived by reading these exact source files; no script below is executed.
SPEC={
 'verifica_integrare_L1.sh':('Inspectarea integrării L1: diff surse/JAR, gărzi și proveniența rapoartelor', 'Repo Git înghețat, commiturile istorice explicite, două JAR, scratch nou', 'Comparație de membri JAR prin SHA-256 independent; canar de scriere externă detectat; diferențele de cod consemnate', 'Introdu un canar inert într-o copie; elimină o clasă din copia JAR și cere diferență', 'Referă master și merge-tree --write-tree; executarea viitoare numai în copie Git izolată, niciodată repo operațional.'),
 'foi_contact.py':('Foi de contact din capturile inventariate', 'raport.tsv cu 11 ecrane și fișiere imagini sintetice; output nou', 'Fiecare captură cerută apare o singură dată; 10 ecrane/foaie, două foi pentru 11; lipsa capturii refuzată', 'Șterge o captură în fixture și compară rc/numărător; ordinea sursă păstrată', 'Imaginea arhivată nu certifică ecranul curent; generarea vizuală se verifică separat.'),
 'fragment_public.py':('Clasificarea fragmentelor mascate față de textul public din JAR', 'Mască sintetică, JAR fixat, text public și token sintetic necunoscut', 'Fragment prezent doar în resursele admise se raportează fără dezvăluirea valorii; necunoscut rc1', 'Text cunoscut în afara directoarelor publice și token cu diacritice', 'Absența unei scurgeri în aceste fișiere nu echivalează cu audit universal de date private.'),
 'reteta_L6.sh':('Orchestrarea probei native de ajutor, din meniu și buton, și restituirea clonei', 'După gate: slot oficial, clonă sintetică nouă, JAR fixat, inventar E, mască și scratch unic', 'N/N ro, minimum10 ecrane TEXTE en și Perioade en; revenire ro; JAR clone=Git; slot/container restituit la succes/refuz', 'Un rând ro eliminat produce N−1/N și rc1; întrerupere controlată verifică trap și resurse zero', 'Scriptul șterge outputuri în calea de dovezi; nu se rulează pe arhiva sigilată. Arhiva se citește, o copie izolată se pregătește numai după aprobare.'),
 'c8_lot.py':('Corelarea problemelor de referințe cu rândurile unui lot', '00_progres.tsv și două loguri refs controlate, ecran cu/fără problemă', 'Numărătorul pe ecran și constatări unice reflectă sursele, fără extindere la ecrane din alt lot', 'Log duplicat și ecran din alt lot; fără intrare nu se inventează OK', 'Scrie constatări; analiza semantică nu rezultă din numărători.'),
 'citate_butoane.py':('Compararea citatelor RO cu etichetele și literalii reali', 'Lot mic, etichete.tsv și Java din snapshot; citat existent/inexistent', 'Citatul necunoscut semnalat cu sursa exactă; numărătorul citatelor examinate separat de validarea semantică', 'Același text în alt context și citat absent; revizuire manuală a candidatului', 'Potrivirea textuală nu dovedește acțiunea butonului.'),
 'clase_corpus.py':('Controalele K1–K6 pe corpusul ajutorului', 'Inventar E, resurse RO/EN, etichete și referințe; consultanță ca sursă', 'Numitori expliciți per K1–K6; diferențele numerice/etichete/ref se disting de controalele informative', 'Mutanți unici: număr EN, etichetă inexistentă, referință nemarcată', 'K1/K5 sunt informative; K6 numără necesarul citirii, nu o certifică.'),
 'construieste_lot.py':('Generarea rapoartelor din citiri și constatări individuale', 'Lot controlat, eșantion, constatări explicite, manual și tabel V', 'Fiecare verdict generat se justifică independent printr-o citire; lipsa unei constatări nu poate servi singură drept audit pozitiv', 'Rând fără constatare și fără probă; duplicat manual/supliment; copil subprocess eșuat', 'Sursa generează OK în ramura fără constatare; acest implicit este o limită de metodă de verificat, nu verdict produs nou.'),
 'fisa.py':('Selectarea eșantionului și provenienței pentru citirea ajutorului', 'Chei rol/buton/camp impar/par, citare legală; text RO+EN duplicat', 'Selecția reproduce regulile declarate; --lista și supliment au numitori separați; primul text identic identificat', 'Câmp par fără citare exclus; legal cu cifră inclus; traducere EN diferită nu se deduplică', 'Eșantionul nu reprezintă toate câmpurile, iar deduplicarea textuală nu deduplică automat comportamentele.'),
 'garzi.sh':('Gărzi de parteneri și date personale pentru dovezile auditorului', 'Copie izolată Git și fișiere sintetice; căile fixe înlocuite numai în harness consemnat', 'Canar inert detectat; ieșiri gardă individuale, nu doar exit final; se verifică și indexul/starea izolată', 'Canar de POST și token sintetic, fără apel extern; refuzul copilului nu se pierde', 'rm -rf pe scratch fix și merge-tree --write-tree: este runner cu efecte, nu simplu text; nicio executare înainte de gate.'),
 'manual_cap.py':('Corelarea capitolului manual cu meniul, titlul și etichetele', 'Clase E, ManualEvA/ManualReges, EvaMetadata/EvaSagaMenuDef, etichete', 'Titlu și cale meniu cu ancoră exactă; citatele necunoscute listate; REGES separat', 'Titlu/etichetă schimbată doar în fixture și clasă fără capitol', 'Textul manualului nu demonstrează deschidere ZK ori drepturi native.'),
 'numara_lot.py':('Numărătorile eșantionului versus totalul lotului', 'Două loturi, câmpuri impare/pare și rânduri legale, fisa.py exact', 'Numitor total versus selectat per familie; raport independent pe același TSV', 'Rând supliment duplicat/lot străin; zero rânduri nu se confundă cu acoperire100%', 'Numărul citit efectiv trebuie dovedit independent; scriptul numără selecția.'),
 'refs_nemarcate.py':('Verificarea ancorelor de cod necitate între backtick', 'Java/TSV sintetice cu ancoră și două fișiere de același nume', 'Identificator prezent pe intervalul cerut; absent/ambiguu evidențiat separat', 'Identificator mutat în afara intervalului și basename duplicat', 'Potrivirea de text nu validează semantica cerinței.'),
 'mutanti_aud_b_r1.py':('Generarea mutanților proprii pentru lotul B T343', 'Export CESIRO1 autorizat și versiune fixată distinct de acest repo; copie temporară', 'Fiecare mutant schimbă exact ținta, compilare eșuată=NERULAT; martor original intact', 'Țintă absentă, două potriviri și mutant supraviețuitor; fiecare raportat individual', 'Dependența către al doilea repo nu moștenește SHA EVA; sursele site trebuie fixate separat; nicio anulare/rambursare externă.'),
 'rulare_aud_b_r1.sh':('Execuția comparată a mutanților într-un laborator izolat', 'După gate/slot: copie CESIRO1, container fără rețea și DB sintetică, secrete efemere nepublicate', 'Original/mutant și rc/efect individual; compilare/fixture eșuată nu înseamnă mutant ucis; retry și bilanț resurse', 'Mutant supraviețuitor versus test absent versus compilare eșuată; toate distincte', 'Necesită slot/clone și credențiale locale; pregătire internă, fără copierea sau afișarea secretelor.'),
 'test_clasa_lot_b_r1.sh':('Testul agregator LR1–LR3 al auditorului T343', 'Arhiva EVA fixată plus repo site separat fixat, garda și cele trei seturi de teste', '0 NOI și canar rc1; mutanți vii subset{A02,A07}, nerulat0 numai după revizuirea echivalențelor', 'Eșec gardă, mutant necunoscut și --fara-mutanti; nu se acordă integral când mutantul nu rulează', 'Agregarea CLI nu certifică pipeline de comandă/AWB; dovezi tranzacționale separate.'),
 'proba_buton.py':('Proba nativă din meniu→ecran→buton Ajutor→panou', 'După gate: clonă sintetică mascată, rol și AD_Menu/AD_Form, inventar E și JAR fixat', 'Observat versus așteptat din resurse exacte; ID meniu/formă, limbă RO→EN→RO și capturi mascate; erori ZK explicite', 'Panou absent, etichetă greșită, eroare/notificare ZK, captură nemascată refuzată', 'Este instrument dinamic cu citiri DB și schimbare preferință în clonă; fără execuție acum.'),
 'test_clasa_verifica_proba.py':('Testul și mutanții judecătorului rapoartelor de ajutor', 'Fixture exact12 ecrane RO/10 TEXTE EN; clase Perioade/REGES/manual/supliment', 'Raport complet12/12 și10/10; fiecare R1–R11 stricată refuzată; mutanții au caz martor care îi detectează', 'Raport lipsă/ilizibil, captură goală, duplicate și regulă slăbită; numărul nominal se verifică din lista sursă', 'Nu browser/DB; demonstrează judecătorul fixturelor, nu completitudinea ecranelor native.'),
 'verifica_proba.py':('Judecătorul raportului de ajutor și acoperirea inventarului E', 'E și raport.tsv independente, capturi locale, așteptat/observat păstrate', 'Toate R1–R11; lipsă ecran=N−1/N rc1; ilizibilrc2; EN distinct minimum10 și Perioade/restaurare', 'Elimină ecran, duplică EN, alterează zonă, titlu sau captură; fișier din afara fixturei refuzat/semnalat', 'Așteptat și observat provin din același producător; peer-ul trebuie să verifice independent un set de oracole.'),
}
assert set(SPEC)=={pathlib.PurePosixPath(p).name for p in technical_new}

edges=[]
for consumer,text in sources.items():
    if consumer not in technical_new:continue
    for target in technical_new:
        if consumer==target:continue
        name=pathlib.PurePosixPath(target).name
        for lineno,line in enumerate(text.splitlines(),1):
            if name in line:
                edges.append({'consumer':consumer,'target':target,'source_line':lineno,'text':line,'kind':'SOURCE_REFERENCE_NOT_EXECUTED','direction':'consumer_to_tool','requires_binding_review':True})
assert edges
fiches=[]
new_dispatch=[]
for path in technical_new:
    name=pathlib.PurePosixPath(path).name;t=group(path);owner,peer,control,peercontrol=ROUTING[t]
    purpose,fixture,oracle,negative,limit=SPEC[name];src=sources[path]
    ident='F'+hashlib.sha256(path.encode()).hexdigest()[:20]
    fiche={'schema':'eva.audit.r12.file-plan/1','audit_file_id':ident,'head':HEAD,'base':BASE,'source':dict(new_tree[path],sha256=source_refs[path]['sha256']),'provenance':source_refs[path],'status':'PLAN_ONLY_PENDING_A11_GATE','task':task_ref(t),'assignment':{'owner':owner,'peer':peer,'basis':'Explicit root allocation R12; T240 ownership A08 with native-help control A09-C25 shared, no invented A08 help control','control':control,'peer_control':peercontrol,'pipeline_candidates':controls['C/'+control]['candidate_pipelines'],'control_source':dict(ref(E/'R11_plan_delta/Manifest_Dispatch_tehnic_integral.json'),pointer='/controls/C~1'+control)},'objective':purpose,'actor':'Auditor autorizat în copie sintetică; rol nativ/identitate tenant numai când cazul o cere','native_reuse':'Se reutilizează instrumentul existent și AD_Menu/AD_Form/ZK ori procesul nativ numit; fără implementarea unui mecanism paralel. Componenta helper nu înlocuiește proba nativă.','fixture':fixture,'expected_oracle':oracle,'negative_or_mutant':negative,'before_after_retry':{'before':'SHA sursă și inputs, numitori, inventar resurse și starea fixturei','after':'Rezultat per caz și efecte/fișiere/DB citite din nou, ID și limite explicite','retry':'Reia pe fixture proaspătă; compară numitor și efecte, separă nondeterminismul vizual de efectele business','observed':None},'boundary':limit,'dependencies':[e for e in edges if e['consumer']==path],'consumers':[e for e in edges if e['target']==path],'postcondition':'Sursele Git și dovezile sigilate intacte; output nou; zero efecte externe; resurse proprii restituite cu inventar','axes':{'read_for_plan':True,'syntax_executed':False,'component_executed':False,'native_executed':False,'installed_binding':'UNKNOWN_CURRENT_REVISION','peer_verdict':None,'business_acceptance':None},'future_output_contract':['requirement ID or explicit unassigned','actor/role/tenant','exact source and installed version','expected→observed with units','positive and counterexample','before/after/retry IDs','fixture delta and cleanup','peer receipt separate from executor']}
    fp=A/'fise_noi'/f'{ident}.json';save(fp,fiche);fiches.append(dict(ref(fp),path_in_git=path,task=t))
    new_dispatch.append({'id':ident,'path':path,'git_object':new_tree[path]['git_object'],'mode':new_tree[path]['mode'],'family':'LIVRARE_PROBE','class':'INSTRUMENT_AUDIT_PROMOVAT' if path.startswith('Documentatie/') else 'TEST_FIXTURĂ_RUNNER','delta':'A','priority':'P0_R12_NEW_AUDIT_TOOL','owner':owner,'peer':peer,'control':control,'peer_control':peercontrol,'pipeline_candidates':controls['C/'+control]['candidate_pipelines'],'routing_rule':'R12_EXPLICIT_TASK_OWNER','task_candidates':[t],'canonical_task':task_ref(t)['canonical'],'profile':'RUNNER' if path.endswith('.sh') else 'FIXTURE','review_state':'QUEUED_NO_EXECUTION_CURRENT_HEAD','evidence_credit':None,'file_plan':ref(fp),'association_mode':'EXACT_TASK_IN_SOURCE_AND_TRACKER','execution_current_revision':False})

new_by={r['path']:r for r in new_dispatch}
catalog=[]
for path,n in sorted(new_tree.items()):
    if path in old_by:
        row=copy.deepcopy(old_by[path]);row.update(n)
    else:
        t=group(path);owner,peer,_,_=ROUTING[t]
        ext=pathlib.PurePosixPath(path).suffix
        cl='ISTORIC_DOCUMENTAR_SAU_CAPTURĂ'
        if path in new_by:cl=new_by[path]['class']
        elif ext in ('.tsv','.json'):cl='DATE_AUDIT_SAU_REGISTRU'
        row=dict(n,**{'class':cl,'family':'LIVRARE_PROBE' if path in new_by else 'ISTORIC_DOCUMENTAR','primary':owner,'peer':peer})
    row.update(head=HEAD,base=BASE,delta='UNCHANGED_EXACT_TREE' if path not in delta else delta[path]['status'],evidence_credit=None,static_read=False,runtime_tested_this_revision=False)
    row['read_for_plan']=path in sources
    row['in_technical_dispatch']=path in dispatch_by or path in new_by
    row['identity_comparison']={'base_oid':old_tree[path]['git_object'] if path in old_tree else None,'base_mode':old_tree[path]['mode'] if path in old_tree else None,'same_oid_and_mode':path in old_tree and old_tree[path]==n}
    if path in new_by:row['promoted_file_plan']=new_by[path]['file_plan']
    catalog.append(row)
dispatch=[]
for old in old_dispatch:
    row=copy.deepcopy(old);row.update(head=HEAD,base=BASE,delta='UNCHANGED_EXACT_TREE',review_state='QUEUED_NO_EXECUTION_CURRENT_HEAD',execution_current_revision=False,evidence_credit=None)
    row['R11_reference_only']={'commit':BASE,'source':ref(E/'R11_plan_delta/Dispatch_tehnic_integral.jsonl.gz'),'original_review_state':old['review_state'],'credit_transferred':False}
    dispatch.append(row)
dispatch.extend(new_dispatch);dispatch.sort(key=lambda r:r['path'])
assert len(dispatch)==6728 and len({r['path'] for r in dispatch})==6728
assert all(r['owner']!=r['peer'] for r in dispatch)

doc_rows=[]
for path,d in sorted(delta.items()):
    if not path.startswith('Documentatie/'):continue
    t=group(path);owner,peer,_,_=ROUTING[t];name=pathlib.PurePosixPath(path).name;ext=pathlib.PurePosixPath(path).suffix
    refs=[]
    for consumer,text in sources.items():
        if consumer not in technical_new:continue
        for lineno,line in enumerate(text.splitlines(),1):
            if name in line and (group(consumer)==t or t=='SHARED_HELP'):
                refs.append({'consumer':consumer,'line':lineno,'text':line,'classification':'LEXICAL_REFERENCE_REQUIRES_DIRECTION_CHECK','executed':False})
    classification='PROMOTED_EXECUTABLE_AUDIT_INSTRUMENT' if path in new_by else ('HISTORICAL_VISUAL_CAPTURE' if ext in ('.jpg','.png') else ('AUDIT_DATA_OR_TRACKER' if ext in ('.tsv','.json') else ('HISTORICAL_LOG_OR_TEXT_CAPTURE' if ext=='.txt' else 'NORMATIVE_OR_NARRATIVE_DOCUMENT')))
    doc_rows.append({'path':path,'delta':d,'classification':classification,'task_group':t,'task':task_ref(t),'owner':owner,'peer':peer,'read_for_plan':path in sources,'source':source_refs.get(path),'technical_promotion':new_by.get(path,{}).get('file_plan'),'consumer_references':refs,'consumer_status':'PROMOTED_TOOL' if path in new_by else ('REFERENCED_DATA_OR_OUTPUT_DIRECTION_UNRESOLVED' if refs else 'NO_CONSUMER_PROVEN_IN_27_BLOB_SCOPE'),'execution_credit':None,'review_obligation':'Confirmă autorul, data, versiunea sursă și dacă e input/output/oracol; orice consumator executabil se promovează explicit. Referința lexicală sau istoricul singur nu validează funcția.'})
assert len(doc_rows)==562

catalog_ref=gzrows(OUT/'Catalog_Git_integral_per_fisier_R12.jsonl.gz',catalog)
dispatch_ref=gzrows(OUT/'Dispatch_tehnic_integral_R12.jsonl.gz',dispatch)
preserve_ref=gzrows(A/'Comparatie_exacta_6709.jsonl.gz',old_preservation)
save(A/'Documentatie_562_clasificare.json',{'head':HEAD,'rows':doc_rows,'counts':dict(collections.Counter(r['classification'] for r in doc_rows)),'limitation':'Clasificare de plan: nu reprezintă citirea semantică a celor 562 artefacte; 27 bloburi total citite și hash verificate, dintre care 24 în Documentatie. Consumatori lexicali sunt candidați, nu binding executat.'})
save(A/'Dependente_19_instrumente.json',{'head':HEAD,'edges':edges,'edge_meaning':'Text exact și linie în sursa înghețată, fără executarea producer/consumer; sensul final se verifică înainte de rulare. Nu reprezintă graful complet al aplicației.','external_repo':'T343 solicită export separat CESIRO1; SHA și tree obligatorii înainte de execuție, nu transferat din EVA.'})
save(A/'Index_19_fise.json',{'head':HEAD,'count':19,'rows':fiches})
area=[]
for zone in [f'A{i:02}' for i in range(1,11)]:
    own=[r for r in dispatch if r['owner']==zone];prior=[r for r in old_dispatch if r['owner']==zone];added=[r for r in new_dispatch if r['owner']==zone]
    area.append({'owner':zone,'old_technical_files_preserved':len(prior),'new_tools':len(added),'total_dispatch':len(own),'new_paths':[r['path'] for r in added],'secondary_review_new_count':sum(r['peer']==zone for r in new_dispatch),'current_head_executions':0,'code_identity_is_not_functional_credit':True})
summary={'schema':'eva.audit.r12.intake/1','utc':UTC,'state':'PLAN_ONLY_PENDING_A11_GATE','base':BASE,'head':HEAD,'comparison_method':'Two complete git ls-tree -r -z snapshots; exact path/mode/type/OID and independent diff. No ancestry inference, no product execution.','tree_receipts':[old_receipt,new_receipt],'repository_observation':{'path':REPO,'server':'saga-server@192.168.100.151','observed_is_shallow':False,'note':'Parent shallow clone is distinct; no merge-base ancestry conclusion used.'},'counts':{'all_tracked_base':182912,'all_tracked_head':183469,'delta':565,'added':557,'modified':8,'deleted':0,'unchanged_technical':6709,'changed_old_technical':0,'new_tools_outside_archives':3,'promoted_documentation_tools':16,'new_technical_tools_total':19,'technical_dispatch_total':6728,'documentation_delta':562,'documentation_non_executable_remainder':546,'historic_completed_task_dossiers':652,'historic_criteria':2619,'live_p01':693,'live_all':996,'newly_executed_product_tests':0,'source_blobs_read_for_plan':27},'live':{'capture':'2026-11-02T22-49-25-027Z','comparison':ref(live_dir/'Comparatie_ultimul_checkpoint.json'),'population_unchanged':True,'task_states_not_modified':True,'note':'T232/T240 implementare și T343 audit rămân în afara cohortei istorice 652; fără taskuri noi inventate.'},'changed_task_groups':[{ 'group':t,'task':task_ref(t),'changed_paths':sum(group(p)==t for p in delta),'new_technical':sum(group(p)==t for p in technical_new),'owner':ROUTING[t][0],'peer':ROUTING[t][1]} for t in sorted({group(p) for p in delta})],'zones':area,'catalog':catalog_ref,'dispatch':dispatch_ref,'preserved_6709':preserve_ref,'new_fiches':ref(A/'Index_19_fise.json'),'documentary_classification':ref(A/'Documentatie_562_clasificare.json'),'dependencies':ref(A/'Dependente_19_instrumente.json'),'prior_gate':ref(E/'R11_plan_delta/A11_verdict_plan_delta_R11_v3.json'),'prior_val04':ref(E/'R11_fisiere/A12/Val_04/MANIFEST_val_04.json'),'invariant':'R11/R10 și sigiliile lor rămân imuabile. OID identic permite o comparație, nu transferă execuția sau instalarea la noul commit. Toate axele de execuție R12 sunt neexecutate.','unresolved':['A11 gate R12 încă necesar înaintea oricărei execuții','Consumatori definitivi ai celor 546 artefacte rămase: citire nominală și separare input/output/oracol; 16 scripturi promovate imediat','T343 versiunea repo CESIRO1 și izolarea după gate','T240 rețetă cu ștergere outputuri: copie izolată și scratch nou obligatorii, nu arhiva sigilată','Rapoarte generate cu OK implicit necesită revizuire semantică independentă; nu se importă verdicte automat','Cei 17 contracte R11 rămân deschiși; acest catalog nu este certificare funcțională']}
save(A/'Rezumat_inventar_dispatch_R12.json',summary)
# Verify serialized outputs and identity preservation before the external, non-circular manifest.
roundtrip=readgz(OUT/'Dispatch_tehnic_integral_R12.jsonl.gz');assert len(roundtrip)==6728
assert {r['path'] for r in roundtrip}==set(dispatch_by)|set(technical_new)
assert all(r['execution_current_revision'] is False and r['evidence_credit'] is None for r in roundtrip)
for r in roundtrip:
    if r['path'] in dispatch_by:
        old=dispatch_by[r['path']]; assert all(r[k]==old[k] for k in ('id','path','git_object','mode','owner','peer','control','peer_control'))
qa={'utc':datetime.now(timezone.utc).isoformat(),'plan_only':True,'report':ref(A/'Rezumat_inventar_dispatch_R12.json'),'checks':{'all_base_catalog_rows_equal_live_git_tree':182912,'all_new_catalog_rows':183469,'independent_delta_rows_equal_input':565,'old_technical_mode_oid_preserved':6709,'old_owner_peer_control_preserved':6709,'new_fiches':19,'owner_not_peer':6728,'new_source_blob_and_sha256_verified':27,'doc_rows_classified':562,'new_head_execution_credit':0},'issues':[],'quality_grade':None}
save(A/'QA_inventar_dispatch_R12.json',qa)
inputs=[OUT/'Inventar_delta_brut.json',OUT/'Manifest_sources_lues.json',E/'R11_plan_delta/Catalog_Git_integral_per_fisier.jsonl.gz',E/'R11_plan_delta/Dispatch_tehnic_integral.jsonl.gz',E/'R11_plan_delta/Manifest_Dispatch_tehnic_integral.json',E/'R11_plan_delta/A12_registru_693_stari_alias_v2.json',live_dir/'Comparatie_ultimul_checkpoint.json',live_dir/'00_STATUS_TASKURI.json',E/'R11_fisiere/A12/Val_04/MANIFEST_val_04.json']
artifacts=[OUT/'Catalog_Git_integral_per_fisier_R12.jsonl.gz',OUT/'Dispatch_tehnic_integral_R12.jsonl.gz']+sorted(p for p in A.rglob('*') if p.is_file())
manifest={'schema':'eva.audit.r12.inventory-manifest/1','utc':datetime.now(timezone.utc).isoformat(),'head':HEAD,'base':BASE,'state':'PLAN_PROPOSED_NO_PRODUCT_EXECUTION','artifacts':[ref(p) for p in artifacts],'inputs':[ref(p) for p in inputs],'no_self_reference':True}
save(OUT/'Manifest_A12_inventar_dispatch_R12.json',manifest)
assert all(sha((B/r['path']).read_bytes())==r['sha256'] for r in manifest['artifacts']+manifest['inputs'])
print(json.dumps({'summary':ref(A/'Rezumat_inventar_dispatch_R12.json'),'qa':ref(A/'QA_inventar_dispatch_R12.json'),'manifest':ref(OUT/'Manifest_A12_inventar_dispatch_R12.json'),'counts':summary['counts']},ensure_ascii=False,indent=2))
