from pathlib import Path
import json, subprocess, fitz, time
BASE=Path(__file__).resolve().parent
ROOT=BASE.parent
TMP=BASE/'ocr_temporar'
TMP.mkdir(exist_ok=True)
OUT=BASE/'ocr'
OUT.mkdir(exist_ok=True)
rows=json.loads((BASE/'inventar.json').read_text(encoding='utf-8'))
unique={}
for r in rows:
    if r['extensie']=='.pdf' and r['detalii'].get('pagini_fara_text_suficient'):
        unique.setdefault(r['sha256'],r)
# Firmele sunt primele, apoi restul arhivei.
jobs=sorted(unique.values(),key=lambda r:(not r['cale'].startswith('04.'),r['cale']))
for i,r in enumerate(jobs):
    target=OUT/(r['sha256']+'.json')
    if target.exists():continue
    try:
        doc=fitz.open(ROOT/r['cale']);manifest=[]
        for num in r['detalii']['pagini_fara_text_suficient']:
            page=doc[num-1];scale=min(2,2200/max(page.rect.width,page.rect.height))
            img=TMP/(r['sha256']+'_'+str(num)+'.png')
            page.get_pixmap(matrix=fitz.Matrix(scale,scale),alpha=False).save(img)
            manifest.append({'page':num,'image':str(img)})
        doc.close()
        mp=TMP/'batch.json';mp.write_text(json.dumps(manifest,ensure_ascii=False),encoding='utf-8')
        p=subprocess.run(['C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(BASE/'ocr_windows.ps1'),'-ManifestPath',str(mp)],capture_output=True,timeout=max(120,len(manifest)*20))
        rp=Path(str(mp)+'.result.json')
        if p.returncode:raise RuntimeError(p.stderr.decode('utf-8',errors='replace')[:1000])
        results=json.loads(rp.read_text(encoding='utf-8-sig'))
        target.write_text(json.dumps({'sursa':r['cale'],'metoda':'Windows OCR en-US; text automat neverificat, poate greși caractere germane și cifre','pagini':results},ensure_ascii=False,indent=2),encoding='utf-8')
        (OUT/(r['sha256']+'.txt')).write_text('\n\n'.join('PAGINA '+str(x['page'])+'\n'+x['text'] for x in results),encoding='utf-8')
        # Șterge numai imaginile temporare generate de acest script, sub folder map/ocr_temporar.
        for x in manifest:
            img=Path(x['image']).resolve()
            if img.parent==TMP.resolve():img.unlink()
        if rp.resolve().parent==TMP.resolve():rp.unlink()
        print(f'OCR {i+1}/{len(jobs)}: {len(results)} pagini — {r["cale"]}',flush=True)
    except Exception as exc:
        print(f'OCR EROARE {r["cale"]}: {exc}',flush=True)
