from pathlib import Path
from datetime import datetime,timezone,timedelta
import json,copy,base64,hashlib,os,shutil,sys
sys.stdout.reconfigure(encoding='utf-8')
r=Path.cwd();fm=r/'folder map';a=r/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail';out=r/'08. Corespondenta/2026.11.02 Check-email PECH';cap=r/'08. Corespondenta/2026.10.29 Capra Baupolizei'; day='2026.11.02';tz=timezone(timedelta(hours=2));now=datetime.now(tz); tag=now.strftime('%H-%M-%S');stamp=now.isoformat(timespec='seconds');hist=fm/(day+' Istoric PECH seara '+tag);hist.mkdir()
rd=lambda f:json.loads(f.read_text(encoding='utf-8-sig'))
rel=lambda f:f.relative_to(r).as_posix()
sha=lambda x:hashlib.sha256(x).hexdigest()
d=rd(fm/'2026.11.02 Surse PECH control seara.json');q=d['evidence']; bas=q['baseline']; rows={x['cale']:x for x in rd(fm/'inventar.json')};changed=[]
def preserve(f):
 if f.is_file():
  h=hist/f.relative_to(r);h.parent.mkdir(parents=True,exist_ok=True)
  if not h.exists():shutil.copy2(f,h)
def put(f,v):
 raw=v.encode('utf-8') if isinstance(v,str) else v
 if f.exists() and f.read_bytes()==raw:
  if rows.get(rel(f),{}).get('sha256')!=sha(raw):changed.append(f)
  return
 preserve(f);f.parent.mkdir(parents=True,exist_ok=True);tmp=f.with_name(f.name+'.pech-seara.tmp');tmp.write_bytes(raw);os.replace(tmp,f);changed.append(f)
def js(f,obj):put(f,json.dumps(obj,indent=2,ensure_ascii=False))
def pre(f,s):put(f,s+'\n\n'+(f.read_text(encoding='utf-8-sig') if f.exists() else ''))
def local(dt):return datetime.fromisoformat(dt.replace('Z','+00:00')).astimezone(tz).strftime('%Y.%m.%d %H:%M:%S')
assert not q['errors'] and all(p['offset']+len(p['ids'])>=p['total'] for p in q['pages'])
assert all(si==sa==sha((r/path).read_bytes()) for path,si,sa in bas['refs'])
draft_old=rd(r/bas['refs'][-2][0])['draft']
assert all(draft_old[k]==q['draft'][k] for k in ['id','status','updated_at','subject','body','to','cc','attachments'])
regf=a/(day+' Registru comunicatii.json');reg=rd(regf);atf=a/(day+' Registru atasamente.json');areg=rd(atf);oldgeneral=copy.deepcopy(reg['acoperire']['verificare_incrementala']);olddrafts=copy.deepcopy(reg['drafturi'])
proof=out/(day+' '+tag+' Dovezi PECH.json');report=out/(day+' '+tag+' Verificare PECH.txt')
can={};alias=[];aliases_doc=out/(day+' MA37 - exemplare EVA din conexiunea secundara.json');manifest=[];download={}
for doc in d['messages']:
 e=doc['email'];assert not e['truncated']
 if doc['link']==q['sync'][0]['link']:can[e['thread_id']]=e
 else:alias.append(doc)
 for at in e['attachments']:
  parts=sorted((p for p in d['chunks'] if p['id']==at['id']),key=lambda p:p['offset']);bb=b''
  for p in parts:
   chunk=base64.b64decode(p['bytes'],validate=True);assert p['offset']==len(bb) and p['len']==len(chunk) and p['sha']==sha(chunk);bb+=chunk
  assert len(bb)==at['size'] and parts[-1]['eof'];download[at['id']]=bb
primary_sent=next(e for e in can.values() if e['is_sent']);mirror_sent=next(x['email'] for x in alias if x['email']['is_sent'])
p_byname={x['name']:x for x in primary_sent['attachments']};s_byname={x['name']:x for x in mirror_sent['attachments']}
for name,at in p_byname.items():
 b1=download[at['id']];b2=download[s_byname[name]['id']];f=cap/'Atasamente'/(day+' TRIMIS 1c804e3a - '+name);assert f.read_bytes()==b1 and rows[rel(f)]['sha256']==sha(b1)
 manifest.append({'id':at['id'],'email_id':primary_sent['id'],'partener':'MA37','data':day,'nume_original':name,'octeti':len(b1),'sha256':sha(b1),'cale':rel(f),'stare':'Original verificat la sursa EVA și identic fișierului deja arhivat.'})
 if name.endswith('.eml'):
  assert b1!=b2 and base64.b64decode(b''.join(b2.split()),validate=True)==b1
  f2=out/(day+' MA37 - confirmare istorica, reprezentare EVA secundara.eml');put(f2,b2);state='Reprezentare diferită în sursa secundară; după decodare base64, exact aceiași octeți ca EML-ul original. Nu este o altă programare.'
 else:assert b1==b2;f2=f;state='PDF identic în ambele conexiuni.'
 manifest.append({'id':s_byname[name]['id'],'email_id':mirror_sent['id'],'canonical_email_id':primary_sent['id'],'partener':'MA37','data':day,'nume_original':name,'octeti':len(b2),'sha256':sha(b2),'cale':rel(f2),'stare':state})
