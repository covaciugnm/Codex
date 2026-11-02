from pathlib import Path
from datetime import datetime,timezone,timedelta
from email.parser import BytesParser
from email import policy
import json,hashlib,copy,csv,sqlite3,os,sys,shutil
sys.stdout.reconfigure(encoding='utf-8')
r=Path.cwd();b=r/'folder map';arch=r/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail';cap=r/'08. Corespondenta/2026.10.29 Capra Baupolizei';out=r/'08. Corespondenta/2026.11.02 Check-email PECH';day='2026.11.02';now=datetime.now(timezone(timedelta(hours=2)));stamp=now.isoformat(timespec='seconds');tag=now.strftime('%H-%M-%S');hist=b/(day+' Istoric PECH 13 '+tag);hist.mkdir()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));rel=lambda p:p.relative_to(r).as_posix()
q=read(b/'2026.11.02 Sursa control PECH 13.json');data=read(b/'2026.11.02 Mise en archive PECH 13.json');stage=b/'2026.11.02 Surse MA37 control PECH 13';man=read(stage/'2026.11.02 Manifest verificat.json');e=data['capra']['e'];alias=data['alias']['e'];ID=e['id'];aid=alias['id'];assert not e['is_sent'] and not e['truncated'] and e['text']==alias['text'] and q['draft']['status']=='pending'
changed={}; archived={}
def backup(f):
 if f.exists():
  h=hist/f.relative_to(r);h.parent.mkdir(parents=True,exist_ok=True)
  if not h.exists():shutil.copy2(f,h)
def write(f,data,text=None,desc=None):
 f.parent.mkdir(parents=True,exist_ok=True);raw=data.encode('utf-8') if isinstance(data,str) else data
 if not f.exists() or f.read_bytes()!=raw:
  backup(f);tmp=f.with_name(f.name+'.pech13-tmp');tmp.write_bytes(raw);os.replace(tmp,f)
 changed[f]=(text if text is not None else data if isinstance(data,str) else '',desc or 'Monitorizare PECH – sursă și status')
def wrj(f,v,desc=None):write(f,json.dumps(v,ensure_ascii=False,indent=2),desc=desc)
def prepend(f,txt):
 prev=f.read_text(encoding='utf-8-sig') if f.exists() else ''
 if not prev and f.parent==arch/'Parteneri':
  olds=sorted(f.parent.glob('*'+f.name[10:]));prev=('Istoric precedent: '+rel(olds[-1])+'\n') if olds else ''
 write(f,txt+'\n\n'+prev)
for a in man:
 seq=a['id'][:8];mime=next(x['content_type'] for x in e['attachments'] if x['id']==a['id']);raw=(r/a['local']).read_bytes();sha=hashlib.sha256(raw).hexdigest();assert sha==a['sha256']
 if mime=='application/pdf':
  p=cap/'Atasamente'/(day+' MA37 raspuns GZ 1501240-2026-2.pdf');tx=next(x['extras'] for x in man if 'extras' in x);desc='Scrisoarea oficială MA37 către Capra privind consultarea planurilor pentru EZ 2235 Meidling'
 elif mime=='message/rfc822':
  p=cap/'Atasamente'/(day+' MA37 catre Capra GZ 1501240-2026-2 - original.eml');m=BytesParser(policy=policy.default).parsebytes(raw);body=m.get_body(preferencelist=('plain',));tx='\n'.join(str(m.get(k,'')) for k in ['Date','From','To','Subject','Message-ID'])+'\n'+body.get_content()+'\nAtașament: MA 37 Antwort.pdf';desc='E-mailul original transmis de MA37 avocatului; conține aceeași scrisoare în PDF'
 else:p=cap/'Atasamente'/(day+' '+seq+' Capra '+a['nume']);tx='Imagine de semnătură a e-mailului.';desc=tx
 if sha not in archived:write(p,raw,tx,desc);archived[sha]=p
 a['cale']=rel(archived[sha]);a.pop('local',None)
