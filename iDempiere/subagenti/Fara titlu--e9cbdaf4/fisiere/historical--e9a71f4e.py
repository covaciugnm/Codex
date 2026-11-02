import io,subprocess,pathlib,json,hashlib,re,sys
O=pathlib.Path(__file__).parent;E=O.parent;f=E/'R4/T259_ZK/test_original_versionat.json';items=json.loads(f.read_text(encoding='utf-8-sig'));oids=[x['git_oid'] for x in items];assert len(oids)==5 and all(re.fullmatch('[0-9a-f]{40}',i) for i in oids)
c=subprocess.run(['ssh','-o','BatchMode=yes','-o','ConnectTimeout=6','-o','StrictHostKeyChecking=yes','saga-server@192.168.100.151','git -C /home/saga-server/Documents/EvA-Contab cat-file --batch'],input=('\n'.join(oids)+'\n').encode(),capture_output=True,timeout=40);assert c.returncode==0,c.stderr[:120]
stream=io.BytesIO(c.stdout);rows=[]
for x in items:
 head=stream.readline().split();assert head[0].decode()==x['git_oid'] and head[1]==b'blob';raw=stream.read(int(head[2]));assert stream.read(1)==b'\n' and hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==x['git_oid'] and hashlib.sha256(raw).hexdigest()==x['file_sha256']
 data=raw.decode('utf-8-sig',errors='replace').splitlines();comp=[]
 for pos,fragment in x['selected_evidence']:
  if not isinstance(pos,int):continue
  line=data[pos-1]; comp.append({'line':pos,'exact':line==fragment,'fragment_or_normalized':str(fragment).strip() in line or line.strip() in str(fragment)})
 rows.append({'source':x['path'],'git_oid':x['git_oid'],'sha256':x['file_sha256'],'rows':len(data),'excerpts_examined':len(comp),'exact_matches':sum(v['exact'] for v in comp),'frag_matches':sum(v['fragment_or_normalized']for v in comp),'has_0_1_0':any('0→1→0' in s.replace(' ','') or '0->1->0' in s.replace(' ','') for s in data),'matching_signal_lines':[(i, re.sub(r'\b(?:[0-9a-f]{16,}|\S+@\S+\.\S+)\b','[redactat]',s.strip())[:120]) for i,s in enumerate(data,1) if re.search(r'3/3|0\s*[-→]+\s*1\s*[-→]+\s*0|C3.*VERDE|T259-PROBA',s,re.I)][:5],'scope':'Historical versioned proof only; selected fields assessed independently.'})
(O/'T259_historic_blob_readback.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8');print([(x['rows'],x['excerpts_examined'],x['exact_matches'])for x in rows])