for z in manifest:
 if not any(x['id']==z['id'] for x in areg):areg.append(z)
descs={'1c804e3a':'cerere de programare trimisă, respinsă la ambele adrese','325025ff':'raport automat de nelivrare, cod 550; nu este răspunsul autorității','05d34c06':'alertă tehnică pentru aceeași nelivrare, nu reprezintă o a doua expediere'}
for e in can.values():
 k=e['id'][:8];sens='TRIMIS' if e['is_sent'] else 'PRIMIT';jpath=cap/(day+' '+sens+' MA37 livrare '+k+'.json');old=rd(jpath)['email'];assert all(old[key]==e[key] for key in ['id','text','subject','from_address','to','cc','received_at','is_sent']) and rows[rel(jpath)]['sha256']==sha(jpath.read_bytes())
 txt=out/(day+' '+sens+' MA37 '+k+'.txt');put(txt,'Statut: '+sens+' | '+local(e['received_at'])+' România\nSubiect: '+e['subject']+'\nExpeditor: '+e['from_address']+'\nCătre: '+', '.join(e['to'])+'\nCC: '+(', '.join(e['cc']) or '—')+'\nID Eva-Mail: '+e['id']+'\nInterpretare: '+descs[k]+'\nAtașamente: '+(', '.join(x['name'] for x in e['attachments']) or 'niciunul')+'\n\nText original:\n'+e['text'])
 if not any(x['id']==e['id'] for x in reg['comunicatii']):
  reg['comunicatii'].append({'data':day,'ora_utc':e['received_at'][11:19],'partener':'MA37','domeniu':'Consultare dosar / livrare','sens':sens,'subiect':e['subject'],'expeditor':e['from_address'],'destinatari':e['to'],'cc':e['cc'],'id':e['id'],'cale':rel(txt),'json':rel(jpath),'atasamente':[x['cale'] for x in manifest if x['email_id']==e['id']],'trunchiat':False,'data_preluarii':day,'deja_raportat_punctual':True,'observatii':descs[k]})
alias_records=[]
for x in alias:
 e=x['email'];ce=can[e['thread_id']];assert all(e[k]==ce[k] for k in ['to','cc','subject','from_address','is_sent']);assert e['received_at'][:19]==ce['received_at'][:19]
 why='Identice mesajul identificat prin Message-ID, antetele de adresare, subiectul și secunda expedierii. '
 if e['is_sent']:why+='Corpurile extrase nu sunt identice: în copia secundară este redată confirmarea veche codificată. EML diferit binar, identic după decodare; PDF identic.'
 else:assert e['text']==ce['text'];why+='Textele integrale sunt identice.'
 row={'alias_id':e['id'],'canonical_id':ce['id'],'link_id':x['link'],'cale':rel(aliases_doc),'verificare':why};alias_records.append(row)
 if not any(v['alias_id']==e['id'] for v in reg['aliasuri_email_EVA']):reg['aliasuri_email_EVA'].append(row)