stem=cap/(day+' 12-15-10 PRIMIT Capra dd5df6a9'); emtxt=Path(str(stem)+'.txt');emjson=Path(str(stem)+'.json'); aliasfile=cap/(day+' Alias EVA Capra 5eb8107e.json')
wrj(emjson,{'data_lizibila':day+' 12:15:10 România','statut':'PRIMIT','link_id':data['capra']['link'],'email':e,'alias':aid,'atasamente':man},'Mesajul integral al avocatului și manifestul originalelor MA37')
write(emtxt,day+' 12:15:10 România | PRIMIT\nDe la: '+e['from_address']+'\nCătre: '+', '.join(e['to'])+'\nCC: —\nSubiect: '+e['subject']+'\nID Eva-Mail: '+ID+'\nAlias al aceleiași comunicări: '+aid+'\n\nText original integral:\n'+e['text'])
wrj(aliasfile,{'statut':'PRIMIT – același mesaj','data_lizibila':day+' 12:15:10 România','link_id':data['alias']['link'],'canonical_id':ID,'email':alias})
report=out/(day+' '+tag+' Verificare PECH.txt');proof=out/(day+' '+tag+' Dovezi PECH.json')
pdf=next(a['cale'] for a in man if a['nume'].endswith('.pdf')); eml=next(a['cale'] for a in man if a['nume'].endswith('.eml'))
sync={}
for i,s in enumerate(q['sync']):
 for box in s['boxes']:
  sync[('Primary ' if i==0 else 'Secundar ')+box['email']]=datetime.fromisoformat(box['last_sync'].replace('Z','+00:00')).astimezone(now.tzinfo).strftime('%Y.%m.%d %H:%M:%S')
result='MA37 oferă consultarea documentelor din dosarul imobilului (Hauseinlage) sau de la supraveghere (Überwachung), EZ 2235, KG Meidling. Scrisoarea nu localizează distinct exemplarul vizat Parie C și nu stabilește o programare.'
step='Capra să ceară responsabilului DI Johannes Walter să verifice disponibilitatea exemplarului vizat Parie C pentru MA37/1539234-2021-1 și să indice locul și un termen de consultare a dosarului de supraveghere. Folosiți referința răspunsului 1501240-2026-2. Nicio rezervare sau trimitere efectuată prin acest control.'
web='https://www.wien.gv.at/kontakt/ma37-baupolizei-planarchiv-bewilligte-plaene'
note=f'''{day} {now.strftime('%H:%M:%S')} România | Verificare PECH
Status: nicio comunicare sau nelivrare PECH nouă. Últimul răspuns direct: DI Bernhard Ployer, 2026.10.27. Accesul a fost trimis la 2026.10.28, fără confirmare de la PECH. Ciorna de amânare {q['draft']['id']} este în continuare NETRIMISĂ; întâlnirea propusă pentru 2026.11.03 nu este confirmată.
Noutate pentru proiect: la 2026.11.02 12:15:10 România, Bogdan Capra a transmis către office@ac-wohnart.at, fără CC, răspunsul MA37 adresat avocatului. E-mailul municipalității a fost trimis la 12:11:28 România, GZ 1501240-2026-2. {result} Scrisoarea nu include planșe vizate.
Următorul pas: {step}
Instrucțiuni Stadt Wien: pentru proceduri în curs consultarea se stabilește cu responsabilul dosarului; programarea obișnuită la Planarchiv este distinctă. {web}
Surse: {pdf}; {eml}; {rel(emtxt)}. ID Eva-Mail {ID}; alias {aid}. Dintre cele șase intrări de atașament, două PDF-uri sunt identice, inclusiv cu PDF-ul din EML. Trei imagini sunt elemente ale semnăturii. Cinci conținuturi distincte, o singură scrisoare oficială; arhivate ca originale.
Acoperire: 2026.11.01–2026.11.02, cu suprapunere față de controlul PECH 2026.11.02 11:50:18 și controlul general 11:52:27. {len(q['pages'])} pagini, {len(q['ids'])} ID-uri distincte. Am verificat primit/trimis, căutările globale de proiect/contract și nelivrările. Aliasul BERGER nou vizibil este același e-mail din 2026.11.01 deja raportat, fără o nouă comunicare. Sincronizare afișată (România): {', '.join(k+' '+v for k,v in sync.items())}. Mesajele încă neindexate pot lipsi. Dovezi: {rel(proof)}.
'''.replace('Últimul','Ultimul')
write(report,note)
q.update({'checked_at_iso':stamp,'data_lizibila':day,'mesaje_noi_PECH':0,'mesaje_proiect_noi':1,'originale':man,'raspuns_MA37':result,'sursa_reguli_consultare':web,'surse':[rel(emjson),pdf,eml],'raport':rel(report),'sync_local':sync,'decizie':'NOTIFY – răspuns oficial nou cu pas următor pentru consultarea planurilor'})
wrj(proof,q)
rp=r/q['register']['path'];reg=read(rp);initial_general=copy.deepcopy(reg['acoperire']['verificare_incrementala']);initial_drafts=reg['drafturi'].copy(); arpath=arch/(day+' Registru atasamente.json');ar=read(arpath)
if not any(x.get('id')==ID for x in reg['comunicatii']):
 reg['comunicatii'].append({'data':day,'ora_utc':'10:15:10','sens':'PRIMIT','partener':'CERHA HEMPEL','domeniu':'Recuperare planuri autorizate – răspuns MA37','expeditor':e['from_address'],'destinatari':e['to'],'cc':e['cc'],'subiect':e['subject'],'id':ID,'cale':rel(emtxt),'json':rel(emjson),'atasamente':list(dict.fromkeys(a['cale'] for a in man)),'trunchiat':False,'data_preluarii':day,'deja_raportat_punctual':True})
