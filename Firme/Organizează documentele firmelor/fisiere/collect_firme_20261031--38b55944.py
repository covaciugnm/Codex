import os, re, json, hashlib, shutil, unicodedata, zipfile, io, datetime, time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import threading
BASE=Path('Z:/00. Firme')
RUN=BASE/'00. RAPORT ARHIVA'/'Colectare 2026-10-31'
INV=Path('C:/Users/User/AppData/Local/Temp/inventar-firme-20261031.txt')
REG=json.loads((BASE/'00. RAPORT ARHIVA/Unificare 2026-10-01/REGISTRU_FIRME.json').read_text(encoding='utf-8-sig'))
REG.setdefault('REVO 5C SRL',{'name':'REVO 5C SRL','cui':'','aliases':['REVO 5C SRL','REVO 5C'],'historic':False})
def digest_file(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
OCR_ENGINE=None
def ocr_image(image):
    global OCR_ENGINE
    if OCR_ENGINE is None:
        from rapidocr_onnxruntime import RapidOCR
        OCR_ENGINE=RapidOCR(intra_op_num_threads=1,inter_op_num_threads=1)
    result,_=OCR_ENGINE(image)
    return '\n'.join(x[1] for x in (result or []))
def norm(s):
    return re.sub(r'[^A-Z0-9]+',' ',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().upper()).strip()
ALIASES={k:[norm(a) for a in v['aliases'] if len(norm(a))>=6] for k,v in REG.items()}
ALIASES.setdefault('3D SPACE ARIDE IT SRL',[]).extend(['3 D SPACE ARIDE','3D SPACE ARIDE'])
def matches(s):
    s=' '+norm(s)+' '
    return [k for k,v in REG.items() if (v.get('cui') and re.search(r'(?<!\d)'+v['cui']+r'(?!\d)',s)) or any(' '+a+' ' in s for a in ALIASES[k])]
DOCS={'.pdf','.docx','.doc','.xlsx','.xls','.xlsm','.ods','.odt','.rtf','.txt','.csv','.xml','.pptx','.ppt','.eml','.msg','.zip','.rar','.7z','.p7s','.p7m'}
IMAGES={'.jpg','.jpeg','.png','.tif','.tiff','.bmp'}
KEY=re.compile(r'CONSTAT|CONSTITUT|CERTIFICAT|INMATRICUL|ONRC|ACTE FIR|HOTARAR|HOTARIR|COMODAT|SEDIU|SPECIMEN|BENEFICIAR REAL|CONTRACT|FACTUR|BILANT|BALANT|DECLARAT|AUTORIZ|AVIZ|EXTRAS|FIRME|SOCIETAT|SCAN')
def inspect(path):
    p=Path(path); out={'source':path,'firms':matches(str(p)),'method':'cale','error':''}
    try:
        if p.suffix.lower() in {'.zip','.rar','.7z'}:
            with p.open('rb') as f:out['sha256']=hashlib.file_digest(f,'sha256').hexdigest()
            out['size']=p.stat().st_size;out['category_text']=norm(p.name);out['date']='';out['classifier_version']=2
            out['business_keyword']=bool(KEY.search(norm(p.name)))
            if p.suffix.lower()=='.zip':
                with zipfile.ZipFile(p) as z:names='\n'.join(z.namelist())
                out['firms']=sorted(set(out['firms']+matches(names)));out['business_keyword']|=bool(KEY.search(norm(names)))
                out['method']+=' + inventar ZIP';out['archive_entries']=len(names.splitlines())
            else:out['content_unread']=True
            return out
        data=p.read_bytes();out['size']=len(data);out['sha256']=hashlib.sha256(data).hexdigest()
        ext=p.suffix.lower().strip();text='';method=''
        if ext=='.pdf':
            import fitz
            with fitz.open(stream=data,filetype='pdf') as d:
                parts=[];ocr_pages=0
                for page in d:
                    pt=page.get_text()
                    if len(pt.strip())<40 and page.get_images():
                        import numpy as np
                        pix=page.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False,colorspace=fitz.csRGB)
                        pt=ocr_image(np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,3));ocr_pages+=1
                    parts.append(pt)
                text='\n'.join(parts);out['pages']=len(d);out['ocr_pages']=ocr_pages;out['ocr_done']=True
            method='text PDF';out['scan_without_text']=len(text.strip())<40
        elif ext in IMAGES:
            import cv2,numpy as np
            text=ocr_image(cv2.imdecode(np.frombuffer(data,dtype=np.uint8),cv2.IMREAD_COLOR));method='OCR imagine';out['ocr_done']=True
        elif ext in {'.docx','.xlsx','.xlsm','.pptx','.odt','.ods'}:
            from xml.etree import ElementTree as ET
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                parts=[n for n in z.namelist() if n.endswith('.xml') and (n.startswith(('word/','xl/worksheets/','ppt/slides/')) or n in ('xl/sharedStrings.xml','content.xml'))]
                text='\n'.join(' '.join(ET.fromstring(z.read(n)).itertext()) for n in parts)
            method='text XML Office'
        elif ext in {'.txt','.csv','.xml','.rtf','.eml'}:
            text=data.decode('utf-8',errors='replace');method='text'
        elif ext=='.xls':
            import xlrd
            book=xlrd.open_workbook(file_contents=data,on_demand=True)
            text='\n'.join(' '.join(str(c.value) for c in row) for sheet in book.sheets() for row in sheet.get_rows());book.release_resources();method='celule XLS'
        elif ext in {'.doc','.msg','.ppt'}:
            import olefile
            with olefile.OleFileIO(io.BytesIO(data)) as ole:
                chunks=[]
                for stream in ole.listdir():
                    blob=ole.openstream(stream).read()
                    for enc in ('utf-16le','cp1252'):
                        chunks.extend(re.findall(r'[A-Za-z0-9][A-Za-z0-9 .,;:/()&\-\r\n]{8,}',blob.decode(enc,errors='ignore')))
                text='\n'.join(chunks)
            method='text binar OLE (verificare necesara)';out['content_unread']=True
        else: out['content_unread']=True
        found=matches(text)
        if found:
            out['firms']=sorted(set(out['firms']+found));out['method']+=' + '+method
        out['category_text']=norm(p.name)
        out['business_keyword']=bool(KEY.search(norm(p.name))) or bool(re.search(r'\b(?:FACTURA|BILANT|BALANTA DE VERIFICARE|COD UNIC DE INREGISTRARE|CERTIFICAT CONSTATATOR|ACT CONSTITUTIV|REGISTRUL COMERTULUI|SOCIETATEA COMERCIALA|FURNIZOR|BENEFICIAR|CUI|CIF)\b',norm(text)))
        out['classifier_version']=2
        out['date']=''
        for pat,reverse in [(r'(?<!\d)((?:19|20)\d{2})[._ -](0?[1-9]|1[0-2])[._ -](0?[1-9]|[12]\d|3[01])(?!\d)',False),(r'(?<!\d)(0?[1-9]|[12]\d|3[01])[._ -](0?[1-9]|1[0-2])[._ -]((?:19|20)\d{2})(?!\d)',True)]:
            m=re.search(pat,p.name)
            if m:
                a,b,c=map(int,m.groups())
                try: out['date']=datetime.date(c,b,a).strftime('%Y.%m.%d') if reverse else datetime.date(a,b,c).strftime('%Y.%m.%d')
                except ValueError: pass
                if out['date']:out['date_evidence']='denumire originala';break
        if not out['date'] and text:
            dates=set()
            for m in re.finditer(r'(?i)\bdata\s*(?:emiterii|eliberarii|eliberării|documentului|incheierii|încheierii)?\s*[:\-]?\s*(\d{1,2})[./-](\d{1,2})[./-]((?:19|20)\d{2})',text):
                try:dates.add(datetime.date(int(m[3]),int(m[2]),int(m[1])).strftime('%Y.%m.%d'))
                except ValueError:pass
            if len(dates)==1:out['date']=dates.pop();out['date_evidence']='camp Data din continut (valoare unica)'
    except Exception as e:out['error']=str(e)
    return out
