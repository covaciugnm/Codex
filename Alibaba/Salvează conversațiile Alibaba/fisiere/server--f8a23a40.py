"""Local Alibaba archive. No Alibaba login cookies are read or stored."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'packages'))
import json, re, os, secrets, hashlib, threading, queue, html, mimetypes
from datetime import datetime, timezone
from urllib.parse import urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler
from flask import Flask, request, jsonify, abort, send_file, Response

EXTENSION = 'chrome-extension://acpjchllabdlkfhmfllaggiebjkmbadf'
PORT = 8765
def now(): return datetime.now(timezone.utc).isoformat()
def digest(value): return hashlib.sha256(str(value).encode()).hexdigest()[:20]
def safe(value):
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', str(value)).strip().rstrip('. ')[:85]
    if re.match(r'^(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)', value, re.I): value = '_' + value
    return value or 'Partener'
def allowed(url):
    try:
        p = urlsplit(url)
        return p.scheme == 'https' and not p.username and not p.password and p.port in (None,443) and any(p.hostname == d or (p.hostname or '').endswith('.'+d) for d in ('alibaba.com','alicdn.com','alibabacloud.com'))
    except ValueError: return False
class SafeRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not allowed(newurl): raise ValueError('Redirecționare în afara domeniilor Alibaba')
        return super().redirect_request(req, fp, code, msg, headers, newurl)

class Archive:
    def __init__(self, root, worker=True):
        self.root = Path(root).resolve(); self.root.mkdir(parents=True, exist_ok=True)
        self.lock = threading.RLock(); self.jobs = queue.Queue(); self.queued = set(); self.docs = {}
        for path in self.root.glob('*/conversation.json'):
            d = json.loads(path.read_text(encoding='utf-8-sig'))
            d['folder'] = path.parent.name
            self.reconcile_legacy(d)
            for a in d.get('attachments', []):
                if a.get('status') == 'downloading': a['status'] = 'pending'
            self.docs[str(d['id'])] = d
            self.persist(d)
        if worker:
            threading.Thread(target=self.work, daemon=True).start()
            for d in self.docs.values(): self.schedule(d)

    def folder(self, d):
        folder = (self.root / d['folder']).resolve()
        if folder.parent != self.root: raise ValueError('Folder invalid')
        return folder

    def reconcile_legacy(self, d):
        groups = {}
        for m in d['messages']:
            text = re.sub(r'\s+',' ',m.get('text','')).strip()
            groups.setdefault(text,[]).append(m)
            if not m.get('time'):
                match = re.search(r'\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{2}',text)
                if match: m['time']=match[0]
        removed=set(); aliases={}
        for text,items in groups.items():
            old=[m for m in items if m['key'].startswith('legacy:')]
            new=[m for m in items if not m['key'].startswith('legacy:')]
            # Merge only unambiguous one-to-one matches between export versions.
            if text and len(old)==1 and len(new)==1:
                aliases[old[0]['key']]=new[0]['key'];removed.add(id(new[0]))
                old[0].update(new[0])
        d['messages']=[m for m in d['messages'] if id(m) not in removed]
        for a in d.get('attachments',[])+d.get('unresolved',[]):
            if a.get('messageKey') in aliases: a['messageKey']=aliases[a['messageKey']]

    def persist(self, d):
        folder = self.folder(d); folder.mkdir(parents=True, exist_ok=True)
        status = 'Începutul istoricului observat' if d.get('historyComplete') else 'Istoric parțial — numai mesajele încărcate'
        report = '\n'.join(f"{a.get('name','Fișier')}: {a.get('status','pending')} {a.get('error','')}" for a in d['attachments'])
        report += '\n' + '\n'.join(a.get('name','Fișier') + ': fără link direct' for a in d.get('unresolved',[]))
        txt = d['contact'] + '\n' + status + '\n\n' + '\n\n'.join(m.get('text','') for m in d['messages']) + '\n\nATAȘAMENTE\n' + report
        esc = html.escape
        body = '<!doctype html><meta charset="utf-8"><title>'+esc(d['contact'])+'</title><style>body{font:16px system-ui;max-width:900px;margin:40px auto}article{white-space:pre-wrap;border-bottom:1px solid #ddd;padding:15px}img,video{max-width:100%;max-height:400px}</style><h1>'+esc(d['contact'])+'</h1><p>'+esc(status)+'</p>'
        for m in d['messages']:
            body += '<article>'+esc(m.get('text',''))
            for a in d['attachments']:
                if a.get('messageKey') != m['key'] or a.get('status') != 'complete': continue
                link = esc(a['localPath'], quote=True)
                body += '<p><a href="'+link+'">'+esc(a.get('name','Fișier'))+'</a></p>'
                if a.get('kind') == 'image': body += '<img loading="lazy" src="'+link+'">'
                if a.get('kind') == 'video': body += '<video controls preload="none" src="'+link+'"></video>'
            body += '</article>'
        body += '<h2>Atașamente</h2><pre>'+esc(report)+'</pre>'
        for name, text in [('conversation.txt',txt),('conversation.html',body),('conversation.json',json.dumps(d,ensure_ascii=False,indent=2))]:
            tmp = folder / (name+'.tmp'); tmp.write_text(text, encoding='utf-8'); os.replace(tmp,folder/name)

    def capture(self, s):
        if not isinstance(s,dict) or not s.get('id') or not isinstance(s.get('messages'),list) or not s['messages']: raise ValueError('Conversație fără ID sau mesaje')
        with self.lock:
            ident = str(s['id'])
            d = self.docs.get(ident) or {'id':ident,'contact':str(s.get('contact') or 'Partener'),'folder':safe(s.get('contact') or 'Partener')+' ['+safe(ident)[:35]+'-'+digest(ident)[:8]+']','messages':[],'attachments':[],'unresolved':[],'firstSavedAt':now(),'historyComplete':False}
            messages = {m['key']:m for m in d['messages']}
            for m in s['messages']:
                if not isinstance(m,dict) or not isinstance(m.get('key'),str): raise ValueError('Mesaj fără cheie')
                messages[m['key']] = {k:m[k] for k in ('key','text','time','sender') if k in m}
            d['messages'] = list(messages.values())
            attachments = {a['key']:a for a in d['attachments']}
            for a in s.get('attachments',[]):
                if not isinstance(a.get('key'),str): raise ValueError('Atașament fără cheie')
                old = attachments.get(a['key'])
                if old:
                    old['url'] = a.get('url',''); old['name'] = a.get('name') or old['name']
                else:
                    name = safe(a.get('name') or 'fisier')
                    if not re.search(r'\.[a-zA-Z0-9]{2,5}$',name) or name.lower().endswith(('.htm','.html')): name += {'image':'.jpg','video':'.mp4'}.get(a.get('kind'),'.bin')
                    attachments[a['key']] = {**{k:a.get(k,'') for k in ('key','url','name','kind','messageKey')},'status':'pending','attempts':0,'localPath':'files/'+digest(a['key'])+'_'+name}
            d['attachments'] = list(attachments.values())
            missing = {a['key']:a for a in d.get('unresolved',[])}
            for a in s.get('unresolved',[]): missing[a['key']] = a
            d['unresolved'] = [a for a in missing.values() if not any(f.get('messageKey')==a.get('messageKey') and f.get('kind')==a.get('kind') for f in d['attachments'])]
            d['contact'] = str(s.get('contact') or d['contact']); d['updatedAt'] = now()
            if isinstance(s.get('profile'),dict):
                profile=d.setdefault('profile',{})
                for field in ('company','alibabaCategory','country','source'):
                    value=s['profile'].get(field)
                    if isinstance(value,str) and value.strip():profile[field]=value.strip()[:300]
            d['historyComplete'] = d['historyComplete'] or bool(s.get('historyComplete'))
            self.reconcile_legacy(d)
            self.persist(d); self.docs[ident] = d; self.schedule(d)
            return dict(messages=len(d['messages']),files=len(d['attachments']),unresolved=len(d['unresolved']),folder=str(self.folder(d)))

    def schedule(self, d):
        for a in d['attachments']:
            job = (d['id'],a['key'])
            if a['status'] == 'pending' and job not in self.queued:
                self.queued.add(job); self.jobs.put(job)

    def download(self, url, dest):
        if not allowed(url): raise ValueError('Adresă de descărcare neacceptată')
        tmp = dest.with_suffix(dest.suffix+'.part'); dest.parent.mkdir(parents=True,exist_ok=True)
        try:
            req = Request(url,headers={'User-Agent':'Mozilla/5.0','Referer':'https://message.alibaba.com/'})
            with build_opener(SafeRedirect()).open(req,timeout=40) as response, tmp.open('wb') as output:
                if 'text/html' in response.headers.get('Content-Type',''): raise ValueError('Serverul a returnat o pagină de autentificare, nu fișierul')
                total = 0
                while chunk := response.read(1024*1024):
                    total += len(chunk)
                    if total > 2*1024**3: raise ValueError('Fișier peste limita de 2 GB')
                    output.write(chunk)
                expected = response.headers.get('Content-Length')
                if not total or (expected and total != int(expected)): raise ValueError('Descărcare incompletă')
            os.replace(tmp,dest)
        finally:
            tmp.unlink(missing_ok=True)

    def work(self):
        while True:
            ident,key = self.jobs.get()
            try:
                with self.lock:
                    d = self.docs[ident]; a = next(a for a in d['attachments'] if a['key']==key)
                    a['status']='downloading'; a['attempts']+=1; url=a['url']; dest=self.folder(d)/a['localPath']; self.persist(d)
                try:
                    self.download(url,dest); status='complete'; error=''
                except Exception as e:
                    status='failed'; error=type(e).__name__ + ': descărcare nereușită; reîncearcă după redeschiderea conversației.'
                with self.lock:
                    a['status']=status; a['error']=error; self.persist(d)
            except Exception:
                import logging; logging.exception('Eroare la salvarea unui atașament')
            finally:
                with self.lock: self.queued.discard((ident,key))
                self.jobs.task_done()

    def retry(self):
        with self.lock:
            for d in self.docs.values():
                for a in d['attachments']:
                    if a['status']=='failed': a['status']='pending'
                self.persist(d); self.schedule(d)

    def status(self):
        with self.lock:
            return {'root':str(self.root),'conversations':[{'id':d['id'],'contact':d['contact'],'messages':len(d['messages']),'complete':sum(a['status']=='complete' for a in d['attachments']),'failed':sum(a['status']=='failed' for a in d['attachments']),'pending':sum(a['status'] in ('pending','downloading') for a in d['attachments']),'unresolved':len(d['unresolved']),'historyComplete':d['historyComplete'],'updatedAt':d.get('updatedAt'),'preview':d['messages'][-1].get('text','')[:140]} for d in self.docs.values()]}

def create_app(root, token, worker=True):
    app=Flask(__name__); app.config['MAX_CONTENT_LENGTH']=32*1024*1024
    archive=Archive(root,worker); app.archive=archive
    origins={EXTENSION,f'http://127.0.0.1:{PORT}'}
    @app.before_request
    def auth():
        if request.host != f'127.0.0.1:{PORT}': abort(403)
        origin=request.headers.get('Origin')
        if origin and origin not in origins: abort(403)
        if request.method=='OPTIONS': return '',204
        if request.path.startswith('/api/') or request.path.startswith('/files/'):
            provided=request.headers.get('X-Archive-Key','')
            if request.path.startswith('/files/'): provided=request.args.get('key','')
            if not secrets.compare_digest(provided,token): abort(401)
    @app.after_request
    def headers(response):
        origin=request.headers.get('Origin')
        if origin in origins:
            response.headers['Access-Control-Allow-Origin']=origin
            response.headers['Vary']='Origin'
            response.headers['Access-Control-Allow-Headers']='Content-Type, X-Archive-Key'
            response.headers['Access-Control-Allow-Methods']='GET, POST, OPTIONS'
        response.headers['X-Content-Type-Options']='nosniff'
        response.headers['Referrer-Policy']='no-referrer'
        response.headers['Cache-Control']='no-store'
        response.headers['Content-Security-Policy']="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self'; media-src 'self'; frame-ancestors 'none'; object-src 'none'"
        return response
    @app.get('/')
    def home(): return Response((HERE/'viewer.html').read_text(encoding='utf-8').replace('__TOKEN__',token),mimetype='text/html')
    @app.get('/api/status')
    def status(): return jsonify(archive.status())
    @app.get('/api/conversation/<path:ident>')
    def conversation(ident):
        with archive.lock:
            d=archive.docs.get(ident)
            if not d: abort(404)
            # Do not expose signed download links to the viewer.
            result=json.loads(json.dumps(d))
            for a in result['attachments']:
                a.pop('url',None); a['fileKey']=digest(a['key'])
            return jsonify(result)
    @app.post('/api/capture')
    def capture():
        try: return jsonify(archive.capture(request.get_json()))
        except (ValueError,KeyError,TypeError) as e: return jsonify(error=str(e)),400
    @app.post('/api/retry')
    def retry(): archive.retry(); return jsonify(retried=True)
    @app.get('/files/<ident>/<filekey>')
    def file(ident,filekey):
        with archive.lock:
            d=archive.docs.get(ident)
            if not d: abort(404)
            a=next((a for a in d['attachments'] if digest(a['key'])==filekey and a['status']=='complete'),None)
            if not a: abort(404)
            path=(archive.folder(d)/a['localPath']).resolve()
            if not path.is_relative_to(archive.folder(d)): abort(403)
            inline=a['kind'] in ('image','video') and path.suffix.lower() in ('.jpg','.jpeg','.png','.gif','.webp','.mp4','.webm')
            return send_file(path,as_attachment=not inline,download_name=safe(a.get('name') or path.name),conditional=True)
    return app

if __name__=='__main__':
    from waitress import serve
    config=json.loads((HERE/'config.json').read_text(encoding='utf-8-sig'))
    app=create_app(config['root'],config['token'])
    serve(app,host='127.0.0.1',port=PORT,threads=4,max_request_body_size=32*1024*1024)
