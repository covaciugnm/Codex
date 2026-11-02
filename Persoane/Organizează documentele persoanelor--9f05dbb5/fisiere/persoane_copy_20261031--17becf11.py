import sys,os,json,re,hashlib,datetime,time,collections,concurrent.futures,unicodedata
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import persoane_scan_20261031 as s
L=s.LOCAL;D=s.DEST;A=s.AUDIT
def records(path):
    if not path.exists():return []
    out=[]
    for line in path.read_text('utf-8').splitlines():
        try:out.append(json.loads(line))
        except ValueError:pass
    return out
def digest(p):
    with open(p,'rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def safe(st):return re.sub(r'[<>:"/\\|?*\x00-\x1f]',' ',st).strip(' .')
def closematch(text,people,partial=False):
    n=' '+s.norm(text)+' '; found=[]
    for p in people:
        ts=p['tokens']; surname=ts[0]
        if p['cnp'] and re.search(r'(?<!\d)'+p['cnp']+r'(?!\d)',n):found.append(p['name']);continue
        for m in re.finditer(r'\b'+re.escape(surname)+r'\b',n):
            span=len(' '.join(ts))+32
            window=n[max(0,m.start()-span):m.end()+span]
            toks=set(window.split())
            if set(ts)<=toks:found.append(p['name']);break
            if partial and len(ts)>2 and any(t in toks for t in ts[1:]):
                possible=[q for q in people if q['tokens'][0]==surname and any(t in toks for t in q['tokens'][1:])]
                if len(possible)==1:found.append(p['name']);break
    return sorted(set(found))
def classify(r,people):
    pathpeople=closematch(r['relative'],people,True)
    textpeople=[]
    if r.get('text_people'):
        txt=L/'text'/(r['sha256']+'.txt')
        if txt.exists():textpeople=closematch(txt.read_text('utf-8'),people)
    names=sorted(set(pathpeople+textpeople))
    c=r.get('cnps',[])
    if not (names or c or r.get('personal_path')):return None
    byname={p['name']:p for p in people}
    if len(names)==1 and len(c)<=1:
        p=byname[names[0]]
        if c and p['cnp'] and c[0]!=p['cnp']:
            folder=D/'00. Documente comune';prefix='CNP de completat - DOCUMENT COMUN';reason='Persoana asociata si CNP diferit; titulari de verificat'
        else:
            folder=D/p['folder'];prefix=(p['cnp'] or 'CNP de completat')+' - '+p['name'];reason='Nume/CNP identificat in cale sau continut'
    elif len(names)>1 or len(c)>1:
        folder=D/'00. Documente comune';prefix='CNP de completat - DOCUMENT COMUN';reason='Mai multe persoane asociate; document pastrat integral'
    else:
        folder=D/'99. De verificat';prefix=(c[0] if len(c)==1 else 'CNP de completat')+' - TITULAR NEIDENTIFICAT';reason='Indicii de document personal; titular neconfirmat'
    filename=Path(r['source']).stem
    dates=re.findall(r'(?<!\d)(?:[0-3]?\d[.\-_/][01]?\d[.\-_/](?:19|20)\d{2}|(?:19|20)\d{2}[.\-_/][01]?\d[.\-_/][0-3]?\d)(?!\d)',filename)
    dt=datetime.datetime.fromtimestamp(r['mtime']).strftime('%Y.%m.%d')
    datelabel='' if dates else ' - modificat '+dt
    stem=safe(prefix+' - '+filename)
    tail=datelabel+' - '+r['sha256'][:10]+r['ext']
    stem=stem[:max(35,235-len(str(folder))-len(tail))].rstrip(' .')
    return {'target':str(folder/(stem+tail)),'persons':names,'cnps':c,'classification':reason,'date_basis':'Data din denumirea sursei, pastrata ca atare' if dates else 'Data modificarii sursei; data documentului necunoscuta','source_dates':dates}
def copyjob(item):
    r,plan=item;p=Path(plan['target']);result={**r,**plan};result.pop('blank_pages',None)
    try:
        p.parent.mkdir(parents=True,exist_ok=True)
        if p.parent.parent==D and p.parent.name not in {'00. Documente comune','99. De verificat'}:
            archive=D/'00. Arhiva'/p.parent.name
            if not archive.exists():
                for sub in ['01. Acte anterioare si variante','02. Dubluri identice','03. Fise istorice']:(archive/sub).mkdir(parents=True,exist_ok=True)
        if p.exists():
            if digest(p)==r['sha256']:result['status']='DEJA_EXISTENT';return result
            p=p.with_name(p.stem+' - '+r['sha256'][10:18]+p.suffix);result['target']=str(p)
        with open(r['source'],'rb') as src,open(p,'xb') as dst:
            h=hashlib.sha256()
            for b in iter(lambda:src.read(1024*1024),b''):dst.write(b);h.update(b)
        if h.hexdigest()!=r['sha256']:raise RuntimeError('Sursa schimbata dupa inventariere; copie necesita verificare')
        if digest(p)!=r['sha256']:raise RuntimeError('Verificare SHA256 copie esuata')
        os.utime(p,(r['mtime'],r['mtime']))
        result['status']='COPIAT_VERIFICAT_SHA256'
    except Exception as e:result['status']='EROARE_COPIERE';result['copy_error']=str(e)
    return result
def main():
    s.init();people=s.PEOPLE
    extra=L/'extra_people.json'
    if extra.exists():people+=json.loads(extra.read_text('utf-8'))
    baseline=L/'baseline.json'
    if baseline.exists():existing=json.loads(baseline.read_text('utf-8'))
    else:
        prev=json.loads((D/'00. Arhiva/00. Administrativ/Organizare 2026-10-01/final_docs.json').read_text('utf-8'))
        existing=[{'sha256':x['sha'],'path':str(D/x['target'])} for x in prev if x.get('sha') and x.get('target')]
        print('Folosesc indexul anterior; copiile sunt create exclusiv fara suprascriere.',flush=True)
    known={x['sha256']:x['path'] for x in existing}
    ledger=L/'copies.jsonl';old=records(ledger);seen={x['source'] for x in old};previous={x['source']:x for x in old}
    for r in old:
        if r.get('status') in {'COPIAT_VERIFICAT_SHA256','DEJA_EXISTENT'}:known[r['sha256']]=r['target']
    rows=records(L/'scan.jsonl');ocr={r.get('sha256'):r for r in records(L/'ocr.jsonl')};jobs=[];duplicates=[];rejected=0;pending={}
    for r in rows:
        if r.get('sha256') in ocr:
            r.update({k:v for k,v in ocr[r['sha256']].items() if k not in {'source','sha256'}})
        if 'error' in r or not r.get('sha256'):continue
        before=previous.get(r['source'])
        if before and (not r.get('ocr_complete') or before.get('ocr_complete')):continue
        plan=classify(r,people)
        if not plan:rejected+=1;continue
        sha=r['sha256']
        if before:
            was_review='99. De verificat' in Path(before.get('target','')).parts
            now_identified=bool(plan['persons']) and '99. De verificat' not in Path(plan['target']).parts
            if was_review and now_identified:
                if sha in pending:
                    duplicates.append({**r,**plan,'target':pending[sha],'status':'DUBLURA_SURSA'})
                else:jobs.append((r,plan));pending[sha]=plan['target']
                continue
            duplicates.append({**r,**plan,'target':before['target'],'status':'INDEX_ACTUALIZAT_DUPA_OCR'});continue
        if sha in known:
            duplicates.append({**r,**plan,'target':known[sha],'status':'DEJA_EXISTENT_SHA256'})
        elif sha in pending:
            duplicates.append({**r,**plan,'target':pending[sha],'status':'DUBLURA_SURSA'})
        else:jobs.append((r,plan));pending[sha]=plan['target']
    print(json.dumps({'new_unique':len(jobs),'duplicates':len(duplicates),'not_relevant':rejected}),flush=True)
    with ledger.open('a',encoding='utf-8') as out:
        for r in duplicates:out.write(json.dumps(r,ensure_ascii=False)+'\n')
        out.flush()
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            for i,r in enumerate(pool.map(copyjob,jobs)):
                out.write(json.dumps(r,ensure_ascii=False)+'\n');out.flush()
                if i%25==0:print(json.dumps({'copied_processed':i+1,'total':len(jobs)}),flush=True)
    print('COPY_BATCH_COMPLETE',flush=True)
if __name__=='__main__':main()