for source_id,alias_id,fn in [(ID,aid,aliasfile),(data['berger']['id'],data['berger']['alias'],proof)]:
 if not any(x.get('alias_id')==alias_id for x in reg['aliasuri_email_EVA']):
  reg['aliasuri_email_EVA'].append({'canonical_id':source_id,'alias_id':alias_id,'link_id':data['alias']['link'],'cale':rel(fn),'verificare':'Corp, subiect, oră, expeditor, destinatari, CC, thread_id identice, nume și mărimi liste de anexe identice; fără duplicarea comunicării.'})
for a in man:
 if not any(x.get('id')==a['id'] for x in ar):
  ar.append({'id':a['id'],'email_id':ID,'data':day,'partener':'CERHA HEMPEL','nume_original':a['nume'],'octeti':a['octeti'],'sha256':a['sha256'],'cale':a['cale'],'stare':'Original verificat integral pe fragmente SHA-256. Aceeași cale pentru octeți identici.'})
cs=next(x for x in reg['statusuri'] if x['partener']=='CERHA HEMPEL');ps=next(x for x in reg['statusuri'] if x['partener']=='Pech')
if cs.get('sursa_ultimul_primit')!=rel(emtxt):
 cs.setdefault('istoric_status',[]).append({k:copy.deepcopy(cs.get(k)) for k in ['status','ultimul_raspuns','urmatorul_pas','ultima_comunicare','sursa_status']})
cs.update({'status':result,'ultimul_raspuns':day+' 12:15:10 România. Capra retransmite scrisoarea MA37, GZ 1501240-2026-2. Fără planuri livrate.','ultima_comunicare':day,'ultimul_primit':day,'subiect_ultimul_primit':e['subject'],'sursa_ultimul_primit':rel(emtxt),'sursa_status':[rel(emtxt),pdf,eml],'urmatorul_pas':step,'data_actualizarii':day,'mesaje':sum(x.get('partener')=='CERHA HEMPEL' for x in reg['comunicatii'])})
entry={'data':day,'checked_at_iso':stamp,'parteneri':['Pech'],'mesaje_noi':0,'mesaje_conexe_noi':1,'id_conex':ID,'sursa':rel(proof),'raport':rel(report),'draft_amanare_status':'pending','paginare_completa':True,'metadate_unice':len(q['ids']),'sincronizare_Romania':sync,'decizie_notificare':'NOTIFY'}
ps['verificare_punctuala_PECH']=entry;ps['documente_autorizare_ultima_noutate']={'data':day,'id_eva_mail':ID,'sursa':pdf,'status':result};reg['acoperire']['verificare_punctuala_PECH']=entry
h=reg.setdefault('verificari_parteneri',[])
if not any(x.get('checked_at_iso')==q['previous_PECH'] for x in h):
 h.append({'checked_at_iso':q['previous_PECH'],'parteneri':['Pech'],'mesaje_noi':0,'sursa':q['previous_PECH_source'],'sursa_reconciliata':True})
