from pathlib import Path
import json, hashlib, shutil
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent;DATE='2026.10.13'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def rel(p):return str(p.relative_to(ROOT)).replace('\\','/')
def rec(p):return {'cale':rel(p),'sha256':sha(p),'octeti':p.stat().st_size}
def fresh(p,s):assert not p.exists(),p;p.write_text(s,encoding='utf-8')
def prepend(p,s):p.write_text(s.rstrip()+'\n\nISTORIC PĂSTRAT\n\n'+p.read_text(encoding='utf-8-sig'),encoding='utf-8')
transfer=read(OUT/f'{DATE} Registru transfer preambul R08.json')
eva=read(OUT/f'{DATE} Registru EVA drafturi R08.json')
exports=read(OUT/f'{DATE} Registru export emailuri EVA R08.json')
assert (OUT/f'{DATE} Audit final emailuri si atasamente R08.txt').is_file()
assert len(eva['drafturi'])==2 and len(exports['drafturi'])==2 and exports['mesaje_trimise']==0
assert read(OUT/f'{DATE} Control integritate PDF R08.json')['status']=='PASS'
deliverables=[]
for item in transfer['operatiuni']:
    pdf=ROOT/item['PDF_expected'];src=ROOT/item['R08_source'];folder=ROOT/item['public_folder']
    assert sha(src)==item['R08_sha256'] and sha(folder/src.name)==sha(src)
    assert sha(ROOT/item['R07_source'])==item['R07_sha256']
    assert sha(ROOT/item['offer_original_copy'])==item['offer_sha256']
    qa=OUT/f"{DATE} QA text PDF {item['provider']} R08.json"
    assert read(qa)['text_status']=='PASS' and read(qa)['pdf_sha256']==sha(pdf)
    visual=OUT/f"{DATE} QA vizual {item['provider']} R08.txt";assert visual.is_file()
    draft=next(d for d in eva['drafturi'] if d['provider']==item['provider'])
    assert draft['status']=='pending' and len(draft['attachments'])==2
    for att in draft['attachments']:assert sha(ROOT/att['local_path'])==att['sha256']
    deliverables.append({'provider':item['provider'],'pdf':{**rec(pdf),'pagini':len(PdfReader(pdf).pages)},'sursa':rec(src),'oferta_originala':rec(ROOT/item['offer_original_copy']),'qa_text':rec(qa),'qa_vizual':rec(visual),'draft_EVA_id':draft['draft_id'],'status':'pending / NETRIMIS'})
oldregistry=ROOT/f'00.Proiect/09. Vertraege/{DATE} Propuneri contract R07 - intern/{DATE} Registru propuneri R07 final.json'
old=read(oldregistry)
for item in old['livrabile']:
    for key in ['pdf','sursa','oferta_originala']:assert sha(ROOT/item[key]['cale'])==item[key]['sha256']
for item in old['drafturi']['drafturi']:assert sha(ROOT/item['EML'])==item['EML_sha256']
old06=read(ROOT/old['istoric_R06']['cale'])
for item in old06['livrabile']:
    assert sha(ROOT/item['pdf']['cale'])==item['pdf']['sha256']
    assert sha(ROOT/item['sursa_canonica']['cale'])==item['sursa_canonica']['sha256']
for item in old06['contracte_R05_frozen']:assert sha(ROOT/item['cale'])==item['sha256']
regpath=ROOT/f'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/{DATE} Registru comunicatii.json'
partners=ROOT/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri'
targets=[ROOT/f'{DATE} Status proiect.txt',ROOT/f'{DATE} Log progres proiect.txt',partners/f'{DATE} Log discutii - Markus Berger.txt',partners/f'{DATE} Log discutii - Pech.txt',regpath,ROOT/'folder map/README.md']
history=OUT/f'{DATE} Istoric jurnale inainte R08';history.mkdir(exist_ok=False)
backups=[]
for p in targets:
    dest=history/(p.name if p.name.startswith(DATE) else f'{DATE} {p.name}')
    shutil.copy2(p,dest);assert sha(p)==sha(dest)
    backups.append({'original':rel(p),'copie':rel(dest),'sha256_inainte':sha(p)})
