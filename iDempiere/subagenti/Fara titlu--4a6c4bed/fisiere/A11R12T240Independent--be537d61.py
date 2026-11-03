import pathlib, tempfile, shutil, subprocess, hashlib, json, datetime, sys, copy, os, zipfile, struct, zlib
sys.stdout.reconfigure(encoding='utf8')
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01')
P=R/'executie/R12_plan_delta'
O=R/'executie/R12_fisiere/A11/T240_lot01'
O.mkdir(parents=True,exist_ok=True)
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return {'path':p.relative_to(R).as_posix(),'sha256':h(p)}
assert not (O/'Control_independent_T240_v1.json').exists()
assert h(P/'A11_verdict_plan_delta_R12_v2.json')=='84e3735906d868f2153bc6b71c8f0e0e7a0211367ba4d3df5f8509d008d1f2a4'
ann=j(P/'Plan_instrumente_noi_A10_v2.json')
s=next(x['source'] for x in ann['items'] if x['audit_control_id']=='R12-I19')
src=P/'Sources_lues'/s['path'];raw=src.read_bytes()
assert h(src)==s['sha256'] and hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==s['git_object']
# Schema and values below are an independent written fixture, not an import of test_clasa_verifica_proba.py.
cols='ecran limba tip meniu deschis buton_asteptat buton_afisat buton_in_ecran panou titlu_asteptat titlu_afisat titlu_inventar h3_asteptat h3_afisat sectiuni_asteptate sectiuni_afisate rol_asteptat rol_afisat campuri_asteptate campuri_afisate img_asteptat img_afisat latime_asteptata latime_afisata zone_json zone_afisate camp_n zone_afara stare_asteptata stare_afisata nota_en_asteptata nota_en_afisata captura_ecran captura_panou motiv'.split()
per='WSagaSetariFirmaPerioadeForm'
screens=['WA11Auditor%02dForm'%n for n in range(1,13)]+[per]
def row(screen,lang):
    r=dict.fromkeys(cols,'');en=lang=='en_US';manual=screen==per
    title=('Help' if en else 'Ajutor')+' — '+screen
    r.update(ecran=screen,limba=lang,tip='MANUAL' if manual else 'TEXTE',meniu='synthetic/'+screen,deschis='DA',buton_asteptat='Help' if en else 'Ajutor',buton_afisat='Help' if en else 'Ajutor',buton_in_ecran='DA',panou='DA',titlu_asteptat=title,titlu_afisat=title,titlu_inventar=screen,h3_asteptat='Capitol sintetic' if manual else '',h3_afisat='Capitol sintetic' if manual else '',sectiuni_asteptate='≥1' if manual else 'Rol | Câmpuri',sectiuni_afisate='Pași' if manual else 'Rol | Câmpuri',rol_asteptat='Utilitate sintetică',rol_afisat='Utilitate sintetică',campuri_asteptate='1',campuri_afisate='1',img_asteptat='NU',img_afisat='NU',zone_afara='0',stare_asteptata='CIORNA',stare_afisata='CIORNA',nota_en_asteptata='Romanian only' if en and manual else '',nota_en_afisata='Romanian only' if en and manual else '',captura_ecran='captures/'+screen+'_'+lang+'_screen.png',captura_panou='captures/'+screen+'_'+lang+'_help.png')
    return r
