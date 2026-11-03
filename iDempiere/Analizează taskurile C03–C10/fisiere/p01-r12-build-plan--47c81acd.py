from pathlib import Path
import json, hashlib, datetime, copy, html

R = Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
P = R/'executie/R12_plan_delta'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p): return {'path':p.relative_to(R).as_posix(), 'sha256':hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes':p.stat().st_size}
def save(name,d):
 p=P/name
 if p.exists(): raise RuntimeError('Ediție deja existentă: '+str(p))
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
 return ref(p)

BASE='2fe90ed3f128c33dff7cf9f8674e664a70679390'
HEAD='df85d33c1648ce2b2df130a60a05ef696e2e5480'
checkpath=R/'executie/R11_fisiere/A11/Checklist_A11_dupa_val04_v1.json'
checks=read(checkpath)
intake=read(P/'A12/v2/Rezumat_inventar_dispatch_R12_v2.json')
annex= P/'Plan_instrumente_noi_A10_v1.json'
inventory_manifest=P/'Manifest_A12_receptie_R12_v2.json'
assert annex.exists() and inventory_manifest.exists(), 'Așteaptă anexele sigilate A10 și A12'
assert intake['head']==HEAD and intake['counts']['technical_dispatch_total']==6728

zone_data=[
 ('A01','Securitate, autentificare și izolarea cabinet/firmă/canal','A08',
  'Căi CUI, proxy, JWT/cookie, sesiune nativă AD_Session, AD_Role și interdicții server; numai propriile tokenuri sintetice.',
  'N03, D01 și V04-HR: redirect intern/extern la ruta montată; logout/revocare; v1/v2 member/read cu setarea explicită EVA_IDM_MEMBER_WRITE. Diferența de politică nu este automat breșă între firme.',
  'Drept nativ citit din AD_Role și probe cu doi clienți/organizații; refuz fără efect DB și fără forwarding de credentiale către destinație neautorizată.'),
 ('A02','Dicționar iDempiere, schemă și migrații','A10',
  'AD_Table/Column/Window/Process/Sequence/DocType, chei și indici, migrare/idempotentă, versiuni schema versus Git.',
  'N08 și D02: coliziuni de ID fix cu serie business existentă; două execuții ale migrării pe clonă, apoi emitere și citire document nativ. Configurația reală observată nu certifică sursa master.',
  'Reutilizare AD_Sequence și mecanisme de model/migrare existente; ID numeric liber nu este identitate business. Observare din conexiune nouă după commit și rollback.'),
 ('A03','Contabilitate, fiscalitate, salarizare și cost','A04',
  'Fact_Acct, scheme/valute/perioade, active, taxe și declarații, bancă, salarizare și manoperă G2 în G1.',
  'N09, D03/D06 și V04-HR: D112 complet pe GeneratorDeclaratie/DUK/AD_Attachment; contabilizare și inversare, mirror HR real fără mock, cutii/manoperă o singură dată.',
  'DocAction și motorul de posting nativ; compară rânduri și sume Fact_Acct înainte/după/repostare. Zero net nu dovedește absența postărilor duplicate; testele SQLite nu închid contabilitatea.'),
 ('A04','Achiziții, importuri, SPV și documente primare','A03',
  'Import/staging, e-Factura/SPV, SAGA, asociere document/furnizor/an și recuperare după eșec.',
  'N10: doi ani cu același furnizor/număr, celula ZK și selectarea/asocierea prin PO; guardul reassocierii se probează separat. Mapare explicită a datelor lipsă, fără completări fiscale fictive.',
  'Folosește documentele native C_Invoice/C_BPartner și atașamentele existente. Staging→document și document→fișier trebuie să păstreze aceeași identitate și perioada.'),
 ('A05','Gestiuni G1/G2, inventar și WMS','A03',
  'Mai multe G1 și G2, locatori, CPP/CPA distincte, BOM, asamblare/dezasamblare, pick și inventar.',
  'N05 și D02/D03: concurență editare BOM versus asamblare prin intrarea nativă; rețeta istorică, locator, cantități, set indivizibil și ambalaje. beforeSave izolat nu este PO.saveEx/OSGi.',
  'PP_Product_BOM/BOMLine, M_Product, M_Warehouse/M_Locator, documente de mișcare/inventar native și extensia EVA existentă. Conservarea componentelor, zero stoc contabil nou pentru CPA dezasamblabil, cost o singură dată în G1.'),
 ('A06','Comenzi și disponibilitate G3','A07',
  'Disponibilitate comună CPP/CPA, rezervare, conversie canal, stoc fizic și importul comenzii.',
  'Reconfirmă filtrarea liniilor inactive/alt client și datele vânzătorului; rezervare concurentă pe coș mixt P1/S1/S2 și anulare. G3 nu însumează stocul virtual al combinațiilor.',
  'M_Product/M_Storage și C_Order/Line cu metodele native și cititorii EVA existenți. Din aceeași origine verifică ID, UOM, cantitate, TVA, monedă, net/brut și adrese facturare/livrare.'),
 ('A07','Expediție, AWB, factură, plată și retur','A06',
  'Pick/aviz, validare comercială, AWB, facturare configurabilă, încasări/rambursuri și retur fizic/financiar.',
  'N06 și D05/D06: înfometarea elementului 2001, chei cu separator, retry și ordine greșită; aviz CO nu reprezintă livrare curier. Corelează resturi după livrare/retur parțial.',
  'M_InOut, C_Invoice, C_Payment/Allocation, DocAction. Nu se contactează curier/bancă/ANAF real; transportul sintetic se declară și persistarea documentului nativ se citește independent.'),
 ('A08','Canale, magazine, catalog și comisionari','A01',
  'Site pe canal, CPP/CPA și identitate, checkout, mapare, prețuri, drepturi comisionar; administrarea comenzilor numai ERP.',
  'N04: coliziuni ID/SKU/EAN/UPC în ambele ordini până la C_OrderLine.M_Product_ID; profil la checkout anonim și revocare. Documentația nouă pentru ajutor nu repară automat portalul.',
  'Catalog și conversii existente, API cu drepturi native pe firmă/canal. Oracol de preț calculat independent, adresă F/L separată și ID persistent; JSON local nu certifică o comandă ERP.'),
 ('A09','Frontend, meniuri, setări și experiența utilizatorului','A01',
  'Portal Flask, UI ZK nativ, meniuri contabile, ajutor contextual, formulare și setări compatibile pe gestiuni.',
  'N07, V04-UX/CLI/C67 și instrumentele R12 de ajutor: dry-run bootstrap, eșec de mapare, 16/70 rute fără articol dedicat; /app/remote versus aserțiunea istorică /webui/. Patru suite C67 împreună și oracol payload/200, nu acceptarea lui 500.',
  'AD_Menu/Window/Form/Process și dicționarul de ajutor existent. Probe desktop/mobil/tastatură, focus, stări gol/încărcare/eroare/timeout/parțial/succes, păstrarea datelor și revenire; UI până la efect server.'),
 ('A10','Build, distribuție, operare și unelte de audit','A02',
  'Dependințe, JAR/OSGi, readiness, restaurare, laboratoare, CI și toate scripturile executabile promovate din documentație.',
  'N11 și anexa celor 19: exit0 nu dovedește sănătatea ori conformitatea; test pozitiv și mutant cu eroare reală; timeout și ieșire distinctă. Un mutant nerulat nu este omorât; separă echivalent de supraviețuitor.',
  'Reutilizare runner și lifecycle existente numai după verificarea căilor/efectelor. Comparație SHA/OID, bundle activ, AD metadata, DB și endpoint; listă proprie de resurse cu curățare verificată.')
]
zones=[]
for aid,title,peer,scope,nextwork,native in zone_data:
 src=R/(aid+'_plan.json'); assert src.exists()
 zones.append({'id':aid,'title':title,'owner':aid,'peer':peer,'scope':scope,'detailed_original_plan':ref(src),'next_work':nextwork,'native_first_and_oracle':native,
  'boundary':'Responsabilitatea exactă pe cale este în Dispatch_R12; acest capitol adaugă control transversal. Titularul nu validează singur raportul propriu; granițele se acceptă de producător și consumator, apoi A11.',
  'front_back_db':'Pentru fiecare fișier legat de comportament: cale normală UI/API/job→serviciu→tabel/PO/document; pentru bibliotecă, test la apelant. Testele citite, parsarea, execuția, efectul persistent și recepția au stări distincte.',
  'status':'PLAN; NICIO EXECUȚIE PE R12'})

case_source=R/'executie/R11_plan_delta/A12_inventar_si_receptie_v2.json'
cases=copy.deepcopy(read(case_source)['bidirectional_transactional_cases'])
assert len(cases)==17
for case in cases:
 case['inherited_case_source']={'file':ref(case_source),'id':case['id']}
 case['r12_candidate']=HEAD
 case['r12_state']='DESCHIS; execuția nouă așteaptă planul A11 10/10'
 case['r12_reuse']='Ancora istorică și sursele candidate R11 rămân pentru trasabilitate; fiecare OID se confruntă cu catalogul R12, iar configurația/bundle/runtime se observă din nou înaintea creditului R12. Nicio probă istorică nu se redenumește drept executată R12.'

schema={
 'identity':['case_id','head_git','path_git','file_oid','mode','source_sha256','owner','peer','role','normal_entrypoint','requirement_source_hash_pointer','canonical_task_or_specific_mapping_gap','control_ids','pipeline_ids','producer_consumer'],
 'method':['actor_and_native_role','cabinet_client_org_channel','native_method_symbol_and_version','frontend_backend_db_path','fixture_seed_hash','config_dependency_runtime_hashes','preconditions','command_or_steps','positive_expected','counterexample_expected','independent_oracle','timeout_budget','before_after_new_connection','retry_reversal','cleanup_plan'],
 'result':['UTC_start_end','actual_positive','actual_counterexample','log_artifact_hashes','persistent_effect_or_justified_na','source_read_status','execution_status','persistence_status','peer_reception_status','limitations','finding_severity_confidence','open_actions'],
 'not_applicable':'N/A cere justificare pe fișier și consumator, validată de peer/A11. Documentația și imaginea au control de conținut/proveniență/consumator, nu se execută automat. O bibliotecă fără main se testează prin apelant; lipsa mediului este NEEXECUTAT, nu N/A.',
 'case_example':'Judecătorul T240: un report.tsv sintetic conform + capturi controlate versus rând lipsă/duplicat/invalid. Se compară rândurile și regulile R1–R11 cu un oracol independent, nu doar returncode. Se păstrează manifestul de intrare, stdout, rc, report și fișierele produse; nu există efect ERP în această probă.'
}

anchors=[R/'A11_rubrica_control.json',R/'A11_verdict_plan.json',R/'Index_trasabilitate.json',R/'Matrice_interfete.json',R/'executie/Matrice_nativa_reutilizare.json',
 R/'executie/R11_plan_delta/Plan_delta_R11_v3.json',R/'executie/R11_plan_delta/A11_verdict_plan_delta_R11_v3.json',
 R/'executie/R11_fisiere/A12/Val_04/MANIFEST_val_04.json',R/'executie/R11_fisiere/A11/Verdict_A11_R11_val04_v1.json',checkpath,
 P/'Inventar_delta_brut.json',P/'Manifest_sources_lues.json',P/'Manifest_A12_inventar_dispatch_R12.json',inventory_manifest,annex,
 P/'Catalog_Git_integral_per_fisier_R12_v2.jsonl.gz',P/'Dispatch_tehnic_integral_R12.jsonl.gz',P/'A12/Index_19_fise.json',P/'A12/v2/Documentatie_562_clasificare_v2.json',P/'A12/Dependente_19_instrumente.json',
 P/'A12/v2/Index_invers_R12_v2.jsonl.gz',P/'A12/v2/Matrice_forward_index_R12_v2.jsonl.gz',P/'A12/v2/QA_index_invers_R12_v2.json',P/'A12/v2/Corectie_nominala_T315_T316.json',P/'A12/Controale_audit_R12_I01_I19.json']
plan={
 'schema':'eva.audit.plan.R12.revision.1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base':BASE,'candidate':HEAD,
 'state':'PREDAT PENTRU A11; NICIO EXECUȚIE CANDIDAT PÂNĂ LA RECEPȚIA INDEPENDENTĂ 10/10','quality_score_plan':None,'gate_owner':'A11',
 'mandate':'Audit profesional fișier cu fișier pentru întregul backend/frontend EVA–iDempiere; cele zece zone lucrează cu A12 pentru fișele nominale și A11 pentru control independent. Folosirea maximă a iDempiere nativ și documentație clară sunt obligatorii.',
 'anchors':[ref(p) for p in anchors],
 'version_policy':{'observed_github_head':HEAD,'observed_utc':'2026-11-02T22:49:25.027Z','last_tested_received_head':BASE,'installed_candidate':'NECONFIRMAT; Git nu dovedește montarea. Se capturează separat JAR/bundle/AD/schema și clientul vizat.',
 'comparison':'Arbori compleți de pe Git server read-only, verificare mod/tip/OID; copia locală shallow nu permite concluzie de rescriere istoric doar din merge-base.',
 'new_change_gate':'Înainte de orice lot se verifică HEAD/populație/mediul laboratorului. Alt HEAD: nu se mută eticheta rezultatelor; se deschide delta și revizie de plan, cu A11 înaintea testelor noului candidat. Testele începute pe commit fix continuă numai pe acel commit.'},
 'population':intake['counts'],'population_snapshot':intake['live'],'authoritative_intake':read(inventory_manifest)['authoritative'],
 'coverage':{'full_tree':'183.469 căi urmărite nominal în catalog; 6.728 fișiere tehnice repartizate, inclusiv 16 scripturi din arhivă. 546 alte artefacte documentare modificate au clasificare și consumatori, fără credit de execuție.',
 'unchanged':'Toate cele 6.709 fișiere tehnice precedente au același mod/OID. Rămân în audit; egalitatea nu reprezintă lectură semantică, execuție, persistare sau recepție R12.',
 'previous_received':'Val_04: 116 fișiere cu exercițiu parțial, 20 criterii cu observații limitate în 6 taskuri; 652 fișe istorice/2.619 criterii. Nu sunt totaluri de validări integrale. 17 contracte rămân deschise.',
 'reuse_conditions':['Exact OID/mod plus închidere a dependențelor de cod/config/resurse/JAR și consumator.','Aceleași ipoteze de actor, fixture, runtime și metodă; altă condiție determină reexecutare sau limită explicită.','Referință la hashul original și verdictul A11; se marchează REUTILIZARE JUSTIFICATĂ, nu execuție nouă.','Defectele vechi se etichetează demonstrate la 2fe90; prezența actuală se decide pe call-chain curent și dependențe, fără deducție numai din numele fișierului.'],
 'no_blanket_exclusion':'A12 confruntă toată arhiva și referințele din build/runner/importuri. Un fișier consumat de execuție se promovează indiferent de director; o captură se verifică prin proveniență și concordanța cu UI, nu doar existență.',
 'count_rules':'Evenimente pytest/subteste, teste distincte, programe și fișiere sunt numitori separați. Skip/nerulat nu este PASS, retestul a trei cazuri HR nu transformă două suite întregi în succes.'},
 'zones':zones,'A12':{'role':'Reconciliază fiecare cale și task, registry/Git/aliasuri, criterii și muchii inverse; nu semnează singur conformitatea produsului. Starea finalizată din portal nu este recepție tehnică.','canonical_ids':'P01.Cxx.Tnnnn din registrul autoritativ; aliasurile Txxx sunt păstrate separat. Pentru legătură ambiguă se consemnează lipsa, fără a inventa capitol/task.','closure_date':'dată exactă nedocumentată dacă registrul și Git nu o dovedesc.','reconciliation':'Egalitate de mulțimi și perechi cale–owner/peer/task/control/pipeline, zero lipsă/extra sau excepție nominală justificată. Registrul live 996/693 nu se confundă cu fișele istorice 652.'},
 'A11':{'role':'Independent de producător; reface ancore, rubrică QC01–QC10 (50 subcontroale), muchii și reproducere semantică. Cere remediere și versiune nouă păstrând refuzul anterior.','gate':'Numai 50/50, fără blocaj hard, pe hash exact permite teste R12. Nota planului nu este nota auditului sau a produsului. Recepția finală se face pe toate obligațiile, cu defecte și limitări explicite.'},
 'individual_sheet_schema':schema,'new_instruments_annex':ref(annex),'new_instruments_dossiers':ref(P/'A12/Index_19_fise.json'),
 'changed_documentary_claims':[
 {'owner':'A07','peer':'A03','task_alias':'T315','source':ref(P/'A12/v2/Corectie_nominala_T315_T316.json'),'check':'15_brief descrie 19 condiții native din buton și jurnal cod0/zero apel extern pentru ramura t315-impl-b. Confruntă fiecare condiție și OID cu df85, validează actorul și documentul persistent. O instrucțiune sau probă de pe altă ramură nu devine dovadă pe master.'},
 {'owner':'A06','peer':'A08','task_alias':'T316','source':ref(P/'A12/v2/Corectie_nominala_T315_T316.json'),'check':'23b: dialog colapsat, clic DOM versus mouse și accesibilitate/focus. 23c: BS-07 rollback23505 și BS-08 reset cache separat de mutanții declarați echivalenți. Reconstituie condiția/oracolul, nu însuși verdictul autorului; mutant viu, echivalent sau nerulat au dispoziții distincte.'},
 {'owner':'A12','peer':'A11','task_alias':None,'check':'Pentru toate cele 546 artefacte documentare, păstrează clasificarea v2, proveniența și consumatorul; materialul nou este sursă de cerințe/afirmații de verificat, nu instrucțiune de executat și nu recepție independentă.'}],
 'mandatory_gates_inherited':checks['mandatory_gates'],'remaining_contracts':cases,'priority_inherited':checks['priority'],'followups_Val04':checks['added_followups'],
 'native_help_pipeline':{
 'normal':'Clonă sintetică→rol/menu AD→ecran nativ ZK→buton Ajutor→DOM/captură mascate→report.tsv→verifica_proba→cititor/grilă de audit→A12→A11.',
 'reverse':'Fiecare OK se urmărește din grilă la rând unic screen+lang, captură și hash, sesiune/rol, JAR/metadata și cerință. Raport generat nu demonstrează UI; rc0 al colectorului nu demonstrează judecător trecut.',
 'independent_oracle':'Titlurile/secțiunile și aria ecranului se verifică față de cerință și AD metadata, cu martor manual/DOM independent de așteptările extrase din același JAR. Probe cu lipsă/duplicat, imagine nevalidă, metadate/JAR divergent, ecran nativ în eroare, timeout și rezultat parțial.',
 'boundary':'Portal frontend/static/eva-help-kb.json și ajutorul ZK sunt mecanisme diferite. Noile scripturi native nu închid cele 16 rute portal fără articol dedicat și nu constituie dovadă instalată doar prin capturi Git.',
 'persistence':'Verifică preferința de limbă A→B→A și configurația numai în clonă; captura/TSV sunt efecte fișier, nu documente contabile. Capturile sunt mascate înainte de publicare.'},
 'instrument_preflight':[
 'Nu se execută direct surse noi înaintea planului 10/10. După poartă: inspectare căi absolute, ștergeri, subprocese, conexiuni, shell expansion, env și scrieri Git; numai copie de lucru sintetică dedicată.',
 'git merge-tree --write-tree poate modifica magazinul de obiecte; scripturile T232 și garzi.sh nu sunt read-only doar prin comentariu. Se folosesc clone de laborator proprii; niciun proces remote operațional care scrie.',
 'garzi.sh poate șterge scratch absolut; reteta_L6.sh poate înlocui dovezi-80. Se verifică destinația absolută și proprietarul înainte; pathurile operaționale, arhivele sigilate și bazele sursă nu se montează cu scriere.',
 'Când este necesară adaptarea pathurilor: păstrează originalul/OID și patchul de harness; rezultatul este comparator declarat, nu execuție originală byte-identică. Fără destinații rămase necontrolate; altfel proba rămâne NEEXECUTAT.',
 'Judge/corpus: OK implicit în lipsa observațiilor nu este dovadă. Ieșire 0 care doar tipărește probleme se verifică semantic. Mutant care nu pornește este NERULAT; mutant echivalent cere argument și peer, fără a umfla scorul.'
 ],
 'native_clone_reuse':{'preferred_existing':'tools/help/pregateste_cabinet_help.sh și tools/status/containere_test.sh, plus captureaza_ecrane.py și mecanismul de mascări existente; se fixează OID înaintea folosirii.',
 'source':'Helperul implicit pornește de la q31/backup operațional. Nu se execută implicit. Se pregătește seed GardenWorld/sintetic cu proveniență, hash și compatibilitate release; zero date personale/producție. Dacă seedul nu e compatibil, reconstituire minimală documentată înaintea oricărei capturi.',
 'bootstrap':'JDBC singur nu inițializează CConnection/AdempiereDatabase/Service.locator. Preferă runtime/OSGi existent pe clonă, nu înlocuirea PO cu dubluri numite native. startupEnvironment poate atinge email/config; exclude outbound și joburi/schedulere.',
 'preflight':'Local Docker engine este momentan oprit; nu se pornesc containere pe serverul operațional. Verifică runtime local existent, spațiu, porturi loopback libere și registre de laboratoare. Nu presupune disponibilitatea pe baza unui script.',
 'restore_ready':'Nu accepta pg_restore || true sau ultima afișare HTTP drept dovadă. Refuz la restaurare incompletă, lipsă tabele/config, bundle inactiv sau endpoint nesănătos după buget. Oracle independent DB + API/DOM + rol sintetic.',
 'cleanup':'ID resursă/proprietar/rundă/port/volum/dataset, shutdown/drop și verificare proces+port+fișier. Nu se șterge resursa altei execuții. Se păstrează numai dovezile minimizate și seedurile autorizate.'},
 'execution_schedule':[
 {'stage':'0 — plan','owners':['COORDONATOR','A12','A10','A11'],'work':'Inventar complet, lectură pentru plan, anexe și audit 50/50; fără teste produs.'},
 {'stage':'1 — instrumente pure','owners':['A09','A10'],'peer':['A01','A02'],'work':'După A11: validatoare/fixtures originale T240 și contraexemple independente; cititori de grile/corpus, registre și mutanți într-un scratch nou. Niciun efect operațional.'},
 {'stage':'2 — regresii și resturi','owners':['A01','A02','A03','A04','A05','A06','A07','A08','A09','A10'],'work':'Coada N03–N11 și V04: loturi de cel mult două laboratoare scriitoare independente; restul lectură/peer. Fiecare executor verifică resurse active și dependențe înainte. Probele pe 6709 neschimbate continuă, fără substituire cu numai delta.'},
 {'stage':'3 — nativ și granițe','owners':['A05','A03','A07','A08','A09','A10'],'work':'Clonă sintetică nativă și 17 contracte cu predare înainte/înapoi. Lipsa runtime pentru o probă nu oprește lecturile și componentele realizabile.'},
 {'stage':'4 — recepție','owners':['A12','A11'],'work':'Reconciliere nominală, fișier→cerință și invers, publicare română, verdict separat audit/produs, reluare a probelor insuficiente.'}],
 'performance_and_budgets':{'pure_tools':'Măsoară validare pe corpusul original, apoi 1.000 și 10.000 rânduri sintetice cu duplicate la început/sfârșit; timeout 60s pe lot și limită 256MiB urmărită. Pragurile sunt bugete de laborator, nu SLA produs. Dacă parserul refuză legitim volumul în afara contractului, raportează limita; nu inventa obligație comercială.',
 'ui':'Timeout explicit per ecran/acțiune, două dimensiuni 1366×900 și 390×844 pentru suprafețele responsive, tastatură/focus; UI nativ poate avea constrângere desktop documentată, nu se presupune suport mobil.',
 'backend':'Concurență cu două tranzacții/barieră și citire din conexiune nouă; paginare 1999/2000/2001 la T216. Query plan și cost pe date sintetice; niciun load-test operațional.'},
 'reporting':['Raportul român separă problemă observată, condiție, efect, nivel probă, ajustare nativă recomandată și test de recepție. Nu se schimbă aplicația în acest audit.','Fiecare raport include auto-checklist și peer; A11 respinge lipsa oracolului, erori ascunse, duplicarea numărătorilor sau concluzii mai largi decât proba.','Rundele/sigiliile anterioare rămân imuabile; paginile publice curente trimit la R11 recepționat și R12 în starea lui reală. Notificări doar pentru progres material/eroare/recepție/dependență externă indispensabilă.'],
 'external_dependency':'Nicio dependență externă nu blochează acum tot auditul. Stația WMS nu condiționează codul. Se continuă componentele și pregătirea nativă; dacă rămâne exclusiv o intervenție externă, se semnalează exact o dată și se suspendă reluările conform mandatului.',
 'closure':'Plan 10/10 nu înseamnă audit finalizat. Numai A11 poate recepționa integral după toate controalele și contractele ori neaplicabilități individuale acceptate; zero înlocuire a rezultatelor negative prin sumă mare de teste verzi.'
}
plan_ref=save('Plan_delta_R12_v1.json',plan)
sections=[]
for z in zones:
 sections.append('<section><h2>'+html.escape(z['id']+' — '+z['title'])+'</h2><p>'+html.escape(z['scope'])+'</p><p><b>Următoarele probe:</b> '+html.escape(z['next_work'])+'</p><p><b>Reutilizare și rezultat verificabil:</b> '+html.escape(z['native_first_and_oracle'])+'</p><p>Peer: '+z['peer']+'. <a href="../../'+z['detailed_original_plan']['path']+'">Checklistul detaliat moștenit</a></p></section>')
page='''<!doctype html><html lang="ro"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Plan de audit R12 — EVA iDempiere</title><style>body{font:17px/1.6 system-ui;margin:auto;max-width:1100px;padding:24px;color:#172c40;background:#f7fafc}section{padding:20px;margin:18px 0;background:white;border:1px solid #cbd5e1;border-radius:12px}h1,h2{line-height:1.25}code{overflow-wrap:anywhere}a{color:#075b91}li{margin:8px 0}.gate{border-left:6px solid #ac6500;padding:15px;background:#fff5dc}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px}</style><h1>Plan R12 — auditul întregului backend și frontend</h1>'''
page+='<p class="gate"><b>Plan predat A11. Execuția noii revizii așteaptă 10/10.</b> Documentul nu este rezultat de test și nu certifică produsul.</p>'
page+='<p>GitHub candidat: <code>'+HEAD+'</code>. Ultimul cod testat și recepționat parțial: <code>'+BASE+'</code>.</p>'
page+='<section><h2>Ce s-a schimbat și ce rămâne de verificat</h2><p>183.469 căi Git; 565 diferențe: 557 adăugate și opt modificate. Cele 6.709 fișiere tehnice precedente sunt identice. Adăugăm 19 instrumente: trei în tools și 16 promovate din documentație. Auditul continuă pe toate cele 6.728 fișiere tehnice.</p><p>Val_04 are 116 fișiere cu exercițiu parțial și 20 criterii în șase taskuri; toate cele 17 contracte sunt deschise. Starea finalizată a unui task și aceeași identitate Git nu reprezintă dovadă nouă.</p><p><a href="Plan_delta_R12_v1.json">Planul complet și ancorele SHA</a> · <a href="Plan_instrumente_noi_A10_v1.html">Cele 19 instrumente — probe individuale</a> · <a href="A12/v2/Rezumat_inventar_dispatch_R12_v2.json">Inventarul A12</a></p></section>'
page+='<section><h2>Ordinea de lucru și metoda comună</h2><ol>'+''.join('<li><b>'+html.escape(s['stage'])+'</b> — '+html.escape(s['work'])+'</li>' for s in plan['execution_schedule'])+'</ol><p>Pentru fiecare fișier: OID, responsabil și peer, cerință, cale normală, actor, metodă nativă, martor pozitiv și contraexemplu, rezultat, efect persistent și limită. Inventarierea, lectura, execuția și recepția se consemnează separat.</p></section>'
page+=''.join(sections)
for title,content in [('Porțile obligatorii',plan['mandatory_gates_inherited']),('Siguranța și corectitudinea instrumentelor',plan['instrument_preflight']),('Laboratorul nativ — reutilizarea existentului',plan['native_clone_reuse']),('Șablonul obligatoriu de probă',schema)]:
 page+='<section><h2>'+html.escape(title)+'</h2><pre>'+html.escape(json.dumps(content,ensure_ascii=False,indent=2))+'</pre></section>'
page+='<p>SHA plan JSON: <code>'+plan_ref['sha256']+'</code>. A11 acordă separat nota planului, recepția probelor și verdictul final. Auditul nu schimbă sistemele operaționale.</p></html>'
(P/'Plan_delta_R12_v1.html').write_text(page,encoding='utf-8')
print(json.dumps({'plan':plan_ref,'html':ref(P/'Plan_delta_R12_v1.html')},ensure_ascii=False))
