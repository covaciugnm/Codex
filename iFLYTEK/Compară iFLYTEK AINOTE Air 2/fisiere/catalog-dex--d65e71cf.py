"""Complete, structural dictionary. No inferred business names or wire constraints."""
import json, sqlite3, pathlib, tempfile, hashlib, shutil, zipfile, time
root=pathlib.Path(__file__).resolve().parent.parent
out=root/'catalog-parametri-functii'
(out/'dex-date').mkdir(parents=True,exist_ok=True)
data=json.loads((root/'inventar/api-complete.json').read_text(encoding='utf-8'))
tmp=pathlib.Path(tempfile.mkdtemp(prefix='ifly-dictionary-'))
db=sqlite3.connect(tmp/'catalog-apk.sqlite')
db.executescript('''
PRAGMA journal_mode=OFF;
CREATE TABLE metadata(key TEXT PRIMARY KEY,value TEXT);
CREATE TABLE classes(name TEXT PRIMARY KEY,dex TEXT,access INTEGER,super TEXT,interfaces_json TEXT,source_file TEXT,html_fragment TEXT);
CREATE TABLE functions(id TEXT PRIMARY KEY,class_name TEXT,name TEXT,descriptor TEXT,return_type TEXT,access INTEGER,dex TEXT,code_offset INTEGER,kind TEXT,html_fragment TEXT);
CREATE TABLE parameters(id TEXT PRIMARY KEY,function_id TEXT,position INTEGER,name TEXT,type_descriptor TEXT,java_type TEXT,value_class TEXT,direction TEXT,FOREIGN KEY(function_id) REFERENCES functions(id));
CREATE TABLE fields(id TEXT PRIMARY KEY,class_name TEXT,name TEXT,type_descriptor TEXT,java_type TEXT,access INTEGER,kind TEXT);
CREATE TABLE value_classes(id TEXT PRIMARY KEY,format TEXT,domain TEXT,limits_note TEXT);
''')
primitive={'V':'void','Z':'boolean','B':'byte','S':'short','C':'char','I':'int','J':'long','F':'float','D':'double'}
def typ(d):
    if d.startswith('['): return typ(d[1:])+'[]'
    return primitive.get(d,d[1:-1].replace('/','.') if d.startswith('L') and d.endswith(';') else d)
def category(d):
    if d.startswith('['): return 'array'
    return d if d in primitive else 'object'
def ident(kind,s): return kind+'-'+hashlib.sha256(s.encode()).hexdigest()[:20]
classes=[];chunk=[];methods=inputs=outputs=fields=0;chunkno=0
for ci,c in enumerate(data):
    if ci and ci%1000==0:
        (out/'dex-date'/f'{chunkno:03}.js').write_text('window.DEX_CHUNK='+json.dumps(chunk,ensure_ascii=False,separators=(',',':'))+';',encoding='utf-8')
        chunk=[];chunkno+=1
    fragment=f'{chunkno:03}/{len(chunk)}'
    classes.append([c['name'],fragment,len(c['methods']),len(c['fields']),c['dex']])
    db.execute('INSERT INTO classes VALUES(?,?,?,?,?,?,?)',(c['name'],c['dex'],c['access'],c.get('super'),json.dumps(c.get('interfaces',[])),c.get('sourceFile'),fragment))
    compact=[]
    for mi,m in enumerate(c['methods']):
        desc='('+''.join(m['args'])+')'+m['returnType'];fid=ident('df',c['name']+'#'+m['name']+desc)
        html=fragment+'/'+str(mi)
        db.execute('INSERT INTO functions VALUES(?,?,?,?,?,?,?,?,?,?)',(fid,c['name'],m['name'],desc,typ(m['returnType']),m['access'],c['dex'],m.get('codeOffset'),m.get('kind'),html))
        for pos,d in enumerate(m['args']):
            db.execute('INSERT INTO parameters VALUES(?,?,?,?,?,?,?,?)',(fid+'-p'+str(pos),fid,pos,'arg'+str(pos),d,typ(d),category(d),'input'))
            inputs+=1
        if m['returnType']!='V':
            db.execute('INSERT INTO parameters VALUES(?,?,?,?,?,?,?,?)',(fid+'-return',fid,-1,'return',m['returnType'],typ(m['returnType']),category(m['returnType']),'output'))
            outputs+=1
        compact.append([m['name'],m['args'],m['returnType'],m['access'],m.get('codeOffset'),m.get('kind'),fid])
        methods+=1
    fcompact=[]
    for f in c['fields']:
        d=f.get('type',f.get('descriptor','?'));fn=f['name'];fid=ident('dc',c['name']+'#'+fn+':'+d)
        db.execute('INSERT INTO fields VALUES(?,?,?,?,?,?,?)',(fid,c['name'],fn,d,typ(d),f.get('access'),f.get('kind')))
        fields+=1;fcompact.append([fn,d,f.get('access'),f.get('kind'),fid])
    chunk.append([c['name'],c['dex'],compact,fcompact,c.get('super'),c.get('interfaces',[])])
