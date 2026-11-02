import json, hashlib, shutil
from pathlib import Path
from datetime import datetime, timezone, timedelta

root=Path.cwd()
day='2026.10.23'
now=datetime.now(timezone(timedelta(hours=3)))
assert now.strftime('%Y.%m.%d')==day
stamp=now.isoformat()
base=Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail')
oldreg=base/'2026.10.22 Registru comunicatii.json'
regpath=base/(day+' Registru comunicatii.json')
folder=Path('08. Corespondenta')/(day+' Verificare zilnica')
folder.mkdir(parents=True,exist_ok=True)
proofpath=folder/(day+' Dovezi verificare EVA.json')
reportpath=folder/(day+' Raport verificare zilnica.txt')
history=Path('folder map')/(day+' Istoric verificare '+now.strftime('%H-%M-%S'))
history.mkdir(parents=True,exist_ok=True)
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,s):
 p=Path(p)
 if p.exists():
  h=history/p
  h.parent.mkdir(parents=True,exist_ok=True)
  shutil.copy2(p,h)
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(s,encoding='utf-8')
def jsave(p,o):save(p,json.dumps(o,ensure_ascii=False,indent=2))
payload=read('folder map/2026.10.23 Dovezi etapa monitorizare.json')
r=read(oldreg)
known={x['id'] for x in r['comunicatii']}
assert len(known)==len(r['comunicatii'])==834
e=next(x for x in payload['full_emails'] if x['id']=='c7338d5a-3f90-44e6-8843-17681af20732')
assert not e['truncated'] and not e['attachments']
ep=folder/'2026.10.22 17-52-22 PRIMIT Pech c7338d5a.txt'
ej=ep.with_suffix('.json')
jsave(ej,{'data_lizibila':'2026.10.22','statut':'PRIMIT','original_EVA':e,'sursa':'Eva-Mail get_email; corp integral, nu export MIME original'})
save(ep,'Data: 2026.10.22; ora Romania: 17:52:22; data tehnica originala: '+e['received_at']+'\nStatut: PRIMIT\nID Eva-Mail: '+e['id']+'\nCont: '+e['account_email']+'\nExpeditor: '+e['from_address']+'\nDestinatari: '+', '.join(e['to'])+'\nCC: '+', '.join(e['cc'])+'\nSubiect original: '+e['subject']+'\nSursa: Eva-Mail; corp API integral, nu MIME original\n\nTEXT ORIGINAL NEMODIFICAT\n\n'+e['text'])
r['comunicatii'].append({'data':'2026.10.22','ora_utc':'14:52:22','partener':'Pech','domeniu':'Constructii - Consultanta','sens':'PRIMIT','subiect':e['subject'],'expeditor':e['from_address'],'destinatari':e['to'],'cc':e['cc'],'id':e['id'],'cale':ep.as_posix(),'json':ej.as_posix(),'atasamente':[],'trunchiat':False,'data_preluarii':day})
wohr=[x for x in payload['pending_incidental'] if x.get('raportare_generala_pendenta')]
assert {x['email_id'] for x in wohr}=={'311d134f-5056-4f7b-bb04-9fda1fb94fc6','c79e7db0-ee20-42db-9c20-43259139527a'}
for p in wohr:assert Path(p['sursa']).is_file()
ps='PECH raspunde la 2026.10.22 17:52:22 Romania: dl. Ployer poate confirma 2026.10.27 14:00 ora Vienei, cu conditia ca beneficiarul sa vina la biroul PECH pentru discutarea contractului. Confirmare conditionata de deplasarea beneficiarului, nu acceptare/semnare contract. Adresa din semnatura: Johann-Strauß-Gasse 32/6, 1040 Wien.'
pn='Confirmarea disponibilitatii de a veni la biroul PECH la 2026.10.27 14:00 Viena (15:00 Romania); pregatirea punctelor contractuale, fara acceptarea ofertei prin acest control.'
ws='A&C a trimis la 2026.10.22 15:10:22 Romania confirmarea ca mentenanta WÖHR poate avea loc la 2026.10.27 07:00–10:00 ora Vienei; WÖHR a raspuns multumind la 15:32:35. Programare viitoare acceptata de beneficiar, raspuns de multumire primit; lucrarea nu este executata/confirmata ca efectuata.'
wn='Organizarea accesului, eliberarii tuturor locurilor de masini/obiecte, informarii utilizatorilor si afisarii anuntului pentru 2026.10.27 07:00–10:00 Viena, conform cerintelor WÖHR deja arhivate.'
bs='Fara raspuns nou BERGER la propunerea de intalnire din 2026.10.27 11:00 Viena; propunerea trimisa este deja raportata, ora/locul raman neconfirmate in emailurile disponibile.'
mailboxes=payload['mailboxes']['mailboxes']
syncs={m['email']:m.get('last_sync') for m in mailboxes}
entry={'data':day,'checked_at_iso':stamp,'perioada':'2026.10.21–2026.10.23; suprapunere de o zi fata de verificarea generala 2026.10.22','cautari_complete':len({json.dumps({k:v for k,v in p['args'].items() if k!='offset'},sort_keys=True) for p in payload['pages']}),'pagini':len(payload['pages']),'paginare_completa':not payload['errors'],'acoperire_actuala_office_completa':True,'mesaje_noi_ID':1,'mesaje_primite_ID':1,'mesaje_trimise_ID':0,'documente_originale_integrale_ID':0,'oferta_noua_identificata':False,'mesaje_deja_arhivate_raportate_acum':[x['email_id'] for x in wohr],'sincronizari_originale':syncs,'stare':'Raspuns PECH privind intalnirea, conditionata de venirea beneficiarului la birou; WÖHR confirmare trimisa si multumire primita, preluate pentru raportarea generala. Fara oferte/preturi/documente noi.','limite':'Office pana la 2026.10.23 08:00:16 Romania; Gmail pana la 2026.10.23 03:25:32 Romania; mesajele ulterioare pot lipsi. Cosmin@ig.ro ramas la 2026.10.10 02:30:10 Romania. Shared/team nesearchable excluse. Newsletterul JINHAN are corp trunchiat de API, exclus pe baza fragmentului; mesajul relevant PECH este integral.','sursa':proofpath.as_posix()}
assert entry['cautari_complete']==64 and entry['pagini']==64
for p in payload['pages']:
 assert p['args']['offset']+len(p['result']['items'])>=p['result']['total']
