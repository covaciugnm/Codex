import pathlib,json,hashlib,zipfile,io,ast,warnings,datetime,struct
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere'); B=R/'A10_Instrumente_ramase_lot03';O=R/'A11/Val03_loturi'
def sha(b):return hashlib.sha256(b).hexdigest()
s=(B/'sources/verifica_integrare_L1.sh').read_bytes();assert sha(s)=='2bc0c75667a31b8b90efbcaa4f8a563d01f13f70c6f85462c618a2474ed98a0f'
src=s.decode().split("<<'PY'\n",1)[1].split('\nPY\n',1)[0]
node=next(n for n in ast.parse(src).body if isinstance(n,ast.FunctionDef) and n.name=='m')
frag=ast.get_source_segment(src,node);env={'zipfile':zipfile};exec(compile(ast.Module(body=[node],type_ignores=[]),'<exact original m from I01>','exec'),env)
def jar(entries):
 f=io.BytesIO()
 with warnings.catch_warnings():
  warnings.simplefilter('ignore',UserWarning)
  with zipfile.ZipFile(f,'w',compression=zipfile.ZIP_STORED) as z:
   for n,b in entries:z.writestr(n,b)
 return f.getvalue()
base=jar([('Peer.class',b'base-peer')]);good=jar([('Peer.class',b'altered-peer'),('Peer.class',b'base-peer')]);reverse=jar([('Peer.class',b'base-peer'),('Peer.class',b'altered-peer')])
corrupt=bytearray(base);name_len,extra_len=struct.unpack_from('<HH',corrupt,26);corrupt[30+name_len+extra_len]^=1
cases=[]
for name,b in [('baseline',base),('duplicate_last_base',good),('duplicate_last_variant',reverse),('corrupt_payload_same_directory_crc',bytes(corrupt))]:
 got=env['m'](io.BytesIO(b)); rows=[]
 with zipfile.ZipFile(io.BytesIO(b)) as z:
  for i in z.infolist():
   try:payload=z.read(i);rows.append({'name':i.filename,'payload_sha256':sha(payload),'read_error':None})
   except zipfile.BadZipFile as e:rows.append({'name':i.filename,'payload_sha256':None,'read_error':type(e).__name__+': '+str(e)})
 cases.append({'id':'A11_CRC_'+name,'input_sha256':sha(b),'input_bytes_hex':b.hex(),'original_m_result':got,'equals_baseline_map':got==env['m'](io.BytesIO(base)),'oracle_preserves_all_members':rows})
assert [x['equals_baseline_map'] for x in cases]==[True,True,False,True]
assert cases[-1]['oracle_preserves_all_members'][0]['read_error']
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'A11','head':'df85d33c1648ce2b2df130a60a05ef696e2e5480','method':'Funcția m exactă din here-documentul original I01, extrasă AST fără executarea scriptului Bash ori a restului modulului. Patru arhive independente exclusiv BytesIO; oracolul citește fiecare ZipInfo și conservă duplicatele.','source_sha256':sha(s),'fragment':frag,'fragment_sha256':sha(frag.encode()),'cases':cases,'limit':'Defect/limită a comparatorului de identitate JAR; nu demonstrează ce membru încarcă JVM/OSGi. Nu se execută bytecode, shell ori Git și nu se scrie nicio fixtură pe disc.','cleanup':'Toate obiectele BytesIO/ZipFile închise; nicio resursă creată în afara acestui raport.'}
p=O/'Proba_A11_CRC_I01_lot03_v1.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps({'path':str(p),'sha256':sha(p.read_bytes()),'cases':4}))
