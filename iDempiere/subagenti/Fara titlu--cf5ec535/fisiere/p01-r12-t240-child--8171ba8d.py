"""Harness A08. Se pornește exclusiv după poarta independentă transmisă de coordonator."""
from pathlib import Path
import sys,os,json,time,tempfile,runpy,importlib.util,traceback,hashlib,struct,zlib,copy,socket,subprocess,tracemalloc
ROOT=Path(sys.argv[1]).resolve()
MODE=sys.argv[2]
SOURCE=ROOT/'source'
OUT=ROOT/('result_'+MODE+'.json')
TMP=ROOT/'tmp';TMP.mkdir(exist_ok=True)
tempfile.tempdir=str(TMP)
sys.dont_write_bytecode=True
blocked=[]
def inside(p):
 try:return Path(p).resolve().is_relative_to(ROOT)
 except (TypeError,ValueError):return False
def audit(event,args):
 if event.startswith('socket.') or event.startswith('subprocess.') or event in ('os.system','os.exec','os.posix_spawn','ctypes.dlopen'):
  blocked.append({'event':event});raise PermissionError('audit harness: operation denied '+event)
 if event=='open':
  p,mode,flags=args
  writing=isinstance(mode,str) and any(c in mode for c in 'wax+') or isinstance(flags,int) and flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)
  if writing and not isinstance(p,int) and not inside(p):raise PermissionError('write outside owned scratch')
 if event in ('os.remove','os.rmdir','os.mkdir','shutil.rmtree') and not inside(args[0]):raise PermissionError('mutation outside owned scratch')
 if event in ('os.rename','os.replace') and not all(inside(x) for x in args[:2]):raise PermissionError('rename outside owned scratch')
sys.addaudithook(audit)
for target in ('socket','subprocess','external_write'):
 try:
  if target=='socket':socket.socket()
  elif target=='subprocess':subprocess.run([sys.executable,'-c','pass'])
  else:open(ROOT.parent/('forbidden_'+ROOT.name),'w')
 except PermissionError:pass
 else:raise RuntimeError('Guard failed: '+target)
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def write_result(d):
 d['blocked_operations']=blocked;d['scope']='Componentă Python pe fișiere sintetice; fără UI/DB/native/runtime iDempiere.'
 OUT.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')

if MODE in ('original','original_full'):
 sys.argv=[str(SOURCE/'test_clasa_verifica_proba.py')]+(['--fara-mutanti'] if MODE=='original' else [])
 runpy.run_path(sys.argv[0],run_name='__main__')
elif MODE=='selected':
 m=load('original_suite',SOURCE/'test_clasa_verifica_proba.py')
 results=[];skips=[]
 for i,(n,tr,rc,fragment) in enumerate(m.CAZURI):
  actual=m.ruleaza_caz(m.V,str(TMP/('c%02d'%i)),n,tr,rc,fragment)
  results.append({'name':n,'passed':actual[0],'expected_rc':rc,'actual_rc':actual[1],'expected_fragment':fragment,'last_line':actual[2],'origin':'CAZURI','index':i})
 for i,(n,extra,rc,fragment,tr) in enumerate(m.CAZURI_FIS):
  if extra.__name__=='caz_fisier_nu':
   skips.append({'name':n,'origin':'CAZURI_FIS','index':i,'status':'NEEXECUTAT_WINDOWS','reason':'Nume de fișier NU: ... incompatibil Windows; sursa originală nu este schimbată.'});continue
  actual=m.ruleaza_caz(m.V,str(TMP/('f%02d'%i)),n,tr or (lambda rows:rows),rc,fragment,extra)
  results.append({'name':n,'passed':actual[0],'expected_rc':rc,'actual_rc':actual[1],'expected_fragment':fragment,'last_line':actual[2],'origin':'CAZURI_FIS','index':i})
 actual=m.ruleaza_caz(m.V,str(TMP/'p00'),'Perioade în afara E',lambda rs:[r for r in rs if r['ecran']!=m.PER],1,'în E: NU')
 results.append({'name':'Perioade în afara E','passed':actual[0],'expected_rc':1,'actual_rc':actual[1],'last_line':actual[2],'origin':'suita final case'})
 write_result({'mode':MODE,'source_unchanged':True,'cases':results,'skipped':skips,'source_cases':len(m.CAZURI)+len(m.CAZURI_FIS)+1,'mutants_declared':len(m.MUTANTI),'mutants_executed':0,'whole_original_suite_pass':False,'native_evidence':False})
