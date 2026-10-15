from pathlib import Path
import json, hashlib, shutil
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent;DATE='2026.10.13'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def rel(p):return str(p.relative_to(ROOT)).replace('\\','/')
def rec(p):return {'cale':rel(p),'sha256':sha(p),'octeti':p.stat().st_size}
def fresh(p,s):assert not p.exists(),p;p.write_text(s,encoding='utf-8')
edit=read(OUT/f'{DATE} Registru aplicare editoriala R07.json')
drafts=read(OUT/f'{DATE} Registru drafturi locale R07.json')
assert len(drafts['drafturi'])==2 and drafts['mesaje_trimise']==0 and drafts['drafturi_EVA_create']==0
deliverables=[]
for operation in edit['operatiuni']:
    provider=operation['provider'];pdf=ROOT/operation['PDF_expected'];src=ROOT/operation['R07']
    assert sha(src)==operation['R07_sha256'] and sha(ROOT/operation['public_source'])==sha(src)
    assert sha(ROOT/operation['source_R06']['file'])==operation['source_R06']['sha256']
    assert sha(ROOT/operation['offer_copy'])==operation['offer_sha256']
    qa=read(OUT/f'{DATE} QA text {provider} R07.json')
    assert qa['text_status']=='PASS' and qa['pdf_sha256']==sha(pdf) and qa['source_sha256']==sha(src)
    visual=OUT/f'{DATE} QA vizual {provider} R07.txt';assert visual.exists()
    deliverables.append({'provider':provider,'pdf':{**rec(pdf),'pagini':len(PdfReader(pdf).pages)},'sursa':rec(src),'oferta_originala':rec(ROOT/operation['offer_copy']),'qa_text':rec(OUT/f'{DATE} QA text {provider} R07.json'),'qa_vizual':rec(visual)})
oldregistry=ROOT/'00.Proiect/09. Vertraege/2026.10.13 Baza comuna negociere BERGER PECH/2026.10.13 R06 propuneri negociere/2026.10.13 Registru contracte elegante R06.json'
old=read(oldregistry)
for d in old['livrabile']:assert sha(ROOT/d['pdf']['cale'])==d['pdf']['sha256'];assert sha(ROOT/d['sursa_canonica']['cale'])==d['sursa_canonica']['sha256']
for r in old['contracte_R05_frozen']:assert sha(ROOT/r['cale'])==r['sha256']
regpath=ROOT/f'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/{DATE} Registru comunicatii.json'
partners=ROOT/'08. Corespondenta/2026.09.30 Arhiva Eva-Mail/Parteneri'
targets=[ROOT/f'{DATE} Status proiect.txt',ROOT/f'{DATE} Log progres proiect.txt',partners/f'{DATE} Log discutii - Markus Berger.txt',partners/f'{DATE} Log discutii - Pech.txt',regpath,ROOT/'folder map/README.md']
history=OUT/f'{DATE} Istoric jurnale inainte R07';assert not history.exists();history.mkdir()
backup=[]
for p in targets:
    dest=history/(p.name if p.name.startswith(DATE) else f'{DATE} {p.name}');shutil.copy2(p,dest);assert sha(p)==sha(dest);backup.append({'original':rel(p),'copie':rel(dest),'sha256_inainte':sha(p)})
