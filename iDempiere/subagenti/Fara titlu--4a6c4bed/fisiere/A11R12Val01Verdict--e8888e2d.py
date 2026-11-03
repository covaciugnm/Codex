from pathlib import Path
import json,hashlib,datetime,shutil,sys
sys.stdout.reconfigure(encoding='utf8')
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');O=R/'executie/R12_fisiere/A11/Val01';V=R/'executie/R12_fisiere/A12/Val_01';T=R/'executie/R12_fisiere/A11/T240_lot01'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return {'path':p.relative_to(R).as_posix(),'sha256':h(p),'bytes':p.stat().st_size}
control=O/'Control_A11_R12_Val01_v1.json';assert h(control)=='183aa6c59a9e871eb106d0b069b6d223deb733b3c533e5494e70aa5e135fa3a6'
peer=T/'Peer_receptie_T240/Peer_receptie_T240_v1.json';sealpeer=T/'Peer_receptie_T240/Sigiliu_peer_receptie_T240_v1.json'
assert h(peer)=='a35a066ed2bdf73980fdede92b565878eac4ba9cba32dd25aa05175e87b04057'
assert h(sealpeer)=='d1775ffbc20af9c7c16086c1eed2fdc88ecb40479d044daad81c435f913fef1d'
pj=j(peer);assert len(pj['checks'])==64 and all(x['passed'] for x in pj['checks'])
for x in pj['inputs']:assert h(R/x['path'])==x['sha256']
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
oldcheck=T/'Checklist_A11_dupa_T240_lot01_v1.json';check=j(oldcheck);check['schema']='A11.R12.after_Val01.checklist.v1';check['utc']=utc;check['previous_immutable_checklist']=ref(oldcheck)
for s in check['next_actions']:
 if s['id']=='N10':s['status']='EXECUTAT — Val01 primit limitat, fără închideri de task/fișier/criteriu';s['received_manifest']=ref(V/'MANIFEST_R12_Val01.json')
 if s['id']=='N11':s['status']='RECEPȚIE_VAL01_ÎNCHEIATĂ; verifică HEAD/populația înaintea următorului lot și păstrează porțile.'
cp=O/'Checklist_A11_dupa_R12_Val01_v1.json';assert not cp.exists();cp.write_text(json.dumps(check,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
out={
 'schema':'A11.R12.Val01.verdict.v1','utc':utc,'author':'A11 independent','candidate':'df85d33c1648ce2b2df130a60a05ef696e2e5480',
 'decision':'ADMIS_CHECKPOINT_DE_REGISTRU_CU_RECEPȚIE_COMPONENTĂ_LIMITATĂ',
 'meaning':'Val01 este coerent cu inventarul și dovezile sigilate. Această recepție nu este o închidere a auditului, T240, C03 sau C10 și nu certifică produsul integral.',
 'inputs':[ref(V/'MANIFEST_R12_Val01.json'),ref(V/'Handoff_R12_Val01.json'),ref(V/'QA_R12_Val01.json'),ref(control),ref(T/'Verdict_A11_R12_T240_lot01_v1.json')],
 'independent_verification':{'aggregate_checks':29,'aggregate_checks_passed':29,'identity_dimensions_per_file':8,'identities_compared':6728,'different_path_ID_OID_mode_or_assignment':0,'reference_edges_rehashed_and_pointers_resolved':6814,'distinct_reference_files':48,'additional_historic_dossiers_rehashed':652,'new_product_tests':0},
 'reconciliation':{
  'technical_current':6728,'old_exact_OID_mode':6709,'new_instruments':19,
  'R12_component_sources_partially_exercised':2,'R12_sources_without_component_execution_in_wave':6726,'remaining_new_instruments':17,
  'R11_historical_component_sources_reference_only':116,'R11_credit_transferred_to_R12':0,
  'historic_tasks':652,'historic_criteria':2619,'historic_criteria_credited_by_this_wave':0,
  'active_task_separate':'P01.C14.T0001 / T240, implementare, în afara cohortei istorice652; rămâne neînchis.',
  'whole_files':0,'whole_tasks':0,'native_UI_ERP_files':0,'whole_contracts':0,'contracts_open':17,
  'not_defect_count':'6726 este lipsa exercițiului de componentă în acest val, nu un număr de defecte sau afirmația că aceste fișiere nu au fost citite niciodată.'},
 'metrics_retained':{
  'original_cases_without_mutants':'46/46, fără adaptor/omisiuni',
  'mutants':'33/33 în7loturi disjuncte,1518evaluări ale acelorași46cazuri; nu1518teste unice',
  'full_original_program':'TIMEOUT60, fără credit sau verdict de defect din această tentativă',
  'additional':'20martori A08 prin funcție +1CLI UTF8 și19CLI A11 păstrate distinct',
  'fixture':'13RO +10EN TEXTE +1Perioade EN=24rânduri.12din docstring/fișa A12 inițială este istoric; planul v2 a fixat13 înaintea rulării. Nicio validare nativă suplimentară de ecran.',
  'OS':'Preflight și originalul au infirmat ipoteza incompatibilității generale «NU: …» pe scratchul NTFS; ADS creat și eliminat. Fără adaptor preventiv.'},
 'findings':'Cele5grupe și dispozițiile A11 sunt păstrate exact: R3/Ecol2 confirmat P2 numai helper; numitor E dublat separat; contract prag/tipuri fără severitate automată; UTF8 P3 cu refuz; proveniență/decodare/containment ca limite declarate. Nicio remediere de produs executată în audit.',
 'T343':'Val01 păstrează recepția documentară23:15. C-2.2 CO|CO|CO|linii nu devine IP prin simpla observație a registrului; se cere amendament nominal recepționat. D05/D06 și D01/D10 rămân deschise.',
 'peer_supplement':{'report':ref(peer),'seal':ref(sealpeer),'checks':64,'result':'Oracolul celor4fixture R3 recalculat direct, surse/arhive/limite confirmate fără supralicitare.','timing':'Supliment primit după sigilarea A12 Val01; este referință nouă aici, nu conținut introdus retroactiv în Val01.','new_product_execution':False},
 'scores':{'plan_R12_v2_received_separately':10,'whole_execution':None,'product':None,'tasks':None},
 'next_checkpoint':ref(cp),
 'continuation':'Continuă cele17instrumente conform planului, verifică consumatorii judecător/collector și pregătește clona nativă sintetică prin mecanismele existente. Există acțiuni interne realizabile; nu este justificată suspendarea pentru o dependență externă.',
 'resources':'Nicio resursă de produs creată în recepția Val01. Cleanupul lotului T240 rămâne confirmat; doar fișiere de audit noi.',
 'immutable':'Manifestul A12, rapoartele A08, probele și verdicturile anterioare nu sunt modificate.'
}
vp=O/'Verdict_A11_R12_Val01_v1.json';assert not vp.exists();vp.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
for n in ['A11R12Val01Check.py','A11R12Val01Verdict.py']:
 dst=O/n;assert not dst.exists();shutil.copyfile(Path('D:/CodexWork')/n,dst)
sp=O/'Sigiliu_A11_R12_Val01_v1.json';assert not sp.exists();items=[ref(p) for p in sorted(O.iterdir()) if p.is_file()]
sp.write_text(json.dumps({'utc':utc,'verdict':ref(vp),'artifacts':items,'input_manifest':ref(V/'MANIFEST_R12_Val01.json'),'no_self_reference':True},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
for x in items:assert h(R/x['path'])==x['sha256']
print(json.dumps({'verdict':ref(vp),'seal':ref(sp),'checklist':ref(cp)},ensure_ascii=False))
