from pathlib import Path
import json,hashlib,datetime,zipfile
OUT=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_Nativ_lot02')
sha=lambda b:hashlib.sha256(b).hexdigest()
base=json.loads((OUT/'Cache_binar_reutilizabil.json').read_text(encoding='utf8'))
entries={}
for item in base['files']:
 with zipfile.ZipFile(item['path'])as z:
  text=z.read('META-INF/MANIFEST.MF').decode(errors='replace').replace('\r\n ','').replace('\n ','')
  symbolic=next((x.split(':',1)[1].strip().split(';')[0]for x in text.splitlines()if x.startswith('Bundle-SymbolicName:')),None)
  if symbolic:entries[symbolic]=item
explicit=['org.apache.felix.scr','org.eclipse.equinox.event','org.adempiere.base','org.postgresql.jdbc','com.zaxxer.HikariCP','org.compiere.db.postgresql.provider']
active=[]
for line in (OUT/'bootstrap_attempt5_po.stdout.txt').read_text(encoding='utf8').splitlines():
 if line.startswith('ACTIVE_END|'):
  name=line.split('|')[1];active.append({'symbolic_name':name,**entries[name]})
annex={
 'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'primary_manifest':{'path':'MANIFEST_A05_Nativ_lot02.json','sha256':sha((OUT/'MANIFEST_A05_Nativ_lot02.json').read_bytes())},
 'minimum_explicit_start_sequence':[{'order':i+1,'symbolic_name':name,**entries[name]}for i,name in enumerate(explicit)],
 'actual_active_bundles':active,
 'minimum_limit':'Aceasta este lista minimă de pornire explicită folosită și lista efectivă activă. Closure-ul tuturor bundle-urilor RESOLVED nu a fost redus la un minimum demonstrat; cache-ul complet și regula de excludere sunt păstrate. Nu afirma că cele 6 bundle-uri sunt singurele necesare.',
 'guard_source':{'path':'harness/A05OsgiProbe.java','sha256':sha((OUT/'harness/A05OsgiProbe.java').read_bytes())},
 'probe_source':{'path':'po_v2.A05NativePoProbe.java','sha256':sha((OUT/'po_v2.A05NativePoProbe.java').read_bytes())},
 'probe_jar':{'path':'po_v2.jar','sha256':sha((OUT/'po_v2.jar').read_bytes())},
 'ordered_protocol':[
  '1. Creează un lot nou de audit, un director local unic cu prefix a05-r12-native-lab- și verifică absența unei execuții pe același port. Copiază harnessurile în lotul nou; schimbă explicit OUT și LAB/ROOT în copiile de lucru. Nu modifica fișierele sigilate. DSN-ul folosit în probe este 127.0.0.1:56455; dacă îl schimbi, schimbă și constanta probei native și toate controalele, apoi recompilare și canari.',
  '2. Verifică SHA seed și toate SHA-urile JAR din Cache_binar_reutilizabil.json. Ant este un bundle de director arhivat local; Manifest_bundle_Ant.json păstrează SHA pentru fiecare intrare originală. Nu copia configul aplicației operaționale.',
  '3. Inițializează PG16 local: initdb -D <LAB>/pgdata -U a05lab --auth-host=scram-sha-256 --auth-local=scram-sha-256 --pwfile=<fișier sintetic> --encoding=UTF8 --locale=C. Configurează listen_addresses=127.0.0.1, port56455, statement_timeout30s și idle_in_transaction_session_timeout45s. Valorile de parolă păstrate în harness sunt exclusiv de fixture, nu credențiale operaționale.',
  '4. Pornește pg_ctl numai cu stdout/stderr către fișiere reale, conform a05_r12_pg_resume.py. NU reproduce capture_output=True din prima tentativă a05_r12_pg_restore.py: pe Windows procesul postgres moștenește pipe-ul și communicate poate rămâne în așteptare. Scriptul vechi este păstrat exclusiv ca dovadă.',
  '5. createdb idempiere; rol adempiere sintetic; pg_restore --exit-on-error --no-owner --no-privileges; acordă doar drepturile necesare în schema restaurată. Reutilizează pașii din pg_resume, dar în OUT nou. Orice rc nenul oprește evaluarea; nu folosi restaurarea q31 cu ||true din helperul operațional.',
  '6. Dezactivează în clonă schedulerele, procesoarele și configurările de validatori pentru baseline generic; neutralizează SMTP la127.0.0.1:1, email și tokenurile sintetice, conform pg_isolation. Această dezactivare împiedică recepția semantică WMS până la un lot separat cu handler-ele originale reactivate.',
  '7. Readiness înainte de PO: doar clienții0/11, actor GardenAdmin101, rol102, organizație11; dreptul AD_User_Roles confirmat. Compară Version și LastBuildInfo cu binarul. Placeholderul LastBuildInfo și IsFailOnBuildDiffer=N rămân limită, nu se rescriu pentru a obține PASS. Verifică fizic AD/schema/migrări pentru loturile de produs.',
  '8. Compilează A05OsgiProbe cu JDK21 și frameworkul hashuit; setează java.security.manager=allow. Launcherul rulează cei7canari înainte de clasele iDempiere, apoi instalează bundle-uri dormant, cu excluderile din sursă. Activează serviciile în ordinea explicită de mai sus, folosind osgi.compatibility.bootdelegation=true, confirmată read-only în runtime.',
  '9. Confirmă logul NATIVE_PG_PROVIDER și NATIVE_SERVICE_LOCATOR. Compilează A05NativePoProbe și împachetează manifestul exact din a05_r12_build_po.py. Rulează saveEx/commit/readback, rollback, duplicat și retry. Minimumul de fixture include C_UOM_ID, M_Product_Category_ID și C_TaxCategory_ID; omiterea ultimei coloane explică tentativa PO1, fără defect de produs.',
  '10. Recitește independent prin psycopg, tranzacție read-only și conexiune nouă: exact2rânduri fixture,0rollback,1CPPValue, descrierea retry și0sesiuni native rămase. Nu transfera această dovadă în contractele CPP/CPA, SKU/EAN, G1/G2/G3 ori WMS.',
  '11. Închide pool-ul DB, oprește frameworkul și verifică event64. Launcherul finalizează controlat JVM pentru executorii statici; nu elimină garda în timpul probei. pg_ctl stop pentru clusterul propriu, verificare port închis, copie loguri, verificare cale absolută și eliminare numai LAB. Cache-ul este un set de fișiere reutilizabile; nu se păstrează niciun serviciu activ.'
 ],
 'failed_attempts':'Descrise explicit și păstrate în Raport_A05_N08_Nativ_lot02.json și logurile bootstrap1–5/PG1–2; nu sunt convertite în rezultate PASS.',
 'production_operations':'Doar read-only SSH pentru metadata/binare/configurare selectată; zero scrieri de metadata, zero start/stop/run remote.',
 'live_resources':0
}
target=OUT/'Anexa_reproducere_v1.json';assert not target.exists();target.write_text(json.dumps(annex,ensure_ascii=False,indent=2),encoding='utf8')
manifest={'schema':'A05.R12.N08.repro.appendix.v1','utc':annex['utc'],'immutable_primary_manifest':annex['primary_manifest'],'entries':[{'path':target.name,'sha256':sha(target.read_bytes()),'bytes':target.stat().st_size}],'scope':'Anexă nouă, fără rescrierea lotului sigilat; pași exacți și SHA-urile bundle-urilor active.'}
target2=OUT/'MANIFEST_reproducere_v1.json';assert not target2.exists();target2.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'appendix':sha(target.read_bytes()),'manifest':sha(target2.read_bytes()),'active_bundles':len(active)},ensure_ascii=False))
