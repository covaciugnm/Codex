from pathlib import Path
import json, shutil, hashlib

helper=Path(__file__).with_name('2026.10.13 Publicare baza negociere.py')
src=helper.read_text(encoding='utf-8')
prefix=src.split('assert_frozen()\nmatrix_file=')[0]
body=src[src.index("d=doc('Poziții comune de negociere"):src.index("\nmanifest={'data':DATE")]
namespace={}
exec(compile(prefix,str(helper),'exec'),namespace)
ROOT,WORK,OUT,DATE=[namespace[x] for x in ['ROOT','WORK','OUT','DATE']]
objections_file=WORK/f'{DATE} Obiectii negociere reformulate.json'
objections=json.loads(objections_file.read_text(encoding='utf-8-sig'))
assert len(objections['mapare_30'])==30
assert len(objections['puncte_negociere'])==16
namespace['assert_frozen']()
OUT.mkdir(exist_ok=True)
dest=OUT/objections_file.name
assert not dest.exists();shutil.copy2(objections_file,dest)
namespace['objections']=objections
namespace['objections_file']=objections_file
exec(compile(body,str(helper),'exec'),namespace)
p=namespace['objections_doc']
manifest={'data':DATE,'documente':[{'prestator':'Obiecții negociere','docx':p.relative_to(ROOT).as_posix()}],
 'sursa_json_sha256':hashlib.sha256(objections_file.read_bytes()).hexdigest(),
 'docx_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
out=OUT/f'{DATE} Export obiectii negociere pentru verificare.json'
assert not out.exists();out.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
namespace['assert_frozen']()
print(json.dumps(manifest,ensure_ascii=False))
