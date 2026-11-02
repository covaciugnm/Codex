from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,shutil,hashlib
root=Path.cwd();tz=ZoneInfo('Europe/Bucharest');now=datetime.now(tz);day=now.strftime('%Y.%m.%d');tag=now.strftime('%H-%M-%S');stamp=now.isoformat()
assert day=='2026.10.26'
base=Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail');regpath=base/(day+' Registru comunicatii.json')
out=Path('08. Corespondenta')/(day+' Verificare Berger Pech');out.mkdir(exist_ok=True)
proof=out/(day+' '+tag+' Dovezi verificare EVA.json');report=out/(day+' '+tag+' Raport verificare BERGER PECH.txt')
hist=Path('folder map')/(day+' Istoric BP '+tag)
def read(p):return json.loads((root/p).read_text(encoding='utf-8-sig'))
def save(p,t):
 p=Path(p);dest=root/p
 if dest.exists():
  b=root/hist/p;b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dest,b)
 dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(t,encoding='utf-8')
def jsave(p,x):save(p,json.dumps(x,ensure_ascii=False,indent=2))
def local(s):return datetime.fromisoformat(s.replace('Z','+00:00')).astimezone(tz).strftime('%Y.%m.%d %H:%M:%S')
p=read(Path('folder map/2026.10.26 Dovezi etapa BP dupa-amiaza.json'));r=read(regpath)
oldids={x['id'] for x in r['comunicatii']};assert len(oldids)==len(r['comunicatii'])==p['baseline_count']==836
assert len(p['searches'])==25 and not p['errors']
for page in p['searches']:assert page['args']['offset']+len(page['result']['items'])>=page['result']['total']
assert len(p['full_emails'])==3 and all(not x.get('truncated') and not x.get('attachments') for x in p['full_emails'])
general=r['acoperire']['verificare_incrementala'].copy();saved={}
for e in p['full_emails']:
 assert e['id'] not in oldids
 partner='Markus Berger' if any('bmberger.at' in s.lower() for s in [e['from_address']]+e['to']) else 'Pech'
 firm='BERGER' if partner=='Markus Berger' else 'PECH';sens='TRIMIS' if e['is_sent'] else 'PRIMIT'
 dt=datetime.fromisoformat(e['received_at'].replace('Z','+00:00'));ld=dt.astimezone(tz)
 stem=f"{ld.strftime('%Y.%m.%d %H-%M-%S')} {sens} {firm} {e['id'][:8]}"
 txtpath=out/(stem+'.txt');jpath=out/(stem+'.json')
 jsave(jpath,e)
 text=f"Data: {ld.strftime('%Y.%m.%d')}; ora Romania: {ld.strftime('%H:%M:%S')}; data tehnica originala: {e['received_at']}\nStatut: {sens}\nID Eva-Mail: {e['id']}\nCont: {e['account_email']}\nExpeditor: {e['from_address']}\nDestinatari: {', '.join(e['to'])}\nCC: {', '.join(e.get('cc',[]))}\nSubiect original: {e['subject']}\nSursa: Eva-Mail; text API integral, nu MIME original. Fara atasamente.\n\nTEXT ORIGINAL NEMODIFICAT\n\n"+e['text']
 save(txtpath,text);saved[e['id']]={'txt':txtpath.as_posix(),'json':jpath.as_posix()}
 r['comunicatii'].append({'data':ld.strftime('%Y.%m.%d'),'ora_utc':dt.strftime('%H:%M:%S'),'partener':partner,'domeniu':'Structura / intalnire contract','sens':sens,'subiect':e['subject'],'expeditor':e['from_address'],'destinatari':e['to'],'cc':e.get('cc',[]),'id':e['id'],'cale':txtpath.as_posix(),'json':jpath.as_posix(),'atasamente':[],'trunchiat':False,'data_preluarii':day})
