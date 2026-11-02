from pathlib import Path
import gzip,json
B=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01');D=Path('D:/CodexWork/A12_evidence_20261102/blobs');data=json.loads((B/'executie/R10_pregatire/A12/Cai_nominale_873_fara_dublare.json').read_text('utf8'));spec={x['task']:x for x in data['records']}
for t in ['T35.11','T35.10','T22.15','T04.12']:
 x=spec[t];l=x['source_locator'];raw=gzip.decompress((D/(l['blob_or_file_sha']+'.gz')).read_bytes());print('===== '+t)
 if t=='T22.15':
  cur=json.loads(raw)['ramase'][5];print(cur['copii'][0]); print({k:v for k,v in cur.items()if k not in ['copii','descriere']});continue
 for i,S in enumerate(raw.decode().splitlines(),1):
  if (t=='T35.11' and (i<35 or 'OK' in S or 'FAIL'in S)or t=='T35.10'and(i<17 or 58<=i<=71 or 'AD_Note' in S or 'CalendarFiscal' in S)or t=='T04.12'and(68<=i<=75 or 'L9' in S)):
   print(i,S[:360])
