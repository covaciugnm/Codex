import pathlib,json,gzip,hashlib,datetime,collections
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');B=R/'executie/R12_fisiere';L=B/'A05_Comanda_rezervare_lot05';O=B/'A11/Val05_loturi'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return {'path':p.relative_to(R).as_posix(),'sha256':sha(p)}
def enc(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
checks=[]
def ck(n,b):checks.append({'check':n,'ok':bool(b)});assert b,n
bf=L/'migration_original_v2.baseline_rows.json.gz';base=json.loads(gzip.decompress(bf.read_bytes()));names=['migration_original_v2.readback_01_migration_before.json','migration_original_v2.readback_02_migration_after_1.json','migration_original_v2.readback_03_migration_after_2.json'];snap=[j(L/n) for n in names]
for k,rows in base.items():ck('Baseline brut '+k,hashlib.sha256(enc(rows)).hexdigest()==snap[0]['fingerprints'][k]['sha256'] and len(rows)==snap[0]['fingerprints'][k]['count'])
current=base;row_counts=[]
for stage,s in enumerate(snap[1:],1):
 ck('Readback readonly '+str(stage),s['session']['readonly']=='on')
 rebuilt={}
 for k,delta in s['changes'].items():
  counts=collections.Counter(enc(x) for x in current[k]);remove=collections.Counter(enc(x) for x in delta['removed']);add=collections.Counter(enc(x) for x in delta['added']);ck(f'Retraits existants {stage} {k}',all(counts[x]>=n for x,n in remove.items()));counts.subtract(remove);counts.update(add);rows=[json.loads(x) for x,n in counts.items() for _ in range(n)]
  if k=='schema_columns':rows.sort(key=lambda x:(x['table_name'],x['column_name']))
  elif k=='schema_indexes':rows.sort(key=lambda x:(x['tablename'],x['indexname']))
  else:rows.sort(key=enc)
  ck(f'Reconstruction {stage} {k}',hashlib.sha256(enc(rows)).hexdigest()==s['fingerprints'][k]['sha256'] and len(rows)==s['fingerprints'][k]['count']);rebuilt[k]=rows
  if stage==2:ck('Pass2 sans delta '+k,not delta['removed'] and not delta['added'])
 row_counts.append({k:len(v) for k,v in rebuilt.items()});current=rebuilt
ck('Deux tables nominales',set(r['tablename'] for r in snap[1]['changes']['ad_table']['added'])=={'EVA_CanalGrupa','EVA_CanalFunctie'})
ck('8 instances natives avec succès',len(snap[1]['changes']['ad_pinstance']['added'])==8 and all(r['result']==1 for r in snap[1]['changes']['ad_pinstance']['added']))
for k in ['c_order','c_orderline','m_inout','m_inoutline','m_storagereservation','m_storagereservationlog','m_transaction','m_costdetail','fact_acct','c_channel','c_campaign','eva_canalvanzare']:ck('Business inchangé '+k,base[k]==current[k])
log=(L/'migration_original_v2.stdout.txt').read_text(encoding='utf8');ck('Appels originaux et logs vides','MIGRATION_ORIGINAL|pass=1|T214=0|T211=8|log=\n' in log and 'MIGRATION_ORIGINAL|pass=2|T214=0|T211=0|log=\n' in log)
checked=L/'Reconciliere_T211_verificata_v1.json';q=j(checked);ck('SHA rapport réconciliation',sha(checked)=='346ad3c040910eec253e41b5e639238dec4bf5b67d870bd4ac3f92db87912aa7')
for ix in q['indexes']:ck('Index ready/valid '+ix['name'],ix['indisvalid'] and ix['indisready'] and ix['definition'] in [r['indexdef'] for r in current['schema_indexes']])
bc=[]
for item in q['bc_witness']:
 t=item['table'];key=item['key'];rid=item['id'];a=[r for r in base[t] if r[key]==rid];b=[r for r in current[t] if r[key]==rid];ck('BC toutes colonnes '+str(rid),len(a)==len(b)==1 and a==b and len(a[0])==item['columns_count'] and all(a[0][k]==v.replace(' ','T',1) for k,v in item['bc_values'].items()));bc.append({'table':t,'id':rid,'columns':len(a[0]),'comparison_note':'Rândurile brute sunt comparate byte/câmp exact; numai afișarea SQL timestamp spațiu este confruntată cu separatorul ISO T al to_jsonb.'})
out={'schema':'A11.R12.Val05.migration.readback.oracle.v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'A11 independent','method':'Recalcul indépendant des empreintes de tous les rowsets bruts, reconstruction multiensemble de chaque delta et confrontation des deux passes. Aucune connexion PostgreSQL ni nouvelle exécution de migration.','decision':'RECONCILIEREA NOMINALĂ ESTE SUSȚINUTĂ DE READBACK-URILE PĂSTRATE; ACEASTA NU RECEPȚIONEAZĂ BUSINESS A/B.','head':'df85d33c1648ce2b2df130a60a05ef696e2e5480','inputs':[ref(bf)]+[ref(L/n) for n in names]+[ref(checked),ref(L/'migration_original_v2.stdout.txt')],'checks':checks,'table_count':len(base),'row_counts_after_passes':row_counts,'bc_witnesses':bc,'scope':['2 tabele, 24 coloane și 6 elemente noi; 8 procese native și 16 linii log sunt efecte ale instalării.','Pass2: toate cele 24 de rowseturi urmărite au aceleași rânduri/valori. Nu este idempotență globală a instalării pe alte seeduri.','C_Channel existent nu a fost schimbat. Ramura set_ValueNoCheck din ensureT214 nu primește credit de execuție.','AD_Process statistici nu au baseline; nu se afirmă delta lor zero. Nu se pretinde atomicitate globală a migrării.','Contorul returnat T211=8 nu este numărul tuturor efectelor persistente.','Schema/AD și serviciile se reverifică în JVM business proaspăt; faza A/B și logurile de rezervare au recepție separată.'],'product_score':None,'whole_acceptance':False,'A11_product_executions':0,'A11_operational_writes':0}
# Raportul este în română; etichetele tehnice interne ale controalelor sunt normalizate aici.
for c in checks:
 for a,b in [('Baseline brut','Baseline brut'),('Retraits existants','Rânduri retrase existente'),('Reconstruction','Reconstrucție'),('Pass2 sans delta','Pass2 fără delta'),('Deux tables nominales','Două tabele nominale'),('8 instances natives avec succès','8 instanțe native reușite'),('Business inchangé','Business neschimbat'),('Appels originaux et logs vides','Apeluri originale și jurnale fără erori'),('SHA rapport réconciliation','SHA raport reconciliere'),('BC toutes colonnes','BC toate coloanele')]:c['check']=c['check'].replace(a,b)
out['method']='Recalcul independent al amprentelor tuturor rowseturilor brute, reconstrucția fiecărei diferențe ca multiset și confruntarea celor două treceri. Fără conexiune PostgreSQL ori execuție nouă de migrare.'
out['reviewer_calibration']={'first_attempt':'Recalculul rowseturilor și al celor două treceri a trecut; primul martor BC a oprit comparatorul A11 deoarece afișarea SQL conține spațiu, iar to_jsonb conține T.','correction':'Numai reprezentarea așteptată din martorul SQL este convertită la ISO. Rândurile brute înainte/după rămân comparate exact și nu sunt modificate.','saved_first_runner':ref(O/'Runner_migrare_calibrare_timestamp_BC.py'),'product_failure':False}
op=O/'Contraoracol_A11_migrare_T211_v1.json';assert not op.exists();op.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8');rp=O/'Runner_A11_migrare_T211_v1.py';assert not rp.exists();rp.write_bytes(pathlib.Path(__file__).read_bytes());sp=O/'SIGILIU_A11_migrare_T211_v1.json';assert not sp.exists();sp.write_text(json.dumps({'utc':out['utc'],'files':[ref(op),ref(rp)],'immutable':True},ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps({'verdict':ref(op),'seal':ref(sp),'checks':len(checks)},ensure_ascii=False))
