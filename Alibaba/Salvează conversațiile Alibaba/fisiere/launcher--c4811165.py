"""Persistent local dashboard and fixed-command archive server launcher."""
from server import HERE
import json, os, sys, secrets, socket, subprocess, threading, time
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from flask import Flask, Response, request, jsonify, abort

PORT=8766
WORKER='http://127.0.0.1:8765'

class Controller:
    def __init__(self, token):
        self.token=token; self.lock=threading.Lock()
    def health(self):
        try:
            with urlopen(Request(WORKER+'/api/status',headers={'X-Archive-Key':self.token}),timeout=2) as r:
                data=json.load(r)
                return isinstance(data.get('conversations'),list)
        except Exception: return False
    def spawn(self):
        with (HERE/'server-output.log').open('ab') as out, (HERE/'server-error.log').open('ab') as err:
            child=subprocess.Popen([sys.executable,str(HERE/'server.py')],cwd=HERE,stdin=subprocess.DEVNULL,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        (HERE/'server.pid').write_text(str(child.pid),encoding='ascii')
        return child
    def start(self):
        with self.lock:
            if self.health(): return {'running':True,'started':False}
            with socket.socket() as sock:
                if sock.connect_ex(('127.0.0.1',8765))==0:
                    raise RuntimeError('Portul serverului este ocupat, dar serviciul nu răspunde corect. Verifică jurnalul serverului.')
            child=self.spawn()
            deadline=time.monotonic()+10
            while time.monotonic()<deadline:
                if self.health(): return {'running':True,'started':True}
                if child.poll() is not None: break
                time.sleep(.3)
            raise RuntimeError('Pornirea nu a fost confirmată. Verifică server-error.log și încearcă din nou.')

def create_launcher(token,controller=None,root=None):
    app=Flask(__name__);app.config['MAX_CONTENT_LENGTH']=32*1024*1024
    control=controller or Controller(token)
    from contacts import Contacts
    contacts=Contacts(root) if root else None
    app.contacts=contacts
    @app.before_request
    def auth():
        if request.host!=f'127.0.0.1:{PORT}': abort(403)
        if request.headers.get('Origin') not in (None,f'http://127.0.0.1:{PORT}'): abort(403)
        if request.path!='/':
            supplied=request.args.get('key','') if request.path.startswith('/files/') else request.headers.get('X-Archive-Key','')
            if not secrets.compare_digest(supplied,token): abort(401)
    @app.after_request
    def headers(r):
        r.headers['Cache-Control']='no-store';r.headers['X-Content-Type-Options']='nosniff'
        r.headers['Referrer-Policy']='no-referrer'
        r.headers['Content-Security-Policy']="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self'; media-src 'self'; frame-ancestors 'none'; object-src 'none'"
        return r
    @app.get('/')
    def home():
        page=(HERE/'viewer.html').read_text('utf-8-sig').replace('__TOKEN__',token)
        page=page.replace('</html>','<style>'+(HERE/'crm.css').read_text('utf-8')+'</style><script>'+(HERE/'crm.js').read_text('utf-8')+'</script></html>')
        return Response(page,mimetype='text/html')
    @app.get('/crm/contacts')
    def contact_list():
        if not contacts:abort(503)
        return jsonify(contacts=contacts.all(),errors=contacts.errors)
    @app.route('/crm/contact/<ident>',methods=['GET','POST'])
    def contact_detail(ident):
        if not contacts:abort(503)
        contacts.scan()
        try:return jsonify(contacts.update(ident,request.get_json()) if request.method=='POST' else contacts.get(ident))
        except KeyError:abort(404)
        except ValueError as e:return jsonify(error=str(e)),400
    @app.get('/crm/search')
    def search_contacts():
        if not contacts:abort(503)
        return jsonify(results=contacts.search(request.args.get('q','')[:500]))
    @app.get('/control/status')
    def status():return jsonify(running=control.health())
    @app.post('/control/start')
    def start():
        try:return jsonify(control.start())
        except RuntimeError as e:return jsonify(error=str(e)),503
    @app.route('/api/<path:path>',methods=['GET','POST'])
    @app.get('/files/<path:path>')
    def proxy(path):
        route=request.path
        if not (route.startswith('/files/') or route.startswith('/api/conversation/') or route in ('/api/status','/api/retry')):abort(404)
        if request.method=='POST' and route!='/api/retry':abort(405)
        url=WORKER+route
        if route.startswith('/files/'):url+='?key='+token
        headers={'X-Archive-Key':token}
        if request.headers.get('Range'):headers['Range']=request.headers['Range']
        req=Request(url,headers=headers,method=request.method,data=b'' if request.method=='POST' else None)
        try:upstream=urlopen(req,timeout=15)
        except HTTPError as e:return Response(e.read(),status=e.code,mimetype='text/plain')
        except Exception:return jsonify(error='Serverul de comunicare nu răspunde. Apasă Pornește serverul.'),503
        def stream():
            try:
                while chunk:=upstream.read(256*1024):yield chunk
            finally:upstream.close()
        response=Response(stream(),status=upstream.status)
        for h in ('Content-Type','Content-Length','Content-Disposition','Content-Range','Accept-Ranges'):
            if upstream.headers.get(h):response.headers[h]=upstream.headers[h]
        response.call_on_close(upstream.close)
        return response
    return app

if __name__=='__main__':
    from waitress import serve
    config=json.loads((HERE/'config.json').read_text('utf-8-sig'))
    serve(create_launcher(config['token'],root=config['root']),host='127.0.0.1',port=PORT,threads=6)