elif MODE=='independent':
 tracemalloc.start()
 v=load('original_judge',SOURCE/'verifica_proba.py')
 COLS=['ecran','limba','tip','meniu','deschis','buton_asteptat','buton_afisat','buton_in_ecran','panou','titlu_asteptat','titlu_afisat','titlu_inventar','h3_asteptat','h3_afisat','sectiuni_asteptate','sectiuni_afisate','rol_asteptat','rol_afisat','campuri_asteptate','campuri_afisate','img_asteptat','img_afisat','latime_asteptata','latime_afisata','zone_json','zone_afisate','camp_n','zone_afara','stare_asteptata','stare_afisata','nota_en_asteptata','nota_en_afisata','captura_ecran','captura_panou','motiv']
 TEXT=['WCursuriForm','WFacturiForm','WSalarizareForm','WSagaGrupeArticoleForm','WEvaPontajTipZiForm','WSagaClientiForm','WSagaJurnalValutaForm','WSagaBilantForm','WEvaAccesMobilForm','WSagaIesiriForm']
 PER='WSagaSetariFirmaPerioadeForm';REG='WEvaRegesAplicatieForm';MAN='WSagaIntrariForm';E=TEXT+[PER,REG,MAN]
 def chunk(name,data):return struct.pack('>I',len(data))+name+data+struct.pack('>I',zlib.crc32(name+data)&0xffffffff)
 PNG=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',1,1,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(b'\x00\xff\xff\xff'))+chunk(b'IEND',b'')
 def image_oracle(b):
  if not b.startswith(b'\x89PNG\r\n\x1a\n'):return False
  try:
   pos=8;idata=b'';seen=[]
   while pos<len(b):
    size=struct.unpack('>I',b[pos:pos+4])[0];typ=b[pos+4:pos+8];dat=b[pos+8:pos+8+size];crc=struct.unpack('>I',b[pos+8+size:pos+12+size])[0]
    if (zlib.crc32(typ+dat)&0xffffffff)!=crc:return False
    seen.append(typ)
    if typ==b'IDAT':idata+=dat
    pos+=12+size
   return seen[0]==b'IHDR' and seen[-1]==b'IEND' and zlib.decompress(idata)==b'\x00\xff\xff\xff'
  except Exception:return False
 def row(screen,lang='ro_RO',kind='TEXTE'):
  name='Ecran sintetic '+screen;label='Ajutor' if lang=='ro_RO' else 'Help'
  r=dict.fromkeys(COLS,'');r.update(ecran=screen,limba=lang,tip=kind,meniu=name,deschis='DA',buton_asteptat=label,buton_afisat=label,buton_in_ecran='DA',panou='DA',titlu_asteptat=label+' — '+name,titlu_afisat=label+' — '+name,titlu_inventar=name,sectiuni_asteptate='Câmpuri | Butoane',sectiuni_afisate='Câmpuri | Butoane',rol_asteptat='Rol de referință '+lang,rol_afisat='Rol de referință '+lang,campuri_asteptate='2',campuri_afisate='2',img_asteptat='DA',img_afisat='DA',latime_asteptata='1',latime_afisata='1',zone_json='1,2',zone_afisate='1,2',camp_n='1,2',zone_afara='0',stare_asteptata='CIORNA',stare_afisata='CIORNA',captura_ecran='ecran.png',captura_panou='panou.png')
  if kind!='TEXTE':r.update(h3_asteptat='Capitol '+screen,h3_afisat='Capitol '+screen,sectiuni_asteptate='≥1',sectiuni_afisate='Pași',rol_asteptat='',rol_afisat='',campuri_asteptate='',campuri_afisate='',img_asteptat='NU',img_afisat='NU',latime_asteptata='',latime_afisata='',zone_json='',zone_afisate='',camp_n='',zone_afara='',stare_asteptata='',stare_afisata='')
  if kind=='REGES':r.update(titlu_asteptat='prefix:Ajutor — ',titlu_afisat='Ajutor — Acasă',h3_asteptat='',h3_afisat='Prezentare')
  if screen==PER and lang=='en_US':r.update(nota_en_asteptata='This help is available in Romanian only.',nota_en_afisata='This help is available in Romanian only.')
  return r
 def base_rows():return [row(e) for e in TEXT]+[row(PER,kind='MANUAL'),row(REG,kind='REGES'),row(MAN,kind='MANUAL+SUPLIMENT')]+[row(e,'en_US') for e in TEXT]+[row(PER,'en_US','MANUAL')]
 def folder(name,rows,bad_image=False):
  d=TMP/name;d.mkdir();(d/'ecran.png').write_bytes(b'x' if bad_image else PNG);(d/'panou.png').write_bytes(b'x' if bad_image else PNG)
  (d/'raport.tsv').write_text('\t'.join(COLS)+'\n'+'\n'.join('\t'.join(r[c] for c in COLS) for r in rows)+'\n',encoding='utf-8');return d
 cases=[]
 def case(name,rows,expected_rc,ecr=None,enmin=10,alter=None,classification='control',extra_oracle=None,bad_image=False):
  d=folder(name,rows,bad_image)
  if alter:alter(d)
  before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in d.iterdir() if p.is_file()};t=time.perf_counter()
  try:rc,out=v.judeca(str(d),E if ecr is None else ecr,enmin);exc=None
  except Exception as er:rc=None;out=[];exc=type(er).__name__+': '+str(er)
  elapsed=time.perf_counter()-t;after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in d.iterdir() if p.is_file()}
  (ROOT/(name+'_report.tsv')).write_bytes((d/'raport.tsv').read_bytes())
  item={'case_id':name,'expected_rc':expected_rc,'actual_rc':rc,'exception':exc,'output':out,'expected_observed_equal':rc==expected_rc,'elapsed_seconds':elapsed,'classification':classification,'rows':len(rows),'E_length':len(E if ecr is None else ecr),'E_unique':len(set(E if ecr is None else ecr)),'en_min':enmin,'files_before':before,'files_after':after,'source_inputs_unchanged':before==after,'independent_image_oracle':all(image_oracle((d/n).read_bytes()) for n in ('ecran.png','panou.png')),'additional_oracle':extra_oracle,'persistent_effect':'Judecătorul citește; nicio modificare input și nicio operație DB/native. Harness-ul păstrează raportul sintetic și verdictul.'}
  cases.append(item)
  return item
 b=base_rows()
 case('I01_conform',copy.deepcopy(b),0)
 case('I02_lipsa_ro',copy.deepcopy(b[1:]),1)
 case('I03_duplicat_rand',copy.deepcopy(b+[b[0]]),1)
 bad=copy.deepcopy(b);bad[0]['deschis']='NU';case('I04_ecran_nedeschis',bad,1)
 bad=copy.deepcopy(b);bad[0]['titlu_afisat']='Alt titlu';case('I05_titlu_diferit',bad,1)
 bad=copy.deepcopy(b);bad[0]['zone_afara']='1';case('I06_zona_afara',bad,1)
 case('I07_antet_ilizibil',copy.deepcopy(b),2,alter=lambda d:(d/'raport.tsv').write_text('ANTET\n',encoding='utf-8'))
 case('I08_E_gol',copy.deepcopy(b),1,ecr=[])
 case('I09_E_duplicat',copy.deepcopy(b),1,ecr=E+[E[0]],classification='validation_boundary',extra_oracle='Inventarul trebuie să numere ecrane distincte; duplicatul nu este ecran nou. Se consemnează acceptarea dacă survine, fără verdict de UI.')
 case('I10_enmin_negativ',copy.deepcopy([r for r in b if r['limba']=='ro_RO']),1,enmin=-1,classification='configuration_boundary',extra_oracle='Pragul negativ nu dovedește minimum10 ecrane EN; apelantul trebuie să valideze configurația.')
 bad=copy.deepcopy(b);bad[len(TEXT)]['tip']='MANUAL_NEDEFINIT';case('I11_tip_manual_arbitrar',bad,1,classification='schema_boundary',extra_oracle='Tipul nu este unul dintre tipurile fixturei declarate; startswith MANUAL poate accepta extensii necontractate. Nu se numește defect nativ fără schema autoritativă.')
 case('I12_capturi_false',copy.deepcopy(b),0,bad_image=True,classification='documented_oracle_limit',extra_oracle='R10 cere numai existență/mărime; oracolul extern decodează imaginea și o respinge. rc0 nu dovedește captură nativă.')
 bad=copy.deepcopy(b);bad[0]['rol_asteptat']=bad[0]['rol_afisat']='Rol falsificat identic'
 case('I13_asteptat_observat_falsificate',bad,0,classification='documented_trust_boundary',extra_oracle={'external_expected_role':'Rol de referință ro_RO','reported_both':'Rol falsificat identic','external_conformity':False,'meaning':'Proveniența și cerința trebuie verificate independent de TSV; judecătorul intern nu poate certifica cele două valori falsificate.'})
 case('I14_UTF8_invalid',copy.deepcopy(b),2,alter=lambda d:(d/'raport.tsv').write_bytes(b'\xff\xfe\x80'),classification='input_error_boundary')
 for n in (1000,10000):
  rows=base_rows();e=list(E)
  for i in range(n-len(rows)):
   name='WVolume%05dForm'%i;rows.append(row(name));e.append(name)
  case('I15_volum_'+str(n),rows,0,ecr=e,classification='performance_parser_only',extra_oracle='PNG sintetic comun reutilizat; măsoară parserul și verificarea fișierelor, nu UI sau capturi autentice.')
  dup=copy.deepcopy(rows);dup.insert(0,dict(dup[-1]));case('I16_duplicat_la_inceput_'+str(n),dup,1,ecr=e,classification='performance_negative')
  dup=copy.deepcopy(rows);dup.append(dict(dup[0]));case('I17_duplicat_la_final_'+str(n),dup,1,ecr=e,classification='performance_negative')
 memory_current,memory_peak=tracemalloc.get_traced_memory()
 write_result({'mode':MODE,'fixture_origin':'Construit independent, fără funcțiile rand_texte/raport_complet din suita candidat. Schema celor35 coloane transcrisă din contractul documentat.','fixture_count':{'RO':13,'EN_TEXTE':10,'EN_PERIOADE':1,'total':24},'cases':cases,'native_evidence':False,'PNG_independent_crc_and_deflate_verified':image_oracle(PNG),'mutants_executed':0,'memory_tracemalloc_peak_bytes':memory_peak,'memory_limit_note':'Peak Python tracked allocations; nu RSS sau limită OS.'})
else:raise RuntimeError('mode unknown')
