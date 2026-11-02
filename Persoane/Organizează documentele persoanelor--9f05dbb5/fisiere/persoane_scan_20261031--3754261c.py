import os, re, json, hashlib, unicodedata, zipfile, time, sys, collections, concurrent.futures, datetime, shutil, io
from pathlib import Path
ROOT=Path('Z:/')
DEST=ROOT/'00. Persoane'
LOCAL=Path('C:/Users/User/AppData/Local/Temp/persoane-20261031')
LOCAL.mkdir(exist_ok=True)
AUDIT=DEST/'00. Arhiva/00. Administrativ/Completare 2026-10-31'
INV=Path('C:/Users/User/AppData/Local/Temp/persoane-20261031-inventar.txt')
def norm(s):
    return re.sub(r'[^A-Z0-9]+',' ',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().upper()).strip()
def people():
    result=[]
    for p in DEST.iterdir():
        if p.is_dir() and not p.name[:1].isdigit():
            n=p.name.split(' - ')[0]; c=re.search(r'\b[1-9]\d{12}\b',p.name)
            result.append({'name':n,'folder':p.name,'cnp':c.group() if c else '', 'tokens':norm(n).split()})
    return result
PEOPLE=[]
def init():
    global PEOPLE
    PEOPLE=json.loads((LOCAL/'people.json').read_text('utf-8'))
    extra=LOCAL/'extra_people.json'
    if extra.exists():
        byname={p['name']:p for p in PEOPLE}
        for p in json.loads(extra.read_text('utf-8')):byname.setdefault(p['name'],p)
        PEOPLE=list(byname.values())
def match(s):
    n=' '+norm(s)+' '; tokens=set(n.split()); out=[]
    for p in PEOPLE:
        t=p['tokens']
        if (p['cnp'] and p['cnp'] in n) or (len(t)>1 and set(t)<=tokens):out.append(p['name'])
    return out
KEY=re.compile(r'\b(CI|C I|CV|C V|CNP|CIM|CURRICULUM|BULETIN|PASAPORT|PASSPORT|DIPLOM[A-Z]*|BACALAUREAT|IDENTITATE|PERSONALE|SALARIAT[A-Z]*|ANGAJAT[A-Z]*|ANGAJARE|ADEVERINTA|IMPUTERNICIRE|PROCURA|VOLUNTARIAT|NOMINAL[A-Z]*|MOSTENITOR|NASCUT|NASTERE|CASATORIE|DECES|RESURSE UMANE|DOSAR PERSONAL|PERMIS DE CONDUCERE)\b')
DOCEXT={'.pdf','.docx','.doc','.rtf','.odt','.xlsx','.xlsm','.xls','.ods','.pptx','.ppt','.txt','.csv','.html','.htm','.eml','.msg'}
IMGEXT={'.jpg','.jpeg','.png','.tif','.tiff','.bmp','.webp','.jfif'}
def cnpvalid(s):
    if not re.fullmatch('[1-9][0-9]{12}',s):return False
    v=sum(int(a)*int(b) for a,b in zip(s[:12],'279146358279'))%11
    if (1 if v==10 else v)!=int(s[-1]):return False
    try:datetime.date(2000+int(s[1:3]),int(s[3:5]),int(s[5:7]))
    except ValueError:return False
    return True
def extract(path,ext,data=None):
    errors=[]; pages=0; blank=[]; text=''
    if ext=='.pdf':
        import fitz
        fitz.TOOLS.mupdf_display_errors(False)
        with fitz.open(stream=data,filetype='pdf') if data is not None else fitz.open(path) as d:
            pages=len(d)
            if d.needs_pass:return '',pages,[],['PDF protejat cu parola']
            tt=[]
            for i,p in enumerate(d):
                t=p.get_text()
                if len(t.strip())<40:blank.append(i)
                tt.append(t)
            text='\n'.join(tt)
    elif ext in {'.docx','.xlsx','.xlsm','.pptx','.odt','.ods'}:
        import xml.etree.ElementTree as ET
        with zipfile.ZipFile(io.BytesIO(data) if data is not None else path) as z:
            names=[n for n in z.namelist() if (n.startswith('word/') or n.startswith('xl/worksheets/') or n=='xl/sharedStrings.xml' or n.startswith('ppt/slides/') or n=='content.xml') and n.endswith('.xml')]
            text='\n'.join(' '.join(ET.fromstring(z.read(n)).itertext()) for n in names)
    elif ext in {'.doc','.xls','.ppt','.msg'}:
        b=data if data is not None else Path(path).read_bytes()
        text='\n'.join(x.decode('utf-16le',errors='ignore') for x in re.findall(rb'(?:[\x20-\xff]\x00){5,}',b))+'\n'+'\n'.join(x.decode('cp1250',errors='ignore') for x in re.findall(rb'[\x20-\x7e\x80-\xff]{8,}',b))
        errors.append('Format binar vechi: extragere euristica, verificare vizuala necesara')
    else:
        b=data if data is not None else Path(path).read_bytes()
        try:text=b.decode('utf-8')
        except UnicodeDecodeError:text=b.decode('cp1250',errors='replace')
    return text,pages,blank,errors
