"""Local contact index. User annotations are kept separate from captured data."""
import json, re, sqlite3, threading, time, unicodedata
from pathlib import Path
from datetime import datetime

FIELDS=('alias','category','tag','company','email','phone','country','website','notes')
def normalized(s):return ''.join(c for c in unicodedata.normalize('NFD',str(s).casefold()) if not unicodedata.combining(c))
def message_date(m):
    match=re.search(r'\b(\d{4}-\d{1,2}-\d{1,2})[ T](\d{1,2}:\d{2})',str(m.get('time') or m.get('text','')))
    if not match:return ''
    try:return datetime.strptime(' '.join(match.groups()),'%Y-%m-%d %H:%M').isoformat(timespec='minutes')
    except ValueError:return ''

class Contacts:
    def __init__(self,root):
        self.root=Path(root);self.root.mkdir(parents=True,exist_ok=True)
        self.lock=threading.RLock();self.last_scan=0;self.errors=[];self.signatures={}
        self.db=sqlite3.connect(self.root/'contacte.sqlite3',check_same_thread=False,timeout=20)
        self.db.execute('PRAGMA journal_mode=DELETE')
        self.db.execute('CREATE TABLE IF NOT EXISTS contacts (id TEXT PRIMARY KEY, original TEXT NOT NULL, source TEXT NOT NULL, personal TEXT NOT NULL DEFAULT "{}", signature TEXT NOT NULL, search_text TEXT NOT NULL)')
        self.db.commit()
    def scan(self,force=False):
        with self.lock:
            if not force and time.monotonic()-self.last_scan<15:return
            self.errors=[]
            for path in self.root.glob('*/conversation.json'):
                try:
                    stat=path.stat();sig=str(stat.st_mtime_ns)+':'+str(stat.st_size)
                    if self.signatures.get(str(path))==sig:continue
                    # Stable ID, independent of folder/display-name changes.
                    d=json.loads(path.read_text('utf-8-sig'));ident=str(d['id'])
                    old=self.db.execute('SELECT signature FROM contacts WHERE id=?',(ident,)).fetchone()
                    if old and old[0]==sig:
                        self.signatures[str(path)]=sig;continue
                    messages=d.get('messages',[]);dated=[(message_date(m),m) for m in messages]
                    latest=max(dated,key=lambda x:x[0]) if dated else ('',{})
                    profile=d.get('profile') or {};facts=[];seen=set()
                    # Candidate contact details retain sender and evidence; never silently assign them.
                    for m in messages:
                        if m.get('sender')=='self':continue
                        text=m.get('text','')
                        for kind,pattern in [('email',r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}'),('phone',r'(?<!\w)\+\d[\d ()-]{7,22}\d'),('website',r'https?://[^\s<>]+')]:
                            for match in re.finditer(pattern,text):
                                value=match.group().rstrip('.,;)')
                                if kind=='website' and ('?' in value or 'token' in value.lower()):continue
                                if kind=='phone' and not 8<=len(re.sub(r'\D','',value))<=15:continue
                                if (kind,value) in seen:continue
                                seen.add((kind,value));facts.append({'field':kind,'value':value,'messageKey':m.get('key'),'sender':m.get('sender','unknown'),'excerpt':text[max(0,match.start()-50):match.end()+65]})
                    source={'company':str(profile.get('company',''))[:300],'alibabaCategory':str(profile.get('alibabaCategory',''))[:300],'country':str(profile.get('country',''))[:150],'profileSource':str(profile.get('source',''))[:300],'facts':facts[:100],'lastMessageAt':latest[0],'preview':latest[1].get('text','')[:160],'messageCount':len(messages),'folder':path.parent.name,'messages':[{'key':m.get('key'),'text':m.get('text',''),'time':m.get('time','')} for m in messages]}
                    search_text=normalized(d.get('contact','')+' '+json.dumps(source,ensure_ascii=False))
                    self.db.execute('INSERT INTO contacts(id,original,source,signature,search_text) VALUES(?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET original=excluded.original,source=excluded.source,[CREDENTIAL_REDACTED]',(ident,d.get('contact',''),json.dumps(source,ensure_ascii=False),sig,search_text))
                    self.signatures[str(path)]=sig
                except (OSError,ValueError,KeyError) as e:self.errors.append(path.parent.name+': '+type(e).__name__)
            self.db.commit();self.last_scan=time.monotonic()
    def get(self,ident):
        with self.lock:
            row=self.db.execute('SELECT original,source,personal FROM contacts WHERE id=?',(ident,)).fetchone()
            if not row:raise KeyError(ident)
            source=json.loads(row[1]);source.pop('messages',None)
            return {'id':ident,'original':row[0],'source':source,'personal':json.loads(row[2])}
    def all(self):
        self.scan()
        with self.lock:return [self.get(row[0]) for row in self.db.execute('SELECT id FROM contacts').fetchall()]
    def update(self,ident,values):
        if not isinstance(values,dict) or any(k not in FIELDS for k in values):raise ValueError('Câmp necunoscut')
        if any(not isinstance(v,str) or len(v)>(5000 if k=='notes' else 300) for k,v in values.items()):raise ValueError('Valoare prea lungă sau invalidă')
        with self.lock:
            contact=self.get(ident);personal=contact['personal'];personal.update({k:v.strip() for k,v in values.items()})
            with self.db:self.db.execute('UPDATE contacts SET personal=? WHERE id=?',(json.dumps(personal,ensure_ascii=False),ident))
            return self.get(ident)
    def search(self,query):
        self.scan();q=normalized(query.strip())
        if not q:return []
        result=[]
        with self.lock:
            for ident,original,source_json,personal in self.db.execute('SELECT id,original,source,personal FROM contacts').fetchall():
                source=json.loads(source_json)
                matches=[m for m in source.get('messages',[]) if q in normalized(m['text'])]
                metadata=original+' '+personal+' '+source.get('company','')+' '+source.get('alibabaCategory','')
                if matches or q in normalized(metadata):
                    first=matches[0] if matches else None
                    result.append({'id':ident,'count':len(matches),'messageKey':first['key'] if first else None,'snippet':first['text'][:240] if first else ''})
        return result
