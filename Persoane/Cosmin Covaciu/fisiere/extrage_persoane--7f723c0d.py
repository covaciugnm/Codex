import os, sys, io, re, json, sqlite3, hashlib, zipfile, time, traceback, html, gzip, threading, subprocess, atexit
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed, wait, FIRST_COMPLETED
from collections import Counter
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE / 'deps'))
ROOT = Path(r'Z:\00. Persoane')
INDEX = Path(r'C:\Users\User\persoane-index-complet.txt')
DB = BASE / 'inventar.sqlite'
OCR = None
LOCAL = threading.local()
CHILDREN = []

def connect():
    c = sqlite3.connect(DB, timeout=60)
    c.execute('pragma journal_mode=WAL')
    c.executescript('''
    CREATE TABLE IF NOT EXISTS files(path TEXT PRIMARY KEY,person TEXT,category TEXT,ext TEXT,size INTEGER,mtime REAL,sha256 TEXT,status TEXT,error TEXT);
    CREATE INDEX IF NOT EXISTS file_hash ON files(sha256);
    CREATE TABLE IF NOT EXISTS documents(sha256 TEXT PRIMARY KEY,ext TEXT,status TEXT,pages INTEGER,ocr_pages INTEGER,text_path TEXT,json_path TEXT,chars INTEGER,error TEXT,processed_at TEXT);
    CREATE VIRTUAL TABLE IF NOT EXISTS search USING fts5(sha256 UNINDEXED, text, tokenize='unicode61 remove_diacritics 2');
    ''')
    return c

def progress(c, phase, extra=None):
    d={'phase':phase,'updated_at':datetime.now(timezone.utc).isoformat(),
       'files':dict(c.execute('select status,count(*) from files group by status')),
       'documents':dict(c.execute('select status,count(*) from documents group by status'))}
    if extra:d.update(extra)
    tmp=BASE/'progres.tmp';tmp.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8');tmp.replace(BASE/'progres.json')
    print(json.dumps(d,ensure_ascii=False),flush=True)

def identify(p):
    parts=Path(p).relative_to(ROOT).parts
    if parts[0]=='00. Arhiva' and len(parts)>1:person=parts[1];cat='ARHIVA / '+' / '.join(parts[2:-1])
    else:person=parts[0];cat=' / '.join(parts[1:-1])
    return person,cat

def fingerprint(p):
    try:
        st=os.stat(p);h=hashlib.sha256()
        with open(p,'rb') as f:
            for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
        return p,st.st_size,st.st_mtime,h.hexdigest(),None
    except Exception as e:return p,None,None,None,f'{type(e).__name__}: {e}'

def decode(b):
    for enc in ('utf-8-sig','utf-16','cp1250','cp1252'):
        try:return b.decode(enc)
        except UnicodeError:pass
    return b.decode('utf-8',errors='replace')

def ocr_image(im):
    global OCR
    from PIL import Image,ImageOps
    import numpy as np
    from rapidocr_onnxruntime import RapidOCR
    if OCR is None:OCR=RapidOCR(intra_op_num_threads=2,inter_op_num_threads=1)
    im=ImageOps.exif_transpose(im).convert('RGB')
    if max(im.size)>2400:im.thumbnail((2400,2400))
    result,_=OCR(np.array(im))
    result=result or []
    score=sum(float(x[2]) for x in result)/max(len(result),1)
    # Sideways pages occur in the source archive. Retry the orientation if
    # little text is recognized or the recognized confidence is weak.
    if len(''.join(x[1] for x in result))<45 or score<.72:
        alt,_=OCR(np.array(im.rotate(90,expand=True)));alt=alt or []
        quality=lambda r:sum(len(x[1])*float(x[2]) for x in r)
        if quality(alt)>quality(result):result=alt
    return '\n'.join(x[1] for x in result),[{'text':x[1],'confidence':float(x[2]),'box':x[0]} for x in result]

