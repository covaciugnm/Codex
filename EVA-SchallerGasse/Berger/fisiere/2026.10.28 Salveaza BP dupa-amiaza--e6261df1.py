from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,hashlib,shutil

ROOT=Path(__file__).resolve().parent.parent;DAY='2026.10.28';TZ=ZoneInfo('Europe/Bucharest');NOW=datetime.now(TZ)
STAMP=NOW.isoformat(timespec='seconds');TAG=NOW.strftime('%H-%M-%S')
BASE=Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail');REG=BASE/(DAY+' Registru comunicatii.json')
OUT=Path('08. Corespondenta')/(DAY+' Verificare Berger Pech');ACCESS=Path('08. Corespondenta/2026.10.28 Acces servieta BERGER PECH')
PROOF=OUT/(DAY+' '+TAG+' Dovezi verificare EVA - fara parole.json');REPORT=OUT/(DAY+' '+TAG+' Raport verificare BERGER PECH.txt')
HIST=Path('folder map')/(DAY+' Istoric BP '+TAG)

def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def save(p,text):
    p=Path(p);dest=ROOT/p
    if dest.exists():
        old=ROOT/HIST/p;old.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dest,old)
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(text.encode('utf-8'))
def jsave(p,d):save(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def prepend(p,text):
    p=Path(p);old=(ROOT/p).read_text(encoding='utf-8-sig') if (ROOT/p).exists() else ''
    save(p,text+'\n\nISTORIC PASTRAT\n\n'+old)
def clock(s):return datetime.fromisoformat(s.replace('Z','+00:00')).astimezone(TZ)
def local(s):return clock(s).strftime('%Y.%m.%d %H:%M:%S') if s else 'indisponibila'

p=read(Path('folder map/2026.10.28 Dovezi etapa BP dupa-amiaza - fara parole.json'));r=read(REG)
ids={x['id'] for x in r['comunicatii']};assert len(ids)==len(r['comunicatii'])==p['baseline_count']==843
assert len(p['searches'])==29 and not p['errors']
for x in p['searches']:assert x['result']['offset']+len(x['result']['items'])>=x['result']['total']
scoped=set(p['scoped_email_ids']);new=scoped-ids
assert new=={'6c121750-efc5-4e17-8e64-6c52c23ffd4b','8fe2ffcc-a7e5-45a5-aab2-cb27e85e5860'}
messages=[x for x in p['full_emails'] if x['id'] in new];assert len(messages)==2
assert all(x['is_sent'] and not x['truncated'] and not x['attachments'] and '[PAROLA OMISA]' in x['text'] for x in messages)
assert len(p['drafts'])==2 and all(x['status']=='sent' for x in p['drafts'])
assert all(not x['attachments'] for x in p['full_emails'])
general=r['acoperire']['verificare_incrementala'].copy();sources={};exported=[]

for m in messages:
    partner='Markus Berger' if m['to']==['office@bmberger.at'] else 'Pech';name='BERGER' if partner=='Markus Berger' else 'PECH'
    prefix=clock(m['received_at']).strftime('%Y.%m.%d %H-%M-%S')+' TRIMIS '+name+' '+m['id'][:8]+' - copie fara parola'
    j=OUT/(prefix+'.json');t=OUT/(prefix+'.txt')
    jsave(j,{'data_lizibila':DAY,'statut':'TRIMIS','email_EVA_copie_redactata':m,'redactare':'Parola este omisa din copia locala, jurnal si index. Corpul original integral ramane in EVA. Metadatele tehnice sunt pastrate. Nu este export MIME original.'})
    header='Data: '+local(m['received_at'])+' Romania; data tehnica originala: '+m['received_at']+'\nStatut: TRIMIS\nID Eva-Mail: '+m['id']+'\nCont: '+m['account_email']+'\nExpeditor: '+m['from_address']+'\nDestinatari: '+', '.join(m['to'])+'\nCC: '+', '.join(m['cc'])+'\nSubiect: '+m['subject']+'\nCOPIE LOCALA CU PAROLA OMISA; originalul integral ramane in EVA; nu este export MIME.\n\n'
    save(t,header+m['text']);sources[partner]={'txt':t.as_posix(),'json':j.as_posix(),'id':m['id'],'data_trimiterii_originala':m['received_at']};exported.append(t.as_posix())
    r['comunicatii'].append({'data':DAY,'ora_utc':m['received_at'][11:19],'partener':partner,'domeniu':'Acces servieta digitala proiect','sens':'TRIMIS','subiect':m['subject'],'expeditor':m['from_address'],'destinatari':m['to'],'cc':m['cc'],'id':m['id'],'cale':t.as_posix(),'json':j.as_posix(),'atasamente':[],'trunchiat':False,'redactat':'numai parola omisa; original integral in EVA','data_preluarii':DAY})
    draft=next(d for d in p['drafts'] if d['to']==m['to'])
    records=[d for d in r['drafturi'] if d.get('id',d.get('draft_id'))==draft['id']]
    record=records[0] if records else {'id':draft['id'],'partener':partner,'istoric_status':[{'status':'pending / NETRIMIS la creare','sursa':(ACCESS/(DAY+' Drafturi EVA - copie fara parole.json')).as_posix()}]}
    record.update(status='sent',statut='TRIMIS verificat prin mesaj Sent si get_draft',account_email=draft['account_email'],destinatari=draft['to'],cc=draft['cc'],bcc=draft['bcc'],subiect=draft['subject'],email_trimis_id=m['id'],data_trimiterii=m['received_at'],data_verificarii=STAMP,sursa=t.as_posix())
    if not records:r['drafturi'].append(record)
    r.setdefault('mesaje_incidentale_pentru_verificare_generala',[]).append({'data':DAY,'email_id':m['id'],'partener':partner,'sursa':t.as_posix(),'raportare_generala_pendenta':False,'nota':'Raportat la verificarea BERGER/PECH de la 16:00; accesul la servieta este TRIMIS, nu confirmat ca primit/functionand. Nu se repeta ca noutate la urmatoarea verificare generala.'})

sections={}
for s in r['statusuri']:
    partner=s.get('partener')
    if partner not in sources:continue
    m=next(m for m in messages if m['id']==sources[partner]['id']);time=local(m['received_at'])
    s.setdefault('istoric_status',[]).append({'data_preluarii':DAY,'status':s['status'],'ultimul_raspuns':s.get('ultimul_raspuns'),'urmatorul_pas':s.get('urmatorul_pas'),'sursa_status':s.get('sursa_status')})
    s['status']+=' '+time+' Romania: emailul cu accesul la servieta digitala este TRIMIS catre '+m['to'][0]+', fara CC/BCC sau atasamente. Ciorna EVA are status sent. Nicio confirmare a primirii ori a functionarii accesului.'
    s['ultima_comunicare']=DAY;s['ultimul_trimis']=DAY;s['ultima_trimitere']='Acces servieta: '+time+' Romania; ID '+m['id']
    s['urmatorul_pas']='Urmarirea confirmarii ca accesul functioneaza si a listei de documente necesare; pastrate deschise punctele comerciale si tehnice anterior consemnate. '+s['urmatorul_pas']
    s['sursa_status']=list(s.get('sursa_status',[]))+[sources[partner]['txt']];s['data_actualizarii']=DAY
    s['mesaje']=sum(x.get('partener')==partner for x in r['comunicatii'])
    s['verificare_punctuala_BERGER_PECH_2026_10_28']={'checked_at_iso':STAMP,'mesaje_noi':1,'mesaje_trimise_noi':1,'mesaje_primite_noi':0,'sursa':PROOF.as_posix()}
    sections[partner]=partner+'\nStatus scurt: '+s['status']+'\nUltimul raspuns extern: '+str(s.get('ultimul_raspuns','conform sursei anterioare'))+'\nUltima trimitere: '+s['ultima_trimitere']+'\nUrmatorul pas: '+s['urmatorul_pas']+'\nSursa noua: '+sources[partner]['txt']+'\n'

sync={x['email']:x.get('last_sync') for x in p['mailboxes']['mailboxes']}
limits='Sincronizare Romania: office '+local(sync['office@ac-wohnart.at'])+'; Gmail '+local(sync['covaciu.gnm@gmail.com'])+'. Mesajele ulterioare pot lipsi; shared/team nesearchable excluse.'
entry={'data':DAY,'checked_at_iso':STAMP,'parteneri':['Markus Berger','Pech'],'mesaje_noi':2,'mesaje_trimise_noi':2,'mesaje_primite_noi':0,'atasamente_noi':0,'continuturi_documentare_noi':0,'query_count':29,'page_count':29,'perioada':'2026.10.27–2026.10.28, suprapunere de o zi si deduplicare fata de verificarea generala 08:00 si punctuala 10:00','paginare_completa':True,'control_integral_casute':True,'sincronizare_office':sync['office@ac-wohnart.at'],'sincronizare_gmail':sync['covaciu.gnm@gmail.com'],'sursa':PROOF.as_posix()}
r['acoperire']['verificare_punctuala_BERGER_PECH']=entry;r.setdefault('verificari_parteneri',[]).append(entry)
assert r['acoperire']['verificare_incrementala']==general
assert len(r['comunicatii'])==len({x['id'] for x in r['comunicatii']})==845
jsave(REG,r)
proofdata={'verificare':entry,'baseline_unique_ids':843,'final_unique_ids':845,'new_BP_email_ids':sorted(new),'previously_archived_not_repeated':sorted(scoped&ids),'general_baseline_preserved':general,'sources':sources,'dovezi_originale_cu_parole_omise':p,'nota':'2 mesaje TRIMISE si 2 ciorne cu status sent, fara raspuns extern nou sau confirmare de acces. 4 mesaje anterioare nu se raporteaza repetat. 36 metadate nelegate de BERGER/PECH excluse. attachment_names din cautare poate include fisiere din conversatie; get_email confirma zero atasamente pentru cele doua raspunsuri vechi recitite. Niciun atasament nou de descarcat. Agentul nu a trimis emailuri sau modificat documente comerciale.'}
jsave(PROOF,proofdata)
summary=DAY+' '+NOW.strftime('%H:%M:%S')+' | Verificare BERGER/PECH\n\nStatus scurt: Cele doua emailuri cu accesul la servieta sunt TRIMISE: BERGER '+local(next(m['received_at'] for m in messages if m['to']==['office@bmberger.at']))+' Romania; PECH '+local(next(m['received_at'] for m in messages if m['to']==['office@zt-pech.at']))+' Romania. Ciornele au status sent. Nu exista raspuns extern nou, confirmare de primire, confirmare a functionarii accesului, oferta sau pret nou, observatii contractuale ori atasamente noi.\n\n'+'\n'.join(sections.values())+'\nAcoperire: 29 cautari / 29 pagini paginate integral; domenii/adrese/firme, Schallergasse si referinte contractuale, inclusiv nelivrari si control integral primit/trimis fara filtru de text in office/Gmail. 42 metadate unice: 6 relevante BERGER/PECH (2 noi trimise, 4 deja arhivate), 36 nerelevante acestui control. Registrul are 845 ID-uri unice. Registrul atasamentelor ramane 2026.10.27, fara fisiere noi.\n'+limits+'\nSursa: '+PROOF.as_posix()+'\nCopiile locale au numai parola omisa; originalele integrale raman in EVA. Nu s-au transmis mesaje prin acest agent, nu s-au modificat contracte, semnat sau efectuat plati. Trimiterea nu este confirmare de primire sau de acces.\n'
save(REPORT,summary)
for name in ('Status proiect','Log progres proiect'):prepend(Path(DAY+' '+name+'.txt'),summary)
for partner,section in sections.items():prepend(BASE/'Parteneri'/(DAY+' Log discutii - '+partner+'.txt'),DAY+' '+NOW.strftime('%H:%M:%S')+' | Verificare BERGER/PECH\n\n'+section+'\n'+limits+'\nSursa: '+PROOF.as_posix())
prepend(Path('folder map/README.md'),summary+'Raport: ../'+REPORT.as_posix())
status={'verificat':STAMP,'status':'AMBELE TRIMISE, verificat in EVA Sent si status ciorne sent','mesaje':sources,'drafturi_copie_fara_parole':p['drafts'],'confirmare_primire':False,'confirmare_functionare_acces':False,'sursa':PROOF.as_posix(),'istoric':'Copiile DRAFT NETRIMIS sunt pastrate ca stare istorica la creare. Parolele nu sunt salvate.'}
jsave(ACCESS/(DAY+' '+TAG+' Status trimitere verificat - fara parole.json'),status)
prepend(ACCESS/(DAY+' Jurnal pregatire.txt'),DAY+' '+NOW.strftime('%H:%M:%S')+' | VERIFICARE TRIMITERE\nAmbele mesaje sunt TRIMISE; ciornele au status sent. Surse: '+json.dumps(sources,ensure_ascii=False)+'\nNu exista confirmare de primire sau ca accesul functioneaza. Nu s-au trimis mesaje de acest agent. Copiile anterioare NETRIMIS sunt istoric; parolele sunt omise in toate copiile locale noi.')
print(json.dumps({'report':REPORT.as_posix(),'proof':PROOF.as_posix(),'count':845,'drafts':len(r['drafturi']),'new_sent':2,'new_received':0,'attachments_new':0,'general_coverage_preserved':True},ensure_ascii=False))
