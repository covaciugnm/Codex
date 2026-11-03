import pathlib,json,hashlib,datetime
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere');B=R/'A05_N05_lot03';O=R/'A11/Val03_loturi'
def ref(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def load(p):return json.loads(p.read_text(encoding='utf8'))
seal=B/'SIGILIU_supliment_N05_v1.json';assert ref(seal)['sha256']=='d87a6da533b6c945c3b1649935b118f16b67d6c1d5ce18673d615afbe0b685d8'
for e in load(seal)['files']:assert ref(B/e['path'])['sha256']==e['sha256']
old={e['path']:e for e in load(B/'Fise_sursee_N05_v1.json')['files']}
for e in load(B/'Fise_supliment_cale_normala_v1.json')['files']:
 assert 'normal_path' not in old[e['path']]
 assert {k:v for k,v in e.items() if k!='normal_path'}==old[e['path']]
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'A11','base_receipt':ref(O/'Verdict_A11_N05_lot03_v1.json'),'supplement':ref(seal),'disposition':'ACCEPTAT completarea exclusivă normal_path pentru JobFundal/ProceseEcran, fără schimbarea sigiliilor și fără credit nou.','source_scope_clarification':{'total_sources':46,'static_only':29,'business_method_paths_including_transitive':11,'transitive_type_record_usage_without_individual_method_trace':2,'fixture_or_binding_only':3,'binding_and_metadata_only':1,'type_sources':['wms/MiscareWms.java','wms/TipMiscareWms.java'],'rule':'Cele13 rânduri TRANSITIVE_BUSINESS_PARTIAL din matrice includ11 trasee de metode și2 utilizări de tip/record. Nu raporta13 metode testate direct; nu credita restul claselor/ramurilor. Nu se schimbă identitățile sau numitorul46.'},'review_calibration':'Prima încercare locală de citire QA a business_v1.stdout ca UTF-8 a refuzat un octet Windows legacy; nu s-a scris niciun verdict atunci. Pentru rehash păstrez byte-exact; verificarea ancorelor de binding se face ASCII, decodareLatin1 numai pentru tokenizare. Mesajele nominale N03 sunt validate în business_v2 UTF-8. Aceasta nu este eroare de produs.','no_new_execution':True,'full_file_or_task_closures':0,'open_contracts':17}
p=O/'Supliment_A11_N05_trasabilitate_v1.json';assert not p.exists();p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
s=O/'SIGILIU_A11_N05_supliment_v1.json';assert not s.exists();s.write_text(json.dumps({'files':[ref(p)],'immutable':True},ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps({'report':ref(p),'seal':ref(s)},ensure_ascii=False))
