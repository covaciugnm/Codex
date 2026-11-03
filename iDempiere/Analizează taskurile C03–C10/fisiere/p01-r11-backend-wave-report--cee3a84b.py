from pathlib import Path
import collections
import datetime
import gzip
import hashlib
import json

root = Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
folder = root/'executie/R11_fisiere/Backend_extindere_Val04'
folder.mkdir(exist_ok=True)
dest = folder/'Raport_8_suite_backend.json'
assert not dest.exists()
read = lambda p:json.loads(p.read_text(encoding='utf8'))
sha = lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ref = lambda p:{'path':p.relative_to(root).as_posix(),'sha256':sha(p)}
v13 = root/'executie/R11_fisiere/Suite_originale_backend_extindere_v13'
v13b = root/'executie/R11_fisiere/Suite_originale_backend_extindere_v13b'
original = read(v13/'Rezultate_suite_originale.json')
supplement = read(v13b/'Rezultate_suite_originale.json')
old = read(root/'executie/R11_fisiere/Suite_originale_reconciliate/Consolidare_55_suite.json')
old_names = {row['file'] for row in old['rows']}
rows = [row for row in original['rows'] if row['file'] != 'backend/tests/test_help_kb.py'] + supplement['rows']
assert len(rows) == 8 and len({row['file'] for row in rows}) == 8
assert all(row['file'] not in old_names for row in rows)
assert all(row['exit'] == 0 for row in rows)
with gzip.open(root/'executie/R11_plan_delta/Dispatch_tehnic_integral.jsonl.gz','rt',encoding='utf8') as f:
    dispatch = {row['path']:row for row in map(json.loads,f)}
subjects = {
 'test_accounting_trace.py':('Prezentarea notei contabile și trasabilitatea documentului','EvaAccountingTraceService, Fact_Acct citit prin FakeReadDB; factură echilibrată versus nepostată','Nu se creează Fact_Acct și nu se invocă motorul contabil nativ.'),
 'test_assets_currency.py':('Activ imobilizat din factură și rezumat valută','EvaAssetFromInvoiceService + currency_ui; categorie corectă/lipsă, idempotent, curs disponibil/lipsă','FixedAsset este modelul local EVA pe SQLite; nu certifică A_Asset și procesarea contabilă iDempiere.'),
 'test_bank.py':('Parser bancar, import, deduplicare și reconciliere','Parsers MT940/CAMT/CSV; cifre etalon și reimport, API pe context tenant simulat','Nicio conexiune la bancă, import SOAP real sau alocare nativă C_AllocationHdr.'),
 'test_bpartner_balance.py':('Situația partenerului, rol și sold pe monede','EvaBPartnerBalanceService pe FakeReadDB: client/furnizor/net, nealocat, scadență, mascare bani','Nu este probă SQL pe Fact_Acct/C_Invoice/C_Payment reale.'),
 'test_help_kb.py':('Indexul de ajutor și cheile obligatorii','Citire KB versionată; JSON/schema și chei minimale','5 teste trecute nu contrazic cele 16 rute fără articole dedicate: setul de chei obligatorii este mai restrâns.'),
 'test_bank_psd2_scheduler.py':('Sincronizare programată, repetare și izolare pe tenant/provider','EvaBankScheduler pe SQLite și Finqware mock; due/idempotent/skip reauth','background_org_ctx este simulat explicit în original, nu validare nativă a autorității.'),
 'test_audit_and_office.py':('Jurnal de mutații și stocare document','API partener→audit/trace_id; refuz DELETE; SHA etalon document și callback','Fișierul este numai în fixture; răspunsul callback 200 nu probează editorul OnlyOffice sau rețeaua reală.'),
 'test_t32_l6j_rute.py':('Rute cabinet, manager/super și portofoliu','Fixture samanta_l6j cu două cabinete, token JWT sintetic, SQLite; propriul versus străin și fără token','Interogări de scheme/registru și contextul ERP sunt dublate în original; nu dovedește runtime ZK, schema PostgreSQL sau toate cele 17 contracte.')
}
records = []
counts = collections.Counter()
for row in rows:
    d = dispatch[row['file']]
    assert d['git_object'] == row['git_blob']
    objective, method, limit = subjects[Path(row['file']).name]
    source = v13b if row['file'].endswith('/test_help_kb.py') else v13
    events = collections.Counter((c['report_type'],c['outcome']) for c in row['cases'])
    counts.update(events)
    records.append({'file':row['file'],'file_id':d['id'],'git_oid':row['git_blob'],'sha256':row['source_sha256'],
                    'owner':d['owner'],'peer':d['peer'],'control':d['control'],'role':'Test original de componentă/API',
                    'executor':'COORDONATOR','requirement':objective,'normal_path_and_native_boundary':method,
                    'positive_and_counterexamples':[c['id'] for c in row['cases']],
                    'actor':'Actorii și rolurile sintetice din testul original; nu cont operațional',
                    'result':{'exit':row['exit'],'events':[{'type':k[0],'outcome':k[1],'count':v} for k,v in events.items()]},
                    'persistent_effect':'Efecte locale declarate în SQLite/fișiere temporare; fără credit pentru tabele native sau conexiune de producție',
                    'receipt':ref(source/'Rezultate_suite_originale.json'),'limit':limit,'integral_accepted':False})
result = {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':original['head'],
          'status':'SUPLIMENT NOU, ÎN AȘTEPTAREA RECEPȚIEI A11/A12',
          'plan_gate':ref(root/'executie/R11_plan_delta/A11_verdict_plan_delta_R11_v3.json'),
          'source_receipts':[ref(v13/'Rezultate_suite_originale.json'),ref(v13b/'Rezultate_suite_originale.json')],
          'source_manifests':[ref(v13/'Surse_izolate_Git.json'),ref(v13b/'Surse_izolate_Git.json')],
          'no_original_test_edits':True,'programs':8,'programs_exit0':8,
          'events':[{'type':k[0],'outcome':k[1],'count':v} for k,v in counts.items()],
          'no_overlap_with_previous_55':True,'record_count_if_admitted':63,
          'records':records,'calibration':'V13 help_kb a eșuat fiindcă runnerul nu copiase frontend/static în fratele backend. V13b include sursele Git exacte și trece 5/5; V13 se păstrează, nu se cumulează eșecul de mediu.',
          'T58_C67':'Suita originală test_t32_l6j_rute.py lipsă din Val_03 este acum exercitată 29/29. A12 trebuie să reconcilieze toate cele patru suite ale subcondiției înainte de orice extindere a creditului, fără transfer la Java/ZK.',
          'cleanup':{'fixtures_removed':original['temporary_fixture_removed'] and supplement['temporary_fixture_removed'],'operational_writes':0},
          'method_erratum':'Câmpul origin moștenit din V10 descrie T58/Node și este INAPLICABIL V12/V13/V13b. Implementarea child V12 interzice orice subprocess; în aceste probe nu s-a executat Node. Audit hook este un control al laboratorului, nu sandbox OS.'}
dest.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
erratum = root/'executie/R11_fisiere/Triaj_fixture_UI_Val03/Erata_metoda_V12_V13.json'
assert not erratum.exists()
erratum.write_text(json.dumps({'utc':result['utc'],'reason':'Corecție explicită cerută de A11; artefactele sigilate nu sunt rescrise.','applicable_receipts':[ref(root/'executie/R11_fisiere/Suite_originale_config_sintetice_v12/Rezultate_suite_originale.json'),*result['source_receipts']],'correct_method':result['method_erratum'],'product_defect':False},ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'report':ref(dest),'events':result['events'],'erratum':ref(erratum)},ensure_ascii=False))
