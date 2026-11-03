from pathlib import Path
import collections
import datetime
import gzip
import hashlib
import json
import shutil

root = Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
folder = root/'executie/R11_fisiere/Triaj_fixture_UI_Val03'
dest = folder/'Raport_triaj_UI_config.json'
assert not dest.exists()
read = lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
reference = lambda p:{'path':p.relative_to(root).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
v12 = root/'executie/R11_fisiere/Suite_originale_config_sintetice_v12'
receipt = read(v12/'Rezultate_suite_originale.json')
sources = {row['file']:row for row in read(v12/'Surse_izolate_Git.json')['rows']}
with gzip.open(root/'executie/R11_plan_delta/Dispatch_tehnic_integral.jsonl.gz','rt',encoding='utf8') as stream:
    dispatch = {row['path']:row for row in map(json.loads,stream)}
help_path = folder/'Proba_help_browser_v2.json'
help_result = read(help_path)
observations = [
    {'id':'UI-V03-01','kind':'PRECONDIȚIE_ABSENTĂ_ÎN_TEST','files':['frontend/tests/test_event_theme_admin.py','frontend/tests/test_storefront_admin_i18n.py','frontend/app.py'],
     'actor':'Manager sintetic, cabinet/firmă AUDIT001, site cesiro1 sintetic.',
     'normal_path':'GET /app/api/storefront/sites; PATCH /app/api/admin/storefront/sites/cesiro1; paginile de setări în 6 limbi.',
     'requirement':'Setări clare de canal, teme aprobate și refuzul unei teme necunoscute.',
     'positive':'2 teste părinte event și 3 admin trec; 20 subteste distincte pe theme_id/lang trec.',
     'counterexample':'Temă inexistentă primește 400; originale identice fără storefront_sites.json eșuează în setup.',
     'result':'Cele 5 erori de setup sunt explicate de fișiere locale neversionate. Manifestele Git oferă metadata necesară unei fixture reproductibile.',
     'persistent_effect':'Scrieri JSON numai în copia temporară, restaurate de tearDown și eliminate la cleanup; nu s-a măsurat efect în ERP.',
     'native_reuse':'Păstrează handlerul existent de administrare și manifestele existente; propune doar fixture de test explicită.',
     'limit':'Auth/me este simulat; niciun certificat de autorizare reală sau de traducere semantică completă.'},
    {'id':'UI-V03-02','kind':'PRECONDIȚII_AUTH_CONTEXT_ȘI_ASSERT_ÎNVECHIT','files':['frontend/tests/test_saga_completeness_audit_ui.py','frontend/tests/test_idempiere_web_module_coverage.py','frontend/app.py'],
     'actor':'Manager sintetic cu răspuns auth/me valid și cookie eva_cui=AUDIT001.',
     'normal_path':'Pagină import SAGA, proxy archive/completeness/tables, proxy /app/api/iddata/process/123.',
     'requirement':'Actor verificat, firmă selectată, query și corp propagate corect; acces nativ prin consola existentă.',
     'positive':'10 evenimente SAGA anterior eșuate și testul proxy proces trec cu precondițiile explicite. 4/4 teste modul trec; SAGA 5 părinte+6 subteste trec.',
     'counterexample':'Fără token sau cu auth/me invalid, 302 către login, zero apeluri către proxy. Cu fixture inițială, DNS de autentificare este refuzat sau tenant rămâne gol.',
     'result':'SAGA păstrează 1 test eșuat: cere literal /webui/, în timp ce cardul curent renderizat este /app/remote. Testul original rămâne eșuat; migrarea așteptării necesită validarea navigării native complete.',
     'persistent_effect':'Nu există efect ERP; backendul țintă este funcția simulată din testul original.',
     'native_reuse':'Păstrează require_login, active_cui și consola eva_remote; nu reintroduce o legătură directă doar ca să treacă testul.',
     'limit':'Nu s-a exercitat autentificarea nativă ZK, execuția procesului 123 sau datele unei firme reale.'},
    {'id':'UI-V03-03','kind':'PRECONDIȚIE_CATALOG_SINTETIC','files':['frontend/storefront/tests/test_event_themes.py','frontend/storefront/tests/test_seasonal_themes.py','frontend/storefront/tests/test_audit_regressions.py','frontend/storefront/app/cms.py','frontend/storefront/app/factory.py','frontend/storefront/templates/themes/generic/product.html'],
     'actor':'Vizitator al magazinului sintetic cesiro1.',
     'normal_path':'Home/produs/legal pentru 8 teme și 6 limbi; API comenzi cu mapping disponibil și indisponibil în testul original audit_regressions.',
     'requirement':'Teme configurabile cu pagini coerente și semnalizarea distinctă a comenzii fără mapare de stoc.',
     'positive':'3 programe originale exit0. Event și seasonal verifică împreună 144 răspunsuri de pagină; registrul provine din 9 manifeste Git exacte.',
     'counterexample':'0 și 1 imagine nu randează galeria, conform condiției originale product.images|length > 1; 2 imagini intră pe ramura testată. Temă invalidă revine la marketplace_pro. Originalul audit_regressions distinge new/pending_stock_mapping.',
     'result':'Lipsa registrului și precondiția de minimum două imagini explică eșecurile acestui lot. Nu se declară remediere în aplicație.',
     'persistent_effect':'Originalele verifică răspunsurile comenzilor și invarianta catalogului; nu demonstrează C_Order/C_OrderLine sau confirmare ERP.',
     'native_reuse':'Reutilizează manifeste, CMS, factory, template și handlerul de comandă existente.',
     'limit':'Textul catalogului/legal este sintetic; traducerile operaționale nu sunt certificate. 157 încercări DNS cumulate au fost blocate și tratate prin fallback. Nicio expediere/comandă reală.'},
    {'id':'UI-V03-04','kind':'LACUNĂ_DOCUMENTAȚIE_UX_CONFIRMATĂ','files':['frontend/tests/test_help_coverage.py','frontend/static/eva-help.js','frontend/static/eva-help-kb.json','frontend/static/eva-help.css','frontend/app.py'],
     'actor':'Utilizator care deschide ajutorul paginii, în DOM gazdă sintetic.',
     'normal_path':'Buton data-eva-page-help → openPageHelp → normalizePageKey → articol KB sau page:/app/default.',
     'requirement':'Experiență explicabilă pentru utilizator contabil/software/iDempiere de bază, inclusiv paginile de import, salarizare și fiscalitate.',
     'positive':'Un articol dedicat existent apare cu titlul corect; cele 16 rute fără articol dedicat afișează fallbackul general în Chromium, fără erori JS.',
     'counterexample':'Aceleași chei lipsesc efectiv din KB, deși pagina este detectată de testul AST; nu este dovedită absența totală a ajutorului.',
     'result':'16 din 70 rute statice randate nu au articol dedicat în index. Inventarul exact este în Proba_help_browser_v2.json.',
     'persistent_effect':'Doar DOM și fetch simulate; nicio scriere DB. Browserul și contextele efemere au fost închise.',
     'native_reuse':'Completează dicționarul existent eva-help-kb.json și leagă instrucțiunile de ferestre/procese native; nu propune un motor de ajutor nou.',
     'limit':'Se verifică widgetul exact pe fiecare cale într-un DOM sintetic; nu este recepția completă a paginilor, navigării sau ZK.'}
]
records = []
for name in sorted({name for obs in observations for name in obs['files']}):
    d = dispatch[name]
    src = sources[name]
    assert src['git_blob'] == d['git_object']
    matched = [obs for obs in observations if name in obs['files']]
    records.append({'path':name,'git_oid':src['git_blob'],'sha256':src['sha256'],'file_id':d['id'],
                    'owner':d['owner'],'peer':d['peer'],'executor':'COORDONATOR; recepție solicitată A11',
                    'role':d['class'],'control':d['control'],'task_candidates':d.get('task_candidates',[]),
                    'task_assignment':'Nu se inventează asociere nominală; A12 verifică cerința și consumatorul.',
                    'observations':[obs['id'] for obs in matched],
                    'normal_paths':[obs['normal_path'] for obs in matched],
                    'requirements':[obs['requirement'] for obs in matched],
                    'positive':[obs['positive'] for obs in matched],
                    'counterexample':[obs['counterexample'] for obs in matched],
                    'result':[obs['result'] for obs in matched],
                    'persistent_effect':[obs['persistent_effect'] for obs in matched],
                    'limit':[obs['limit'] for obs in matched],'whole_file_accepted':False})

case_events = collections.Counter((case['report_type'],case['outcome']) for row in receipt['rows'] for case in row.get('cases',[]))
result = {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':receipt['head'],
          'gate':reference(root/'executie/R11_plan_delta/A11_verdict_plan_delta_R11_v3.json'),
          'population':reference(root/'executie/delta/2026-11-02T22-21-42-843Z/Comparatie_ultimul_checkpoint.json'),
          'status':'PROPUS PENTRU RECEPȚIE A11; rezultate componente, fără notă integrală',
          'original_tests_unchanged':True,'suite_receipt':reference(v12/'Rezultate_suite_originale.json'),
          'source_manifest':reference(v12/'Surse_izolate_Git.json'),
          'help_receipt':reference(help_path),'help_screenshot':reference(folder/'Help_fallback_browser_v2.png'),
          'programs':{'total':7,'exit0':6,'exit1':1},
          'pytest_events':[{'type':k[0],'outcome':k[1],'count':v} for k,v in case_events.items()],
          'observations':observations,'file_records':records,
          'calibrations':'V11/V11b/V11c/V11d se păstrează ca probe de precondiție; nu se adună la V12. V11b adaugă diagnostic; V11c are 1 imagine; V11d are 2. Browser v2 așteaptă finalul animației numai pentru captură; v1 se păstrează.',
          'remaining_original_signals':['3 cazuri HR au nevoie de fixture DB nativă, preluate A01.','Testul SAGA cu /webui/ este învechit față de cardul /app/remote; verificarea fluxului nativ rămâne necesară.','16 articole dedicate lipsesc; fallbackul funcționează.','CLI retail_ux_improvements și cesiro_demo_i18n_matrix cer date de traducere/catalog; nu au fost fabricate traduceri doar pentru a trece testele.'],
          'native_limit':'Zero documente native, înregistrări contabile sau fluxuri complete recepționate prin acest lot.',
          'cleanup':{'synthetic_fixtures_removed':receipt['temporary_fixture_removed'],'browser_closed':True,'production_writes':0,'new_listening_services':0},
          'independent_reception':None}
assert result['cleanup']['synthetic_fixtures_removed']
for filename in ['p01-r11-help-witness-v2.py','p01-r11-build-fixture-v12.py','p01-r11-triage-report.py']:
    shutil.copyfile(Path('D:/CodexWork')/filename,folder/filename)
dest.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'report':reference(dest),'events':result['pytest_events'],'files':len(records)},ensure_ascii=False))