rows=[row(x,'ro_RO') for x in screens]+[row(x,'en_US') for x in screens[:10]]+[row(per,'en_US')]
assert len(rows)==24 and len(cols)==35
def chunk(kind,data):return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',1,1,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(b'\0\xff\xff\xff'))+chunk(b'IEND',b'')
# Independent image decoder validates only the synthetic fixture; no native screenshot is claimed.
sys.path.insert(0,'D:/CodexWork/eva-a01-fixture-deps')
from PIL import Image
import io
Image.open(io.BytesIO(png)).verify()
child=r'''import sys,os,pathlib,runpy,socket
sys.stdout.reconfigure(encoding='utf8');sys.stderr.reconfigure(encoding='utf8')
root=pathlib.Path(sys.argv[1]).resolve();source=sys.argv[2];argv=sys.argv[3:];sys.dont_write_bytecode=True
def inside(p):
 try:return pathlib.Path(p).resolve().is_relative_to(root)
 except (ValueError,TypeError,OSError):return False
def guard(event,args):
 if event.startswith('socket.') or event in ('subprocess.Popen','os.system','os.posix_spawn','os.spawn','ctypes.dlopen'):raise PermissionError('A11 outbound/subprocess denied')
 if event=='open':
  mode=args[1];flags=args[2];writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))
  if writing and not inside(args[0]):raise PermissionError('A11 outside scratch write denied')
 if event in ('os.remove','os.rmdir','os.mkdir','os.rename','os.replace'):
  for p in args[:2] if event in ('os.rename','os.replace') else args[:1]:
   if not inside(p):raise PermissionError('A11 outside scratch mutation denied')
sys.addaudithook(guard)
for label,fn in [('socket',lambda:socket.socket()),('outside_write',lambda:open(root.parent/'A11_should_not_exist_sentinel.tmp','wb'))]:
 try:fn()
 except PermissionError:print('GUARD_OK '+label,file=sys.stderr)
 else:raise RuntimeError('guard did not refuse '+label)
sys.argv=[source]+argv
runpy.run_path(source,run_name='__main__')
'''
scratch=pathlib.Path(tempfile.mkdtemp(prefix='a11-r12-t240-',dir='D:/CodexWork')).resolve()
assert scratch.parent==pathlib.Path('D:/CodexWork').resolve() and scratch.name.startswith('a11-r12-t240-')
results=[];preflight={'candidate':ann['candidate'],'source':s,'source_original_bytes':True,'independent_fixture':True,'environment':{'platform':sys.platform,'python':sys.version,'scratch':str(scratch)},'fixture_png_decode':True,'gate':ref(P/'A11_verdict_plan_delta_R12_v2.json'),'population':ref(R/'executie/delta/2026-11-02T23-15-23-444Z/Delta.json'),'os_hypothesis':ref(P/'Addendum_A11_aplicabilitate_gate_T240_T343_v1.json')}
try:
    target=scratch/'verifica_proba.py';target.write_bytes(raw)
    runner=scratch/'child.py';runner.write_text(child,encoding='utf8')
    (scratch/'shared.png').write_bytes(png)
    # Name/ADS preflight: concrete local observation only, no preventative rewriting.
    ads=scratch/'NU: 2 identificatori în clar după mască'
    try:
        ads.write_bytes(b'x')
        preflight['colon_probe']={'write':'ok','read':ads.read_bytes().decode(),'isfile':ads.is_file(),'size':ads.stat().st_size,'base_NU_exists':(scratch/'NU').exists(),'listed_names':[x.name for x in scratch.iterdir()]}
        ads.unlink()
        preflight['colon_probe']['after_stream_delete_exists']=ads.exists()
        if (scratch/'NU').exists():(scratch/'NU').unlink()
    except OSError as e:preflight['colon_probe']={'write':'failed','exception':type(e).__name__,'message':str(e)}
    cases=[
      ('positive',0,'Baseline independent: 13 RO, 10 EN TEXTE, 1 Perioade EN; all internally consistent.'),
      ('display_mismatch',1,'A single displayed role differs: R6 must refuse.'),
      ('missing_ro',1,'One unique inventory screen has no RO row: must refuse.'),
      ('duplicate_report_row',1,'Duplicate same screen/language must refuse.'),
      ('unknown_language',1,'Language outside RO/EN must refuse.'),
      ('empty_capture',1,'Empty file must refuse under R10.'),
      ('missing_capture',1,'Absent file must refuse under R10.'),
      ('nonimage_capture',0,'Documented limitation witness: nonempty bytes accepted, image decoder rejects.'),
      ('traversal_capture',0,'Containment counterexample: ../shared.png inside audit scratch but outside report directory.'),
      ('absolute_capture',0,'Containment counterexample: absolute own fixture outside report directory.'),
      ('duplicate_inventory',0,'N/N can count repeated E entries, not unique screens; 14/14 for 13 unique screens.'),
      ('negative_en_min',0,'Negative threshold accepts zero EN; invalid configuration is not rejected.'),
      ('manual_arbitrary_suffix',0,'Arbitrary MANUAL-prefixed kind accepted; enum interpretation remains contract-dependent.'),
      ('forged_expected_and_display',0,'Both expected/displayed role altered consistently: helper has no independent resource provenance.'),
      ('invalid_header',2,'Malformed header must be classified unreadable.'),
    ]
    for name,expected,oracle in cases:
        d=scratch/name;d.mkdir();(d/'captures').mkdir();rs=copy.deepcopy(rows);E=list(screens);extra=[]
        for r in rs:
            for c in ['captura_ecran','captura_panou']:(d/r[c]).write_bytes(png)
        if name=='display_mismatch':rs[0]['rol_afisat']='Altă utilitate'
        if name=='missing_ro':rs.pop(0)
        if name=='duplicate_report_row':rs.append(copy.deepcopy(rs[0]))
        if name=='unknown_language':extra_row=copy.deepcopy(rs[0]);extra_row['limba']='de_DE';rs.append(extra_row)
        if name=='empty_capture':(d/rs[0]['captura_panou']).write_bytes(b'')
        if name=='missing_capture':(d/rs[0]['captura_panou']).unlink()
        if name=='nonimage_capture':(d/rs[0]['captura_panou']).write_bytes(b'not an image, synthetic A11 witness')
        if name=='traversal_capture':rs[0]['captura_panou']='../shared.png'
        if name=='absolute_capture':rs[0]['captura_panou']=str(scratch/'shared.png')
        if name=='duplicate_inventory':E.append(screens[0])
        if name=='negative_en_min':rs=[r for r in rs if r['limba']=='ro_RO'];extra=['--en-min','-1']
        if name=='manual_arbitrary_suffix':next(r for r in rs if r['ecran']==per and r['limba']=='ro_RO')['tip']='MANUAL_ARBITRAR_A11'
        if name=='forged_expected_and_display':rs[0]['rol_asteptat']=rs[0]['rol_afisat']='Text inventat de auditor, fără resursă nativă'
        header=list(cols)
        if name=='invalid_header':header[0]='wrong_header'
        (d/'raport.tsv').write_text('\t'.join(header)+'\n'+'\n'.join('\t'.join(r[c] for c in cols) for r in rs)+'\n',encoding='utf8')
        (d/'ecrane.tsv').write_text('\n'.join(x+'\t'+x for x in E)+'\n',encoding='utf8')
        args=[sys.executable,'-I','-X','utf8',str(runner),str(scratch),str(target),str(d),'--ecrane',str(d/'ecrane.tsv')]+extra
        started=datetime.datetime.now(datetime.timezone.utc).isoformat()
        completed=subprocess.run(args,cwd=scratch,capture_output=True,text=True,encoding='utf8',timeout=20,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TEMP':str(scratch),'TMP':str(scratch)})
        (d/'stdout.txt').write_text(completed.stdout,encoding='utf8');(d/'stderr.txt').write_text(completed.stderr,encoding='utf8')
        assert completed.returncode==expected,(name,completed.returncode,completed.stderr)
        assert 'GUARD_OK socket' in completed.stderr and 'GUARD_OK outside_write' in completed.stderr
        info={'id':name,'expected_rc_for_actual_component':expected,'observed_rc':completed.returncode,'oracle':oracle,'utc':started,'stdout':completed.stdout,'stderr':completed.stderr,'rows':len(rs),'inventory_entries':len(E),'inventory_unique':len(set(E)),'report_sha256':h(d/'raport.tsv'),'inventory_sha256':h(d/'ecrane.tsv')}
        if name=='nonimage_capture':
            try:Image.open(d/rs[0]['captura_panou']).verify();info['independent_decoder']='accepted'
            except Exception as e:info['independent_decoder']=type(e).__name__
            assert info['independent_decoder']=='UnidentifiedImageError'
        if name in ['traversal_capture','absolute_capture']:info['independent_containment_oracle']=(d/rs[0]['captura_panou']).resolve().is_relative_to(d.resolve());assert info['independent_containment_oracle'] is False
        if name=='duplicate_inventory':assert '14/14 conforme' in completed.stdout
        results.append(info)
    assert h(target)==s['sha256'] and h(src)==s['sha256']
    archive=O/'Fixture_si_iesiri_independente_T240_v1.zip'
    assert not archive.exists()
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(scratch.rglob('*')):
            if f.is_file():z.write(f,f.relative_to(scratch).as_posix())
    childcopy=O/'Child_independent_T240_v1.py';assert not childcopy.exists();childcopy.write_text(child,encoding='utf8')
finally:
    assert scratch.parent==pathlib.Path('D:/CodexWork').resolve() and scratch.name.startswith('a11-r12-t240-')
    shutil.rmtree(scratch)
cleanup={'scratch_absent':not scratch.exists(),'outside_sentinel_absent':not (scratch.parent/'A11_should_not_exist_sentinel.tmp').exists(),'services_created':0,'operational_writes':0}
assert cleanup['scratch_absent'] and cleanup['outside_sentinel_absent']
out={'schema':'A11.R12.T240.independent.v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'preflight':preflight,'method':'CLI original byte-exact executat în procese Python separate; fixture și oracol proprii; nu importă test_clasa_verifica_proba.py. Hook cooperativ, nu sandbox OS. Nicio rețea/DB/browser.','cases':results,'counts':{'cases':len(results),'observed_as_predicted':sum(x['expected_rc_for_actual_component']==x['observed_rc'] for x in results),'product_full_pass_claim':False},'limits':['Fixture folosește 12 nume de ecrane inventate și Perioade; nu dovedește E nativ instalat.','Imaginile sunt PNG 1x1 sintetice, fără capturi UI native.','Limitele de proveniență/imagini și enum configurabil nu devin automat defecte de produs: se clasifică după contract.','Niciun proces iDempiere și niciun efect contabil executat.'],'cleanup':cleanup,'artifacts':[ref(archive),ref(childcopy)],'method_source':{'path':str(pathlib.Path(__file__)),'sha256':h(pathlib.Path(__file__))}}
dest=O/'Control_independent_T240_v1.json';dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'output':ref(dest),'cases':len(results),'cleanup':cleanup,'colon_preflight':preflight['colon_probe']},ensure_ascii=False))
