from pathlib import Path
import json,re,subprocess,hashlib,io,gzip,collections
D=Path(r'D:\CodexWork\A12_evidence_20261102');B=Path(r'Z:\00.Roboti\EVA.Pro\Eva-contab\Audit_P01_2026-11-01');M=json.loads((D/'map.json').read_text(encoding='utf8')); ix=json.loads((B/'A12_index_taskuri.json').read_text(encoding='utf8'))['rows'];ids={x['source_id'] for x in ix if x['individual_review']};extra={};tg=collections.defaultdict(list)
for z in (D/'tree.raw').read_bytes().split(b'\0'):
 if not z:continue
 hd,n=z.split(b'\t',1);path=n.decode();li=path.split('/')
 if len(li)!=4 or not li[-1].lower().endswith('.md') or int(hd.split()[3])>750000: continue
 m=re.match(r'(T\d+(?:\.\d+)?)[-_]',li[-2],re.I);k=m[1].upper() if m else None
 if not k or k not in ids:continue
 name=li[-1].lower()
 if any(p in name for p in ['brief_','audit','auditor','implementare','decizii','model','viza_','predare']):continue
 if not re.search(r'(?:^|_)(?:plan(?:_manager)?(?:_r\d+|_v\d+)?|spec(?:ificatie)?|cerinte(?:le)?|cerinta_proprietar|criterii|brief_proprietar)(?:[_.]|$)',name,re.I): continue
 extra[path]=hd.split()[2].decode();tg[k].append(path)
pend=sorted(o for o in set(extra.values()) if not (D/'blobs'/(o+'.gz')).exists())
if pend:
 rr=subprocess.run(['ssh','-C','-o','BatchMode=yes','saga-server@192.168.100.151','cd /home/saga-server/Documents/EvA-Contab && git cat-file --batch'],input=('\n'.join(pend)+'\n').encode(),capture_output=True,check=True);f=io.BytesIO(rr.stdout)
 for o in pend:
  hdr=f.readline().split();bb=f.read(int(hdr[2]));assert f.read(1)==b'\n' and hashlib.sha1(b'blob '+str(len(bb)).encode()+b'\0'+bb).hexdigest()==o;(D/'blobs'/(o+'.gz')).write_bytes(gzip.compress(bb))
M['target_paths'].update(extra);(D/'map.json').write_text(json.dumps(M,ensure_ascii=False),encoding='utf8');(D/'map_r2_plans.json').write_text(json.dumps(tg,ensure_ascii=False),encoding='utf8');print(len(extra),len(pend),len(tg))

