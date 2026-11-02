import json,sqlite3,zipfile,io,csv,re,hashlib,html,traceback
from pathlib import Path
from loguru import logger
from androguard.core.axml import ARSCParser
from lxml import etree
logger.disable('androguard')
B=Path(r'D:\Codex\iFLYTEK-audit');P=B/'deliverable';C=sqlite3.connect(B/'results/catalog.sqlite');C.row_factory=sqlite3.Row
def write(p,rs):
 p.parent.mkdir(exist_ok=True)
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  cols=list(rs[0]) if rs else ['no_records'];w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(rs)
locales=[];cache={};errors=[]
def comp(z,vid,name):
 if 'resources.arsc' not in z.namelist():return
 b=z.read('resources.arsc');h=hashlib.sha256(b).hexdigest()
 if h not in cache:
  try:
   a=ARSCParser(b);cache[h]=[(pkg,loc.replace('\x00','') or 'default') for pkg in a.get_packages_names() for loc in a.get_locales(pkg)]
  except Exception as ex:cache[h]=[];errors.append({'version':vid,'component':name,'error':str(ex)})
 for pkg,loc in cache[h]:locales.append({'version':vid,'component':name,'resource_package':pkg,'locale':loc,'resources_sha256':h,'interpretation':'Android resources incl SDKs; not proof of translation language support'})
for v in C.execute('select * from versions').fetchall():
 print(v['id'],flush=True)
 with zipfile.ZipFile(v['path']) as z:
  if v['path'].endswith('.xapk'):
   for e in z.infolist():
    if e.filename.endswith('.apk'):comp(zipfile.ZipFile(io.BytesIO(z.read(e))),v['id'],e.filename)
  else:comp(z,v['id'],Path(v['path']).name)
write(P/'03_Conectare_API/android-resource-locales.csv',locales);write(P/'06_Audit/resource-parser-errors.csv',errors)
configs=[];components=[];ns='{http://schemas.android.com/apk/res/android}'
for f in (P/'01_Inventar/manifests').glob('*.xml'):
 x=etree.parse(str(f)).getroot();app=x.find('application');sdk=x.find('uses-sdk')
 if app is None:continue
 configs.append({'manifest':f.name,'package':x.get('package'),'target_sdk':sdk.get(ns+'targetSdkVersion') if sdk is not None else 'not_declared','debuggable_declared':app.get(ns+'debuggable','not_declared'),'allowBackup_declared':app.get(ns+'allowBackup','not_declared'),'usesCleartextTraffic_declared':app.get(ns+'usesCleartextTraffic','not_declared'),'networkSecurityConfig_declared':app.get(ns+'networkSecurityConfig','not_declared'),'interpretation':'declared values only; effective policy requires resource/OS verification'})
 for el in app:
  if el.tag in ['activity','activity-alias','service','receiver','provider']:
   components.append({'manifest':f.name,'kind':el.tag,'name':el.get(ns+'name'),'exported_declared':el.get(ns+'exported','not_declared'),'permission':el.get(ns+'permission','not_declared'),'readPermission':el.get(ns+'readPermission','not_declared'),'writePermission':el.get(ns+'writePermission','not_declared'),'intent_filters':len(el.findall('intent-filter')),'interpretation':'exposure inventory; not an exploitability finding'})
write(P/'06_Audit/manifest-application-policy.csv',configs);write(P/'06_Audit/manifest-components.csv',components)
tests=[('Bluetooth/BLE','Pair/unpair/reconnect each device and app version','GATT service/characteristic UUIDs, negotiated MTU, notification/write directions and message captures'),('Audio','Record/play/translate both directions','Actual PCM/Opus/AAC settings, packet framing, timestamps and results'),('Video/imagine','Capture and transfer image/video','Actual endpoint or transport, file signatures, codecs, throughput, retry/error evidence'),('USB/drivere','Connect each tablet/glasses by USB','VID/PID, USB interfaces/endpoints, Android USB permission and actual driver binding'),('WiFi/retea','Pair device, switch networks, reconnect','WiFi Direct/BLE-to-WiFi handover, TCP/UDP/WebSocket traces, TLS trust results'),('Multilingvism','Test Romanian, English and Chinese in UI, ASR, TTS and translation','Separate UI locale, online translation, offline model availability and account entitlement'),('Autentificare','Owner tests supported country codes and login methods','Server responses and UI behavior; no automated SMS or credential use by this audit'),('Securitate','Review release signatures, exported components, trust handling and storage','Signing certificate fingerprints, source-level reachability and device tests; no conclusion from SDK presence alone'),('Flutter AOT','Recover each distinct libapp hash with compatible Dart/architecture toolchain','Per-hash recovered function table, parser logs and independent address/byte verification')]
write(P/'06_Audit/runtime-and-aot-test-plan.csv',[{'area':a,'test':t,'required_evidence':e,'status':'OPEN'} for a,t,e in tests])
findings=[]
queries=[('Autentificare SMS',"e.kind='const-string' and (e.value like '%/login/phone/%' or e.value like '%account.xfinfr%')"),('Bluetooth si moduri audio',"e.kind='field-use' and (e.value like '%MODE_GLASS_SAME_VOICE%' or e.value like '%MODE_LIVE_LISTENING%')"),('Punte Flutter/native',"e.kind='invoke' and e.value like '%MethodChannel%invokeMethod%'"),('Transport BLE',"e.kind='invoke' and (e.value like '%BluetoothGatt;%writeCharacteristic%' or e.value like '%BluetoothGatt;%setCharacteristicNotification%')"),('USB',"e.kind='invoke' and (e.value like '%UsbManager;%openDevice%' or e.value like '%UsbDeviceConnection;%bulkTransfer%')"),('Video',"e.kind='invoke' and (e.value like '%MediaCodec;%configure%' or e.value like '%MediaMuxer;%writeSampleData%')")]
for title,where in queries:
 for row in C.execute('select distinct e.artifact,e.method_idx,e.offset,e.kind,e.value,m.signature from evidence e join methods m on m.artifact=e.artifact and m.idx=e.method_idx where '+where+' limit 12'):
  findings.append({'finding':title,**dict(row),'assessment':'static evidence only; SDK presence/reachability and device behavior need confirmation'})
