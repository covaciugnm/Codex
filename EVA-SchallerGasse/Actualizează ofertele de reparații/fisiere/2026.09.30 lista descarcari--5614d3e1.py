from pathlib import Path
import json,sys,re
R=Path(__file__).resolve().parent.parent
B=R/'08. Corespondenta'/'2026.09.30 Arhiva Eva-Mail'
emails={}
for p in sorted((B/'Surse').glob('*.json')):
 for e in json.loads(p.read_text(encoding='utf-8')):emails[e['id']]=e
p=R/'08. Corespondenta'/'BAU-WERTE'/'2026.09.30 Eva-Mail - export integral.json'
for e in json.loads(p.read_text(encoding='utf-8'))['emailuri']:emails[e['id']]=e
done=set()
for p in [B/'2026.09.30 Registru atasamente.json',R/'08. Corespondenta'/'BAU-WERTE'/'2026.09.30 Registru atasamente.json']:
 if p.exists():
  for a in json.loads(p.read_text(encoding='utf-8')):
   if a.get('stare')=='salvat original integral' and a.get('cale') and (R/a['cale']).exists():done.add(a['id'])
ats={a['id']:a for e in emails.values() for a in e.get('attachments',[])}
todo=[{'id':a['id'],'name':a.get('name'),'size':a.get('size')} for a in ats.values() if a['id'] not in done]
inline={a['id'] for a in ats.values() if re.fullmatch(r'(image\d+\.(jpg|png|jpeg|gif)|inline|smime\.p7s)',a.get('name',''),re.I) and (a.get('size') or 0)<40000 and (a.get('text_chars') or 0)<40}
remaining_inline=sum(a['id'] in inline for a in todo)
todo=[a for a in todo if a['id'] not in inline]
priority=['e19fdb9c-d484-4017-90da-5b17a9b12eec','56f3a183-e446-49f0-9cd0-5bf90e842701','56a6e773-4eb9-493f-b42d-ef21bafec22d','63d6139a-c03b-49bb-ad3a-bcd3d6152190','e6abea64-190f-486b-bc7c-5496d05551e7']
todo.sort(key=lambda a:(-1 if a['id'] in priority else 0 if re.search(r'1925|1261556|1263320|1264971|honorar|offenes|bescheid|kost|konto|rechnung|34[68]4|HN |242 2026',a.get('name',''),re.I) else 1 if Path(a.get('name','')).suffix.lower() not in ['.png','.jpg','.jpeg','.gif',''] else 2,a['id']))
expected=json.loads((R/'folder map'/'2026.09.30 lista mesaje candidate.json').read_text(encoding='utf-8'))
print(json.dumps({'emails':len(emails),'expected':len(expected),'total_attachments':len(ats),'done':len(done),'remaining':len(todo),'inline_metadata_only':remaining_inline,'todo':todo[:60]},ensure_ascii=False))