sentmap={'91f9677a-b370-4b35-afc2-5f88eb54b8fc':'3bdd4db8-4206-4142-9ece-4524d95e6898','2c18f361-7c05-42f0-8583-63bb5d94aa64':'57452296-d26a-47a8-bb8f-18031c022b2d'}
checks={x['id']:x for x in p['draftchecks']};assert len(checks)==2 and all(x['status']=='sent' for x in checks.values())
for d in r['drafturi']:
 if d['id'] in sentmap:
  ds=checks[d['id']];eid=sentmap[d['id']]
  d.setdefault('istoric_verificari_statut',[]).append({'data':day,'checked_at_iso':stamp,'statut_EVA':'sent','email_id_trimis':eid,'sursa':proof.as_posix()})
  d['statut']='TRIMIS; EVA sent si mesaj din Sent citit integral'
  d['sursa_statut']=proof.as_posix();d['id_email_trimis']=eid;d['cale_email_trimis']=saved[eid]['txt'];d['updated_at']=ds['updated_at']
  d['nota_fisiere_istorice']='Snapshoturile de creare DRAFT/NETRIMIS sunt pastrate ca istoric; nu descriu statutul curent.'
  d['intalnire_propusa']['confirmare_beneficiar']='TRIMISA, verificata in Sent'
  d['intalnire_propusa']['confirmata_prin_trimiterea_draftului']=True
sync={m['email']:m.get('last_sync') for m in p['mailboxes']['mailboxes']}
entry={'data':day,'checked_at_iso':stamp,'parteneri':['Markus Berger','Pech'],'mesaje_noi':3,'mesaje_trimise_noi':2,'mesaje_primite_noi':1,'atasamente_noi':0,'query_count':25,'page_count':25,'perioada':'2026.10.25–2026.10.26, suprapunere de o zi fata de controlul din 2026.10.26 09:57; deduplicare cu registrul si verificarea generala','paginare_completa':True,'sincronizare_office':sync['office@ac-wohnart.at'],'sincronizare_gmail':sync['covaciu.gnm@gmail.com'],'sursa':proof.as_posix(),'new_email_ids':list(saved)}
bstatus='2026.10.26: intalnirea BERGER din 2026.10.27, 11:30 ora Vienei (12:30 Romania), Schönbrunner Straße 123/2, 1050 Wien, este confirmata prin emailul nostru TRIMIS si raspunsul BERGER «Perfekt!». Nu reprezinta acceptarea contractului sau intalnire efectuata.'
pstatus='2026.10.26: confirmarea noastra pentru PECH, 2026.10.27 la 14:00 ora Vienei (15:00 Romania), Johann-Strauß-Gasse 32/6, 1040 Wien, este TRIMISA, cu CC ployer@zt-pech.at. Nu exista raspuns PECH nou la acest control; mesajul din 2026.10.22 conditiona confirmarea de venirea la birou, acceptata in emailul nostru. Fara acceptare de contract ori intalnire efectuata.'
sections={}
for s in r['statusuri']:
 if s.get('partener') not in ('Markus Berger','Pech'):continue
 partner=s['partener'];berger=partner=='Markus Berger';status=bstatus if berger else pstatus
 sources=[saved[x]['txt'] for x in (['3bdd4db8-4206-4142-9ece-4524d95e6898','5d82d6a2-e415-498e-84d0-b1ef52269063'] if berger else ['57452296-d26a-47a8-bb8f-18031c022b2d'])]
 if not berger:sources+=['08. Corespondenta/2026.10.23 Verificare zilnica/2026.10.22 17-52-22 PRIMIT Pech c7338d5a.txt']
 s['status']=status;s['ultima_comunicare']=day
 if berger:
  s['ultimul_primit']=day;s['subiect_ultimul_primit']=next(e['subject'] for e in p['full_emails'] if e['id']=='5d82d6a2-e415-498e-84d0-b1ef52269063')
  s['ultimul_raspuns']='2026.10.26 11:28:15 Romania: BERGER raspunde «Perfekt!» la confirmarea pentru 2026.10.27, 11:30 ora Vienei, cu adresa Schönbrunner Straße 123/2.'
 s['urmatorul_pas']='Participarea la intalnirea din 2026.10.27 si clarificarea contractului pe checklist; consemnarea rezultatului in scris.' if berger else 'Participarea la discutia PECH din 2026.10.27, 14:00 Viena; urmarirea unui eventual raspuns suplimentar si clarificarea AN01/AN02 si clauzelor contractuale.'
 s['sursa_status']=sources;s['nivel']='Sinteza verificata pe mesajele integrale si statusurile EVA ale ciornelor'
 s['verificare_punctuala_BERGER_PECH_2026_10_26']={'checked_at_iso':stamp,'mesaje_noi':2 if berger else 1,'sursa':proof.as_posix()}
 sections[partner]=partner+'\nStatus scurt: '+status+'\nUltimul raspuns: '+s.get('ultimul_raspuns','vezi sursa anterioara')+'\nUrmatorul pas: '+s['urmatorul_pas']+'\nSurse: '+'; '.join(sources)+'\n'
