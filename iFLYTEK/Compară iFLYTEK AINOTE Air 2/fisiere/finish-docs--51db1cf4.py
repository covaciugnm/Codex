import json, pathlib, zipfile, hashlib, re, html, xml.etree.ElementTree as ET
from pypdf import PdfReader
root=pathlib.Path(__file__).resolve().parent.parent
folder=root/'documentatie/arhive-sdk'
records=json.loads((folder/'index.json').read_text(encoding='utf-8-sig'))
errors=[]
for i,r in enumerate(records):
    try:
        if r['status']=='indexed-only-over-20MiB':
            ext=pathlib.Path(r['entry']).suffix.lower()
            r['file']=f'{i+1:06d}'+ext
            with zipfile.ZipFile(root.parent/r['archive']) as z:
                data=z.read(r['entry'])
            (folder/r['file']).write_bytes(data)
            r['status']='extracted-text' if ext=='.txt' else 'extracted-binary-not-text-read'
            if ext=='.txt': r['category']='training-dataset-not-SDK-documentation'
        src=folder/r['file']
        if src.suffix.lower()=='.pdf':
            reader=PdfReader(src)
            text='\n\n'.join(f'PAGE {i+1}\n'+(page.extract_text() or '') for i,page in enumerate(reader.pages))
            r['pages']=len(reader.pages);r['textFile']=src.stem+'.pdf.txt'
            (folder/r['textFile']).write_text(text,encoding='utf8');r['status']='extracted-text-from-pdf'
        elif src.suffix.lower()=='.docx':
            with zipfile.ZipFile(src) as z:
                doc=ET.fromstring(z.read('word/document.xml'))
            text='\n'.join(''.join(el.itertext()) for el in doc.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))
            r['textFile']=src.stem+'.docx.txt';(folder/r['textFile']).write_text(text,encoding='utf8');r['status']='extracted-text-from-docx'
        r['sha256']=hashlib.sha256(src.read_bytes()).hexdigest()
    except Exception as e:
        errors.append({'entry':r['entry'],'error':str(e)});r['status']='conversion-error'
(folder/'index.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8')
topics={k:[] for k in ['bluetooth','wifi','opus','tts','microphone','teleprompter','glassclaw','gatt','audiogram']}
chars=0
for r in records:
    file=r.get('textFile') or r['file']
    if not file or not file.endswith('.txt') or r.get('category'):continue
    body=(folder/file).read_text(encoding='utf8',errors='replace');chars+=len(body)
    for topic in topics:
        matches=list(re.finditer(topic,body,re.I))
        if matches:topics[topic].append({'archive':r['archive'],'entry':r['entry'],'file':file,'occurrences':len(matches),'excerpts':[body[max(0,m.start()-120):m.end()+240] for m in matches[:3]]})
(folder/'correlations.json').write_text(json.dumps(topics,ensure_ascii=False,indent=2),encoding='utf8')
summary={'archivesScanned':137,'archivesWithMatchingDocuments':len(set(r['archive'] for r in records)),'entries':len(records),'processedTextCharactersExcludingDatasets':chars,'errors':errors,'pdfTextExtracted':sum(r['status']=='extracted-text-from-pdf' for r in records),'docxTextExtracted':sum(r['status']=='extracted-text-from-docx' for r in records),'trainingDatasets':sum(bool(r.get('category')) for r in records)}
(folder/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
rows=[]
for r in records:
    f=r.get('textFile') or r.get('file'); link=f'<a href="{f}">Text / fișier</a>' if f else '-'
    rows.append('<tr><td>'+html.escape(r['archive'])+'</td><td>'+html.escape(r['entry'])+'</td><td>'+link+'</td><td>'+html.escape(r['status'])+'</td></tr>')
(folder/'INDEX.html').write_text('<!doctype html><meta charset="utf-8"><title>Documentații din arhive</title><style>body{font:15px system-ui;margin:30px}td,th{border:1px solid #ccc;padding:8px}table{border-collapse:collapse}td{overflow-wrap:anywhere}</style><a href="../../INDEX.html">Catalog APK</a><h1>Documentații și texte din arhivele locale</h1><p>Index automat. Include exemple, licențe și date; nu toate materialele descriu ochelarii iFLYTEK. Extracția textului PDF nu include OCR sau verificare vizuală integrală.</p><p><a href="summary.json">Rezultate</a> · <a href="correlations.json">Corelații tematice</a></p><table><tr><th>Arhivă</th><th>Intrare</th><th>Extras</th><th>Stare</th></tr>'+''.join(rows)+'</table>',encoding='utf8')
print(json.dumps(summary))
