from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,hashlib,shutil
root=Path.cwd();day='2026.11.01';now=datetime.now(ZoneInfo('Europe/Bucharest'));stamp=now.isoformat(timespec='seconds');base=Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail');out=Path('08. Corespondenta')/(day+' Verificare zilnica');hist=Path('folder map')/(day+' Istoric verificare generala');changed=[]
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
def digest(d):return hashlib.sha256(json.dumps(d,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def local(s):return datetime.fromisoformat(s.replace('Z','+00:00')).astimezone(ZoneInfo('Europe/Bucharest')).strftime('%Y.%m.%d %H:%M:%S')
p=read('folder map/2026.11.01 Dovezi etapa generala.json');r=read(p['baseline']['register']);ar=read(base/'2026.10.31 Registru atasamente.json');assert not p['errors']
before={k:digest(r[k]) for k in ('comunicatii','drafturi','aliasuri_email_EVA')};known={x['id'] for x in r['comunicatii']};aliases={x['alias_id']:x['canonical_id'] for x in r.get('aliasuri_email_EVA',[])};groups={}
for x in p['pages']:
 key=json.dumps({k:v for k,v in x['args'].items() if k!='offset'},sort_keys=True);groups.setdefault(key,[]).append(x)
for group in groups.values():
 offset=0
 for page in sorted(group,key=lambda x:x['args']['offset']):
  assert page['args']['offset']==offset;offset+=len(page['result']['items'])
 assert offset>=group[-1]['result']['total']
meta={x['id']:x for page in p['pages'] for x in page['result']['items']};unknown=[x for x in meta.values() if aliases.get(x['id'],x['id']) not in known];excluded=[]
for x in unknown:
 reason='Test tehnic reconectare EVA, fara continut de proiect' if x['subject'].startswith('Test reconectare EVA') else 'Marketing generic, fara legatura specifica proiectului' if x['from_address'] in ('noreply@uber.com','offers@travel.wizznews.com') else None
 assert reason,(x['id'],x['subject']);excluded.append({'id':x['id'],'motiv':reason,'metadata':x})
canonical=sorted({aliases.get(eid,eid) for eid in meta if aliases.get(eid,eid) in known});aliasfound=sorted(eid for eid in meta if eid in aliases)
idx={x['cale']:x for x in read('folder map/inventar.json')};sources=[];active=['CERHA HEMPEL','Donau Versicherung','MA37','Markus Berger','Pech','WOHR']
for s in r['statusuri']:
 if s.get('partener') not in active:continue
 for rel in s.get('sursa_status',[]):
  assert rel in idx and Path(rel).exists(),rel
  sha=hashlib.sha256(Path(rel).read_bytes()).hexdigest();assert sha==idx[rel]['sha256'],rel
  sources.append({'partener':s['partener'],'cale':rel,'sha256':sha,'reutilizat_neschimbat':True})
syncp={x['email']:x.get('last_sync') for x in p['mailboxes_primary']['mailboxes']};syncs={x['email']:x.get('last_sync') for x in p['mailboxes_secondary']['mailboxes']}
limits='Ultima sincronizare afisata: Primary office '+local(syncp['office@ac-wohnart.at'])+'; Gmail '+local(syncp['covaciu.gnm@gmail.com'])+'; office secundar '+local(syncs['office@ac-wohnart.at'])+' Romania. Indicatori de sincronizare, nu dovada exhaustivitatii; mesajele ulterioare neindexate pot lipsi. Shared/team necautabile excluse.'
proof=out/(day+' Dovezi verificare EVA.json');report=out/(day+' Raport verificare zilnica.txt')
entry={'data':day,'checked_at_iso':stamp,'perioada':p['period'],'cautari_complete':len(groups),'pagini':len(p['pages']),'paginare_completa':True,'acoperire_actuala_office_completa':True,'metadate_unice_ID':len(meta),'mesaje_noi_ID':0,'mesaje_noutati_neraportate':0,'mesaje_relevante_canonice_deja_arhivate':len(canonical),'ID_alias_cunoscut':len(aliasfound),'ID_excluse':len(excluded),'atasamente_noi_ID':0,'continuturi_documentare_noi':0,'oferta_noua_identificata':False,'sincronizari_originale_primary':syncp,'sincronizari_originale_secondary':syncs,'limite':limits,'sursa':proof.as_posix(),'decizie_notificare':'DONT_NOTIFY','stare':'Nicio comunicare relevanta noua si nicio actiune noua identificata fata de verificarea generala 2026.10.31 si actualizarile punctuale ulterioare.'}
r.setdefault('istoric_verificari_incrementale',[]).append(r['acoperire']['verificare_incrementala']);r['acoperire']['verificare_incrementala']=entry;r['data_actualizarii']=day
for s in r['statusuri']:
 s['verificare_comunicari_2026_11_01']={'data':day,'checked_at_iso':stamp,'mesaje_noi_identificate':0,'sursa':proof.as_posix(),'nota':'Cautari generale proiect si control integral office, fara schimbarea statusului comercial ori a ultimului raspuns.'}
assert all(digest(r[k])==v for k,v in before.items())
jsave(base/(day+' Registru comunicatii.json'),r);jsave(base/(day+' Registru atasamente.json'),ar)
summary=f"""{day} | VERIFICARE ZILNICA SCHALLERGASSE 35
Verificat: {stamp}
Status scurt: Nu s-au identificat comunicari, oferte, preturi, documente sau actiuni noi fata de verificarea generala 2026.10.31 08:05:46 si actualizarile punctuale ulterioare. DONT_NOTIFY: situatie neschimbata, fara actiune noua.

ACOPERIRE
{len(groups)} cautari/{len(p['pages'])} pagini complete; {len(meta)} ID-uri metadate. Control integral primit/trimis office in ambele conexiuni si cautari globale adresa, firme, referinte de contracte/polite/facturi si nelivrari. Perioada {p['period']}.
Cele {len(canonical)} comunicatii canonice relevante returnate sunt deja arhivate; {len(aliasfound)} aliasuri oglinda cunoscute, fara mesaje noi. {len(excluded)} ID-uri excluse: patru teste tehnice EVA si doua reclame fara legatura specifica proiectului. Excluderea nu inseamna stergere.
Registrul ramane {len(r['comunicatii'])} comunicatii canonice; ciornele, aliasurile, atasamentele si statusurile comerciale sunt pastrate. Nu exista mesaje sau atasamente noi relevante de exportat. {len(sources)} surse locale active au fost verificate SHA-256 fata de index si reutilizate neschimbate.
{limits}

PUNCTE CUNOSCUTE, FARA RENOTIFICARE
CERHA HEMPEL: cererea Capra catre Kornhofer din 2026.10.30 17:09:38 a fost deja raportata; niciun raspuns nou sau plan vizat recuperat identificat.
MA37: niciun raspuns nou al autoritatii identificat.
BERGER/PECH: nicio observatie comerciala, contrapropunere sau anexa noua identificata.
DONAU/WOHR: nicio comunicare noua ori confirmare suplimentara de plata/remediere identificata.
Ultimele raspunsuri si urmatorii pasi raman cele din registru si jurnalele partenerilor; nu se transforma asteptarea in eveniment nou.
Draftul nu este considerat trimis, oferta nu este contract acceptat, invitatia nu este intalnire efectuata si ordinul de plata nu este debit/incasare confirmata.
Nu s-au trimis emailuri, semnat, platit ori modificat documente comerciale/calendar.
Sursa verificare: {proof.as_posix()}
"""
save(report,summary)
for name in ('Status proiect','Log progres proiect'):prepend(day+' '+name+'.txt',summary,'2026.10.31 '+name+'.txt')
for s in r['statusuri']:
 if s.get('partener') not in active:continue
 partner=s['partener'];j=base/'Parteneri'/(day+' Log discutii - '+partner+'.txt')
 prior=sorted((base/'Parteneri').glob('* Log discutii - '+partner+'.txt'));prior=next((x for x in reversed(prior) if x.name<j.name),None)
 text=day+' | '+partner+'\nStatus verificare: FARA NOUTATI; statusul anterior ramane valabil.\nStatus scurt: '+s.get('status','')+'\nUltimul raspuns cunoscut: '+str(s.get('ultimul_raspuns') or s.get('subiect_ultimul_primit') or 'Vezi jurnalul anterior')+'\nUrmatorul pas cunoscut: '+s.get('urmatorul_pas','')+'\nSurse: '+str(s.get('sursa_status',[]))+'\nSursa verificare: '+proof.as_posix()+'\n'+limits
 prepend(j,text,prior)
prepend('folder map/README.md',summary+'\nRaport: ../'+report.as_posix())
jsave(proof,{'verificare':entry,'baseline_unique_ids':len(r['comunicatii']),'final_unique_ids':len(r['comunicatii']),'canonical_ids_deja_arhivate':canonical,'alias_ids_deja_cunoscute':aliasfound,'excluderi':excluded,'surse_reutilizate':sources,'comunicatii_drafturi_aliasuri_nemodificate':True,'dovezi_originale':p,'nota':'Fara noutati relevante; nu exista mesaje/atasamente noi de descarcat sau actiuni externe efectuate.'})
Path('folder map/2026.11.01 Fisiere actualizate verificare generala.json').write_text(json.dumps(changed,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'report':report.as_posix(),'proof':proof.as_posix(),'count':len(r['comunicatii']),'new_messages':0,'decision':'DONT_NOTIFY'},ensure_ascii=False))