def binary_doc(data):
    import olefile,struct
    from striprtf.striprtf import rtf_to_text
    if data.lstrip().startswith(b'{\\rtf'):return rtf_to_text(decode(data)),'rtf'
    if data.startswith(b'PK'):return office_zip(data,'.docx')[0],'ooxml'
    ole=olefile.OleFileIO(io.BytesIO(data))
    wd=ole.openstream('WordDocument').read()
    flags=struct.unpack_from('<H',wd,10)[0]
    if flags&0x100:raise ValueError('Document Word criptat')
    table=ole.openstream('1Table' if flags&0x200 else '0Table').read()
    fc,lcb=struct.unpack_from('<II',wd,418)
    clx=table[fc:fc+lcb];i=0
    while i<len(clx) and clx[i]==1:i+=3+struct.unpack_from('<H',clx,i+1)[0]
    if i>=len(clx) or clx[i]!=2:raise ValueError('Structura Word veche sau tabela de text absenta')
    size=struct.unpack_from('<I',clx,i+1)[0];plc=clx[i+5:i+5+size];n=(size-4)//12
    cps=struct.unpack_from('<'+'I'*(n+1),plc);texts=[]
    for k in range(n):
        packed=struct.unpack_from('<I',plc,(n+1)*4+k*8+2)[0]
        compressed=bool(packed&0x40000000);pos=packed&0x3fffffff;count=cps[k+1]-cps[k]
        if compressed:pos//=2;texts.append(wd[pos:pos+count].decode('cp1250',errors='replace'))
        else:texts.append(wd[pos:pos+2*count].decode('utf-16le',errors='replace'))
    text=''.join(texts).replace('\r','\n').replace('\x07','\t').replace('\x0b','\n')
    return re.sub(r'[\x00-\x08\x0c\x0e-\x1f]','',text),'doc_piece_table'

def office_zip(data,ext):
    from lxml import etree
    from PIL import Image
    z=zipfile.ZipFile(io.BytesIO(data));sections=[];ocr_count=0;issues=[]
    if ext in ('.xlsx','.xlsm'):
        import openpyxl
        # Keep formulas and cached values separately. Neither replaces the other.
        wf=openpyxl.load_workbook(io.BytesIO(data),read_only=True,data_only=False)
        wv=openpyxl.load_workbook(io.BytesIO(data),read_only=True,data_only=True)
        for sh in wf:
            lines=[];cache=wv[sh.title]
            for row,cached_row in zip(sh.iter_rows(),cache.iter_rows()):
                for cell,cached_cell in zip(row,cached_row):
                    if cell.value is not None:
                        v=cell.value;cv=cached_cell.value
                        lines.append(f'{cell.coordinate}\t{v}'+(f'\t[valoare memorata: {cv}]' if cell.data_type=='f' else ''))
            sections.append({'part':sh.title,'method':'xlsx_cells_formulas_and_cache','text':'\n'.join(lines)})
        wf.close();wv.close()
    # Read all text-bearing OOXML parts, including comments, headers, footers,
    # notes and text boxes. Cells above avoid losing the coordinate context.
    for name in z.namelist():
        relevant=(ext in ('.docx','.docm') and name.startswith('word/') and name.endswith('.xml')) or (ext=='.pptx' and name.startswith('ppt/') and name.endswith('.xml')) or (ext in ('.odt','.ods') and name in ('content.xml','styles.xml')) or (ext in ('.xlsx','.xlsm') and ('comment' in name.lower() or 'drawing' in name.lower()) and name.endswith('.xml'))
        if relevant:
            try:
                tree=etree.fromstring(z.read(name));lines=[]
                for el in tree.iter():
                    tag=etree.QName(el).localname
                    if tag in ('t','text:p','p','tab','br','line-break'):
                        if tag=='t' and el.text:lines.append(el.text)
                        elif tag in ('p','br','line-break'):lines.append('\n')
                        elif tag=='tab':lines.append('\t')
                if ext in ('.odt','.ods'):lines=['\n'.join(tree.xpath('//text()'))]
                text=''.join(lines).strip()
                if text:sections.append({'part':name,'method':'office_xml','text':text})
            except Exception as e:issues.append(name+': '+str(e))
        if '/media/' in name or name.startswith('Pictures/'):
            try:
                with Image.open(io.BytesIO(z.read(name))) as im:
                    for k in range(getattr(im,'n_frames',1)):
                        im.seek(k);t,detail=ocr_image(im.copy());sections.append({'part':name,'frame':k+1,'method':'ocr_embedded_image','text':t,'ocr':detail});ocr_count+=1
            except Exception as e:issues.append('Imagine '+name+': '+str(e))
    return sections,ocr_count,issues

