#!/usr/bin/env python3
"""Archive publicly downloadable model attachments; Python 3.10+, standard library only."""
import argparse
import hashlib
import json
import logging
import os
from pathlib import Path
import re
import shutil
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = 'https://api.printables.com/graphql/'
GROUPS = {'stls': 'stl', 'gcodes': 'gcode', 'slas': 'sla', 'otherFiles': 'other'}
class StopRun(Exception): pass
class AccessBlocked(Exception): pass

def safe_name(value):
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', str(value)).strip(' .') or 'file'
    if name.split('.')[0].upper() in {'CON','PRN','AUX','NUL',*(f'COM{i}' for i in range(1,10)),*(f'LPT{i}' for i in range(1,10))}:
        name = '_' + name
    if len(name) > 120:
        suffix = Path(name).suffix[:15]
        name = name[:100] + '_' + hashlib.sha256(name.encode()).hexdigest()[:8] + suffix
    return name

def save_json(path, data):
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    temp.replace(path)

class Archive:
    def __init__(self, args):
        self.args = args
        self.root = Path(args.dest).resolve()
        if not self.root.is_dir():
            raise StopRun('Folderul destinatie nu este accesibil: ' + str(self.root))
        self.control = self.root / '_downloader'
        self.control.mkdir(exist_ok=True)
        self.db = sqlite3.connect(self.control / 'progress.sqlite3')
        self.db.executescript('''
          CREATE TABLE IF NOT EXISTS models(site TEXT,id TEXT,status TEXT DEFAULT 'pending',error TEXT,PRIMARY KEY(site,id));
          CREATE TABLE IF NOT EXISTS files(site TEXT,model TEXT,id TEXT,path TEXT,size INTEGER,sha256 TEXT,PRIMARY KEY(site,model,id));
          CREATE TABLE IF NOT EXISTS cursors(site TEXT PRIMARY KEY,value INTEGER);
        ''')
        self.last_request = 0.0
        self.count = 0

    def check(self, required=0):
        if (self.control / 'STOP').exists():
            raise StopRun('Oprire solicitata prin fisierul _downloader/STOP.')
        if shutil.disk_usage(self.root).free < self.args.min_free_gb * 1024**3 + required:
            raise StopRun('Spatiu liber insuficient; progresul este salvat.')

    def request(self, url, payload=None, auth=False):
        if urllib.parse.urlsplit(url).scheme != 'https':
            raise ValueError('Este permis numai HTTPS.')
        for attempt in range(5):
            self.check()
            time.sleep(max(0, self.args.delay - (time.monotonic() - self.last_request)))
            headers = {'User-Agent': 'EVA-3DArchive/1.0', 'Accept-Encoding': 'identity'}
            if payload is not None:
                headers['Content-Type'] = 'application/json'
            if auth:
                if urllib.parse.urlsplit(url).hostname != 'api.thingiverse.com':
                    raise ValueError('Gazda invalida pentru autentificare')
                headers['Authorization'] = 'Bearer ' + os.environ['THINGIVERSE_TOKEN']
            req = urllib.request.Request(url, data=None if payload is None else json.dumps(payload).encode(), headers=headers)
            self.last_request = time.monotonic()
            try:
                return urllib.request.urlopen(req, timeout=90)
            except urllib.error.HTTPError as exc:
                if exc.code in (401,403):
                    raise AccessBlocked(f'HTTP {exc.code} la {urllib.parse.urlsplit(url).hostname}; autentificare sau verificare anti-bot necesara.') from None
                if exc.code not in (429,500,502,503,504) or attempt == 4:
                    raise
                retry = exc.headers.get('Retry-After','')
                delay = max(2**(attempt+2), int(retry) if retry.isdigit() else 0)
                logging.warning('HTTP %s; reincearca dupa %s secunde.', exc.code, delay)
                for _ in range(delay):
                    self.check()
                    time.sleep(1)
            except (urllib.error.URLError, TimeoutError):
                if attempt == 4:
                    raise
                time.sleep(2**(attempt+2))

    def json(self, url, payload=None, auth=False):
        with self.request(url, payload, auth) as response:
            raw = response.read()
            if b'<html' in raw[:500].lower() or b'<!doctype html' in raw[:500].lower():
                raise AccessBlocked('Serverul a returnat o pagina HTML in loc de date API.')
            return json.loads(raw)

    def gql(self, query, variables=None):
        result = self.json(API, {'query':query, 'variables':variables or {}})
        if result.get('errors'):
            raise RuntimeError(json.dumps(result['errors'], ensure_ascii=False))
        return result['data']

    def verified(self, site, model, key):
        row = self.db.execute('SELECT path,size FROM files WHERE site=? AND model=? AND id=?',(site,model,key)).fetchone()
        if not row:
            return False
        path = self.root / row[0]
        return path.is_file() and path.stat().st_size == row[1]

    def download(self, site, model, key, name, url, folder, expected=None):
        if self.verified(site,model,key):
            return
        self.check(int(expected or 0))
        path = folder / (safe_name(key) + '_' + safe_name(name))
        partial = path.with_name(path.name + '.part')
        digest = hashlib.sha256()
        size = 0
        with self.request(url) as response, partial.open('wb') as out:
            if 'text/html' in response.headers.get('Content-Type','').lower():
                raise AccessBlocked('Descarcarea a returnat HTML in loc de fisier.')
            length = response.headers.get('Content-Length')
            while True:
                self.check()
                block = response.read(1024*1024)
                if not block:
                    break
                out.write(block)
                digest.update(block)
                size += len(block)
            if length and size != int(length):
                raise IOError('Transfer incomplet (Content-Length)')
            if expected and size != int(expected):
                raise IOError(f'Dimensiune diferita: {size} fata de {expected}')
        partial.replace(path)
        self.db.execute('INSERT OR REPLACE INTO files VALUES(?,?,?,?,?,?)',(site,model,key,str(path.relative_to(self.root)),size,digest.hexdigest()))
        self.db.commit()
        logging.info('SALVAT %s (%s bytes)', path.relative_to(self.root), size)

    def printables(self, model):
        query = '''query($id:ID!) { print(id:$id) { id name license { name } user { publicUsername } stls { id name fileSize } gcodes { id name fileSize } slas { id name fileSize } otherFiles { id name fileSize } } }'''
        data = self.gql(query, {'id':model})['print']
        if not data:
            raise RuntimeError('Modelul nu mai este disponibil.')
        folder = self.root / 'Printables' / model
        folder.mkdir(parents=True,exist_ok=True)
        data['source_url'] = f'https://www.printables.com/model/{model}'
        save_json(folder / 'metadata.json', data)
        for group, kind in GROUPS.items():
            for item in data.get(group) or []:
                key = kind + '_' + str(item['id'])
                if self.verified('printables',model,key):
                    continue
                query = '''mutation($id:ID!,$model:ID!,$kind:DownloadFileTypeEnum!) { getDownloadLink(id:$id,printId:$model,fileType:$kind,source:model_detail) { ok errors { messages } output { link } } }'''
                result = self.gql(query,{'id':str(item['id']),'model':model,'kind':kind})['getDownloadLink']
                if not result or not result.get('ok') or not result.get('output',{}).get('link'):
                    raise RuntimeError('Link indisponibil: ' + json.dumps(result))
                self.download('printables',model,key,item['name'],result['output']['link'],folder,item.get('fileSize'))

    def thingiverse(self, model):
        base = 'https://api.thingiverse.com/things/' + model
        data = self.json(base, auth=True)
        files = self.json(base + '/files', auth=True)
        if not isinstance(files,list):
            raise RuntimeError('Lista de fisiere Thingiverse are un format necunoscut.')
        folder = self.root / 'Thingiverse' / model
        folder.mkdir(parents=True,exist_ok=True)
        data['source_url'] = f'https://www.thingiverse.com/thing:{model}'
        data['files'] = files
        save_json(folder / 'metadata.json',data)
        for item in files:
            url = item.get('download_url') or item.get('public_url')
            if not url:
                raise RuntimeError('Lipseste URL-ul fisierului ' + str(item.get('id')))
            self.download('thingiverse',model,str(item['id']),item['name'],url,folder,item.get('size'))

    def process(self,site,ids):
        failures = 0
        for model in ids:
            self.check()
            model = str(model)
            if self.args.max_models and self.count >= self.args.max_models:
                raise StopRun('Limita de modele a acestei rulari a fost atinsa.')
            logging.info('MODEL %s/%s',site,model)
            try:
                getattr(self,site)(model)
                self.db.execute('UPDATE models SET status=\'done\',error=NULL WHERE site=? AND id=?',(site,model))
                failures = 0
            except (StopRun,AccessBlocked):
                raise
            except Exception as exc:
                failures += 1
                self.db.execute('UPDATE models SET status=\'error\',error=? WHERE site=? AND id=?',(str(exc),site,model))
                logging.error('MODEL ESUAT %s/%s: %s',site,model,exc)
            finally:
                self.db.commit()
            self.count += 1
            if failures >= 3:
                raise RuntimeError('Trei modele consecutive au esuat; sursa este oprita pentru verificare.')

    def run_source(self,site):
        if site == 'thingiverse' and not os.environ.get('THINGIVERSE_TOKEN'):
            raise AccessBlocked('Thingiverse necesita variabila locala THINGIVERSE_TOKEN; accesul anonim a fost blocat de Cloudflare.')
        pending = [r[0] for r in self.db.execute("SELECT id FROM models WHERE site=? AND status!='done'",(site,))]
        self.process(site,pending)
        row = self.db.execute('SELECT value FROM cursors WHERE site=?',(site,)).fetchone()
        cursor = row[0] if row else (0 if site=='printables' else 1)
        while True:
            self.check()
            if site == 'printables':
                query = '''query($offset:Int!){ searchPrints2(query:"",printType:print,limit:40,offset:$offset,ordering:latest){items{id name}} }'''
                items = self.gql(query,{'offset':cursor})['searchPrints2']['items']
                step = len(items)
            else:
                items = self.json(f'https://api.thingiverse.com/newest?page={cursor}&per_page=40',auth=True)
                step = 1
            if not isinstance(items,list):
                raise RuntimeError('Format de catalog necunoscut.')
            if not items:
                logging.info('%s: sfarsitul rezultatelor accesibile. Nu garanteaza intregul catalog.',site)
                break
            new_ids=[]
            for item in items:
                model = str(item['id'])
                result = self.db.execute('INSERT OR IGNORE INTO models(site,id) VALUES(?,?)',(site,model))
                if result.rowcount:
                    new_ids.append(model)
            self.db.execute('INSERT OR REPLACE INTO cursors VALUES(?,?)',(site,cursor+step))
            self.db.commit()
            if not new_ids:
                logging.warning('%s: pagina contine numai modele cunoscute; continua la pagina urmatoare.',site)
            self.process(site,new_ids)
            cursor += step

    def status(self):
        return {'models':list(self.db.execute('SELECT site,status,count(*) FROM models GROUP BY site,status')),
                'files':list(self.db.execute('SELECT site,count(*),sum(size) FROM files GROUP BY site'))}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dest',default=str(Path(__file__).resolve().parent.parent))
    parser.add_argument('--site',choices=['all','printables','thingiverse'],default='all')
    parser.add_argument('--max-models',type=int,default=0,help='0 = fara limita')
    parser.add_argument('--min-free-gb',type=float,default=20)
    parser.add_argument('--delay',type=float,default=2.0)
    parser.add_argument('--status',action='store_true')
    parser.add_argument('--model-id',help='Descarca un singur model al sursei alese.')
    args=parser.parse_args()
    if args.delay < 0 or args.min_free_gb < 0 or args.max_models < 0:
        parser.error('Valorile numerice trebuie sa fie pozitive sau zero.')
    if args.model_id and (args.site=='all' or not args.model_id.isdigit()):
        parser.error('--model-id necesita un ID numeric si --site explicit.')
    archive=Archive(args)
    if args.status:
        print(json.dumps(archive.status(),indent=2))
        return
    # OS lock is released on exit/crash; prevents concurrent writers and downloads.
    import msvcrt
    lock=(archive.control/'run.lock').open('a+b')
    lock.seek(0)
    if not lock.read(1):
        lock.write(b'0'); lock.flush()
    lock.seek(0)
    try:
        msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
    except OSError:
        raise SystemExit('Exista deja o descarcare activa.')
    logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s',handlers=[logging.FileHandler(archive.control/'download.log',encoding='utf-8'),logging.StreamHandler()])
    save_json(archive.control/'process.json',{'pid':os.getpid(),'started':time.strftime('%Y-%m-%d %H:%M:%S'),'destination':str(archive.root)})
    outcome='finished'
    try:
        if args.model_id:
            archive.db.execute('INSERT OR IGNORE INTO models(site,id) VALUES(?,?)',(args.site,args.model_id)); archive.db.commit()
            archive.process(args.site,[args.model_id])
        else:
            # Check Thingiverse first so its access failure is reported before a long Printables run.
            for site in (['thingiverse','printables'] if args.site=='all' else [args.site]):
                try:
                    archive.run_source(site)
                except (AccessBlocked,RuntimeError,urllib.error.URLError) as exc:
                    outcome='incomplete'
                    logging.error('SURSA OPRITA %s: %s',site,exc)
    except (StopRun,KeyboardInterrupt) as exc:
        outcome='stopped'
        logging.info('OPRIT: %s',exc)
    except Exception:
        outcome='failed'
        logging.exception('EROARE')
        raise
    finally:
        save_json(archive.control/'last_run.json',{'outcome':outcome,**archive.status()})
        archive.db.close()
        lock.close()

if __name__=='__main__':
    main()