r.setdefault('istoric_verificari_incrementale',[]).append(r['acoperire']['verificare_incrementala'])
r['acoperire']['verificare_incrementala']=entry
r['acoperire']['mesaje_salvate']=835
r['data_actualizarii']=day
r.setdefault('actualizari_punctuale',[]).append({'data':day,'tip':'Verificare generala','mesaje_noi':1,'mesaje_deja_arhivate_raportate_acum':2,'sursa':proofpath.as_posix()})
sources={'Pech':[ep.as_posix(),proofpath.as_posix()],'WOHR':[x['sursa'] for x in wohr]+[proofpath.as_posix()]}
for s in r['statusuri']:
 partner=s.get('partener')
 if partner in ('Pech','WOHR'):
  old={k:s.get(k) for k in ('status','ultimul_raspuns','ultima_comunicare','ultimul_primit','urmatorul_pas','sursa_status')}
  s.setdefault('istoric_status',[]).append({'data_preluarii':day,**old})
  s.update({'status':ps if partner=='Pech' else ws,'ultimul_raspuns':ps if partner=='Pech' else '2026.10.22: WÖHR multumeste pentru confirmarea beneficiarului; sursa arhivata.','urmatorul_pas':pn if partner=='Pech' else wn,'ultima_comunicare':'2026.10.22','ultimul_primit':'2026.10.22','sursa_status':sources[partner],'data_actualizarii':day,'sursa_ultimul_primit':ep.as_posix() if partner=='Pech' else wohr[1]['sursa']})
  if partner=='Pech':s['subiect_ultimul_primit']=e['subject']
  s['mesaje']=sum(x.get('partener')==partner for x in r['comunicatii'])
 if partner in ('Pech','WOHR','Markus Berger'):
  s['verificare_comunicari_2026_10_23']={'data':day,'mesaje_noi':1 if partner=='Pech' else 0,'sursa':proofpath.as_posix()}
for p in r['mesaje_incidentale_pentru_verificare_generala']:
 if p.get('email_id') in {x['email_id'] for x in wohr}:
  p.update({'raportare_generala_pendenta':False,'data_integrarii':day,'raport':reportpath.as_posix(),'statut':'Integrat la prima raportare generala 2026.10.23, fara dublarea ID-ului'})