write(P/'03_Conectare_API/selected-protocol-findings.csv',findings)
dictionary={'methods':'artifact + idx uniquely identify a DEX method_id. defined=1 belongs to class_data; defined=0 reference only. code_offset absolute DEX byte offset; code_hash hashes instruction bytes only, excludes handlers/debug. registers/inputs are register counts, not named original variables. flags are DEX access_flags.','fields':'artifact + idx identifies field_id; defined separates declaration and reference. signature contains owner/name/type.','variables':'debug_info parameter ordinal or local register/address; only names actually present in DEX debug metadata. address in 16-bit code units relative to method instructions.','evidence':'kind invoke/const-string/field-use: offset is code units from method instruction start. kind string-pool: offset is string_id, not byte offset. native-string: offset is ELF file byte offset. asset/Manifest: may use APK version id in artifact and null method_idx. Classification is heuristic.','key_candidates':'sha256 is fingerprint of candidate value, not a server credential. No raw candidate value. Shape/entropy can match hashes, IDs and SDK constants. Never validated against servers.','protocol_constants':'string_id or native byte offset; UUID/path candidate; no automatic claim of GATT service vs characteristic or active API endpoint.','native_symbols':'ELF dynsym/symtab entries (functions/objects/TLS/etc), not all internal stripped functions. defined=0 import; defined=1 has a non-undefined section index.','aot_functions':'Previously recovered Flutter symbols for the exact original libapp SHA only. Declaration is reconstructed analysis, not original Dart source. verified=1 means address/size aligned and within executable file segment, with code SHA256. It does not independently prove each inferred function boundary/name.','aot_field_offsets':'Generated field offset labels from previous AOT analysis, not original source variable names.','comparisons':'Method signature set differences and raw instruction hashes; not semantic equivalence, not whole-body/handler equivalence. All changes include third-party SDKs.','limits':'Static analysis only. No APK execution, server authentication, message sending or hardware testing. No fabricated 10/10. Full source-variable names may be irreversibly stripped.'}
(P/'02_Functii_variabile/data-dictionary.json').write_text(json.dumps(dictionary,ensure_ascii=False,indent=2),encoding='utf-8')
def table(rs):
 if not rs:return '<p>Nu există dovezi în selecția curentă.</p>'
 keys=list(rs[0]);return '<table><tr>'+''.join('<th>'+html.escape(k)+'</th>' for k in keys)+'</tr>'+''.join('<tr>'+''.join('<td>'+html.escape(str(r[k]))+'</td>' for k in keys)+'</tr>' for r in rs)+'</table>'
doc='<!doctype html><html lang="ro"><meta charset="utf-8"><title>iFLYTEK — dovezi și verificări</title><style>body{font:14px system-ui;padding:28px;color:#173243}table{border-collapse:collapse;width:100%;font-size:12px}td,th{border:1px solid #cdd8e1;padding:8px;overflow-wrap:anywhere;text-align:left}th{background:#e5eef4}p{line-height:1.6}</style><h1>Dovezi de conectare și plan de verificare</h1><p><a href="index.html">Raport principal</a>. Fiecare exemplu este legat de hash DEX, metodă și offset. Nu reprezintă un protocol complet confirmat.</p><h2>Exemple concrete</h2>'+table(findings)+'<h2>Resurse de limbă Android</h2><p>Resursele pot aparține SDK-urilor. Nu demonstrează limbile ASR/TTS/traducere disponibile în aplicație sau pe server.</p>'+table(locales)+'<h2>Politici declarate în manifest</h2><p>Valorile nedeclarate nu au fost înlocuite cu presupuneri despre comportamentul efectiv. Componentele complete se află în manifest-components.csv.</p>'+table(configs)+'<h2>Verificări rămase</h2>'+table([{'area':a,'test':t,'required_evidence':e,'status':'OPEN'} for a,t,e in tests])+'</html>'
(P/'00_Raport/dovezi-si-verificari.html').write_text(doc,encoding='utf-8');print('DONE',len(locales),len(configs),len(components),len(findings),'errors',len(errors),flush=True)
