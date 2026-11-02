from pathlib import Path
import json,hashlib,re,subprocess,datetime,collections,zipfile
O=Path(__file__).parent;E=O.parent;R=E.parent;G=Path('D:/CodexWork/eva-audit-p01-readonly-20261102');DEPS=Path('D:/CodexWork/eva-audit-secondary-20261102');C=Path('D:/CodexWork/eva-cesiro1-contract-20261102')
def rd(p):return json.loads(p.read_bytes())
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def w(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
Z=E/'R3_zone/A08';z=rd(Z/'A08_raport.json');assert h(Z/'A08_raport.json')=='9ad85559dc071920d0bb7bd75720489da621fd2beba14d7c9ea0da235ce823d0'
for k,v in z['evidence_index'].items():assert h(E/v['path'])==v['sha256'],(k,v)
stage=rd(Z/'Eliberare_clona_A08_R3.json');dump=Path(stage['dump_synthetic']);assert h(dump)==stage['dump_sha256']
def table(schema,name):
 p=subprocess.run(['D:/CodexWork/p01-local-pg16/pgsql/bin/pg_restore.exe','--data-only','--schema',schema,'--table',name,'-f','-',str(dump)],capture_output=True,text=True,encoding='utf-8');assert p.returncode==0,p.stderr
 lines=p.stdout.splitlines();start=next(i for i,v in enumerate(lines) if v.startswith('COPY '));cols=re.search(r'\((.*)\) FROM stdin;',lines[start]).group(1).split(', ');end=lines.index(r'\.',start+1)
 return [dict(zip(cols,row.split('\t'),strict=True)) for row in lines[start+1:end]]
orders={v['id']:v for v in table('sales','orders')};histor={int(v['id']):v for v in table('sales','order_status_history')};roles={(v['admin_user_id'],v['tenant_id']):v['role']for v in table('identity','admin_tenant_roles')};assert len(orders)==6
inputs=['Probe_UI_editor_viewer_R1.json','Probe_admin_comenzi_site.json'];raw={rd(Z/v)['run']:rd(Z/v) for v in inputs};assert len(raw)==2
traces=[]
for run in z['note_case']['runs']:
 a,b=run['orderA'],run['orderB'];rg=raw[run['run']]
 assert orders[a['id']]['status']==orders[b['id']]['status']=='placed' and orders[a['id']]['payment_status']==orders[b['id']]['payment_status']=='unpaid' and orders[a['id']]['source']==orders[b['id']]['source']=='storefront-next'
 assert list(v['http']for v in rg['probes'])==[403,403,200,404,200,404,403,401,200,200,200]
 others=[x for x in histor.values()if x['order_id']==b['id']];assert len(others)==1
 own=[x for x in histor.values()if x['order_id']==a['id']];assert len(own)==4
 events=[]
 for item in run['notes_added_A']:
  v=histor[item['event']];assert roles[(item['id'],a['tenant_id'])] in ('owner','editor');assert v['actor_id']==item['id']and v['order_id']==a['id'] and v['tenant_id']==a['tenant_id'];assert v['from_status']==v['to_status']=='placed' and v['note']==item['note']
  events.append({'id':item['event'],'role_from_dump':roles[(item['id'],a['tenant_id'])],'via':'SPA' if '-UI-'in item['note'] else 'HTTP','state':'placed→placed'})
 traces.append(dict(run=run['run'],A=a['id'],B=b['id'],A_history_1_to_4=True,B_history_unchanged=True,events=events,negative_backend={'viewer_A':403,'viewer_B':403,'editor_B':404,'owner_B':404,'cross_tenant_header':403,'no_session':401},UI=[{'actor':i['actor'],'result':i['http_note'],'timeout':bool(i['limitation'])}for i in run['UI']]))
refs=rd(Z/'Ancore_site_ERP_comision.json');ann=[]
for v in refs['anchors']:
 p=(C if v['domain']=='C' else G)/v['file'];assert h(p)==v['sha256'] and v['line']<=len(p.read_bytes().splitlines());ln=p.read_text(encoding='utf8').splitlines()[v['line']-1];ann.append([v['file'],v['line'],v['symbol'],ln.strip()])
for v in refs['native_commission']:
 f=DEPS/'native'/v['native_release_source'];assert h(f)==v['source_sha256'] and v['line']<=len(f.read_bytes().splitlines())
 with zipfile.ZipFile(DEPS/v['installed_jar']) as jar:assert hashlib.sha256(jar.read(v['class'])).hexdigest()==v['class_sha256']
assert h(R/refs['AD_snapshot']['file'])==refs['AD_snapshot']['sha256']
for c in z['controls']:
 assert set(c['evidence'])<=set(z['evidence_index'])
 assert set(c['pipeline_ids'])=={p['id'] for p in z['pipelines'] if c['id'] in p['controls']}
for v in z['task_trace']:
 if v.get('r5_file'):assert h(E/v['r5_file'])==v['r5_sha256']
finds={f['finding_id']:{'controls':[c['id']for c in z['controls']if f['finding_id']in c['findings']],'pipelines':[q['id']for q in z['pipelines']if f['finding_id']in q['findings']]} for f in z['findings']};isolated=[a for a,d in finds.items()if not d['controls']or not d['pipelines']];assert isolated==['A08-F03']
f03=z['findings'][2];assert f03['finding_id']=='A08-F03';fx=rd(E/z['evidence_index']['FIX']['path']);assert 'Foreign writer' in str(fx)
ext={name:len(table('sales',name))for name in ['order_integrations','payments','shipments','invoices','outbox_messages','outbox_emails','refunds','returns','stock_reservations']};assert all(v==0 for v in ext.values())
evid=dict(dump_sha=h(dump),method='pg_restore -f - --data-only --schema ... --table ...; lectură offline, fără server sau operații live.',sales_orders_count=len(orders),observed_synthetic_history_count=len(histor),success_runs=traces,external_counts_from_final_dump=ext,src_anchors=ann,commercial_case_f03_provenance={'path':z['evidence_index']['FIX']['path'],'sha256':h(E/z['evidence_index']['FIX']['path']),'selector':f03['selector']},commission_source_classes_and_jar=refs['native_commission'],visual_readback='Editor/owner: lista Istoric și Note interne, salvare afișată; viewer 360px poate apăsa butonul și primește refuz în UI. O captură singură nu identifică actorul. ID și grant au fost extrase independent din dump.',unlinked_findings=isolated)
w(O/'offline.json',evid)
orig=rd(E/'A11_control_zone_R2_lotC.json')['reports']['A08'];rub=rd(R/'A11_rubrica_control.json');masks=['11111','00010','11111','11110','10001','10000','11111','11011','11001','11100']
explan=['49 amprente de evidență, roluri și frontiere ale scope-ului. Dumpul SQL conține realmente șase comenzi, din care patru aparțin celor două execuții valide citate.', '18 taskuri candidate, 10 fișe secundare, cu delimitare; niciun credit comercial transferat din EX. F03 lipsește din indexurile inverse.', 'R3 leagă browser → POST cu actor/grant confirmat → ID persistent din sales.order_status_history. Două execuții separate, ferestre și o tentativă inițială cu erori păstrate. QC03-R1 și R4 sunt acordate pentru observațiile UI verificate în domeniul declarat.', 'Stările comenzii A și comenzii de control B sunt confruntate după scriere împreună cu actorul, fără vreo schimbare de status. QC04-R3 acordat. Niciun ordin administrat în ERP sau marketplace nu este dedus din aceasta.', 'Înregistrări SQL confirmate pe copie offline; 9 efecte conexe rămân zero în acest fixture. Nu sunt certificate toate rutele, declanșatoarele și registrele de produs.', 'O singură operație locală trasabilă; 7 fluxuri rămân incomplete și canalele reale/ERP nu sunt substituite de administratorul local.', 'Actor și apartenență înregistrate server-side, actor viewer A403/B403, editor/owner B404, fără sesiune 401; nimic despre rolul de comisionar pe acest token.', '5 modele de comision și procesul CommissionCalc se regăsesc în Git și JAR-urile instalate. AD nu dovedește configurare operațională, situații private, cote sau export.', 'Dovezi reproductibile pentru efecte și controale în fixture, inclusiv prima tentativă cu 500; test de încărcare și recuperare cross-system lipsesc.', 'F11 confirmat în limite. Eșecurile sunt păstrate; F03 apare în tabel dar nicio legătură către control/flux. Nu se poate închide registrul sau nota globală.']
criteria=[]
for c,m,o,msg in zip(rub['criteria'],masks,orig['scores'],explan):
 rows=[dict(id=x['id'],text=x['text'],earned=0.2 if b=='1'else 0,prior=r['earned'])for x,b,r in zip(c['report_subchecks'],m,o['subchecks'])];criteria.append(dict(id=c['id'],title=c['title'],earned=round(sum(x['earned']for x in rows),1),rationale=msg,subchecks=rows))
score=round(sum(c['earned']for c in criteria),1)
result=dict(reviewer='A11',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='A08-R3',source='R3_zone/A08/A08_raport.json',sha256=h(Z/'A08_raport.json'),quality_score=score,eligible_subchecks=sum(m.count('1')for m in masks),out_of=50,previous_quality=orig['R2_score'],product_score=None,gate='RELUARE; F11 confirmat în limite',criteria=criteria,independent_readback={'path':'A11_reproduceri_A08R3/offline.json','sha256':h(O/'offline.json'),'method_hash':h(O/'audit.py'),'source_anchors':len(ann),'native_classes':6,'hashes_of_index':49,'new_notes':6,'certified_business_order_status_changes':0,'network_or_marketplace_status_test':False,'viewports':[360,1280],'cross_scope':'store_customer, agent comercial, administrator C și utilizator ERP sunt identități distincte.'},correction_history={'C1_to_C3':'Owner A eMag200/Trendyol409, B Trendyol200 separat; revocare cu fereastră SPA 200/200 iframe 1; pointer /results/theme_invalid~1a.', 'initial_clone':'GET detaliu 500 la prima încercare. Datele nu se agregă cu cohorta celor două rulări valide.'},
controls=[dict(id=c['id'],source_state=c['status'],decision='CONFIRMAT_COMPONENTĂ_LOCALĂ' if c['id']=='A08-C14'else 'NATIVE_IDENTIFICATE; SITUAȚIILE_PRIVATE_RĂMÂN_NEEXECUTATE' if c['id']=='A08-C16' else 'ACCEPT_ÎN_STRATUL_DECLARAT; FĂRĂ_PROMOVARE_GLOBALĂ',observed=c['observed'],remaining=c['remaining'],findings=c['findings'])for c in z['controls']],pipelines=[dict(id=p['id'],source_status=p['status'],full_accepted=False,remaining=p['remaining'])for p in z['pipelines']],
findings=[dict(id=k,title=next(f['title']for f in z['findings']if f['finding_id']==k),edge_controls=v['controls'],edge_pipelines=v['pipelines'],disposition=('CONFIRMAT_PROFIL_MUTAT_PE_CHECKOUT_ANONIM_DAR_FĂRĂ_TRASABILITATE_STRUCTURATĂ' if k=='A08-F03' else 'CONFIRMAT_NOTĂ_SITE_OPERARE_LOCALĂ; FĂRĂ_TRANZIȚIE_DE_STARE/ERP/CURIER'if k=='A08-F11'else 'MENȚIN_DISPOZIȚIA_PE_COMPONENTA_PROBATĂ'))for k,v in finds.items()],
corrections=[{'id':'A08R3-Q1','scope':'A08-F03 este singurul finding orfan în indexul control/pipeline: 0 și 0.','next':'Leagă proba checkout anonim cu e-mail existent de un control real pentru integritatea identității/datele de checkout și A08-P03. Evaluează dacă C11/C05 acoperă explicit condiția; altfel înregistrează subcerința de integritate la controlul aplicabil. Confirmă invers prin ID și păstrează scenariul cu cont inactiv.'},{'id':'A08R3-Q2','scope':'F11 dovedește adăugarea unei note în istoricul unei comenzi, cu stare placed→placed.','next':'Politica utilizatorului rezervă administrarea iDempiere. Separă afișarea locală și plasarea comenzii de operații administrative; urmărește în ERP identitatea, dreptul și efectul unei note. Nu folosi drepturile owner/editor ale site-ului pentru a certifica comisionarul. Nu se solicită o anulare reală sau un test pe marketplace.'},{'id':'A08R3-Q3','scope':'C16 și granița publică a F01.','next':'Configurează două identități de comisionar în același canal și un al doilea canal; verifică filtrele DB, exportul și refuzurile pe alt agent. Pe F01 confruntă read-only topologia instalată și rutele active, păstrează diferența dintre expunerea la serviciu și expunerea publică.'}])
p=E/'A11_control_A08_R3.json';w(p,result);print(h(p),score,h(O/'offline.json'))