h.append(entry);reg['data_actualizarii']=day;reg['acoperire']['registru_atasamente_randuri']=len(ar)
assert reg['drafturi']==initial_drafts and reg['acoperire']['verificare_incrementala']==initial_general;wrj(arpath,ar);wrj(rp,reg)
short=note.split('Instrucțiuni Stadt Wien:')[0]+f'Surse: {pdf}; {rel(report)}.\n'
for f in [r/(day+' Status proiect.txt'),r/(day+' Log progres proiect.txt'),arch/'Parteneri'/(day+' Log discutii - Pech.txt')]:prepend(f,short)
for partner in ['CERHA HEMPEL','MA37']:
 f=arch/'Parteneri'/(day+' Log discutii - '+partner+'.txt');prepend(f,f'{day} | MA37 prin Capra | {result}\nUltimul răspuns: GZ 1501240-2026-2 primit prin avocat la 12:15:10 România. Pas următor: {step}\nSurse: {pdf}; {rel(emtxt)} (Eva-Mail {ID}).')
prepend(b/'README.md',f'{day} {now.strftime("%H:%M:%S")} | MA37 oferă consultare pentru EZ 2235, fără confirmarea exemplarului Parie C. PECH: fără mesaj nou; amânare netrimisă. [Raport]({("../"+rel(report)).replace(" ","%20")}).')
# Actualizez exclusiv rândurile schimbate și verific cheile pe disc și în SQLite.
inv=b/'inventar.json'; csvf=b/'inventar.csv';rows={x['cale']:x for x in read(inv)};up={}; db=sqlite3.connect(b/'cautare.sqlite',timeout=35)
for f,(tx,desc) in changed.items():
 if b in f.parents:continue
 raw=f.read_bytes();s=f.stat();sha=hashlib.sha256(raw).hexdigest();path=rel(f);cache=b/'texte'/(sha+'.txt');cache.write_text(tx,encoding='utf-8');row=rows.get(path,{}).copy();row.update(cale=path,folder=rel(f.parent),extensie=f.suffix.lower(),octeti=len(raw),modificat=datetime.fromtimestamp(s.st_mtime).isoformat(),modificat_ns=s.st_mtime_ns,sha256=sha,duplicat_al=row.get('duplicat_al',''),ce_reprezinta=desc,baza_descrierii='E-mail și originale verificate '+day,extras_continut=' '.join(tx.split())[:1050],stare_citire='text extras' if f.suffix.lower() not in ('.jpg',) else 'imagine semnătură',text_cache=rel(cache),detalii={},rezumat_verificat='Consultarea EZ 2235 este posibilă; Parie C nu este identificată distinct în scrisoare.',ocr_cache='');up[path]=row
 db.execute('DELETE FROM documente WHERE cale=?',(path,));db.execute('INSERT INTO documente VALUES(?,?,?,?)',(path,desc,tx,sha))
db.commit();rows={x['cale']:x for x in read(inv)};rows.update(up);ordered=sorted(rows.values(),key=lambda x:x['cale'].lower());tmp=inv.with_name(inv.name+'.pech13-tmp');tmp.write_text(json.dumps(ordered,ensure_ascii=False,indent=2),encoding='utf-8');os.replace(tmp,inv)
tmp=csvf.with_name(csvf.name+'.pech13-tmp')
with tmp.open('w',encoding='utf-8-sig',newline='') as fp:
 w=csv.DictWriter(fp,fieldnames=[k for k in ordered[0] if k!='detalii'],extrasaction='ignore');w.writeheader();w.writerows(ordered)
os.replace(tmp,csvf)
for path,row in up.items():assert db.execute('SELECT sha256 FROM documente WHERE cale=?',(path,)).fetchall()==[(row['sha256'],)]
db.close();assert sum(x.get('id')==ID for x in read(rp)['comunicatii'])==1;assert all(hashlib.sha256((r/a['cale']).read_bytes()).hexdigest()==a['sha256'] for a in man)
print(json.dumps({'report':rel(report),'pdf':pdf,'eml':eml,'index_rows_checked':len(up),'registry':len(reg['comunicatii']),'verified_files':len(archived)},ensure_ascii=False))
