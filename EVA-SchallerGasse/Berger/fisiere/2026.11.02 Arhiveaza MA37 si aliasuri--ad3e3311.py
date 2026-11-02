from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,hashlib,shutil
root=Path.cwd();day='2026.11.02';now=datetime.now(ZoneInfo('Europe/Bucharest'));stamp=now.isoformat(timespec='seconds');base=Path('08. Corespondenta/2026.09.30 Arhiva Eva-Mail');out=Path('08. Corespondenta/2026.11.02 Raspuns MA37 prin Capra');hist=Path('folder map')/(day+' Istoric MA37 '+now.strftime('%H-%M-%S'));changed=[]
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,t):
 p=Path(p)
 if p.exists():
  b=hist/p;b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,b)
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8');changed.append(p.as_posix())
def jsave(p,d):save(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def prepend(p,t):
 p=Path(p);old=p.read_text(encoding='utf-8-sig') if p.exists() else '';save(p,t+'\n\nISTORIC PASTRAT\n\n'+old)
p=read('folder map/2026.11.02 Capra MA37 etapa.json');m=read('folder map/2026.11.02 Manifest anexe MA37 Capra.json');r=read(base/(day+' Registru comunicatii.json'));ar=read(base/(day+' Registru atasamente.json'));e=p['email'];known={x['id'] for x in r['comunicatii']};already=e['id'] in known;files=m['files'];assert m['pdf_copies_identical'] and m['unique_document_contents']==2;assert not e['truncated']
for f in files:assert hashlib.sha256(Path(f['cale']).read_bytes()).hexdigest()==f['sha256'];changed.append(f['cale'])
jp=out/'2026.11.02 12-15-10 PRIMIT CAPRA dd5df6a9.json';tp=jp.with_suffix('.txt')
jsave(jp,{'data_lizibila':'2026.11.02 12:15:10 Romania','statut':'PRIMIT','original_EVA':e,'atasamente_originale':m,'nota':'Capra transmite raspunsul MA37. Doua ID-uri PDF au continut identic; acelasi PDF este si in EML-ul original. Trei imagini mici de semnatura au numai metadate. Textul tertilor si datele tehnice sunt nemodificate.'})
save(tp,'2026.11.02 12:15:10 Romania | PRIMIT\nSubiect: '+e['subject']+'\nDe la: '+e['from_address']+'\nCatre: '+', '.join(e['to'])+'\nCC: '+', '.join(e['cc'])+'\nID Eva-Mail: '+e['id']+'\nOriginal JSON: '+jp.as_posix()+'\n\nTEXT ORIGINAL\n\n'+e['text'])
pdf=next(x['cale'] for x in files if x['id']=='28bc30cf-4f8f-4965-b649-d077750f7dac')
if not already:
 r['comunicatii'].append({'data':day,'ora_utc':'10:15:10','partener':'CERHA HEMPEL','domeniu':'MA37 / recuperare documentatie autorizare','sens':'PRIMIT','subiect':e['subject'],'expeditor':e['from_address'],'destinatari':e['to'],'cc':e['cc'],'id':e['id'],'cale':tp.as_posix(),'json':jp.as_posix(),'atasamente':[x['cale'] for x in files],'trunchiat':False,'data_preluarii':day,'nota':'Transmite raspuns MA37, relevant pentru documentele proiectului; nu este mesaj nou BERGER si nu rezolva proiectul de executie DG.','raportare_in_context_BERGER':True})
fm={x['id']:x for x in files};knownatt={x['id'] for x in ar}
for a in e['attachments']:
 if a['id'] in knownatt:continue
 f=fm.get(a['id']);ar.append({'id':a['id'],'email_id':e['id'],'data':day,'partener':'CERHA HEMPEL / MA37','nume_original':a['name'],'octeti':a['size'],'cale':f['cale'] if f else None,'sha256':f['sha256'] if f else None,'stare':'Original integral recuperat; PDF citit si verificat vizual pe ambele pagini.' if f else 'Numai metadate: imagine mica de semnatura, fara continut documentar.','continut_documentar_nou':bool(f and a['id']!='63c556ff-1b8d-4fdc-9d7d-617e5195d9d6')})
for a,label in [(p['berger_alias'],'BERGER'),(p['capra_alias'],'CAPRA')]:
 assert a['thread_equal'] and a['body_exact'] and a['from_equal']
 if label=='CAPRA':assert a['attachment_names_sizes_equal']
 ap=out/(day+' Alias EVA '+label+' '+a['alias_id'][:8]+'.json');jsave(ap,a)
 if not any(x['alias_id']==a['alias_id'] for x in r.get('aliasuri_email_EVA',[])):
  r.setdefault('aliasuri_email_EVA',[]).append({'alias_id':a['alias_id'],'canonical_id':a['canonical_id'],'link_id':'link_6ae19c4ed7888191a5d7002d96ef4b95','cale':ap.as_posix(),'verificare':'Thread, expeditor si text integral identice in memorie; metadate pastrate. Pentru BERGER citatul cu credentiale nu este rearhivat.'})
summary=(day+' | RASPUNS MA37 PRIN CAPRA\nStatus scurt: Raspunsul autoritatii GZ 1501240-2026-2, datat 2026.11.02, a fost transmis de Capra la 12:15:10 Romania.\nUltimul raspuns: informatiile solicitate pot fi consultate prin Planeinsicht in documentele Hauseinlage sau Überwachung pentru EZ 2235, KG Meidling. Nu sunt planuri atasate, ci raspunsul privind consultarea.\nUrmatorul pas: organizarea consultarii dosarelor, verificarea planurilor vizate/inventarului si obtinerea copiilor. Raspunsul nu confirma recuperarea ori predarea tuturor exemplarelor si nu constituie proiectul de executie DG cerut de BERGER.\nSurse: '+tp.as_posix()+'; '+pdf+'\nEML original MA37 catre Capra: '+str(m['nested_email_headers'])+'\nPDF-ul de doua pagini a fost verificat vizual. Cele doua ID-uri PDF sunt byte-identice, iar acelasi document este inclus in EML. Originalele sunt pastrate.\nNu s-a facut programare, nu s-au trimis emailuri/RSVP, nu s-au modificat contracte ori calendar.\n')
for name in ('CERHA HEMPEL','MA37'):
 s=next(x for x in r['statusuri'] if x.get('partener')==name);s.setdefault('istoric_status',[]).append({'data_preluarii':day,**{k:s.get(k) for k in ['status','ultimul_raspuns','urmatorul_pas','sursa_status']}})
 s.update({'status':'2026.11.02: MA37 raspunde prin scrisoarea GZ 1501240-2026-2 ca informatiile solicitate sunt consultabile in Hauseinlage/Überwachung, EZ 2235 KG Meidling. Capra a transmis originalul, fara predare de planuri.','ultimul_raspuns':'Raspunsul MA37, 2026.11.02, transmis de Capra 12:15:10 Romania; email original MA37 catre avocat 12:11:28 Romania.','urmatorul_pas':'Organizarea Planeinsicht, verificarea inventarului/planurilor vizate si obtinerea copiilor. De clarificat concret ce documente exista si unde; fara a presupune deja recuperarea setului sau existenta proiectului nou de executie DG.','sursa_status':[tp.as_posix(),pdf],'data_actualizarii':day,'ultima_comunicare':day,'ultimul_primit':day})
 dest=base/'Parteneri'/(day+' Log discutii - '+name+'.txt');prepend(dest,summary)
for name in ['Status proiect','Log progres proiect']:prepend(day+' '+name+'.txt',summary)
r.setdefault('mesaje_incidentale_pentru_verificare_generala',[]).append({'data':day,'email_id':e['id'],'partener':'CERHA HEMPEL / MA37','sursa':jp.as_posix(),'raportare_generala_pendenta':False,'statut':'Integrat in registru; de raportat o singura data in checklistul curent, deoarece documentatia de autorizare este relevanta pregatirii proiectarii/BERGER.','nota':'Nu este raspuns sau acceptare BERGER. Nu se confunda planurile vizate consultabile cu proiectul de executie DG.'})
r.setdefault('actualizari_punctuale',[]).append({'data':day,'checked_at_iso':stamp,'tip':'Raspuns MA37 prin Capra identificat la checklist BERGER','email_id':e['id'],'sursa':jp.as_posix(),'nou_nearhivat_la_inceput':not already,'notificare_planificata':not already});r['acoperire']['registru_atasamente_randuri']=len(ar)
jsave(base/(day+' Registru comunicatii.json'),r);jsave(base/(day+' Registru atasamente.json'),ar)
save(out/(day+' Jurnal raspuns MA37.txt'),summary)
decision={'notify':not already,'email_id':e['id'],'pdf':pdf,'email_txt':tp.as_posix(),'email_json':jp.as_posix(),'already_in_register':already,'new_BERGER_messages':0,'new_MA37_message':not already,'summary':summary}
Path('folder map/2026.11.02 MA37 rezultat actualizare.json').write_text(json.dumps(decision,ensure_ascii=False,indent=2),encoding='utf-8');Path('folder map/2026.11.02 Fisiere actualizate MA37.json').write_text(json.dumps(changed,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'count':len(r['comunicatii']),'MA37_new':not already,'BERGER_new':0,'pdf':pdf},ensure_ascii=False))