def extract_bytes(data,ext,depth=0):
    import pymupdf
    from PIL import Image
    sections=[];issues=[];ocr_count=0
    if ext=='.pdf' or data.startswith(b'%PDF'):
        doc=pymupdf.open(stream=data,filetype='pdf')
        if doc.needs_pass:raise ValueError('PDF protejat prin parola')
        for i,pg in enumerate(doc):
            native=pg.get_text('text',sort=True);section={'page':i+1,'method':'pdf_native','text':native}
            annotations=[]
            for annot in pg.annots() or []:
                if annot.info:annotations.append(annot.info)
            if annotations:section['annotations']=annotations;section['text']+='\n[ADNOTARI PDF]\n'+json.dumps(annotations,ensure_ascii=False)
            try:
                image_area=sum(abs((r[2]-r[0])*(r[3]-r[1])) for r in [x['bbox'] for x in pg.get_image_info()])
                if image_area>pg.rect.get_area()*.35 or len(native.strip())<80:
                    px=pg.get_pixmap(matrix=pymupdf.Matrix(2,2),alpha=False);im=Image.frombytes('RGB',[px.width,px.height],px.samples)
                    t,detail=ocr_image(im);section.update(method='pdf_native_and_ocr',ocr_text=t,ocr=detail);ocr_count+=1
            except Exception as e:issues.append(f'Pagina {i+1} OCR: {type(e).__name__}: {e}')
            sections.append(section)
        for name in doc.embfile_names():
            try:
                child=extract_bytes(doc.embfile_get(name),Path(name).suffix.lower(),depth+1);sections.append({'part':'embedded/'+name,'method':'embedded_document','child':child})
            except Exception as e:issues.append('Atasament PDF '+name+': '+str(e))
        return sections,ocr_count,issues
    if ext in ('.docx','.docm','.xlsx','.xlsm','.pptx','.odt','.ods'):return office_zip(data,ext)
    if ext=='.doc':
        t,method=binary_doc(data);sections=[{'method':method,'text':t}]
        # Older DOC files can contain scanned documents. Recover raster images
        # from the compound streams without opening or executing Office macros.
        import olefile
        if data.startswith(bytes.fromhex('d0cf11e0a1b11ae1')):
            ole=olefile.OleFileIO(io.BytesIO(data));seen=set()
            for stream in ole.listdir():
                blob=ole.openstream(stream).read()
                candidates=[m.group(0) for m in re.finditer(b'\xff\xd8\xff.+?\xff\xd9',blob,re.DOTALL)]
                candidates.extend(m.group(0) for m in re.finditer(b'\x89PNG\r\n\x1a\n.+?IEND\xaeB`\x82',blob,re.DOTALL))
                for b in candidates:
                    key=hashlib.sha256(b).hexdigest()
                    if key in seen:continue
                    try:
                        with Image.open(io.BytesIO(b)) as im:
                            if min(im.size)<80:continue
                            tx,detail=ocr_image(im);sections.append({'part':'/'.join(stream),'method':'doc_embedded_image_ocr','text':tx,'ocr':detail});ocr_count+=1;seen.add(key)
                    except Exception:pass
        return sections,ocr_count,issues
    if ext=='.xls':
        import xlrd
        w=xlrd.open_workbook(file_contents=data)
        for sh in w.sheets():
            text='\n'.join(f'R{r+1}C{c+1}\t{sh.cell_value(r,c)}' for r in range(sh.nrows) for c in range(sh.ncols) if sh.cell_value(r,c)!='')
            sections.append({'part':sh.name,'method':'xls_cells','text':text})
        return sections,0,['XLS: valori extrase; formulele binare si imaginile incorporate necesita verificare separata.']
    if ext in ('.jpg','.jpeg','.png','.bmp','.tif','.tiff','.gif','.webp'):
        with Image.open(io.BytesIO(data)) as im:
            for k in range(getattr(im,'n_frames',1)):
                im.seek(k);t,detail=ocr_image(im.copy());sections.append({'page':k+1,'method':'image_ocr','text':t,'ocr':detail});ocr_count+=1
        return sections,ocr_count,issues
    if ext in ('.zip','.rar'):
        if depth>12:raise ValueError('Arhiva imbricata peste 12 niveluri; necesita examinare separata')
        if ext=='.zip':z=zipfile.ZipFile(io.BytesIO(data));members=[(x.filename,x.file_size,x.is_dir()) for x in z.infolist()];read=z.read
        else:
            import rarfile
            z=rarfile.RarFile(io.BytesIO(data));members=[(x.filename,x.file_size,x.isdir()) for x in z.infolist()];read=z.read
        for name,size,isdir in members:
            if isdir:continue
            item={'part':name,'size':size,'method':'archive_member'}
            try:
                b=read(name);item['sha256']=hashlib.sha256(b).hexdigest();ss,oc,ii=extract_bytes(b,Path(name).suffix.lower(),depth+1);item['sections']=ss;item['issues']=ii;ocr_count+=oc
                if ii:issues.extend([name+': '+x for x in ii])
            except Exception as e:item['error']=f'{type(e).__name__}: {e}';issues.append(name+': '+item['error'])
            sections.append(item)
        return sections,ocr_count,issues
    if ext=='.rtf':
        from striprtf.striprtf import rtf_to_text
        return [{'method':'rtf','text':rtf_to_text(decode(data))}],0,[]
    if ext in ('.txt','.csv','.tsv','.json','.jsonl','.log','.md','.xml','.py','.html','.htm'):
        t=decode(data)
        return [{'method':'source_text','text':t}],0,[]
    return [{'method':'binary_metadata','size':len(data),'signature_hex':data[:32].hex()}],0,['Format binar fara extractor de continut: '+ext]