CATEGORIES=[('02. Certificat constatator',r'CONSTAT'),('03. Act constitutiv',r'CONSTITUT'),('08. Hotarari AGA',r'HOTARAR|HOTARIR|\bAGA\b'),('06. Contract sediu',r'COMODAT|SEDIU'),('07. Cont bancar',r'EXTRAS|CONT BANC|IBAN'),('04. TVA',r'\bTVA\b'),('01. Inregistrare ONRC',r'ONRC|INREGISTR|INMATRICUL|\bCUI\b'),('09. Declaratii',r'DECLARAT|SPECIMEN|BENEFICIAR REAL'),('10. Autorizatii si Avize',r'AUTORIZ|AVIZ'),('11. Contracte comerciale',r'CONTRACT|ACORD'),('12. MySMIS si Proiecte',r'MYSMIS|PROIECT|FINANTAR')]
def legacy_main():
    RUN.mkdir(parents=True,exist_ok=True)
    dirs=list(BASE.iterdir())+list((BASE/'0. FIRME ISTORICE SI SECUNDARE (grup)').iterdir())
    destinations={}
    for k,v in REG.items():
        for d in dirs:
            if ((v.get('cui') and v['cui'] in d.name) or norm(v['name']) in norm(d.name)) and d.is_dir():
                destinations[k]=d;break
    seen={};done=set();logpath=RUN/'JURNAL.jsonl'
    # Reuse previous evidence only when the target still exists; re-hash current files below.
    print('Indexare arhiva existenta',flush=True)
    prior=BASE/'00. RAPORT ARHIVA/Unificare 2026-10-01'
    for line in (prior/'JURNAL_MUTARI.jsonl').read_text(encoding='utf-8-sig').splitlines():
        r=json.loads(line)
        if r.get('sha256') and r.get('target'):seen.setdefault(r['sha256'],r['target'].replace('\\\\192.168.100.169\\Comun','Z:'))
    for r in json.loads((prior/'EVIDENTA_CITIRII_DOCUMENTELOR.json').read_text(encoding='utf-8-sig')):
        if r.get('sha256') and r.get('target'):seen[r['sha256']]=r['target'].replace('\\\\192.168.100.169\\Comun','Z:')
    verified=set()
    if logpath.exists():
        for line in logpath.read_text(encoding='utf-8').splitlines():
            try:
                r=json.loads(line);done.add(r['source'])
                if r.get('destination') and r.get('sha256'):seen[r['sha256']]=r['destination']
            except Exception:pass
    paths=INV.read_text(encoding='utf-8-sig').splitlines()
    candidates=[]
    for s in paths:
        if s in done or s.lower().startswith(str(BASE).lower()+'\\') or '\\#recycle\\' in s.lower():continue
        p=Path(s);ext=p.suffix.lower().strip()
        if ext in DOCS or (ext in IMAGES and (matches(str(p)) or KEY.search(norm(str(p))))):candidates.append(s)
    candidates.sort(key=lambda s:(not bool(matches(s)),not bool(KEY.search(norm(Path(s).name))),s))
    print('Candidati',len(candidates),flush=True)
    counts={};start=time.time()
    with logpath.open('a',encoding='utf-8') as log,ProcessPoolExecutor(max_workers=4) as pool:
        for i,r in enumerate(pool.map(inspect,candidates,chunksize=4)):
            status='fara_identificare'
            h=r.get('sha256')
            if h in seen and h not in verified:
                try:
                    if digest_file(Path(seen[h]))==h:verified.add(h)
                    else:seen.pop(h,None)
                except Exception:seen.pop(h,None)
            if r.get('error'):status='eroare_citire'
            elif r.get('sha256') in seen:
                status='identic_existent';r['destination']=seen[r['sha256']]
            elif r['firms'] or r.get('business_keyword'):
                firms=r['firms'];cat=next((c for c,rx in CATEGORIES if re.search(rx,r['category_text'])),'13. Diverse')
                if len(firms)==1 and firms[0] in destinations:targetdir=destinations[firms[0]]/cat
                elif len(firms)>1:targetdir=BASE/'00. Documente comune'/'Colectare 2026-10-31'
                else:targetdir=BASE/'00. DE VERIFICAT'/'Colectare 2026-10-31'/'Firma neidentificata'
                p=Path(r['source']);prefix=(REG[firms[0]].get('cui','')+' - ') if len(firms)==1 and REG[firms[0]].get('cui') else ''
                prefix+=(r.get('date') or 'DATA NECONFIRMATA')+' - '
                filename=prefix+p.stem[:125]+'__'+r['sha256'][:10]+p.suffix
                dest=targetdir/filename
                try:
                    targetdir.mkdir(parents=True,exist_ok=True)
                    # Exclusive creation guarantees that existing documents are never overwritten.
                    with p.open('rb') as src,dest.open('xb') as dst:shutil.copyfileobj(src,dst,1024*1024)
                    shutil.copystat(p,dest)
                    if digest_file(dest)!=r['sha256']:raise RuntimeError('Verificare SHA256 esuata')
                    r['destination']=str(dest);seen[r['sha256']]=str(dest);status='copiat_verificat'
                except Exception as e:status='eroare_copiere';r['error']=str(e)
            r['status']=status;counts[status]=counts.get(status,0)+1
            log.write(json.dumps(r,ensure_ascii=False)+'\n');log.flush()
            if i%100==0:
                summary={'processed':i+1,'candidates':len(candidates),'counts':counts,'seconds':int(time.time()-start)}
                (RUN/'PROGRES.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary),flush=True)
    (RUN/'REZUMAT.json').write_text(json.dumps({'processed':len(candidates),'counts':counts,'inventory_files':len(paths)},indent=2),encoding='utf-8')
    print('TERMINAT',counts,flush=True)
def main():
    RUN.mkdir(parents=True,exist_ok=True)
    dirs=list(BASE.iterdir())+list((BASE/'0. FIRME ISTORICE SI SECUNDARE (grup)').iterdir())
    destinations={}
    for k,v in REG.items():
        for d in dirs:
            if ((v.get('cui') and v['cui'] in d.name) or norm(v['name']) in norm(d.name)):
                destinations[k]=d;break
    seen={};verified=set();done=set();locks={};master=threading.Lock();created=set()
    prior=BASE/'00. RAPORT ARHIVA/Unificare 2026-10-01'
    for line in (prior/'JURNAL_MUTARI.jsonl').read_text(encoding='utf-8-sig').splitlines():
        r=json.loads(line)
        if r.get('sha256') and r.get('target'):seen.setdefault(r['sha256'],r['target'].replace('\\\\192.168.100.169\\Comun','Z:'))
    for r in json.loads((prior/'EVIDENTA_CITIRII_DOCUMENTELOR.json').read_text(encoding='utf-8-sig')):
        if r.get('sha256') and r.get('target'):seen[r['sha256']]=r['target'].replace('\\\\192.168.100.169\\Comun','Z:')
    local=Path('C:/Users/User/AppData/Local/Temp/firme-jurnal-20261031.jsonl')
    logpath=RUN/'JURNAL.jsonl'
    if not local.exists() and logpath.exists():shutil.copyfile(logpath,local)
    if local.exists():
        for line in local.read_text(encoding='utf-8').splitlines():
            try:
                r=json.loads(line)
                needs_ocr=(r.get('scan_without_text') or (r.get('content_unread') and Path(r['source']).suffix.lower() in IMAGES)) and not r.get('ocr_done')
                needs_old_formats=r.get('content_unread') and Path(r['source']).suffix.lower() in {'.xls','.doc','.msg','.ppt'} and r.get('classifier_version',1)<2
                if r['status'] not in ('eroare_copiere','eroare_citire') and not needs_ocr and not needs_old_formats and not (r['status']=='fara_identificare' and r.get('classifier_version',1)<2):done.add(r['source'])
                if r.get('destination') and r.get('sha256'):seen[r['sha256']]=r['destination']
            except Exception:pass
    def transfer(r):
        h=r.get('sha256');status='fara_identificare'
        if not h:r['status']='eroare_citire';return r
        with master: lock=locks.setdefault(h,threading.Lock())
        with lock:
            if h in seen:
                prior_dest=seen[h]
                better_date=r.get('date') and 'DATA NECONFIRMATA' in Path(prior_dest).name
                better_firm=r['firms'] and '00. DE VERIFICAT' in prior_dest and 'Colectare 2026-10-31' in prior_dest
                if better_date or better_firm:
                    r['older_copy_preserved']=prior_dest;seen.pop(h,None);verified.discard(h)
            if h in seen and h not in verified:
                try:
                    if digest_file(Path(seen[h]))==h:verified.add(h)
                    else:seen.pop(h,None)
                except Exception:seen.pop(h,None)
            if h in seen:r['destination']=seen[h];status='identic_existent'
            elif r['firms'] or r.get('business_keyword'):
                firms=r['firms'];cat=next((c for c,rx in CATEGORIES if re.search(rx,r.get('category_text',norm(Path(r['source']).name)))),'13. Diverse')
                if len(firms)==1 and firms[0] in destinations:targetdir=destinations[firms[0]]/cat
                elif len(firms)>1:targetdir=BASE/'00. Documente comune'/'Colectare 2026-10-31'
                else:targetdir=BASE/'00. DE VERIFICAT'/'Colectare 2026-10-31'/'Firma neidentificata'
                p=Path(r['source']);prefix=(REG[firms[0]].get('cui','')+' - ') if len(firms)==1 and REG[firms[0]].get('cui') else ''
                prefix+=(r.get('date') or 'DATA NECONFIRMATA')+' - '
                dest=targetdir/(prefix+p.stem[:125]+'__'+h[:10]+p.suffix)
                try:
                    if str(targetdir) not in created:targetdir.mkdir(parents=True,exist_ok=True);created.add(str(targetdir))
                    if dest.exists():
                        if digest_file(dest)==h:
                            r['destination']=str(dest);seen[h]=str(dest);verified.add(h);r['status']='copie_recuperata_verificata';return r
                        r['partial_prior_copy']=str(dest)
                        dest=targetdir/(dest.stem+'__reluare_'+str(time.time_ns())+dest.suffix)
                    with p.open('rb') as src,dest.open('xb') as dst:shutil.copyfileobj(src,dst,1024*1024)
                    shutil.copystat(p,dest)
                    if digest_file(dest)!=h:raise RuntimeError('Verificare SHA256 esuata')
                    r['destination']=str(dest);seen[h]=str(dest);verified.add(h);status='copiat_verificat'
                except Exception as e:status='eroare_copiere';r['copy_error']=str(e)
            elif r.get('error'):status='eroare_citire'
            r['status']=status;return r
    paths=INV.read_text(encoding='utf-8-sig').splitlines();candidates=[]
    for s in paths:
        if s in done or s.lower().startswith(str(BASE).lower()+'\\') or '\\#recycle\\' in s.lower():continue
        p=Path(s);ext=p.suffix.lower().strip()
        if ext in DOCS or (ext in IMAGES and (matches(str(p)) or KEY.search(norm(str(p))))):candidates.append(s)
    candidates.sort(key=lambda s:(not bool(matches(s)),not bool(KEY.search(norm(Path(s).name))),s))
    print('Candidati ramasi',len(candidates),flush=True)
    counts={};start=time.time();n=0
    with local.open('a',encoding='utf-8') as log,ProcessPoolExecutor(max_workers=4) as readers,ThreadPoolExecutor(max_workers=8) as copiers:
        batch=[]
        for r in readers.map(inspect,candidates,chunksize=4):
            batch.append(copiers.submit(transfer,r))
            if len(batch)<64:continue
            for f in as_completed(batch):
                item=f.result();log.write(json.dumps(item,ensure_ascii=False)+'\n');n+=1;counts[item['status']]=counts.get(item['status'],0)+1
            batch=[];log.flush();shutil.copyfile(local,logpath)
            summary={'processed_this_pass':n,'previously_processed':len(done),'candidates_this_pass':len(candidates),'counts_this_pass':counts,'seconds':int(time.time()-start)}
            (RUN/'PROGRES.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary),flush=True)
        for f in as_completed(batch):
            item=f.result();log.write(json.dumps(item,ensure_ascii=False)+'\n');n+=1;counts[item['status']]=counts.get(item['status'],0)+1
        log.flush();shutil.copyfile(local,logpath)
    (RUN/'REZUMAT.json').write_text(json.dumps({'processed':len(candidates),'counts':counts,'inventory_files':len(paths)},indent=2),encoding='utf-8')
    print('TERMINAT',counts,flush=True)
if __name__=='__main__':main()
