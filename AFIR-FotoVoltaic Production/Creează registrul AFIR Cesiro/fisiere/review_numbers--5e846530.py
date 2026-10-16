import pathlib,json,re
W=pathlib.Path(__file__).parent
L=json.loads((W/'local.json').read_text(encoding='utf-8'))
seen=set()
for r in L:
 if r.get('hash') in seen:continue
 seen.add(r.get('hash'))
 if not r['relative'].startswith(('4.','10.','11.','16.','30.','3.4')):continue
 if any(x in r['relative'].lower() for x in ['draft','arhiva','ce s-a trimis','\\word\\','certific','fisa tehnic']):continue
 if not re.search(r'(?i)(act|c3|memori|adresa|f3|raspuns|cerere|contract|solicit|notific)',r['name']):continue
 t=r['text'];lines=[]
 for m in re.finditer(r'(?i)(?:num[ăa]r\s+de\s+[îi]nregistrare|nr\.?|FN\s*/|R1\s*[- ])[^\n]{0,200}',t[:6500]):
  if re.search(r'\d',m.group()):lines.append(m.group())
 print(json.dumps({'file':r['relative'],'lines':lines[:9],'read':r['read']},ensure_ascii=False))
