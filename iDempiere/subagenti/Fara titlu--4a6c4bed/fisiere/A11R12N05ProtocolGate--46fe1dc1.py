import json,hashlib,datetime,subprocess,gzip
from pathlib import Path
R=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');B=R/'executie/R12_fisiere';N=B/'A05_N05_lot03';O=B/'A11/Val03_preflight'
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(name,obj):
 p=O/name;assert not p.exists();p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return {'path':str(p.relative_to(R)).replace('\\','/'),'sha256':h(p)}
proto=N/'Protocol_N05_nativ_v2.json';assert h(proto)=='4c4e641b22d7e0edd6b930335fd5b18ba5e66991ff7c4ff207097464a4ef533e';d=read(proto)
checks=[]
for x in read(N/'Identitati_sursee_supliment_v2.json'):
 p=N/'surse_df85'/x['path'].split('/src/com/eva/ro/contab/')[1];raw=p.read_bytes();checks.append({'source':x['path'],'sha256':h(p),'oid':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),'expected_oid':x['oid']});assert checks[-1]['sha256']==x['sha256'] and checks[-1]['oid']==x['oid']
catalog=R/'executie/R12_plan_delta/Catalog_Git_integral_per_fisier_R12_v2.jsonl.gz';wanted={x['source']:x for x in checks}
with gzip.open(catalog,'rt',encoding='utf-8') as f:
 for line in f:
  row=json.loads(line)
  if row.get('path') in wanted: wanted[row['path']]['catalog_record']=row;assert wanted[row['path']]['oid'] in str(row)
