from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,hashlib,shutil,sys

ROOT=Path(__file__).resolve().parent.parent;TZ=ZoneInfo('Europe/Bucharest');NOW=datetime.now(TZ);DAY=NOW.strftime('%Y.%m.%d');STAMP=NOW.isoformat(timespec='seconds');TAG=NOW.strftime('%H-%M-%S')
STAGE=Path(sys.argv[1]) if len(sys.argv)>1 else Path('folder map/2026.10.29 Dovezi etapa BP dimineata.json')
BASE=Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail');OUT=Path('08. Corespondenta')/(DAY+' Verificare Berger Pech');PROOF=OUT/(DAY+' '+TAG+' Dovezi verificare EVA.json');REPORT=OUT/(DAY+' '+TAG+' Raport verificare BERGER PECH.txt');HIST=Path('folder map')/(DAY+' Istoric BP '+TAG)
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def save(p,t):
 p=Path(p);dest=ROOT/p
 if dest.exists():
  old=ROOT/HIST/p;old.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dest,old)
 dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(t.encode('utf-8'))
def jsave(p,d):save(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def prepend(p,t):
 p=Path(p);old=(ROOT/p).read_text(encoding='utf-8-sig') if (ROOT/p).exists() else ''
 save(p,t+'\n\nISTORIC PASTRAT\n\n'+old)
def local(s):return datetime.fromisoformat(s.replace('Z','+00:00')).astimezone(TZ).strftime('%Y.%m.%d %H:%M:%S') if s else 'indisponibila'

p=read(STAGE);REG=Path(p['baseline_register']);r=read(REG);known={x['id'] for x in r['comunicatii']};count=p['baseline_count']
assert len(known)==len(r['comunicatii'])==count and not p['errors']
for page in p['searches']:assert page['result']['offset']+len(page['result']['items'])>=page['result']['total']
found={x['id'] for page in p['searches'] for x in page['result']['items']};scoped=set(p['scoped_email_ids']);excluded=set(p['excluded_unrelated_email_ids'])
assert scoped<=known and found==scoped|excluded and not scoped&excluded
before={k:hashlib.sha256(json.dumps(r[k],sort_keys=True,ensure_ascii=False).encode()).hexdigest() for k in ('comunicatii','drafturi')};general=r['acoperire']['verificare_incrementala'].copy()
sync={x['email']:x.get('last_sync') for x in p['mailboxes']['mailboxes']}
limits='Sincronizare Romania: office '+local(sync['office@ac-wohnart.at'])+'; Gmail '+local(sync['covaciu.gnm@gmail.com'])+'. Mesajele ulterioare pot lipsi; shared/team nesearchable excluse.'
entry={'data':DAY,'checked_at_iso':STAMP,'parteneri':['Markus Berger','Pech'],'mesaje_noi':0,'mesaje_trimise_noi':0,'mesaje_primite_noi':0,'atasamente_noi':0,'continuturi_documentare_noi':0,'query_count':len(p['searches']),'page_count':len(p['searches']),'perioada':'2026.10.28–2026.10.29, suprapunere de o zi fata de verificarea generala 2026.10.29 07:58; deduplicare inclusiv fata de verificarile BERGER/PECH si mesajele deja raportate','paginare_completa':True,'control_integral_casute':True,'metadate_unice':len(found),'mesaje_relevante_deja_arhivate':len(scoped),'mesaje_nerelevante_BP':len(excluded),'sincronizare_office':sync['office@ac-wohnart.at'],'sincronizare_gmail':sync['covaciu.gnm@gmail.com'],'sursa':PROOF.as_posix()}
sections={}
for s in r['statusuri']:
 if s.get('partener') not in ('Markus Berger','Pech'):continue
 partner=s['partener'];sections[partner]=partner+'\nStatus scurt: Nicio noutate; situatia pastrata: '+s['status']+'\nUltimul raspuns extern: '+str(s.get('ultimul_raspuns','conform surselor anterioare'))+'\nUltima trimitere: '+str(s.get('ultima_trimitere','conform surselor anterioare'))+'\nUrmatorul pas: '+s['urmatorul_pas']+'\nSurse status anterior: '+str(s.get('sursa_status'))+'\n'
 s['verificare_punctuala_BERGER_PECH_'+DAY.replace('.','_')]={'checked_at_iso':STAMP,'mesaje_noi':0,'sursa':PROOF.as_posix()}
r['acoperire']['verificare_punctuala_BERGER_PECH']=entry;r.setdefault('verificari_parteneri',[]).append(entry)
assert r['acoperire']['verificare_incrementala']==general
for k,h in before.items():assert hashlib.sha256(json.dumps(r[k],sort_keys=True,ensure_ascii=False).encode()).hexdigest()==h
jsave(REG,r)
jsave(PROOF,{'verificare':entry,'baseline_unique_ids':count,'final_unique_ids':count,'new_BP_email_ids':[],'previously_archived_not_repeated':sorted(scoped),'excluded_unrelated_email_ids':sorted(excluded),'general_baseline_preserved':general,'dovezi_originale':p,'nota':'Nicio noutate BERGER/PECH de exportat. Metadatele fara legatura cu acest control sunt excluse dupa expeditor, destinatari, subiect si extras. Se reutilizeaza sursele integrale arhivate anterior si copiile de acces cu parola omisa; nu se recitesc sau salveaza parole. Nicio trimitere, acceptare, semnare, plata sau modificare comerciala.'})
header=DAY+' '+NOW.strftime('%H:%M:%S')+' | Verificare BERGER/PECH\n\n'
short='Nicio noutate BERGER/PECH: nici raspunsuri suplimentare, confirmari ale functionarii accesului, observatii contractuale, contrapropuneri, preturi/servicii, calendar, atasamente ori nelivrari noi. Mesajele de acces TRIMISE in 2026.10.28 sunt deja arhivate si raportate; nu se repeta ca noutati.'
coverage='Acoperire: '+str(len(p['searches']))+' cautari / '+str(len(p['searches']))+' pagini paginate integral, primit/trimis in office si Gmail, cautari globale dupa domenii/adrese/firme, Schallergasse si referinte, inclusiv nelivrari si control integral fara filtru de text in fiecare casuta. '+str(len(found))+' metadate unice: '+str(len(scoped))+' relevante deja arhivate si '+str(len(excluded))+' fara legatura cu acest control. Registrul ramane la '+str(count)+' ID-uri unice. Niciun mesaj relevant nou ori atasament nou de salvat.\n'+limits+'\n'
summary=header+'Status scurt: '+short+'\n\n'+'\n'.join(sections.values())+'\n'+coverage+'Sursa: '+PROOF.as_posix()+'\nNu s-au trimis emailuri, modificat documente comerciale, semnat contracte sau efectuat plati. Mesajele TRIMISE nu sunt confirmari de primire sau acces; invitatia Teams pentru 2026.10.29 nu este considerata sedinta efectuata sau acceptare de contract.\n'
save(REPORT,summary)
for name in ('Status proiect','Log progres proiect'):prepend(Path(DAY+' '+name+'.txt'),summary)
for partner,section in sections.items():prepend(BASE/'Parteneri'/(DAY+' Log discutii - '+partner+'.txt'),header+section+'\n'+coverage+'Sursa: '+PROOF.as_posix())
prepend(Path('folder map/README.md'),summary+'Raport: ../'+REPORT.as_posix())
print(json.dumps({'report':REPORT.as_posix(),'proof':PROOF.as_posix(),'entry':entry,'register_count':count,'general_coverage_preserved':True},ensure_ascii=False))