js(aliases_doc,{'data_lizibila':day,'aliasuri':alias_records,'originale_EVA':alias,'atasamente':manifest})
known={x['id'] for x in reg['comunicatii']}|{x['alias_id'] for x in reg['aliasuri_email_EVA']};global_ids={i for p in q['pages'] if p['args'].get('query') for i in p['ids']};assert all(i in known or i=='87b6e18a-ea11-47a4-addd-d12c0f5ded54' for i in global_ids)
q['ids_confirmate_proiect']=[x['id'] for x in q['ids'] if x['id'] in known];q['sincronizare_Romania']={('Primary' if i==0 else 'Secundar')+' '+z['email']:local(z['last_sync']) for i,s in enumerate(q['sync']) for z in s['boxes']};q.update({'control':stamp,'data_lizibila':day,'originale_atasamente':manifest,'aliasuri':alias_records,'mesaje_directe_PECH_noi':0,'nelivrari_catre_PECH':0,'mesaje_proiect_noi_neraportate':0,'raport':rel(report),'decizie':'DONT_NOTIFY'})
orig=q['dedup_source'];ref=rd(r/bas['prior']['sursa']);assert (r/orig).is_file()
sync=q['sincronizare_Romania']
note=f'''{day} {now.strftime('%H:%M:%S')} România | Verificare PECH
Status: niciun răspuns, mesaj trimis, atașament sau raport de nelivrare nou pentru PECH. Nicio modificare de preț, serviciu, termen ori programare identificată.
Ultimul răspuns direct: DI Bernhard Ployer, 2026.10.27. Ciorna de amânare pentru 2026.11.03 este în continuare netrimisă; nu există o confirmare a reprogramării.
Incident conex deja notificat: cererea de consultare a dosarului de supraveghere, trimisă de A&C la 16:00:23, a fost respinsă pentru destinatar și CC (550, atașament .eml nepermis). Alerta de la 16:05 privește aceeași trimitere. Nu există o confirmare de consultare sau o retrimitere identificată în datele verificate. PDF-ul de 39 EUR este o dispoziție de plată din 2026.09.25; nu dovedește achitarea.
Pas următor deja comunicat: pentru MA37, retransmiterea cererii cu confirmarea veche în PDF și urmărirea confirmării datei și locului. Pentru PECH, urmărirea răspunsului și, dacă se dorește propunerea de amânare, expedierea ciornei de către beneficiar. Nu s-a trimis niciun mesaj în această verificare.
Surse: {orig}; {rel(proof)}. Ultimul mesaj PECH: {bas['refs'][1][0]}. Perioadă 2026.11.01–2026.11.02; control PECH precedent 12:59:20, control general 11:52:27, incident raportat separat la 16:58. {len(q['pages'])} căutări/pagini complete, {len(q['ids'])} ID-uri distincte. Sincronizare afișată, ora României: office {sync['Primary office@ac-wohnart.at']}, Gmail {sync['Primary covaciu.gnm@gmail.com']}, office secundar {sync['Secundar office@ac-wohnart.at']}. Mesajele încă nesincronizate pot lipsi.
'''
entry={'data':day,'checked_at_iso':stamp,'parteneri':['Pech'],'mesaje_noi':0,'noutati_proiect_neraportate':0,'nelivrari_PECH':0,'incident_MA37_raportat':q['notification']['canonical_bounce_id'],'query_count':len(q['pages']),'paginare_completa':True,'metadate_unice':len(q['ids']),'sincronizare_Romania':sync,'draft_amanare_status':'pending','sursa':rel(proof),'raport':rel(report),'decizie_notificare':'DONT_NOTIFY'}
ps=next(s for s in reg['statusuri'] if s['partener']=='Pech');ps['verificare_punctuala_PECH']=entry;reg['acoperire']['verificare_punctuala_PECH']=entry;reg.setdefault('verificari_parteneri',[]).append(entry);m=next(s for s in reg['statusuri'] if s['partener']=='MA37')
m['livrare_cerere_2026_11_02']={'sursa':orig,'statut':'TRIMIS, nelivrat la destinatar și CC','id_mesaj':primary_sent['id'],'id_raport_nelivrare':q['notification']['canonical_bounce_id'],'deja_notificat':True}
m['urmatorul_pas']='Retransmiterea solicitării cu vechea confirmare de programare convertită în PDF; obținerea confirmării datei, locului și disponibilității exemplarului Parie C.';reg['acoperire']['registru_atasamente_randuri']=len(areg);assert oldgeneral==reg['acoperire']['verificare_incrementala'] and olddrafts==reg['drafturi']
js(proof,q);put(report,note);js(atf,areg);js(regf,reg)
# O intrare scurtă, cu trimitere la raportul detaliat, pentru fiecare jurnal.
short=f'{day} {now.strftime("%H:%M:%S")} România | PECH: fără răspuns ori nelivrare nouă; ultima comunicare primită de la Ployer rămâne 2026.10.27. Ciorna pentru 2026.11.03 este netrimisă. Urmărim răspunsul PECH. Respingerea ambelor adrese MA37 din cauza anexei .eml a fost deja raportată separat; nu există o programare confirmată. Pas pentru MA37: retransmitere cu confirmarea veche în PDF. Sursă: {rel(report)}.'
for f in [r/(day+' Status proiect.txt'),r/(day+' Log progres proiect.txt'),a/'Parteneri'/(day+' Log discutii - Pech.txt')]:pre(f,short)
pre(fm/'README.md',f'{day} {now.strftime("%H:%M:%S")} | PECH: fără noutăți directe. Incidentul de nelivrare MA37 era deja notificat. [Verificare](../{rel(report).replace(" ","%20")}).')
filelist=fm/(day+' Fisiere actualizate PECH seara.json');filelist.write_text(json.dumps([rel(f) for f in changed if fm not in f.parents],ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'report':rel(report),'count':len(reg['comunicatii']),'canonical_events':len(can),'aliases':len(alias),'changed':len(changed),'decision':'DONT_NOTIFY'},ensure_ascii=False))