assert all('catalog_record' in x for x in checks)
native=Path('D:/CodexWork/a05-r12-native-cache/org.adempiere.base_13.0.0.202603090043.jar');assert h(native)==d['G01']['native_core_sha256']
jp=subprocess.run(['C:/Program Files/Java/jdk-21/bin/javap.exe','-c','-p','-classpath',str(native),'org.adempiere.util.ProcessUtil'],capture_output=True,text=True,encoding='utf-8',check=True)
textpath=O/'ProcessUtil_native_javap_N05.txt';assert not textpath.exists();textpath.write_text(jp.stdout,encoding='utf-8')
labels=[
('P01','Identitate df85, separată de HEAD1687 și de core/seed','candidate/version_separation/G01'),
('P02','OID/SHA surse și JAR, plus clase încărcate, fără echivalare automată source=bytecode','G01/G03.preflight_effective_binding'),
('P03','Schema fizică versus AD, tipuri, chei/index și parametri efectivi','G01.schema_scope_before_credit'),
('P04','Migrări doar proveniență, LastBuildInfo păstrat, oprire la mismatch relevant','G01.schema_scope_before_credit'),
('P05','Folosirea mecanismelor existente ModelWms/EvaMetadata cu înainte/după/idempotence','G01.before_business_execution'),
('P06','Baseline original ProceseEcran managed=true; JobFundal/UI numai legătură statică','G03.normal_entry/G06_cases.N05-S01'),
('P07','C01/R01 managed=false declarat drept variație de coordonare, nu click identic','G03.transaction_control_variant'),
('P08','Fabrica OSGi și handler-ele originale legate; fără SurseTest sau depozit fals','G03.preflight_effective_binding'),
('P09','Validatori nominali păstrați conform seed, nu dezactivare globală','G03.native_validators'),
('P10','Actor/rol/client/org și refuz drept separat; fără credit autentificare','G03.actor/G06_cases.N05-N03-ROL'),
('P11','Fixture sintetică prin modele existente; identități separate fără revendicare de nereutilizare perpetuă','G05.fixture/G05.fixture_initialization'),
('P12','Serial ambalare/dezambalare cu conservare10 și jurnal semnat','G06_cases.N05-S01'),
('P13','BOM comis folosit refuză modificarea cu cauză exactă și recitire','G06_cases.N05-S02'),
('P14','Concurență READ COMMITTED cu PID/txid/Trx distincte și invizibilitate precommit','G06_cases.N05-C01'),
('P15','11 piese este defect/contraexemplu, nu PASS; timeout/locks nu devin automat defect','G06_cases.N05-C01'),
('P16','Rollback/retry cu instanță nouă și efect recitit, fără pretenție idempotentă','G06_cases.N05-R01'),
('P17','Qty0, stoc insuficient, rol fără acces sunt trei negative distincte cu cauze exacte','G06_cases.N05-N01-QTY/N02-STOC/N03-ROL'),
('P18','Recitire în conexiune nouă, instanța procesului separată de WMS și G1/Fact','G05.snapshots/persistence'),
('P19','Loopback/JVM guard/canari, fără servicii operative și fără relaxare spre exterior','isolation/stop_conditions'),
('P20','Finally/cleanup verificat, păstrarea încercărilor, limitele UI/DocAction/G1G2G3 clare','cleanup/non_scope/stop_conditions')]
v={'schema':'A11.N05.protocol.gate.v2','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'A11 independent','candidate':d['candidate'],'protocol':{'path':str(proto.relative_to(R)).replace('\\','/'),'sha256':h(proto)},'decision':'POARTA_PROTOCOL_CONCRET_ADMISA; RESTAURARE_SINTETICA_SI_PREFLIGHT_PERMISE; BUSINESS_NUMAI_DUPA_CONDITIILE_DE_READINESS_DOCUMENTATE','protocol_plan_score':{'earned':10,'maximum':10,'rubric':'20 controale de proiectare × 0,5 puncte; se evaluează protocolul, nu îndeplinirea precondițiilor runtime sau produsul.'},'controls':[{'id':a,'criterion':b,'anchor':c,'design_status':'ACOPERIT','points':0.5,'runtime_status':'DE_VERIFICAT_LA_EXECUTIE'} for a,b,c in labels],'independent_evidence':{'previous_21_sources_and_jar':'QA_A11_receptie_supliment_0039_v1.json SHA56476bc940401af71775373c75a43d3db852140c6cd2c98c8d702563a15d836c','supplement_2_sources':checks,'native_ProcessUtil':{'artifact':str(textpath.relative_to(R)).replace('\\','/'),'sha256':h(textpath),'core_sha256':h(native),'finding':'startJavaProcess(Properties,ProcessInfo,Trx,boolean,IProcessUI): commit la offset129 și rollback/close la254+ sunt condiționate de managedTrx. Lectură bytecode, fără inițializare/execuție proces.'},'source_reading':'NotaSetWmsProces/StocWms/EvaNotaSetBomEvents și ProceseEcran au fost citite; cauzele qty/drept/piese corespund cheilor existente. Nu se deduce rezultatul concurenței din lectura SQL.'},'execution_conditions':['Arhivează harnessul/bindingul/diffurile înaintea execuției business și păstrează fiecare încercare nereușită ca atare.','Restaurarea strictă și verificarea build/schema/binding preced S01. Un serviciu relevant lipsă, clasă diferită sau mismatch de coloană oprește creditul etapei; nu se repară produsul în probe.','S01 trebuie să confirme calea ProceseEcran originală și înainte/după persistent înainte de concurență.','Concurența cere dovada două sesiuni și efect T1 invizibil extern înainte de T2; altfel cazul este NERULAT/neconcludent, nu respingere funcțională.','Handler-ele globale relevante inventariate nominal; excludere relevantă nouă cere explicarea diferenței înainte de continuarea etapei.','Dacă izolarea refuză o operație, păstrează rezultatul și adaptează numai fixture/harness în limite; nu slăbi gardele către operațional.','Un refuz automat de cleanup se respectă și se raportează ca resursă rămasă, fără ocolire.'],'score_not_transferred':['Zero credit de execuție acordat acum.','Nu închide T355/P01.C03.T0029, C03/C10 ori niciunul dintre cele17 contracte.','Nu validează login/ZK, DocAction/Fact_Acct, cutii/manoperă o singurădată înG1, G3disponibil comun sau identități permanente CPP/CPA.'],'v1_disposition':'Protocolul v1 rămâne imuabil; v2 corectează traseul managedTrx, negativele și precondițiile nominale.','product_score':None,'operational_writes':0}
verdict=save('Verdict_A11_protocol_N05_v2.json',v)
seal=save('Sigiliu_A11_protocol_N05_v2.json',{'files':[verdict,{'path':str(textpath.relative_to(R)).replace('\\','/'),'sha256':h(textpath)}],'no_global_product_score':True})
print(json.dumps({'verdict':verdict,'seal':seal},ensure_ascii=False))
