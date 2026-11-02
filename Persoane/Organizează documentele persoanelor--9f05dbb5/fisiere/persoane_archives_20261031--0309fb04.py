import sys,json,hashlib,re,zipfile,datetime,collections
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import persoane_scan_20261031 as s
import persoane_copy_20261031 as cp
def main():
    s.init();seen={r['source'] for r in cp.records(s.LOCAL/'archives.jsonl')}
    with (s.LOCAL/'archives.jsonl').open('a',encoding='utf-8') as log,(s.LOCAL/'scan.jsonl').open('a',encoding='utf-8') as scanout:
        for rel in s.INV.read_text('utf-8-sig').splitlines():
            p=s.ROOT/rel;ext=p.suffix.lower()
            if ext not in {'.zip','.rar','.7z'} or str(p) in seen:continue
            r={'source':str(p),'relative':rel,'ext':ext,'archive_content_unread':True}
            try:
                names=[];r['path_people']=s.match(rel)
                if ext=='.zip':
                    with zipfile.ZipFile(p) as z:names=z.namelist()
                elif ext=='.rar':
                    import rarfile
                    with rarfile.RarFile(p) as z:names=z.namelist()
                else:
                    import py7zr
                    with py7zr.SevenZipFile(p) as z:names=z.getnames()
                docs=[n for n in names if Path(n).suffix.strip().lower() in s.DOCEXT|s.IMGEXT]
                listing='\n'.join(docs);r['archive_entries']=len(names);r['text_people']=s.match(listing)
                r['personal_path']=bool(re.search(r'\b(CV|BULETIN|PASAPORT|IDENTITATE|DIPLOME|DOSARE PERSONALE|ACTE PERSONALE)\b',s.norm(rel+' '+listing)))
                r['archive_listing_read']=True
                if r['path_people'] or r['text_people'] or r['personal_path']:
                    st=p.stat();r.update(size=st.st_size,mtime=st.st_mtime,sha256=cp.digest(p),cnps=[],text_chars=len(listing),pages=0,blank_pages=[],errors=['Arhiva copiata integral; documentele din interior nu au fost extrase sau citite'])
                    (s.LOCAL/'text'/(r['sha256']+'.txt')).write_text(listing,'utf-8')
                    scanout.write(json.dumps(r,ensure_ascii=False)+'\n');scanout.flush()
            except Exception as e:r['archive_error']=str(e)
            log.write(json.dumps(r,ensure_ascii=False)+'\n');log.flush()
    (s.LOCAL/'archives_complete.txt').write_text(datetime.datetime.now().isoformat(),'utf-8')
if __name__=='__main__':main()