links='\n'.join(d['pdf']['cale'] for d in deliverables)
draftlines='\n'.join(f"{d['provider']}: EVA draft {d['draft_id']}, status {d['status']}; To {', '.join(d['to'])}; CC {', '.join(d['cc']) or '(fără CC)'}" for d in eva['drafturi'])
entry=f'''2026.10.13 | Contracte R08 fără introducere și două emailuri germane în EVA
Status scurt: PDF-urile conțin numai WERKVERTRAG, proiectul și contractul de la § 1; cele trei Vorbemerkungen sunt mutate integral în emailul propriu. 16 capitole, 96 alineate și 6 anexe operative identice cu R07. Fiecare PDF are 32 pagini, cu chenare fine și tabele. Sumele de bază rămân BERGER 45.000 EUR net / 54.000 EUR cu TVA20%; PECH 69.300 EUR net / 83.160 EUR cu TVA20%. Nu s-au adăugat tarife. Opțiunile deja definite și toate clauzele/termenele rămân neschimbate.
Emailuri foarte politicoase în germană: dorința de semnare, propunerea de la avocații proprii și echipa tehnică, explicația întârzierii prin așteptarea finalizării/răspunsului acestora, deschidere la observații și contrapropunere concretă. Atribuirea către avocați este informația expresă cerută de utilizator, nu certificare independentă a autoriei. Nu există referiri la alți ofertanți sau negociere. Semnătura titularului este adăugată de EVA.
{draftlines}
Fiecare draft pending are două PDF-uri reale proprii: contractul R08 și oferta originală Anlage 5. Nicio anexă comparativă/audit/document al celuilalt prestator. Atașamentele, destinatarii, corpul și statusul au fost citite înapoi din EVA și arhivate ca JSON original, TXT și EML X-Unsent:1 cu ID real de draft și atașamente reale verificate. Drafturile nu sunt mesaje trimise.
Ultimul răspuns comercial real: BERGER 2026.08.17; PECH 2026.09.17. Această operațiune nu este un nou scan general zilnic al mesajelor și nu confirmă acceptarea contractelor. Mailbox office verificat activ; timestamp tehnic de sincronizare păstrat în registrul EVA.
Verificare: două controale independente ale transferului fidel, audit separat al emailurilor, control text PDF și inspecția tuturor celor 64 pagini. R07/R06/R05 și ofertele originale rămân intacte.
Următorul pas: lectura celor două drafturi în EVA, apoi decizia utilizatorului privind trimiterea. Nicio trimitere, semnare ori plată efectuată.
PDF-uri curente:
{links}
Registru: {rel(OUT/f'{DATE} Registru contracte emailuri R08 final.json')}
'''
for p in targets[:2]:prepend(p,entry)
for provider,p in zip(['BERGER','PECH'],targets[2:4]):
    d=next(x for x in eva['drafturi'] if x['provider']==provider)
    e=next(x for x in exports['drafturi'] if x['provider']==provider)
    pdf=next(x for x in deliverables if x['provider']==provider)
    last='2026.08.17' if provider=='BERGER' else '2026.09.17'
    prepend(p,f"{DATE} | {provider}: contract R08 și email EVA draft\nStatus scurt: contract numai germană, fără preambul; email foarte politicos, cu trei alineate transferate integral și cele două PDF-uri proprii. Valorile, serviciile și termenele R07 sunt păstrate.\nUltimul răspuns real: {last}; nicio comunicare comercială nouă identificată prin această operațiune punctuală.\nDraft EVA: {d['draft_id']}, pending / NETRIMIS. To: {', '.join(d['to'])}; CC: {', '.join(d['cc']) or '(fără CC)'}. Nu este acceptare/semnare.\nUrmătorul pas: lectura draftului și decizia utilizatorului privind trimiterea.\nSurse: {pdf['pdf']['cale']}; {e['EML']}; {d['server_readback_path']}. Originalele și istoricul sunt păstrate.")
