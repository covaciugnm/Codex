from pathlib import Path
import json,hashlib,datetime,subprocess,os,zipfile
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');OUT=R/'executie/R12_fisiere/A05_N05_lot03'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();j=json.loads((OUT/'Protocol_N05_nativ_v1.json').read_text(encoding='utf8'))
j['schema']='A05.N05.protocol.v2';j['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();j['supersedes_without_overwrite']={'path':'Protocol_N05_nativ_v1.json','sha256':sha(OUT/'Protocol_N05_nativ_v1.json')}
j['G03']['normal_entry']='S01: DialogNotaSetWms → JobFundal.pornesteProces → ProceseEcran.ruleaza original → MProcess.processIt(pi,trx), managedTrx=true → ProcessUtil/Core.getProcess → EvaProcessFactory original → NotaSetWmsProces → StocWms; harness invocă ProceseEcran.ruleaza original, fără UI/click real.'
j['G03']['transaction_control_variant']='C01/R01 folosesc overloadul nativ MProcess.processIt(pi,trx,false), aceeași AD_Process/class/parametri/fabrică, pentru a reține commitul. Este o variație de coordonare a tranzacției din harness; nu se prezintă drept executarea identică a clickului. Baseline S01 managed=true trebuie să reușească înainte de C01.'
j['G03']['native_validators']='Seed verificat offline: LiberoValidator AD_ModelValidator50000=N (clasa lipsește din core13), FixedAssets org.idempiere.fa.model.ModelValidator50004=Y (clasa există în core, abonează Invoice/InvoiceLine/MatchInv), ProductPriceValidator200002=N. Se păstrează stările exact, FixedAssets activ; nu se activează Libero artificial și nu se dezactivează global validatorii.'
j['G03']['preflight_effective_binding']=[
 'Consemnează FrameworkUtil.getBundle/Class CodeSource și SHA resursei .class încărcate pentru EvaProcessFactory, NotaSetWmsProces, EvaNotaSetBomEvents, ProceseEcran și componentele efectiv apelate; compară cu intrările JAR-ului Git df85.',
 'Înregistrează fabrica originală în OSGi real ranking1; enumeră service.reference/service.ranking și identitatea obiectului. Leagă handler-ele originale de EventManager; enumeră serviciile EventHandler pentru același obiect, event.topics și event.filter. Toate cele6abonamente BOM/linie înainte-new/change/delete trebuie prezente.',
 'Citește reflectiv NUMAI valoarea câmpului static NotaSetWmsProces.surseTest și cere null; nu îl modifică. Înregistrările originale și SurseTest=null sunt condiții înainte de creditul procesului.',
 'Inventar nominal de handler-e și excluderi din EvaActivator: EvaNotaSetBomEvents pentruBOM și EvaWmsGardaEvents pentru warehouse/locator/pereche sunt obligatorii. EvaSetLinieEvents (linii de documente), EvaValidareProdusEvents (inventar/linii), EvaValidareWmsEvents (inventar/NIR) sunt inactive doar pentru tabele neatinse în probă. Se verifică și abonamentele globale ale celorlalte handler-e din activator; orice efect relevant necontabilizat oprește etapa și cere completarea protocolului.',
 'Mecanismul nativ ModelValidationEngine.getInfoDetail/registrul seed confirmă validatorul FixedAssets. Nu se pretinde că injectarea actorului este login sau RBAC integral.'
]
j['G01']['schema_scope_before_credit']={
 'tables':['AD_System','AD_MigrationScript','AD_Process','AD_Process_Para','AD_Process_Access','AD_PInstance','AD_User_Roles','M_Product','M_Warehouse','M_Locator','M_StorageOnHand','PP_Product_BOM','PP_Product_BOMLine','EVA_PerecheWms','EVA_StocWms','EVA_MiscareWms','EVA_SetariFirmaPerioada'],
 'comparisons':'AD_Table/AD_Column față de pg_catalog/information_schema, tipuri/null/default, PK/FK/indexuri; toate coloanele consumate și metoda ModelWms exactă. AD_Process VALUE/clasa/unicitate/activ și cele6parametri, tipurile și accesul rolului. Înainte/după orice pas existent de metadata; a doua trecere idempotentă.',
 'build_disposition':'Cele64nume CO/Y sunt doar proveniență. Version2026-03-09/Releaseno13/lastMigration202603090019 plus schema nativă și efectele migrărilor pentru tabelele atinse determină compatibilitatea SCOPATĂ. LastBuildInfo placeholder/FailOnBuildDiffer=N rămâne limită explicită; nici isBuildOK=true, nici actualizarea câmpului nu sunt oracle. Mismatch pe un câmp/serviciu folosit blochează creditul testului. Fără dovadă globală de compatibilitate toate modulele.'
}
for c in j['G06_cases']:
 if c['id']=='N05-S01':c['normal_launcher']='ProceseEcran.ruleaza original; MProcess managedTrx=true, commit/close native.'
 if c['id']=='N05-C01':
  c['barrier_evidence']='În T1 înainte de barieră: SELECT pg_backend_pid(), txid_current(), current_setting(transaction_isolation), Trx.getTrxName, AD_PInstance_ID și stoc în propria tranzacție. Conexiune read-only separată confirmă încă10piese/0set și0mișcări noi ale instanței, deși T1 vede8/1. T2 înregistrează propriul PID/txid/Trx/izolare distincte. Numai după această probă se încearcă saveEx și commitT2; se păstrează ordinea evenimentelor și orice așteptare pg_locks. Eroare în dovada necomiterii invalidează concurența.'
  c['timeouts']='Barieră maximum15s; verificări externe scurte; două tranzacții maximum45s și statement_timeout30s. Dacă T2 e blocat după3s, oracolul citește locks și se elibereazăT1; refuzul/revalidareaT2 după eliberare este evaluat separat, nu calificat ca mutant ucis.'
j['G06_cases']=[c for c in j['G06_cases']if c['id']!='N05-N01']+[
 {'id':'N05-N01-QTY','input':'Qty=0, toate celelalte câmpuri valide','expected_cause':'t355.refuz.cantitate tradus prin Etichete.t original, rezultat procesFalse/pi.error; nu SQLException/ClassNotFound','persistent_oracle':'Aceleași10piese/0set și0mișcări ale instanței; AD_PInstance poate consemna refuzul, separat de stoc.'},
 {'id':'N05-N02-STOC','input':'Qty=6 la BOM2 și stoc10','expected_cause':'t355.refuz.piese pentru codul componentei și lipsă2; comparație cu textul exact parametrizat, nu catch generic','persistent_oracle':'10piese/0set neschimbate și0mișcări; BOM2 neschimbat.'},
 {'id':'N05-N03-ROL','input':'Același proces/parametri valizi și rol demo verificat fără AD_Process_Access=Y sau rol sintetic creat nativ cu acces absent','expected_cause':'t355.refuz.drept exact; contextul și lipsa dreptului sunt capturate înainte','persistent_oracle':'Zero deltaWMS și nicio modificare aBOM pe conexiune nouă; rezultat procesFalse. Nu conferă recepție completă login/tenant.'}
]
j['G05']['fixture_initialization']='Preferat: MProduct/MWarehouse/MLocator/MPPProductBOM/MPPProductBOMLine native; MStorageOnHand.add pentru cantități sintetice inițiale explicit fixture, apoi PerecheWms.activeaza original creeazăG2 și stoculWMS. Această preîncărcare este pregătire de laborator, nu document contabil sau recepțieG1. Snapshotul de neatingere G1/Fact_Acct începe DUPĂ pregătireafixturei.'
j['quality_gate_request']='A11 să valideze protocolul concret; restaurarea și testele nu au pornit. Acceptarea planului nu primește rezultat de produs. V1 păstrat imuabil.'
extra=[];git='D:/CodexWork/eva-audit-p01-src-20261101';env=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0')
for name in ['form/JobFundal.java','form/ProceseEcran.java']:
 path='idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/'+name
 r=subprocess.run(['git','-C',git,'rev-parse',j['candidate']+':'+path],capture_output=True,env=env);assert r.returncode==0;key=r.stdout.decode().strip()
 r=subprocess.run(['git','-C',git,'cat-file','blob',key],capture_output=True,env=env);assert r.returncode==0;data=r.stdout
 target=OUT/'surse_df85'/name;assert not target.exists();target.write_bytes(data)
 extra.append({'path':path,'oid':key,'sha256':sha(target),'owner':'A05','peer':['A09','A11'],'requirement':'G03 traseu normal de lansare proces','role':'JobFundal legătură statică; ProceseEcran baseline de integrare propus','positive':'S01','negative':'N05-N01-QTY/N02-STOC/N03-ROL','persistent_effect':'AD_PInstance și WMS prin proces, neexecutate încă','limit':'Fără UI/JobFundal executat; managed=false doar variație nativă de coordonare pentru C01/R01.'})
(OUT/'Identitati_sursee_supliment_v2.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2),encoding='utf8')
p=OUT/'Protocol_N05_nativ_v2.json';assert not p.exists();p.write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'path':str(p),'sha256':sha(p),'product_started':False},ensure_ascii=False))