def flatten(sections):
    parts=[]
    for s in sections:
        label=s.get('part',f"Pagina {s.get('page','')}")
        parts.append('\n=== '+str(label)+' ['+s.get('method','')+'] ===\n')
        if s.get('text'):parts.append(s['text'])
        if s.get('ocr_text'):parts.append('\n[TEXT OCR]\n'+s['ocr_text'])
        if s.get('sections'):parts.append(flatten(s['sections']))
        if s.get('child'):parts.append(flatten(s['child'][0]))
        if s.get('error'):parts.append('\n[EROARE] '+s['error'])
    return '\n'.join(parts)

def extract_job(item):
    sha,p,ext=item;folder=BASE/'texte'/sha[:2];folder.mkdir(exist_ok=True,parents=True)
    try:
        data=Path(p).read_bytes()
        if hashlib.sha256(data).hexdigest()!=sha:raise ValueError('Sursa s-a modificat dupa inventariere')
        sections,oc,issues=extract_bytes(data,ext);text=flatten(sections)
        jp=folder/(sha+'.json.gz');tp=folder/(sha+'.txt')
        payload={'sha256':sha,'representative_source':p,'extension':ext,'sections':sections,'issues':issues,'ocr_notice':'Text recunoscut automat; poate contine erori, mai ales la scris de mana sau scanuri slabe.'}
        with gzip.open(jp,'wt',encoding='utf-8') as f:json.dump(payload,f,ensure_ascii=False,default=lambda o:o.tolist() if hasattr(o,'tolist') else str(o))
        tp.write_text(text,encoding='utf-8')
        status='partial' if issues else ('ocr' if oc else 'extracted')
        return (sha,ext,status,len(sections),oc,str(tp.relative_to(BASE)),str(jp.relative_to(BASE)),len(text),'\n'.join(issues),datetime.now(timezone.utc).isoformat()),text
    except Exception as e:
        return (sha,ext,'error',0,0,None,None,0,f'{type(e).__name__}: {e}',datetime.now(timezone.utc).isoformat()),''

