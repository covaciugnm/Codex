from pathlib import Path
from urllib.parse import unquote
import re,json,hashlib,zipfile,xml.etree.ElementTree as ET
root=Path('Z:/00. Proiecte 2026/2026.11.27 - SCOLI ISJ CJRAE ONG PARTENER - PEO P7 7.e.3 Scoli pentru viitor')
a=root/'2. ANALIZA SI CLARIFICARI'
s=(root/'00 RAPORT CENTRAL - SCOLI PENTRU VIITOR.html').read_text(encoding='utf-8')
links=re.findall(r'href="([^"]+)"',s)
assert all((root/unquote(x)).exists() for x in links),'Broken link'
results={'local_links':len(links),'broken_links':0,'workbooks':[]}
for row in json.loads((a/'Manifest_bugete_finale_SHA256.json').read_text(encoding='utf-8')):
    p=root/row['file']
    assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']
    with zipfile.ZipFile(p) as z:
        book=ET.fromstring(z.read('xl/workbook.xml'))
        sheets=book.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheets')
        errors=[]
        for n in z.namelist():
            if n.startswith('xl/worksheets/sheet') and n.endswith('.xml'):
                x=ET.fromstring(z.read(n))
                errors += [(n,c.attrib) for c in x.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c') if c.get('t')=='e']
        assert len(sheets)==8 and not errors
        results['workbooks'].append({'file':row['file'],'sheet_count':len(sheets),'error_cells':len(errors),'hash_ok':True})
results['audit_10_present']='10/10' in (a/'Raport_agent_auditor_independent.txt').read_text(encoding='utf-8-sig')
(a/'Verificare_livrare_finala.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False,indent=2))