r['acoperire']['verificare_punctuala_BERGER_PECH']=entry;r.setdefault('verificari_parteneri',[]).append(entry)
assert r['acoperire']['verificare_incrementala']==general
assert len({x['id'] for x in r['comunicatii']})==len(r['comunicatii'])==839
coverage=f"Acoperire: 25 cautari/25 pagini paginate integral, primite si trimise din office si Gmail, global dupa domenii, adrese, firme, Schallergasse si 2026-470/R09, inclusiv nelivrari. 3 ID-uri noi fata de 836 arhivate, total 839. Nicio nelivrare noua sau atasament nou.\nSincronizare Romania: office {local(sync['office@ac-wohnart.at'])}; Gmail {local(sync['covaciu.gnm@gmail.com'])}. Mesajele ulterioare pot lipsi; shared/team nesearchable excluse.\n"
header=day+' '+now.strftime('%H:%M:%S')+' | VERIFICARE BERGER/PECH\n'
txt=header+'Noutati: BERGER confirma intalnirea prin «Perfekt!». Ambele confirmari ale beneficiarului sunt deja TRIMISE; ciornele EVA au statut sent, confirmat prin cele doua mesaje Sent. Acest agent nu a trimis emailuri.\n\n'+'\n'.join(sections.values())+'\n'+coverage+'Nu exista modificari de pret, servicii sau acceptari contractuale in cele trei mesaje noi. Contractele si ofertele nu au fost modificate. Nu s-au semnat contracte sau efectuat plati.\nSursa: '+proof.as_posix()+'\n'
jsave(regpath,r);jsave(proof,{'verificare':entry,'baseline_unique_ids':836,'final_unique_ids':839,'dovezi_originale':p,'fisiere_mesaje_noi':saved,'general_baseline':general,'nota':'Ciornele istorice NETRIMIS sunt pastrate. Statutul curent sent este documentat separat. Nu s-a trimis nimic prin aceasta verificare.'})
save(report,txt)
for name in ('Status proiect','Log progres proiect'):
 path=Path(day+' '+name+'.txt');save(path,txt+'\nISTORIC PASTRAT\n\n'+(root/path).read_text(encoding='utf-8-sig'))
for partner,section in sections.items():
 path=base/'Parteneri'/(day+' Log discutii - '+partner+'.txt');save(path,header+section+'\n'+coverage+'Sursa: '+proof.as_posix()+'\n\nISTORIC PASTRAT\n\n'+(root/path).read_text(encoding='utf-8-sig'))
path=Path('folder map/README.md');save(path,txt+'Raport: ../'+report.as_posix()+'\n\nISTORIC PASTRAT\n\n'+(root/path).read_text(encoding='utf-8-sig'))
print(json.dumps({'entry':entry,'new_files':saved,'report':report.as_posix()},ensure_ascii=False))