def extract_remote(item):
    # One persistent independent interpreter per thread. This isolates PDF/OCR
    # libraries without Windows multiprocessing semaphore dependencies.
    for attempt in range(2):
        proc=getattr(LOCAL,'proc',None)
        if proc is None or proc.poll() is not None:
            log=open(BASE/f'worker-{threading.get_ident()}.log','a',encoding='utf-8')
            proc=subprocess.Popen([sys.executable,'-X','utf8','-u',str(Path(__file__).resolve()),'--worker'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=log,text=True,encoding='utf-8',creationflags=subprocess.CREATE_NO_WINDOW)
            LOCAL.proc=proc;CHILDREN.append(proc)
        try:
            proc.stdin.write(json.dumps(item,ensure_ascii=False)+'\n');proc.stdin.flush()
            line=proc.stdout.readline()
            if not line:raise RuntimeError('Worker inchis: '+str(proc.poll()))
            return json.loads(line)
        except Exception:
            proc.kill();LOCAL.proc=None
            if attempt:
                sha,p,ext=item
                return (sha,ext,'error',0,0,None,None,0,'Worker indisponibil dupa doua incercari',datetime.now(timezone.utc).isoformat()),''

def shutdown_workers():
    for p in CHILDREN:
        try:p.stdin.close();p.wait(timeout=5)
        except Exception:
            try:p.kill()
            except Exception:pass

atexit.register(shutdown_workers)

def export(c):
    c.row_factory=sqlite3.Row
    rows=[dict(r) for r in c.execute('''select f.*,d.status extraction_status,d.pages,d.ocr_pages,d.text_path,d.json_path,d.chars,d.error extraction_error from files f left join documents d using(sha256) order by f.person,f.path''')]
    with (BASE/'inventar_complet.jsonl').open('w',encoding='utf-8') as f:
        for r in rows:f.write(json.dumps(r,ensure_ascii=False)+'\n')
    people={}
    for r in rows:people.setdefault(r['person'],[]).append(r)
    (BASE/'persoane').mkdir(exist_ok=True)
    for person,fs in people.items():
        name=re.sub(r'[<>:"/\\|?*]','_',person)
        with (BASE/'persoane'/(name+'.txt')).open('w',encoding='utf-8') as f:
            f.write(person+'\n'+'='*len(person)+'\n\n')
            for r in fs:
                f.write(r['path']+'\nStare: '+str(r['extraction_status'] or r['status'])+'\nText: '+str(r['text_path'])+'\n')
                if r['extraction_error'] or r['error']:f.write('Observatii: '+str(r['extraction_error'] or r['error'])+'\n')
                f.write('\n')
    status=Counter(r['extraction_status'] or r['status'] for r in rows)
    summary={'source':str(ROOT),'files':len(rows),'people_folders':len(people),'unique_hashes':len({r['sha256'] for r in rows if r['sha256']}),'status_by_file':dict(status),'timestamp':datetime.now(timezone.utc).isoformat()}
    (BASE/'sumar.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    table=[]
    for r in rows:
        link=html.escape(r['text_path'].replace('\\','/')) if r['text_path'] else ''
        table.append('<tr><td>'+html.escape(r['person'])+'</td><td><a href="'+html.escape(Path(r['path']).as_uri())+'">'+html.escape(Path(r['path']).name)+'</a></td><td>'+html.escape(str(r['extraction_status'] or r['status']))+'</td><td>'+('<a href="'+link+'">Text integral</a>' if link else '')+'</td><td>'+html.escape(str(r['extraction_error'] or r['error'] or ''))+'</td></tr>')
    report='''<!doctype html><meta charset="utf-8"><title>Inventar persoane</title><style>body{font:15px system-ui;margin:32px;color:#17222c}input{padding:12px;width:70%;font:inherit}table{border-collapse:collapse;width:100%;margin-top:24px}th,td{text-align:left;padding:10px;border-bottom:1px solid #ddd;vertical-align:top}th{position:sticky;top:0;background:#edf2f5}td:nth-child(2){max-width:650px;overflow-wrap:anywhere}td:last-child{max-width:400px}a{color:#175782}</style><h1>Inventar documente persoane</h1><p>''' + html.escape(json.dumps(summary,ensure_ascii=False)) + '''</p><p>Textul OCR este automat și poate conține erori. „partial” sau „error” indică extrageri care necesită verificare. Originalele nu au fost modificate.</p><input id="q" placeholder="Filtrează persoana, fișierul sau starea"><table><thead><tr><th>Dosar persoană</th><th>Original</th><th>Stare</th><th>Extragere</th><th>Observații</th></tr></thead><tbody>'''+''.join(table)+'''</tbody></table><script>const rows=[...document.querySelectorAll('tbody tr')];q.oninput=()=>{const s=q.value.toLocaleLowerCase();for(const r of rows)r.hidden=!r.textContent.toLocaleLowerCase().includes(s)}</script>'''
    (BASE/'Inventar.html').write_text(report,encoding='utf-8')
    c.row_factory=None
    return summary

def main():
    c=connect();paths=INDEX.read_text(encoding='utf-8-sig').splitlines()
    for p in paths:
        if not p:continue
        person,category=identify(p)
        c.execute('insert or ignore into files(path,person,category,ext,status) values(?,?,?,?,?)',(p,person,category,Path(p).suffix.lower(),'pending_hash'))
    c.commit();progress(c,'hashing_and_extracting')
    pending=[r[0] for r in c.execute("select path from files where status='pending_hash'")]
    existing={r[0] for r in c.execute('select sha256 from documents')}
    jobs=list(c.execute("select f.sha256,min(f.path),f.ext from files f left join documents d using(sha256) where f.sha256 is not null and d.sha256 is null group by f.sha256"))
    jobs.sort(key=lambda r:(r[2] in ('.pdf','.jpg','.jpeg','.png','.tif','.bmp','.zip','.rar'),r[1]))
    last_progress=last_export=time.time();hashed=done=0
    with ThreadPoolExecutor(max_workers=12) as hp, ThreadPoolExecutor(max_workers=8) as ep:
        hf={hp.submit(fingerprint,p):p for p in pending}
        ef={ep.submit(extract_remote,j):j for j in jobs}
        scheduled=existing|{j[0] for j in jobs}
        while hf or ef:
            ready,_=wait(set(hf)|set(ef),timeout=15,return_when=FIRST_COMPLETED)
            for f in ready:
                if f in hf:
                    p,size,mtime,sha,error=f.result();hf.pop(f);hashed+=1
                    c.execute('update files set size=?,mtime=?,sha256=?,status=?,error=? where path=?',(size,mtime,sha,'read_error' if error else 'hashed',error,p))
                    if sha and sha not in scheduled:
                        job=(sha,p,Path(p).suffix.lower());ef[ep.submit(extract_remote,job)]=job;scheduled.add(sha)
                else:
                    ef.pop(f);row,text=f.result();done+=1
                    c.execute('insert or replace into documents values(?,?,?,?,?,?,?,?,?,?)',row)
                    c.execute('delete from search where sha256=?',(row[0],));c.execute('insert into search values(?,?)',(row[0],text))
            c.commit()
            if time.time()-last_progress>20:
                progress(c,'hashing_and_extracting',{'hash_pending':len(hf),'extract_pending':len(ef),'hashed_in_run':hashed,'extracted_in_run':done});last_progress=time.time()
            if time.time()-last_export>120:export(c);last_export=time.time()
    export(c);progress(c,'finished')

if __name__=='__main__':
    try:
        if '--worker' in sys.argv:
            for line in sys.stdin:
                item=json.loads(line);result=extract_job(item);print(json.dumps(result,ensure_ascii=False),flush=True)
        else:main()
    except Exception:
        (BASE/'fatal_error.txt').write_text(traceback.format_exc(),encoding='utf-8');raise
