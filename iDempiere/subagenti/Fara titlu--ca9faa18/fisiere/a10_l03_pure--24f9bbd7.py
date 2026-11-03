from pathlib import Path
import sys,os,importlib.util,json,hashlib,zipfile,struct,socket,subprocess,types,datetime
sys.stdout.reconfigure(encoding='utf-8');sys.stderr.reconfigure(encoding='utf-8');sys.dont_write_bytecode=True
L=Path('D:/CodexWork/a10-r12-l03/pure');L.mkdir(parents=True,exist_ok=False)
S=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A10_Instrumente_ramase_lot03/sources/proba_buton.py')
def checkpath(x):
 if isinstance(x,int):return
 if not Path(os.fsdecode(x)).resolve().is_relative_to(L.resolve()):raise PermissionError('AUDIT_WRITE_OUTSIDE')
def hook(e,a):
 if e.startswith('socket.') or e in ('subprocess.Popen','os.system'):raise PermissionError('AUDIT_EXTERNAL')
 if e=='open' and ((isinstance(a[1],str) and any(c in a[1] for c in 'wax+')) or (isinstance(a[2],int) and a[2]&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))):checkpath(a[0])
 if e in ('os.mkdir','os.rmdir','os.remove','os.chmod','os.utime'):checkpath(a[0])
 if e in ('os.rename','os.link','os.symlink'):checkpath(a[0]);checkpath(a[1])
sys.addaudithook(hook)
can=[]
for name,fn in [('network',lambda:socket.socket()),('exec',lambda:subprocess.run(['cmd','/c','echo','no'])),('write_outside',lambda:Path('D:/CodexWork/a10-outside-canary.txt').write_text('no'))]:
 try:fn();raise AssertionError('GUARD FAILED '+name)
 except PermissionError:can.append({'name':name,'blocked':True})
