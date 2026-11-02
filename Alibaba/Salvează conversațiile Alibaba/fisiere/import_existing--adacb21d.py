"""Import existing exports without changing the original files."""
from server import Archive, safe, digest, now, HERE
from urllib.parse import urlsplit, parse_qs
import json, shutil, re

def run():
    config=json.loads((HERE/'config.json').read_text(encoding='utf-8-sig'))
    root=__import__('pathlib').Path(config['root'])
    source=__import__('pathlib').Path(r'D:\00. Downloads\Chrome\Alibaba_Archive\Lu Vicky_279900891')
    if source.exists() and not (root/source.name).exists(): shutil.copytree(source,root/source.name)
    archive=Archive(root,worker=False)
    for folder in root.iterdir():
        if not folder.is_dir(): continue
        if (folder/'conversation.json').exists():
            d=json.loads((folder/'conversation.json').read_text(encoding='utf-8-sig'))
            d['folder']=folder.name
            for a in d.get('attachments',[]):
                path=(folder/a.get('localPath','__missing__')).resolve()
                if path.is_relative_to(folder.resolve()) and path.is_file() and path.stat().st_size: a['status']='complete'
            archive.persist(d); archive.docs[str(d['id'])]=d
            continue
        sources=[p for p in folder.glob('*.json') if 'manifest' not in p.name]
        if len(sources)!=1: continue
        s=json.loads(sources[0].read_text(encoding='utf-8-sig'))
        ident=parse_qs(urlsplit(s.get('pageUrl','')).query).get('activeAccountId',[None])[0] or 'legacy-'+digest(folder.name)
        if ident in archive.docs: continue
        messages=[]
        for i,m in enumerate(s.get('messages',[])):
            messages.append({'key':'legacy:'+str(i)+':'+digest(m.get('text','')),'text':m.get('text',''),'time':m.get('time',''),'sender':{'me':'self','other':'partner'}.get(m.get('sender'),'unknown')})
        if not messages: continue
        attachments=[]
        for f in (folder/'files').glob('*'):
            if not f.is_file(): continue
            key='local:'+f.name
            kind='image' if f.suffix.lower() in ('.png','.jpg','.jpeg','.webp','.gif') else 'video' if f.suffix.lower() in ('.mp4','.webm') else 'file'
            attachments.append({'key':key,'messageKey':'','url':'','name':f.name,'kind':kind,'status':'complete','attempts':0,'localPath':'files/'+f.name})
        unresolved=[]
        for m in messages:
            for name in re.findall(r'[^\n]{0,70}?\.(?:pdf|docx?|xlsx?|zip|mp4)\b',m['text'],re.I):
                if not any(a['name'].lower() in name.lower() for a in attachments): unresolved.append({'key':m['key']+':'+name,'messageKey':m['key'],'kind':'file','name':name.strip()})
        d={'id':ident,'contact':s.get('contact') or folder.name,'folder':folder.name,'messages':messages,'attachments':attachments,'unresolved':unresolved,'historyComplete':False,'firstSavedAt':s.get('exportedAt') or now(),'updatedAt':s.get('exportedAt') or now()}
        archive.persist(d);archive.docs[ident]=d
    print(json.dumps({'conversations':len(archive.docs),'messages':sum(len(d['messages']) for d in archive.docs.values()),'files':sum(sum(a['status']=='complete' for a in d['attachments']) for d in archive.docs.values())}))
if __name__=='__main__': run()
