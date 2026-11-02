import os,sys,json,time,hashlib,concurrent.futures
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import persoane_scan_20261031 as s
ENGINE=None
def initocr():
    s.init()
def ocr_image(im):
    global ENGINE
    if ENGINE is None:
        from rapidocr_onnxruntime import RapidOCR
        ENGINE=RapidOCR(intra_op_num_threads=1,inter_op_num_threads=1)
    result,_=ENGINE(im)
    return '\n'.join(row[1] for row in (result or []))
def work(r):
    out={'source':r['source'],'sha256':r['sha256'],'ocr_pages':0}
    try:
        import numpy as np
        data=Path(r['source']).read_bytes()
        if hashlib.sha256(data).hexdigest()!=r['sha256']:raise ValueError('Sursa schimbata dupa scanarea initiala')
        parts=[]
        if r['ext']=='.pdf':
            import fitz
            with fitz.open(stream=data,filetype='pdf') as doc:
                for i,page in enumerate(doc):
                    text=page.get_text()
                    if i in r.get('blank_pages',[]) and page.get_images():
                        pix=page.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False,colorspace=fitz.csRGB)
                        text=ocr_image(np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,3));out['ocr_pages']+=1
                    parts.append(text)
        else:
            import cv2
            im=cv2.imdecode(np.frombuffer(data,dtype=np.uint8),cv2.IMREAD_COLOR)
            if im is None:raise ValueError('Imagine necitibila')
            parts=[ocr_image(im)];out['ocr_pages']=1
        text='\n'.join(parts)
        out.update(text_chars=len(text),text_people=s.match(text),cnps=sorted({v for v in s.re.findall(r'(?<!\d)[1-9]\d{12}(?!\d)',text) if s.cnpvalid(v)}),personal_text=bool(s.KEY.search(s.norm(text))),ocr_complete=True)
        if out['text_people'] or out['cnps'] or r.get('personal_path') or r.get('path_people'):
            (s.LOCAL/'text'/(r['sha256']+'.txt')).write_text(text,'utf-8')
    except Exception as e:out['ocr_error']=str(e)
    return out
def main():
    def read(p):
        a=[]
        if p.exists():
            for l in p.read_text('utf-8').splitlines():
                try:a.append(json.loads(l))
                except:pass
        return a
    output=s.LOCAL/'ocr.jsonl';done={r['sha256'] for r in read(output)};todo={}
    for r in read(s.LOCAL/'scan.jsonl'):
        if r.get('sha256') not in done and not r.get('error') and (r.get('blank_pages') or r.get('ext') in s.IMGEXT):todo.setdefault(r['sha256'],r)
    tasks=sorted(todo.values(),key=lambda r:(not r.get('personal_path'),not bool(r.get('path_people')),r.get('pages',0)))
    limit=int(os.environ.get('PERSOANE_OCR_BATCH','500'));tasks=tasks[:limit]
    print(json.dumps({'ocr_to_process':len(tasks),'ocr_pending_total':len(todo)}),flush=True)
    with output.open('a',encoding='utf-8') as out,concurrent.futures.ProcessPoolExecutor(max_workers=2,initializer=initocr) as pool:
        fs=[pool.submit(work,r) for r in tasks]
        for i,f in enumerate(concurrent.futures.as_completed(fs)):
            try:r=f.result()
            except Exception as e:r={'ocr_error':str(e)}
            out.write(json.dumps(r,ensure_ascii=False)+'\n');out.flush()
            if i%10==0:print(json.dumps({'ocr_done':i+1,'batch':len(tasks)}),flush=True)
    print('OCR_BATCH_COMPLETE',flush=True)
if __name__=='__main__':main()