links='\n'.join(d['pdf']['cale'] for d in deliverables)
entry=f'''2026.10.13 | Propunerile A&C de contract R07 și emailuri locale
Status scurt: prezentare externă revizuită la instrucțiunea utilizatorului. Fiecare PDF privește exclusiv A&C și prestatorul său și se intitulează VERTRAGSVORSCHLAG. Nu prezintă alți ofertanți, comparații, comentarii despre diferențe sau despre negociere. Condițiile efective, serviciile și termenele sunt păstrate. R06 și originalele rămân istoric intact.
Prețuri originale nemajorate: BERGER 45.000 EUR net / 54.000 EUR cu TVA20%; PECH 69.300 EUR net / 83.160 EUR cu TVA20%. Toate cele4/6 poziții, alocările și ratele sunt păstrate; nicio taxă PI/BWB/lunară nouă. Vizitele suplimentare deja autorizate rămân opțiuni separate, numai la comandă: BERGER raport2.000/12, maximum1.000 EUR net pentru6; PECH450 EUR net, maximum2.700 EUR net pentru6. Nu sunt adăugate la prețul de bază și nu sunt comandate anticipat.
Structură păstrată:16capitole,96alineate principale și6anexe;12vizite fizice B0+posibil6,18luni B0, T0 inițial inclus separat, PI/§128, Bauwerksbuch existent+intervenții noi, fărăBauKG și managementgeneralREALIG. Sumele și termenele nu au fost modificate prin redactarea editorială.
Verificare: aplicare exactă a 83 de înlocuiri editoriale și ultima neutralizare identică § 3(7) în fiecare document (85 de înlocuiri în total), controale independente de fidelitate și cifre, verificarea textului PDF și inspecție individuală a paginilor. Documentele sunt propuneri, nu contracte acceptate, semnate ori executate.
Emailuri pregătite separat în germană, local TXT/JSON/EML cu atașamente PDF reale: propunerea proprie R07 și oferta proprie originală Anlage5. Cer analiza propunerii, observații scrise sau o contrapropunere concretă dacă nu o pot accepta în forma transmisă; dacă nu au observații pot confirma acordul, semnarea fiind un pas ulterior separat. Nu menționează alți ofertanți ori comparații. EML are X-Unsent:1, ID Eva-Mail draft nul, readback și hashuri atașamente verificate. Nu sunt drafturi create în EVA.
Destinatari: BERGER office@bmberger.at; PECH sekretariat@zt-pech.at, CC ployer@zt-pech.at, confirmați din mesajele originale arhivate.
Ultimul răspuns real: BERGER2026.08.17; PECH2026.09.17. Nicio comunicare nouă primită ori trimisă, fără scan general zilnic EVA în această operațiune.
Următorul pas: lectura PDF-urilor R07 și a textelor email. Folosiți numai pachetul R07 pentru viitoarea transmitere; rapoartele comparative și R06 nu fac parte din atașamente. Nicio trimitere, semnare sau plată efectuată.
PDF-uri curente:
{links}
Registru: {rel(OUT/f'{DATE} Registru propuneri R07 final.json')}
'''
def prepend(p,s):p.write_text(s.rstrip()+'\n\nISTORIC PĂSTRAT\n\n'+p.read_text(encoding='utf-8-sig'),encoding='utf-8')
for p in targets[:4]:prepend(p,entry)
reg=read(regpath);count=len(reg['comunicatii'])
reg.setdefault('actualizari_punctuale',[]).append({'data':DATE,'tip':'propuneri_A_C_contract_R07_prezentare_individuala','registru':rel(OUT/f'{DATE} Registru propuneri R07 final.json'),'livrabile':[d['pdf']['cale'] for d in deliverables],'drafturi_locale':[d['EML'] for d in drafts['drafturi']],'status':'PROPUNERE A&C; NETRIMIS/NESEMNAT; drafturi locale, nu EVA','mesaje_noi':0,'drafturi_EVA_create':0,'mesaje_trimise':0,'semnaturi':0,'plati':0})
assert len(reg['comunicatii'])==count;regpath.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
prepend(targets[5],f'''# 2026.10.13 — Propuneri individuale A&C de contract R07

Punct curent pentru lectură și viitoarea transmitere:

- ../{deliverables[0]['pdf']['cale']}
- ../{deliverables[1]['pdf']['cale']}

Fiecare propunere este VERTRAGSVORSCHLAG, privește exclusiv părțile proprii și păstrează prețul ofertat (45.000/69.300 EUR net). Nu există referiri în textul extern la alți ofertanți, negociere sau diferențe față de ofertă. Condițiile efective rămân:18 luni B0,12vizite plus până la6opționale separat comandate, T0 inclus, PI/§128 și Bauwerksbuch întregul existent/nou. Opțiunile nu sunt adăugate automat la prețul de bază. Originalele și R06 sunt intacte.

În folderele R07 ale fiecărui prestator există PDF, sursa JSON proprie, oferta originală Anlage5 și emailuri locale TXT/JSON/EML NETRIMISE. EML include numai propunerea proprie și oferta originală proprie, cu atașamente reale. Destinatarii sunt cei verificați din arhivă; ID Eva-Mail draft nul, nu au fost create drafturi în EVA. Textul cere analiza propunerii, observații sau contrapropunere concretă; semnarea este separată.

Registru și rapoarte INTERNE, care nu se atașează: ../{rel(OUT/f'{DATE} Registru propuneri R07 final.json')}. Jurnalele păstrează istoricul; numărătorile email rămân neschimbate. Nicio trimitere, semnare sau plată.
''')
audits=list(OUT.glob(f'{DATE} Audit*.txt'));assert len(audits)>=3
record={'data':DATE,'statut':'PROPUNERE A&C DE CONTRACT; emailuri locale NETRIMISE','livrabile':deliverables,'drafturi':drafts,'audituri_interne':[rec(p) for p in audits],'registru_editorial':rec(OUT/f'{DATE} Registru aplicare editoriala R07.json'),'istoric_R06':rec(oldregistry),'istoric_jurnale':backup,'jurnale_actualizate':[rec(p) for p in targets],'mesaje_noi':0,'EVA_drafturi_create':0,'trimiteri':0,'semnaturi':0,'plati':0}
fresh(OUT/f'{DATE} Registru propuneri R07 final.json',json.dumps(record,ensure_ascii=False,indent=2)+'\n');fresh(OUT/f'{DATE} Jurnal actualizare R07.txt',entry)
print(json.dumps({'status':'PASS','PDF':[d['pdf'] for d in deliverables],'drafturi_locale':2,'comunicatii_neschimbate':count,'R06_R05_originale_intacte':True},ensure_ascii=False))