jsave(regpath,r)
proof={'verificare':entry,'baseline_register':oldreg.as_posix(),'baseline_ID_count':834,'final_ID_count':835,'new_relevant_email_ids':[e['id']],'already_archived_now_reported':wohr,'previously_reported_not_repeated':['cd0b4652-d283-4f66-ac8a-19abbdbf7740','40504a61-9760-482c-b35f-b00953971508'],'dovezi_originale':payload,'nota':'Fara email trimis, contract modificat/semnat, calendar creat ori plata efectuata. Fara atasamente noi de descarcat; originalele WÖHR si PECH din verificarile precedente raman arhivate.'}
jsave(proofpath,proof)
header=day+' — Verificare zilnica Schallergasse 35\nVerificat: '+stamp+'\n\n'
pech='PECH\nStatus scurt: '+ps+'\nUltimul raspuns: mesaj PRIMIT, ID '+e['id']+'; fara atasamente.\nUrmatorul pas: '+pn+'\nSursa: '+ep.as_posix()+'\n'
wohrtext='WÖHR — preluare pentru prima raportare generala\nStatus scurt: '+ws+'\nUltimul raspuns: WÖHR multumeste pentru raspunsul A&C; nu adauga preturi sau servicii.\nUrmatorul pas: '+wn+'\nSurse: '+'; '.join(x['sursa'] for x in wohr)+'\n'
coverage='ACOPERIRE\n64 cautari/64 pagini paginate integral, toate mesajele office primite si trimise si cautari globale dupa adresa, firme si referinte; 2026.10.21–2026.10.23. Comparatie cu 834 ID-uri, acum 835. Un mesaj relevant nou, citit integral, fara atasamente noi. Cele doua mesaje WÖHR sunt deja arhivate, acum raportate general; propunerile trimise BERGER/PECH sunt deja raportate, nu se repeta ca noutati. Marketingul ARTUS, Wizz Air, nobilacasa si JINHAN este exclus; JINHAN trunchiat, numai fragment citit.\n'+entry['limite']+'\nSursa: '+proofpath.as_posix()+'\nNu s-au trimis emailuri, modificat documente comerciale, semnat contracte sau efectuat plati.\n'
report=header+'NOUTATI FATA DE ULTIMA RAPORTARE\n\n'+pech+'\n'+wohrtext+'\nALTE VERIFICARI\n'+bs+'\nNu s-au identificat alte comunicari relevante noi, oferte, modificari de pret, confirmari de incasare ori decizii contractuale.\n\n'+coverage
save(reportpath,report)
for stem in ('Status proiect','Log progres proiect'):
 old=Path('2026.10.22 '+stem+'.txt')
 save(Path(day+' '+stem+'.txt'),report+'\nISTORIC PASTRAT\n\n'+old.read_text(encoding='utf-8-sig'))
for partner,text in [('Pech',pech),('WOHR',wohrtext),('Markus Berger','BERGER\nStatus scurt: '+bs+'\nUltimul raspuns: 2026.10.21, deja arhivat; solicita analiza peste weekend.\nUrmatorul pas: urmarirea confirmarii orei/locului si a observatiilor contractuale.\nSursa verificarii: '+proofpath.as_posix()+'\n')]:
 old=base/'Parteneri'/('2026.10.22 Log discutii - '+partner+'.txt')
 save(base/'Parteneri'/(day+' Log discutii - '+partner+'.txt'),header+text+'\n'+coverage+'\nISTORIC PASTRAT\n\n'+old.read_text(encoding='utf-8-sig'))
readme=Path('folder map/README.md')
save(readme,report+'\nPuncte curente: ../'+regpath.as_posix()+'; ../'+day+' Status proiect.txt; ../'+day+' Log progres proiect.txt. Registrul de atasamente ramane 2026.10.22, fara anexe noi.\n\nISTORIC PASTRAT\n\n'+readme.read_text(encoding='utf-8-sig'))
assert len(r['comunicatii'])==len({x['id'] for x in r['comunicatii']})==835
print(json.dumps({'register':regpath.as_posix(),'report':reportpath.as_posix(),'proof':proofpath.as_posix(),'email':ep.as_posix(),'count':835,'new_attachments':0,'entry':entry},ensure_ascii=False))