db.executemany('INSERT INTO value_classes VALUES(?,?,?,?)',[
('Z','boolean Java','false | true','Formatul pe fir nu rezultă din DEX.'),
('B','int8 Java','-128 .. 127','Domeniu de stocare; poate reprezenta uint8 pe fir.'),
('S','int16 Java','-32768 .. 32767','Domeniu de stocare, nu validare funcțională.'),
('C','UTF-16 code unit','0 .. 65535','Nu este automat un caracter Unicode complet.'),
('I','int32 Java','-2147483648 .. 2147483647','Domeniu de stocare, nu limită firmware.'),
('J','int64 Java','-9223372036854775808 .. 9223372036854775807','Domeniu de stocare; aplicațiile JS trebuie să păstreze precizia.'),
('F','IEEE754 binary32','valori finite, ±Infinity, NaN','Nu toate sunt acceptate în JSON.'),
('D','IEEE754 binary64','valori finite, ±Infinity, NaN','Nu toate sunt acceptate în JSON.'),
('array','referință tablou Java','dimensiune / nulabilitate necunoscute','byte[] nu dovedește un codec sau o ordine a octeților.'),
('object','referință obiect Java','clasa declarată; nulabilitate necunoscută','Numele parametrului, formatul, enumul și validările nu sunt păstrate în acest inventar.')])
summary={'classes':len(data),'functions':methods,'inputParameters':inputs,'returnParameters':outputs,'fields':fields,'chunks':chunkno+1,'apkSha256':'73170cdc5c3331cd6055607015c04ed8e0a314f4c0bd2fd4651e2b732d1b3da2','source':'inventar/api-complete.json','level':'structural DEX; includes dependencies, constructors, bridges and synthetic methods','runtimeValidated':False}
db.executemany('INSERT INTO metadata VALUES(?,?)',[(k,json.dumps(v,ensure_ascii=False)) for k,v in summary.items()])
db.executescript('CREATE INDEX functions_class ON functions(class_name);CREATE INDEX functions_name ON functions(name);CREATE INDEX parameters_function ON parameters(function_id);CREATE INDEX parameters_type ON parameters(java_type);CREATE INDEX fields_class ON fields(class_name);')
db.commit()
assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert db.execute('SELECT count(*) FROM parameters p LEFT JOIN functions f ON p.function_id=f.id WHERE f.id IS NULL').fetchone()[0]==0
db.close()
(out/'dex-date'/f'{chunkno:03}.js').write_text('window.DEX_CHUNK='+json.dumps(chunk,ensure_ascii=False,separators=(',',':'))+';',encoding='utf-8')
(out/'dex-index.js').write_text('window.DEX_INDEX='+json.dumps(classes,ensure_ascii=False,separators=(',',':'))+';',encoding='utf-8')
(out/'dex-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
with zipfile.ZipFile(out/'catalog-apk-sqlite.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    z.write(tmp/'catalog-apk.sqlite','catalog-apk.sqlite')
    z.writestr('CITESTE.txt','Dicționar structural complet al APK 1.0.3899. Tabele: classes, functions, parameters, fields, value_classes, metadata.\nLegătura: parameters.function_id = functions.id. Numele argN sunt poziționale, nu nume originale recuperate.\nParametrii return au position=-1. Domeniile Java nu sunt limite firmware.\nDeschide APK_COMPLET.html pentru navigare fără SQLite.\n')
print(json.dumps(summary,ensure_ascii=False))