central=read(regpath);count=len(central['comunicatii']);draftcount=len(central['drafturi'])
for d in eva['drafturi']:
    assert not any(x.get('id')==d['draft_id'] for x in central['drafturi'])
    exp=next(x for x in exports['drafturi'] if x['provider']==d['provider'])
    central['drafturi'].append({'data':DATE,'id':d['draft_id'],'statut':'DRAFT EVA pending / NETRIMIS','cale':exp['TXT'],'expeditor':d['from'],'destinatari':d['to'],'cc':d['cc'],'subiect':d['subject'],'original_EVA':d['server_readback_path'],'EML':exp['EML'],'atasamente':d['attachments']})
central.setdefault('actualizari_punctuale',[]).append({'data':DATE,'tip':'contracte_R08_fara_preambul_emailuri_germane_EVA','registru':rel(OUT/f'{DATE} Registru contracte emailuri R08 final.json'),'livrabile':[d['pdf']['cale'] for d in deliverables],'drafturi_EVA':[d['draft_id'] for d in eva['drafturi']],'status':'2 drafturi EVA pending; NETRIMIS/NESEMNAT','mesaje_noi':0,'drafturi_EVA_create':2,'mesaje_trimise':0,'semnaturi':0,'plati':0})
assert len(central['comunicatii'])==count and len(central['drafturi'])==draftcount+2
regpath.write_text(json.dumps(central,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
prepend(targets[5],f"# {DATE} — Contracte R08 și emailuri germane în EVA\n\nPunct curent pentru lectură:\n\n- ../{deliverables[0]['pdf']['cale']}\n- ../{deliverables[1]['pdf']['cale']}\n\nPDF-urile încep cu WERKVERTRAG și § 1, fără Vorbemerkungen. Cele trei alineate sunt în emailurile proprii, împreună cu intenția de semnare, explicația politicoasă a întârzierii și deschiderea la observații. Toate clauzele, anexele și sumele operative R07 sunt identice: 45.000 / 69.300 EUR net.\n\nDouă drafturi EVA pending / NETRIMISE, cu contractul propriu R08 și oferta proprie originală Anlage 5 ca atașamente PDF reale. În folderele prestatorilor: TXT/JSON/EML și JSON original al readback-ului EVA, ID real, destinatari și CC verificați. Nu au fost trimise mesaje.\n\n{draftlines}\n\nRegistru intern, neatașat: ../{rel(OUT/f'{DATE} Registru contracte emailuri R08 final.json')}. R07 și versiunile anterioare rămân istoric intact; jurnale actualizate, fără dublarea comunicărilor reale sau a atașamentelor primite. Nicio semnare sau plată.")
audits=sorted(OUT.glob(f'{DATE} Audit*.txt'))
emailfiles=[]
for d in exports['drafturi']:
    for key in ['EML','TXT','JSON','server_readback_path']:emailfiles.append(rec(ROOT/d[key]))
record={'data':DATE,'statut':'WERKVERTRAG R08; 2 emailuri EVA DRAFT pending / NETRIMISE','livrabile':deliverables,'drafturi_EVA':eva,'exporturi_email':exports,'emailuri_arhivate_hashuri':emailfiles,'audituri_interne':[rec(p) for p in audits],'transfer_preambul':rec(OUT/f'{DATE} Registru transfer preambul R08.json'),'control_integritate':rec(OUT/f'{DATE} Control integritate PDF R08.json'),'upload_PDF_EVA':rec(OUT/f'{DATE} Registru incarcare PDF in EVA R08.json'),'verificare_octeti_PDF_EVA':rec(OUT/f'{DATE} Verificare octeti PDF EVA R08.json'),'istoric_R07':rec(oldregistry),'istoric_jurnale':backups,'jurnale_actualizate':[rec(p) for p in targets],'comunicatii_reale_neschimbate':count,'drafturi_EVA_create':2,'mesaje_noi':0,'trimiteri':0,'semnaturi':0,'plati':0}
fresh(OUT/f'{DATE} Registru contracte emailuri R08 final.json',json.dumps(record,ensure_ascii=False,indent=2)+'\n')
fresh(OUT/f'{DATE} Jurnal actualizare R08.txt',entry)
print(json.dumps({'status':'PASS','PDF':2,'EVA_drafturi':2,'comunicatii_reale_neschimbate':count,'istoric_originale_intact':True,'trimiteri':0},ensure_ascii=False))
