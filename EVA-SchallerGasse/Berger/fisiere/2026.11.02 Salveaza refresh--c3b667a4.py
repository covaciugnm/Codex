from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,hashlib,shutil,re
root=Path.cwd();day='2026.11.02';now=datetime.now(ZoneInfo('Europe/Bucharest'));stamp=now.isoformat(timespec='seconds');tag=now.strftime('%H-%M-%S');base=Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail');out=Path('08. Corespondenta')/(day+' Refresh manual');hist=Path('folder map')/(day+' Istoric refresh '+tag);changed=[]
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,t):
 p=Path(p)
 if p.exists():
  b=hist/p;b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,b)
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8');changed.append(p.as_posix())
def jsave(p,d):save(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def prepend(p,t,prior=None):
 p=Path(p);old=p.read_text(encoding='utf-8-sig') if p.exists() else Path(prior).read_text(encoding='utf-8-sig') if prior and Path(prior).exists() else ''
 save(p,t+'\n\nISTORIC PASTRAT\n\n'+old)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def digest(d):return hashlib.sha256(json.dumps(d,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def local(s):return datetime.fromisoformat(s.replace('Z','+00:00')).astimezone(ZoneInfo('Europe/Bucharest')).strftime('%Y.%m.%d %H:%M:%S')
p=read('folder map/2026.11.02 Dovezi refresh etapa.json');r=read(p['baseline_register']);ar=read(base/'2026.11.01 Registru atasmente.json') if (base/'2026.11.01 Registru atasmente.json').exists() else read(base/'2026.11.01 Registru atasamente.json');assert not p['errors'];oldcount=len(r['comunicatii']);draft_hash=digest(r['drafturi']);e=p['new_email_redactat'];assert not e['truncated'] and e['id']=='419532fa-fa26-4228-8b90-149e310773e8';known={x['id'] for x in r['comunicatii']};aliases={x['alias_id']:x['canonical_id'] for x in r.get('aliasuri_email_EVA',[])};assert e['id'] not in known
groups={}
for page in p['pages']:
 key=json.dumps({k:v for k,v in page['args'].items() if k!='offset'},sort_keys=True);groups.setdefault(key,[]).append(page)
for group in groups.values():
 offset=0
 for page in sorted(group,key=lambda x:x['args']['offset']):
  assert page['args']['offset']==offset;offset+=len(page['result']['items'])
 assert offset>=group[-1]['result']['total']
meta={x['id']:x for pg in p['pages'] for x in pg['result']['items']};excluded=[]
for x in meta.values():
 if aliases.get(x['id'],x['id']) in known or x['id']==e['id']:continue
 assert x.get('account_email')!='office@ac-wohnart.at',(x['id'],x['subject'])
 assert not re.search(r'berger|pech|schaller|wohnart',json.dumps(x,ensure_ascii=False),re.I),(x['id'],x['subject'])
 excluded.append({'id':x['id'],'motiv':'Mesaj personal/comercial/logistic Gmail fara referinta la proiect ori BERGER/PECH; fara nelivrare relevanta.'})
assert e['attachments']==[] and e['is_sent']==False
jp=out/'2026.11.01 20-59-07 PRIMIT BERGER 419532fa.json';tp=jp.with_suffix('.txt');original=p['manifest_original_integral'];assert sha(original['cale'])==original['encrypted_sha256'];changed.append(original['cale'])
jsave(jp,{'data_lizibila':local(e['received_at'])+' Romania','statut':'PRIMIT','original_EVA_copie_lizibila':e,'original_integral':original,'nota':'Numai parola din citatul istoric este redactata in copia lizibila; noul raspuns BERGER si metadatele sunt nemodificate. Originalul integral este conservat criptat DPAPI pentru utilizatorul Windows curent, cu decriptare verificata identica. Export API, nu MIME original.'})
save(tp,'Data: '+local(e['received_at'])+' Romania\nStatut: PRIMIT\nSubiect: '+e['subject']+'\nExpeditor: '+e['from_address']+'\nDestinatari: '+', '.join(e['to'])+'\nCC: '+', '.join(e['cc'])+'\nID Eva-Mail: '+e['id']+'\nAtasamente: niciunul\nEtichete EVA: '+str(e['labels'])+'\nNota: parola citata din mesajul istoric este redactata aici; originalul integral este conservat separat criptat.\nSursa JSON: '+jp.as_posix()+'\n\nTEXT MESAJ\n\n'+e['text'])
row={'data':'2026.11.01','ora_utc':'18:59:07','partener':'Markus Berger','domeniu':'Proiectare / acces documentatie / proiect de executie DG','sens':'PRIMIT','subiect':e['subject'],'expeditor':e['from_address'],'destinatari':e['to'],'cc':e['cc'],'id':e['id'],'cale':tp.as_posix(),'json':jp.as_posix(),'original_integral_criptat':original['cale'],'atasamente':[],'trunchiat':False,'data_preluarii':day,'etichete_EVA':e['labels']}
r['comunicatii'].append(row)
idx={x['cale']:x for x in read('folder map/inventar.json')};verified=[]
contractdir='00.Proiect/09. Vertraege/bmberger.at/2026.10.29 Werkvertrag R11'
for rel,i in idx.items():
 if rel.startswith(contractdir+'/') and rel.endswith('.pdf'):
  actual=sha(rel);assert actual==i['sha256'];verified.append({'cale':rel,'sha256':actual,'reutilizat':True})
assert len(verified)==2
newer=[x for x in idx if 'bmberger.at/' in x and re.search(r'(Werkvertrag|contract).*R(1[2-9]|[2-9]\d)',Path(x).name,re.I)];assert not newer,newer
ics=Path('08. Corespondenta/2026.10.29 Verificare Berger Pech/2026.10.29 15-03-39 PRIMIT BERGER d5bc6ece.ics');assert sha(ics)==idx[ics.as_posix()]['sha256'];icst=re.sub(r'\n[ \t]','',ics.read_text(encoding='utf-8-sig').replace('\r\n','\n'));uid=re.search(r'^UID:(.+)$',icst,re.M).group(1)
assert 'SEQUENCE:2' in icst and 'DTSTART;TZID=W. Europe Standard Time:20261102T140000' in icst and 'DTEND;TZID=W. Europe Standard Time:20261102T143000' in icst and 'PARTSTAT=NEEDS-ACTION' in icst
calendar=[x for x in p['calendar_readback']['items'] if x.get('title')=='Baubesprechung'];assert len(calendar)==1 and calendar[0]['start']=='2026-10-29T11:00:00Z'
assert p['berger_draft']['status']=='sent' and p['pech_draft']['status']=='pending'
sent=next(x for x in r['comunicatii'] if x['id']=='96e74e69-7ff6-402c-9959-597c0b472950');assert sent['sens']=='TRIMIS' and len(sent['atasamente'])==3
status=next(x for x in r['statusuri'] if x.get('partener')=='Markus Berger');status.setdefault('istoric_status',[]).append({'data_preluarii':day,**{k:status.get(k) for k in ('status','ultimul_raspuns','urmatorul_pas','sursa_status')}})
status.update({'status':'2026.11.01 20:59:07 Romania: BERGER spune ca este pe platforma si apreciaza prezentarea; nu a gasit un Ausführungsplan pentru Dachgeschoss. Accesarea paginii este confirmata de propriul mesaj, fara confirmarea exhaustivitatii setului de documente. Nicio observatie comerciala noua la R11 si nicio anexa.','ultimul_raspuns':'Einen Ausführungsplan für das Dachgeschoss habe ich noch nicht gefunden.','urmatorul_pas':'Clarificare cu arhitectul si BERGER: ce plan de executie DG este necesar, ce versiune exista si cine il furnizeaza/publica. Planselor DG din arhiva nu li se atribuie automat statut de proiect de executie verificat. Ultima invitatie indica 2026.11.02 14:00–14:30 Viena/15:00–15:30 Romania; RSVP NEEDS-ACTION si calendar vechi, neschimbate. Raman de confirmat clauzele comerciale si tehnice R11, fara acceptare presupusa.','sursa_status':[tp.as_posix(),jp.as_posix(),ics.as_posix()],'ultima_comunicare':'2026.11.01','ultimul_primit':'2026.11.01','subiect_ultimul_primit':e['subject'],'data_actualizarii':day})
pech=next(x for x in r['statusuri'] if x.get('partener')=='Pech');pech['refresh_2026_11_02']={'checked_at_iso':stamp,'mesaje_noi':0,'draft_amanare':p['pech_draft']['id'],'status':'pending / NETRIMIS','nota':'2026.11.03 este doar data propusa in draft; nici trimitere, nici confirmare PECH identificata.'}
plan_candidates=[{'cale':x['cale'],'stare':'Candidat din nume/index; nu confirmare tehnica ori document cu statut de executie verificat'} for x in idx.values() if x['cale'].startswith('03. Proiectare/Arhitectura Madalina/') and x['extensie']=='.pdf' and re.search(r'Dachgeschoss',Path(x['cale']).name,re.I)]
# Keep draft history untouched; readbacks are verification evidence only.
assert digest(r['drafturi'])==draft_hash
proof=out/(day+' '+tag+' Dovezi refresh.json');report=out/(day+' '+tag+' Raport refresh.txt')
syncp={x['email']:x.get('last_sync') for x in p['mailboxes_primary']['mailboxes']};syncs={x['email']:x.get('last_sync') for x in p['mailboxes_secondary']['mailboxes']}
limits='Ultima sincronizare afisata: office Primary '+local(syncp['office@ac-wohnart.at'])+'; Gmail '+local(syncp['covaciu.gnm@gmail.com'])+'; office secundar '+local(syncs['office@ac-wohnart.at'])+' Romania. Mesajele ulterioare neindexate pot lipsi; shared/team necautabile excluse.'
entry={'data':day,'checked_at_iso':stamp,'tip':'Refresh manual general + checklist BERGER/PECH','perioada':p['period'],'cautari_complete':len(groups),'pagini':len(p['pages']),'paginare_completa':True,'acoperire_actuala_office_completa':True,'control_Gmail_primit_trimis':True,'metadate_unice_ID':len(meta),'mesaje_noi_ID':1,'mesaje_noutati_neraportate':1,'mesaje_BERGER_noi':1,'mesaje_PECH_noi':0,'atasamente_noi_ID':0,'continuturi_documentare_noi':0,'oferta_noua_identificata':False,'sincronizari_originale_primary':syncp,'sincronizari_originale_secondary':syncs,'sursa':proof.as_posix(),'raport':report.as_posix(),'limite':limits,'stare':'BERGER a accesat platforma, dar nu a gasit proiectul de executie DG. Fara raspuns comercial R11 ori anexe noi. PECH fara comunicari noi, draft de amanare pending.'}
r.setdefault('istoric_verificari_incrementale',[]).append(r['acoperire']['verificare_incrementala']);r['acoperire']['verificare_incrementala']=entry;r['acoperire']['verificare_punctuala_BERGER']=entry;r.setdefault('verificari_parteneri',[]).append(entry);r['data_actualizarii']=day
checks=[
{'punct':1,'criteriu':'Mesaje si nelivrari','rezultat':'UN MESAJ NOU BERGER','detalii':'Raspuns primit 2026.11.01 20:59:07 Romania; eticheta EVA SPAM-ALERT. Nicio nelivrare BERGER/PECH identificata.','surse':[tp.as_posix()]},
{'punct':2,'criteriu':'Raspunsuri contract / versiune','rezultat':'R11 NEMODIFICAT','detalii':'Nicio acceptare, observatie comerciala sau contrapropunere noua. Cele doua PDF-uri R11/comparatie au hash identic indexului.','surse':verified},
{'punct':3,'criteriu':'Preturi si servicii','rezultat':'FARA MODIFICARI DE PRET','detalii':'Propunerea R11 ramane 45.000 net baza +2.500 net Bauwerksbuch=47.500 net/57.000 brut; 8 vizite si pachete suplimentare 1.000 net/4 vizite, fara acceptare noua. Planul de executie arhitectural DG ramane rol extern, fara atribuire noua BERGER.','surse':[sent['cale'],tp.as_posix()]},
{'punct':4,'criteriu':'Atasamente / hash','rezultat':'FARA ATASAMENTE NOI','detalii':'Noul email nu are anexe. Originalul integral al mesajului contine credentiale in citatul istoric: conservat DPAPI, copie lizibila redactata numai la parola; nu este contract ori anexa tehnica noua.','surse':[jp.as_posix(),original]},
{'punct':5,'criteriu':'Draft / Sent / acceptare','rezultat':'BERGER SENT, PECH PENDING','detalii':'R11 trimis 2026.10.29 cu trei PDF-uri in Sent. Raspunsul nou este la accesul platformei, nu confirmare ca a citit/acceptat R11. Draftul PECH pentru 2026.11.03 este NETRIMIS, fara amanare acceptata.','surse':[sent['cale'],'berger_draft si pech_draft in dovezi']},
{'punct':6,'criteriu':'ICS / calendar / RSVP','rezultat':'NESCHIMBAT','detalii':'Ultima invitatie SEQUENCE 2, UID verificat: 2026.11.02 14:00–14:30 Viena/15:00–15:30 Romania. NEEDS-ACTION. Calendarul EVA afiseaza inca evenimentul 2026.10.29; fara intalnire efectuata ori RSVP presupus.','surse':[ics.as_posix(),'calendar_readback in dovezi'],'uid':uid},
{'punct':7,'criteriu':'Actiuni / documente','rezultat':'CLARIFICARE NOUA: PLAN EXECUTIE DG','detalii':status['urmatorul_pas'],'surse':[tp.as_posix()]}
]
jsave(base/(day+' Registru comunicatii.json'),r);jsave(base/(day+' Registru atasamente.json'),ar)
summary=f"""{day} {now.strftime('%H:%M:%S')} | REFRESH MANUAL SCHALLERGASSE 35
Status scurt: Un raspuns nou BERGER; fara oferte, preturi ori anexe noi. PECH fara comunicari noi.
Ultimul raspuns BERGER: 2026.11.01 20:59:07 Romania, mesaj PRIMIT 419532fa. Spune ca este pe platforma si apreciaza prezentarea, dar nu a gasit planul de executie al mansardei (Ausführungsplan für das Dachgeschoss).
Raspunsul confirma accesarea paginii, nu verificarea exhaustiva a documentatiei, primirea/acceptarea R11 ori contract semnat.
Urmatorul pas: {status['urmatorul_pas']}
Surse email: {tp.as_posix()}; {jp.as_posix()}.

CHECKLIST
"""
for c in checks:summary+=str(c['punct'])+'. '+c['criteriu']+' — '+c['rezultat']+'\n'+c['detalii']+'\nSurse: '+str(c['surse'])+'\n\n'
summary+='Planse DG candidate exista in arhiva Arhitectura Madalina, dar indexul/numele nu confirma un set de executie complet, aprobat, actual ori publicat pe platforma. Nu se confunda planul de autorizare cu proiectul de executie. Nicio modificare de planuri sau publicare efectuata.\n'+str(len(groups))+' cautari/'+str(len(p['pages']))+' pagini complete; '+str(len(meta))+' ID-uri metadate. O comunicatie relevanta noua; '+str(len(excluded))+' metadate Gmail fara legatura excluse. Registru '+str(oldcount)+' -> '+str(len(r['comunicatii']))+'.\n'+limits+'\nNu s-au trimis emailuri/RSVP, modificat contracte sau calendar, semnat ori platit.\nSursa verificare: '+proof.as_posix()+'\n'
save(report,summary)
for name in ('Status proiect','Log progres proiect'):prepend(day+' '+name+'.txt',summary,'2026.11.01 '+name+'.txt')
for partner,s in [('Markus Berger',status),('Pech',pech)]:
 dest=base/'Parteneri'/(day+' Log discutii - '+partner+'.txt');prior=next((x for x in reversed(sorted((base/'Parteneri').glob('* Log discutii - '+partner+'.txt'))) if x.name<dest.name),None)
 text=day+' | '+partner+'\nStatus scurt: '+s['status']+'\nUltimul raspuns: '+s.get('ultimul_raspuns','')+'\nUrmatorul pas: '+s['urmatorul_pas']+'\nRefresh: '+('Email nou privind planul de executie DG.' if partner=='Markus Berger' else 'Fara noutati; ciorna amanare pending, NETRIMIS.')+'\nSurse: '+str(s.get('sursa_status',[]))+'\nSursa verificare: '+proof.as_posix()+'\n'+limits
 prepend(dest,text,prior)
prepend('folder map/README.md',summary+'\nRaport: ../'+report.as_posix())
jsave(proof,{'verificare':entry,'checklist':checks,'baseline_unique_ids':oldcount,'final_unique_ids':len(r['comunicatii']),'new_email_id':e['id'],'new_email_export':row,'excluderi':excluded,'planuri_DG_candidate_neconfirmate_tehnic':plan_candidates,'original_integral_protejat':original,'dovezi_originale':p})
Path('folder map/2026.11.02 Fisiere actualizate refresh.json').write_text(json.dumps(changed,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'report':report.as_posix(),'proof':proof.as_posix(),'email':tp.as_posix(),'new_messages':1,'register_count':len(r['comunicatii'])},ensure_ascii=False))