spec=importlib.util.spec_from_file_location('audit_original_proba',S);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
results=[]
def put(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def case(name,fn,oracle):
 try:r=fn();out={'value':r,'exception':None}
 except BaseException as e:out={'exception':type(e).__name__,'message':str(e),'code':e.code if isinstance(e,SystemExit) else None}
 results.append({'id':name,'kind':'ORIGINAL_PURE_COMPONENT','oracle':oracle,'observed':out})
def inventory(text):p=L/'e.tsv';p.write_text(text,encoding='utf-8');return m.citeste_e(p)
case('I17_E_valid',lambda:inventory('# comment\nWOne\tOne\nWTwo\tTwo\n'),'two exact identities with titles')
case('I17_E_duplicate',lambda:inventory('WOne\tOne\nWOne\tOther\n'),'observe whether duplicate identities are refused or retained; no receipt on row count')
case('I17_E_indented_comment',lambda:inventory('  # comment\nWOne\tOne\n'),'observe indented comment parsing; not a valid screen identifier')
case('I17_E_missing_title',lambda:inventory('WOne\n'),'missing title must remain explicit, not verified title')
case('I17_E_empty',lambda:inventory(''),'zero rows is not completed UI population')
case('I17_clean_cell',lambda:m.curat('  A\tB\r\nC  '),'A B C')
case('I17_title_prefix',lambda:[m.titlu_form(x) for x in ['EvA — Mașini','EVA - Mașini','',None]],'only exact existing prefix is removed')
eti={
'ajutor.ecran.buton':('Ajutor','Help'),'ajutor.ecran.titlu':('Ajutor — %s','Help — %s'),
'ajutor.ecran.rol':('La ce folosește','Purpose'),'ajutor.ecran.campuri':('Câmpuri','Fields'),
'ajutor.ecran.butoane':('Butoane','Buttons'),'ajutor.ecran.greseli':('Greșeli','Mistakes'),
'ajutor.ecran.ciorna':('Ciornă','Draft'),'ajutor.ecran.doar_ro':('Doar RO','RO only'),
't40.l5.ajutor.supliment':('Supliment','Supplement'),'t40.l5.ajutor.doar_ro_partial':('Parțial RO','Partly RO'),
'manual.title':('Titlu manual','Manual title')}
def makejar(name,resources,raw=None):
 p=L/(name+'.jar')
 if raw is not None:p.write_bytes(raw);return p
 with zipfile.ZipFile(p,'w') as z:
  z.writestr(m.ETI,'\n'.join('\t'.join((k,*v)) for k,v in eti.items()))
  for k,v in resources:z.writestr(m.RES+k,v)
 return p
def resources(name,rs,fn):
 z=m.Resurse(makejar(name,rs))
 try:return fn(z)
 finally:z.z.close()
tsv='# cheie\tro\ten\n# stare validat\nrol\tRol românesc\tEnglish role\ncamp.1.nume\tNume\tName\nbuton.1.nume\tSalvez\tSave\ngreseala.1\tNu\tNo\n'
case('I17_TEXT_ro',lambda:resources('textro',[('help/WOne.tsv',tsv)],lambda z:m.asteptat(z,{},'WOne','ro_RO','EvA — One')),'TEXTE, Romanian role, one field, no image, VALIDAT')
case('I17_TEXT_en',lambda:resources('texten',[('help/WOne.tsv',tsv)],lambda z:m.asteptat(z,{},'WOne','en_US','EvA — One')),'TEXTE, English role and same source field number')
case('I17_fallback',lambda:resources('fallback',[('help/WOne.tsv','# cheie\ten\tro\nrol\tOnly EN\t\n')],lambda z:z.texte('WOne','ro_RO')),'declared fallback uses EN when requested RO empty; not proof of accepted translation')
case('I17_field_aliases',lambda:resources('aliases',[('help/WOne.tsv','camp.1.nume\tA\tA\ncamp.01.nume\tB\tB\n')],lambda z:m.asteptat(z,{},'WOne','ro_RO','One')),'observe two textual keys resolving to same integer field number; no distinct-field credit')
case('I17_duplicate_key',lambda:resources('duplicatekey',[('help/WOne.tsv','rol\tFirst\tFirst\nrol\tLast\tLast\n')],lambda z:z.texte('WOne','ro_RO')),'duplicate key handling explicit; expected parser currently last-wins')
fakepng=b'XPNG'+b'\0'*12+struct.pack('>II',400,300)
case('I17_fake_png_header',lambda:resources('fakepng',[('img/WOne/WOne.png',fakepng)],lambda z:m.asteptat(z,{},'WOne','ro_RO','One')),'invalid PNG signature must not be mistaken for full image validity; compare parser-only expectation to independently invalid signature')
case('I17_short_png',lambda:resources('shortpng',[('img/WOne/WOne.png',b'PNG')],lambda z:z.png('WOne')),'None')
case('I17_zone_bad_number',lambda:resources('zonebad',[('img/WOne/zone.json','[{"n":"X"}]')],lambda z:z.zone('WOne')),'controlled data invalidity versus ValueError; no pass on exception')
case('I17_zone_duplicates',lambda:resources('zonedup',[('img/WOne/zone.json','[{"n":2},{"n":1},{"n":1}]')],lambda z:z.zone('WOne')),'sorted values retain duplicates; not a count of distinct zones')
case('I17_corrupt_jar',lambda:m.Resurse(makejar('badjar',[],raw=b'not a ZIP')),'BadZipFile, incomplete input')
case('I17_MANUAL_en',lambda:resources('manual',[],lambda z:m.asteptat(z,{'WOne':('eti','manual.title')},'WOne','en_US','One')),'Manual heading remains RO by contract and English RO-only note is present')
case('I17_SUPPLEMENT_en',lambda:resources('sup',[('help/supliment/WOne.tsv','pas.1\tPas\tStep\n')],lambda z:m.asteptat(z,{'WOne':('lit','Manual')},'WOne','en_US','One')),'MANUAL+SUPLIMENT, partial-RO note')
case('I17_REGES',lambda:resources('reges',[],lambda z:m.asteptat(z,{},m.REGES,'en_US','REGES')),'REGES uses its own prefix contract; no native form execution')
def chapters(s):p=L/'Manual.java';p.write_text(s,encoding='utf-8');return m.capitole(p)
case('I17_manual_literal',lambda:chapters('cap("id", "Heading", "WOne");'),'WOne literal Heading')
case('I17_manual_comment',lambda:chapters('// cap("id", "Comment", "WOne");\ncap("id2", "Actual", "WOne");'),'regex sees text in comment; expected resource inference must be reconciled with Java runtime, not accepted semantically')
case('I17_manual_duplicate',lambda:chapters('cap("id", "First", "WOne");\ncap("id2", "Second", "WOne");'),'first retained; duplicate violates known native one-chapter invariant, diagnostic limitation only')
case('I17_manual_expression',lambda:chapters('cap("id", prefix+"Heading", "WOne");'),'unsupported expression omitted, no native absence conclusion')
jar=makejar('premise',[]);digest=hashlib.md5(jar.read_bytes()).hexdigest()
def premise(net='true',checksum=digest,rc=0):
 p=m.Proba.__new__(m.Proba);p.a=types.SimpleNamespace(jar=str(jar));p.st={'NET':'SYNTHETIC','ID':'SYNTHETIC'}
 calls=[]
 def sh(args):
  calls.append(args);return types.SimpleNamespace(stdout=net if args[1]=='network' else checksum+'  synthetic.jar',returncode=0 if args[1]=='network' else rc)
 p.CE=types.SimpleNamespace(sh=sh)
 try:return {'return':p.premise(),'calls':calls}
 except SystemExit as e:return {'SystemExit_code':e.code,'effective_cli_code':1 if isinstance(e.code,str) else e.code,'calls':calls}
case('I17_premise_match',lambda:premise(),'network true and supplied binary md5 equal; only synthetic dependency binding')
case('I17_premise_external_net',lambda:premise('false'),'refusal before second call; docstring promises rc2, observe SystemExit string effective1')
case('I17_premise_hash_mismatch',lambda:premise(checksum='0'*32),'refuse mismatched binary; no browser')
case('I17_premise_docker_error',lambda:premise(rc=125),'failed inspect/exec not accepted from success-looking stdout')
put(L/'Results.json',results);put(L/'Canaries.json',can);put(L/'Boundaries.json',{'source_sha256':hashlib.sha256(S.read_bytes()).hexdigest(),'source_imported_original':True,'constructor_called':False,'database_or_browser_called':False,'CE_in_premise':'explicit stub only','cases':len(results),'guard':'cooperative Python audit hook, not OS sandbox'})
print(json.dumps({'cases':len(results),'canaries':can},ensure_ascii=False))
