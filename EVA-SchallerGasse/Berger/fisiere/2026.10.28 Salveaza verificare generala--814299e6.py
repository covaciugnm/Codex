from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json, hashlib, shutil

ROOT=Path(__file__).resolve().parent.parent
DAY='2026.10.28';PREV='2026.10.27';TZ=ZoneInfo('Europe/Bucharest')
NOW=datetime.now(TZ);STAMP=NOW.isoformat(timespec='seconds')
BASE=Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail')
OUT=Path('08. Corespondenta')/(DAY+' Verificare zilnica')
PROOF=OUT/(DAY+' Dovezi verificare EVA.json')
REPORT=OUT/(DAY+' Raport verificare zilnica.txt')
HIST=Path('folder map')/(DAY+' Istoric verificare '+NOW.strftime('%H-%M-%S'))

def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def save(p,t):
    p=Path(p);dest=ROOT/p
    if dest.exists():
        backup=ROOT/HIST/p;backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dest,backup)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(t.encode('utf-8'))
def jsave(p,d):save(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def dt(s):return datetime.fromisoformat(s.replace('Z','+00:00')).astimezone(TZ)
def local(s):return dt(s).strftime('%Y.%m.%d %H:%M:%S') if s else 'indisponibila'
def prepend_new(p,old,t):
    oldtext=(ROOT/p).read_text(encoding='utf-8-sig') if (ROOT/p).exists() else ((ROOT/old).read_text(encoding='utf-8-sig') if (ROOT/old).exists() else '')
    save(p,t+'\n\nISTORIC PASTRAT\n\n'+oldtext)

p=read(Path('folder map/2026.10.28 Dovezi etapa generala.json'))
r=read(Path(p['baseline_register']));ids={x['id'] for x in r['comunicatii']}
assert len(ids)==len(r['comunicatii'])==p['baseline_count']==841
assert len(p['pages'])==66 and not p['errors']
for page in p['pages']:
    assert page['result']['offset']+len(page['result']['items'])>=page['result']['total']
found={x['id']:x for page in p['pages'] for x in page['result']['items']}
new={m['id'] for m in p['emails']};excluded={x['id'] for x in p['exclusions']}
assert len(new)==2 and len(excluded)==1 and set(found)-ids==new|excluded
assert all(not m['truncated'] and not m['is_sent'] and not m['attachments'] for m in p['emails'])
assert not any(x.get('raportare_generala_pendenta') for x in r.get('mesaje_incidentale_pentru_verificare_generala',[]))
old_drafts=hashlib.sha256(json.dumps(r['drafturi'],sort_keys=True,ensure_ascii=False).encode()).hexdigest()
paths={}
for m in p['emails']:
    partner='Markus Berger' if m['from_address']=='office@bmberger.at' else 'Pech'
    clock=dt(m['received_at']);prefix=clock.strftime('%Y.%m.%d %H-%M-%S')+' PRIMIT '+('BERGER' if partner=='Markus Berger' else 'PECH')+' '+m['id'][:8]
    j=OUT/(prefix+'.json');t=OUT/(prefix+'.txt')
    jsave(j,{'data_lizibila':clock.strftime('%Y.%m.%d'),'statut':'PRIMIT','original_EVA':m,'sursa':'Eva-Mail get_email; corp integral, nu export MIME original'})
    header='Data: '+clock.strftime('%Y.%m.%d')+'; ora Romania: '+clock.strftime('%H:%M:%S')+'; data tehnica originala: '+m['received_at']+'\nStatut: PRIMIT\nID Eva-Mail: '+m['id']+'\nCont: '+m['account_email']+'\nExpeditor: '+m['from_address']+'\nDestinatari: '+', '.join(m['to'])+'\nCC: '+', '.join(m['cc'])+'\nSubiect original: '+m['subject']+'\nSursa: Eva-Mail; corp API integral, nu MIME original\n\nTEXT ORIGINAL NEMODIFICAT\n\n'
    save(t,header+m['text'])
    paths[partner]={'txt':t.as_posix(),'json':j.as_posix(),'id':m['id']}
    r['comunicatii'].append({'data':clock.strftime('%Y.%m.%d'),'ora_utc':m['received_at'][11:19],'partener':partner,'domeniu':'Structura / raspuns dupa discutie','sens':'PRIMIT','subiect':m['subject'],'expeditor':m['from_address'],'destinatari':m['to'],'cc':m['cc'],'id':m['id'],'cale':t.as_posix(),'json':j.as_posix(),'atasamente':[],'trunchiat':False,'data_preluarii':DAY})

info={
 'Markus Berger':{
  'status':'2026.10.27 21:52:35 Romania: BERGER oferteaza Bauwerksbuch conform Wiener Bauordnung la 2.500 EUR net suplimentar. Planificarea, autorul planurilor si Planwechsel trebuie stabilite separat. Multumeste pentru intalnire si schimbul de idei; discutia din 2026.10.27 este astfel confirmata, fara acceptare contractuala.',
  'ultimul_raspuns':'2.500 EUR net pentru Bauwerksbuch; celelalte puncte Planung / Panverfasser [sic] / Planwechsel de stabilit individual. Ii este suficienta o decizie de principiu cu Kostennoten; nu este confirmarea unor preturi suplimentare, persoane sau comenzi concrete.',
  'urmatorul_pas':'Clarificare scrisa: Bauwerksbuch pentru existent + interventii noi, inspectie initiala, documente, inregistrare, responsabil si termen; ce include exact pretul de 2.500 EUR net. Stabilirea responsabililor si a costurilor de proiectare/Planwechsel inainte de orice comanda. Propunerea R10 si calendarul joi raman cu punctele deschise anterior; fara acceptare sau RSVP presupus.'},
 'Pech':{
  'status':'2026.10.27 16:50:06 Romania: DI Bernhard Ployer confirma discutia din acea zi si recomanda arhitectul Roland Gasperl pentru sprijin la autoritate si eventuale replanificari/depuneri. Ployer spune ca a discutat deja cu arhitectul. Recomandare, fara oferta de onorariu, mandat sau contract acceptat.',
  'ultimul_raspuns':'Contact recomandat: Arch. Roland Gasperl, Argentinierstrasse 42/12, 1040 Wien; +43 664 4119935; roland.gasperl@chello.at. Niciun raspuns comercial nou la AN01/AN02 sau acceptare a clauzelor.',
  'urmatorul_pas':'Beneficiarul sa decida contactarea arhitectului; daca doreste, obtinerea unui obiect clar (autoritate, replanificare, depuneri), pret, termene si responsabilitati. Reconcilierea cu PECH a cerintelor de proiectare si a contractului scurt draft din 2026.10.27; nicio comanda presupusa.'}}
for s in r['statusuri']:
    partner=s.get('partener')
    if partner in info:
        s.setdefault('istoric_status',[]).append({'data_preluarii':DAY,'status':s.get('status'),'ultimul_raspuns':s.get('ultimul_raspuns'),'urmatorul_pas':s.get('urmatorul_pas'),'sursa_status':s.get('sursa_status')})
        s.update(info[partner],ultima_comunicare=PREV,ultimul_primit=PREV,data_actualizarii=DAY,sursa_status=[paths[partner]['txt'],paths[partner]['json']])
        m=next(x for x in p['emails'] if x['id']==paths[partner]['id']);s['subiect_ultimul_primit']=m['subject']
        s['mesaje']=sum(x.get('partener')==partner for x in r['comunicatii'])
    s['verificare_comunicari_2026_10_28']={'data':DAY,'checked_at_iso':STAMP,'mesaje_noi':1 if partner in info else 0,'sursa':PROOF.as_posix()}

gasperl={'partener':'Roland Gasperl','domeniu':'Arhitectura / autoritate / posibile replanificari','status':'Recomandat de DI Bernhard Ployer (PECH) in emailul primit 2026.10.27; fara comunicare directa, oferta, mandat sau onorariu cunoscut.','ultima_comunicare':PREV,'ultimul_raspuns':'Nu exista raspuns direct al arhitectului. Ployer transmite datele de contact dupa discutia lor.','urmatorul_pas':'Decizia beneficiarului privind contactarea; obtinere obiect, pret si calendar in scris inainte de atribuire.','sursa_status':[paths['Pech']['txt']],'data_actualizarii':DAY,'contact':{'adresa_originala':'Argentinierstrasse 42/12, 1040 Wien','telefon':'+43 664 4119935','email':'roland.gasperl@chello.at'},'mesaje':0}
assert not any(x.get('partener')=='Roland Gasperl' for x in r['statusuri']);r['statusuri'].append(gasperl)

sync={m['email']:m.get('last_sync') for m in p['mailboxes']['mailboxes']}
limits='Office sincronizat pana la '+local(sync['office@ac-wohnart.at'])+' Romania; Gmail pana la '+local(sync['covaciu.gnm@gmail.com'])+' Romania. Mesajele ulterioare pot lipsi. Celelalte casute sunt acoperite pana la sincronizarile individuale din dovada EVA; shared/team nesearchable excluse.'
entry={'data':DAY,'checked_at_iso':STAMP,'perioada':'2026.10.26–2026.10.28; suprapunere de o zi fata de verificarea generala 2026.10.27; comparatie inclusiv cu verificarea BERGER/PECH si arhivarea contractului adnotat din 2026.10.27','cautari_complete':66,'pagini':66,'paginare_completa':True,'acoperire_actuala_office_completa':True,'mesaje_noi_ID':2,'mesaje_primite_ID':2,'mesaje_trimise_ID':0,'documente_originale_integrale_ID':0,'oferta_noua_identificata':True,'mesaje_deja_arhivate_raportate_acum':[],'sincronizari_originale':sync,'stare':'Doua raspunsuri noi dupa discutiile BERGER si PECH; pret nou Bauwerksbuch 2.500 EUR net si recomandare arhitect. Fara atasamente noi, acceptare contractuala, depunere sau plata.','limite':limits,'sursa':PROOF.as_posix()}
r.setdefault('istoric_verificari_incrementale',[]).append(r['acoperire']['verificare_incrementala']);r['acoperire']['verificare_incrementala']=entry;r['data_actualizarii']=DAY
r.setdefault('actualizari_punctuale',[]).append({'data':DAY,'tip':'Verificare generala','mesaje_noi':2,'sursa':PROOF.as_posix()})
assert hashlib.sha256(json.dumps(r['drafturi'],sort_keys=True,ensure_ascii=False).encode()).hexdigest()==old_drafts
assert len(r['comunicatii'])==len({x['id'] for x in r['comunicatii']})==843
newreg=BASE/(DAY+' Registru comunicatii.json');jsave(newreg,r)
proofdata={'verificare':entry,'baseline_register':p['baseline_register'],'baseline_ID_count':841,'final_ID_count':843,'new_relevant_email_ids':sorted(new),'already_archived_now_reported':[],'previously_reported_not_repeated':sorted(set(found)&ids),'excluded_unrelated_email_ids':sorted(excluded),'dovezi_originale':p,'surse_mesaje_noi':paths,'nota':'Un mesaj Wizz Air promotional fara legatura a fost exclus motivat. Mesajele originale API sunt pastrate integral, fara export MIME. Niciun atasament nou; registrul atasamentelor din 2026.10.27 ramane 908 pozitii. Nu s-au trimis mesaje, modificat documente comerciale, semnat sau platit.'};jsave(PROOF,proofdata)

summary=DAY+' | Verificare zilnica Schallergasse 35\nVerificat: '+STAMP+'\n\nStatus scurt: Doua raspunsuri noi BERGER/PECH dupa discutiile din 2026.10.27. Nu sunt contracte acceptate.\n\n'
for partner,v in info.items():summary+=partner+'\nStatus scurt: '+v['status']+'\nUltimul raspuns: '+v['ultimul_raspuns']+'\nUrmatorul pas: '+v['urmatorul_pas']+'\nSursa: '+paths[partner]['txt']+'\n\n'
summary+='Financiar: oferta BERGER pentru Bauwerksbuch este 2.500 EUR net, suplimentara si neacceptata; pachetul de baza de 45.000 EUR net nu este modificat. Cumulul aritmetic conditionat ar fi 47.500 EUR net daca se convine acelasi obiect si se accepta ambele, fara alte costuri de planificare/Planwechsel necunoscute. Nu reprezinta un nou total contractual acceptat. Nicio suma noua PECH.\n\nAcoperire: 66 cautari / 66 pagini paginate integral, toate mesajele office primite si trimise si cautari globale dupa adresa, firme si referinte, inclusiv numele/contactul arhitectului nou recomandat. 8 ID-uri rezultate: 2 noi relevante, 5 deja arhivate/raportate, 1 reclama Wizz Air exclusa. Registru comunicatii 843 ID-uri unice. Niciun atasament relevant nou; registrul atasamentelor ramane 2026.10.27, 908 pozitii.\n'+limits+'\nSursa: '+PROOF.as_posix()+'\nNu s-au trimis emailuri, modificat contracte, semnat ori efectuat plati. Confirmarea discutiei nu implica acceptarea contractului, a pretului suplimentar sau numirea arhitectului.\n'
save(REPORT,summary)
for name in ('Status proiect','Log progres proiect'):
    prepend_new(Path(DAY+' '+name+'.txt'),Path(PREV+' '+name+'.txt'),summary)
for partner in ('Markus Berger','Pech','WOHR','Roland Gasperl'):
    s=next(x for x in r['statusuri'] if x.get('partener')==partner)
    detail=DAY+' | '+partner+'\nStatus scurt: '+s['status']+'\nUltimul raspuns: '+str(s.get('ultimul_raspuns','conform sursei anterioare'))+'\nUrmatorul pas: '+s['urmatorul_pas']+'\nSursa verificarii: '+PROOF.as_posix()+'\nSurse status: '+str(s.get('sursa_status'))+'\n'+limits+'\n'
    prepend_new(BASE/'Parteneri'/(DAY+' Log discutii - '+partner+'.txt'),BASE/'Parteneri'/(PREV+' Log discutii - '+partner+'.txt'),detail)
prepend_new(Path('folder map/README.md'),Path('folder map/README.md'),summary+'\nPuncte curente: ../'+newreg.as_posix()+'; ../'+DAY+' Status proiect.txt; ../'+DAY+' Log progres proiect.txt.\n')
print(json.dumps({'register':newreg.as_posix(),'report':REPORT.as_posix(),'proof':PROOF.as_posix(),'count':843,'new_relevant':2,'entry':entry},ensure_ascii=False))
