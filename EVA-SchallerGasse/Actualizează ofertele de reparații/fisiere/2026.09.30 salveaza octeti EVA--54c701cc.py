from pathlib import Path
import json,base64,hashlib,re
ROOT=Path(__file__).resolve().parent.parent
base=ROOT/'08. Corespondenta'/'BAU-WERTE'
reg=base/'2026.09.30 Registru atasamente.json'
rows=json.loads(reg.read_text(encoding='utf-8'))
raw=json.loads((ROOT/'folder map'/'2026.09.30 EVA octeti temporari.json').read_text(encoding='utf-8'))
byid={r['id']:r for r in rows}
for f in raw:
    out=[];pos=0
    for c in f['parts']:
        b=base64.b64decode(c['base64']);assert c['offset']==pos and len(b)==c['bytes'];assert hashlib.sha256(b).hexdigest()==c['chunk_sha256'];out.append(b);pos+=len(b)
    b=b''.join(out);assert len(b)==f['size'];digest=hashlib.sha256(b).hexdigest()
    if f.get('sha256'):assert digest==f['sha256']
    r=byid[f['id']];name=re.sub(r'[<>:"/\\|?*]','_',r['name']);p=Path(name)
    stem=(r['date'][:10].replace('-','.')+' '+r['id'][:8]+' '+p.stem)[:85]
    path=base/'Atasamente'/(stem+p.suffix);path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(b)
    r.update(cale=path.relative_to(ROOT).as_posix(),sha256=digest,stare='salvat original integral')
    r.pop('eroare',None)
reg.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'total':len(rows),'salvate':sum(x['stare']=='salvat original integral' for x in rows),'ramase':[x['id'] for x in rows if x['stare']!='salvat original integral']}))