def scan(rel):
    p=ROOT/rel; ext=p.suffix.strip().lower().replace(' ',''); r={'source':str(p),'relative':rel,'ext':ext}
    try:
        st=p.stat();r.update(size=st.st_size,mtime=st.st_mtime)
        r['path_people']=match(rel)
        r['personal_path']=bool(KEY.search(norm(rel)))
        if st.st_size>32*1024*1024 and ext in {'.txt','.csv','.html','.htm'} and not r['path_people'] and not r['personal_path']:
            r['error']='Fisier text/date peste 32 MB fara indicii personale in cale; necesita verificare separata';return r
        data=p.read_bytes()
        r['sha256']=hashlib.sha256(data).hexdigest()
        if ext in DOCEXT:
            cache=LOCAL/'text'/(r['sha256']+'.json')
            if cache.exists():
                r.update(json.loads(cache.read_text('utf-8')));return r
            text,pages,blank,errs=extract(str(p),ext,data)
            r.update(pages=pages,blank_pages=blank,errors=errs,text_chars=len(text),text_people=match(text),cnps=sorted({s for s in re.findall(r'(?<!\d)[1-9]\d{12}(?!\d)',text) if cnpvalid(s)}),personal_text=bool(KEY.search(norm(text))))
            # Keep extracted text locally for review and OCR reconciliation; source files never edited.
            if r['path_people'] or r['text_people'] or r['cnps'] or r['personal_path']:
                (LOCAL/'text'/ (r['sha256']+'.txt')).write_text(text,encoding='utf-8')
            cache.write_text(json.dumps({k:r[k] for k in ['pages','blank_pages','errors','text_chars','text_people','cnps','personal_text']},ensure_ascii=False),'utf-8')
            if ext=='.pdf' and blank and (r['personal_path'] or not r['path_people']) and shutil.disk_usage(LOCAL).free>4*1024**3:
                (LOCAL/'ocr_source').mkdir(exist_ok=True)
                (LOCAL/'ocr_source'/(r['sha256']+'.pdf')).write_bytes(data)
        else:r.update(pages=0,blank_pages=[],errors=[],text_chars=0,text_people=[],cnps=[],personal_text=False)
    except Exception as e:r['error']=str(e)
    return r
def main():
    (LOCAL/'text').mkdir(exist_ok=True)
    pp=people();(LOCAL/'people.json').write_text(json.dumps(pp,ensure_ascii=False),encoding='utf-8');init()
    lines=INV.read_text('utf-8-sig').splitlines()
    selected=[]; skipped=collections.Counter()
    for rel in lines:
        if not rel or rel.startswith('00. Persoane\\') or rel.startswith('#recycle\\'):continue
        p=Path(rel); ext=p.suffix.strip().lower().replace(' ','')
        if p.name.startswith('~$'):skipped['temporare Office']+=1;continue
        technical=any(v in ('/'+rel.replace('\\','/').lower()+'/') for v in ['/node_modules/','/.git/','/site-packages/','/vendor/','/program files/'])
        if ext in DOCEXT and not technical:selected.append(rel)
        elif ext in IMGEXT and (match(rel) or KEY.search(norm(rel)) or rel.lower().startswith(('scan\\','scanari\\','01. acte proprietate\\','dep. resurse umane\\','certificate\\')) or (not technical and not any(v in rel.replace('\\','/').lower() for v in ['images/','datasets/','set de date','node_modules','site-packages','/venv/','/assets/','/icons/','/screenshots/','/wp-content/']) and re.match(r'^(scan|img[_ -]?\d|image[_ -]?\d|whatsapp|photo[_ -]?\d|doc[_ -]?\d)',p.name,re.I))):selected.append(rel)
        else:skipped[ext or 'fara extensie']+=1
    (LOCAL/'selection.json').write_text(json.dumps({'inventory':len(lines),'selected':len(selected),'skipped':dict(skipped)},ensure_ascii=False,indent=2),'utf-8')
    done=set()
    outf=LOCAL/'scan.jsonl'
    if outf.exists():
        for l in outf.read_text('utf-8').splitlines():
            try:done.add(json.loads(l)['relative'])
            except:pass
    selected=[x for x in selected if x not in done]
    selected.sort(key=lambda x:(not bool(match(x)),not bool(KEY.search(norm(x))),Path(x).suffix.lower() not in {'.pdf','.docx','.doc'},x))
    print(json.dumps({'inventory':len(lines),'to_scan':len(selected),'already_scanned':len(done)}),flush=True)
    with outf.open('a',encoding='utf-8') as out, concurrent.futures.ProcessPoolExecutor(max_workers=12,initializer=init) as pool:
        futures={pool.submit(scan,x):x for x in selected}
        n=len(done); start=time.time()
        for f in concurrent.futures.as_completed(futures):
            try:r=f.result()
            except Exception as e:r={'relative':futures[f],'error':str(e)}
            out.write(json.dumps(r,ensure_ascii=False)+'\n');out.flush();n+=1
            if n%100==0:
                status={'scanned':n,'total':len(done)+len(selected),'seconds':round(time.time()-start)}
                (LOCAL/'status.json').write_text(json.dumps(status),'utf-8');print(json.dumps(status),flush=True)
    print('SCAN_COMPLETE',flush=True)
    (LOCAL/'last_scan_complete.json').write_text(json.dumps({'inventory_bytes':INV.stat().st_size,'inventory_lines':len(lines),'completed_at':datetime.datetime.now().isoformat()}),'utf-8')
if __name__=='__main__':main()
