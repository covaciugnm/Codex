exec(open(__file__.replace('details','probe'),encoding='utf8').read().split("for t in ['T35.11'")[0])
for t in ['T35.10','T35.11']:
 l=spec[t]['source_locator'];s=gzip.decompress((D/(l['blob_or_file_sha']+'.gz')).read_bytes()).decode().splitlines();print('===',t)
 for i,a in enumerate(s,1):
  if t=='T35.10' and(i<=17 or i in [30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,65,66]) or t=='T35.11' and (i>100 and any(a1 in a for a1 in ['VERDICT','INTEGRA','INTEGR','B-L1a-1','10/10','merge'])):print(i,a[:355])
f=B/'executie/R9_pregatire/A12/Relectura_882_addendum_aliasuri.json';d=json.loads(f.read_text('utf8'));print(d.keys());print(str(d)[:1100]);
