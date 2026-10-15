from pathlib import Path
from decimal import Decimal
import hashlib, json

BASE=Path.cwd()
OUT=BASE/'00.Proiect/09. Vertraege/2026.10.13 Contracte R08 - intern'
R06=BASE/'00.Proiect/09. Vertraege/2026.10.13 Baza comuna negociere BERGER PECH/2026.10.13 R06 propuneri negociere'
EXPECTED={'BERGER':'9797b24b4e40fb55deb2520c756a6b190d58bac652846903d70d13e3957f6983','PECH':'c81e78c1e166d0a2095569d84391153dd70b957504f0dcf31360a80dfb90d8c5'}
NET={'BERGER':Decimal('45000'),'PECH':Decimal('69300')}
OPT={'BERGER':Decimal('1000'),'PECH':Decimal('2700')}
FIELDS=['sections','annexes','signatures','presentation']

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def dec(v): return Decimal(v.replace('.','').replace(',','.'))
def eur(v): return str(v.quantize(Decimal('.01')))

regp=OUT/'2026.10.13 Registru transfer preambul R08.json'
registry=read(regp)
records=[]
for item in registry['operatiuni']:
 who=item['provider']
 p7=BASE/item['R07_source']; p8=BASE/item['R08_source']; ep=BASE/item['R08_email_source']
 assert sha(p7)==item['R07_sha256'], (who,'R07 source hash')
 assert sha(p8)==item['R08_sha256']==EXPECTED[who], (who,'R08 source hash')
 assert sha(ep)==item['R08_email_sha256'], (who,'email source hash')
 s7=read(p7);s8=read(p8);mail=read(ep)
 for f in FIELDS: assert s8[f]==s7[f], (who,'operative field changed',f)
 assert len(s8['sections'])==16 and len(s8['annexes'])==6
 assert s8.get('preamble',[])==[], (who,'contract preamble not removed')
 pre=s7['preamble'];assert len(pre)==3
 assert pre==item['preamble_moved_verbatim'], (who,'registry preamble mismatch')
 body=mail['body_de']; paragraphs=body.split('\n\n')
 positions=[]
 for p in pre:
  assert body.count(p)==1, (who,'preamble occurrence wrong')
  assert p in paragraphs, (who,'not an intact standalone paragraph')
  positions.append(paragraphs.index(p))
 assert positions==list(range(positions[0],positions[0]+3)), (who,'preamble order changed')
 assert mail['eva_mail_draft_id'] is None and 'NETRIMIS' in mail['status']
 assert mail['attachments']==[], (who,'source claims attachments before publication')
 evidence=mail['recipient_evidence']; srcmail=BASE/evidence['source_mail']; sm=read(srcmail)
 assert sha(srcmail)==evidence['sha256'] and sm['id']==evidence['eva_mail_id']
 assert mail['to']==[sm['from_address'].lower()]
 assert [v.lower() for v in mail['cc']]==[v.lower() for v in sm['cc']]
 assert 'Bitte prüfen Sie den Vorschlag und teilen Sie uns Ihre Anmerkungen mit.' in body
 assert 'einen konkreten Gegenvorschlag' in body
 assert 'Die beiderseitige Unterzeichnung des Vertrags erfolgt anschließend gesondert.' in body
 other='PECH' if who=='BERGER' else 'BERGER'
 assert other.lower() not in body.lower(), (who,'other provider named in email')
 r6=read(R06/f'2026.10.13 Werkvertrag {who} R06 Entwurf.json')
 a8=s8['annexes'][3]
 assert len(a8['tables'])==6
 for x,y in zip(a8['tables'],r6['annexes'][3]['tables']): assert x['rows']==y['rows'], (who,'audited price row changed')
 net=NET[who];opt=OPT[who]
 totals=[dec(v) for v in a8['tables'][0]['rows'][-1][1:]]
 assert totals==[net,net*Decimal('.20'),net*Decimal('1.20')]
 assert sum(dec(r[-1]) for r in a8['tables'][1]['rows'][:-1])==net
 budget=a8['tables'][5]['rows']
 assert [dec(v) for v in budget[0][2:]]==[opt,opt*Decimal('1.20')]
 assert [dec(v) for v in budget[1][2:]]==[net+opt,(net+opt)*Decimal('1.20')]
 records.append({'provider':who,'status':'PASS surse','R07_source':item['R07_source'],'R07_sha256':sha(p7),'R08_source':item['R08_source'],'R08_sha256':sha(p8),'R08_email_source':item['R08_email_source'],'R08_email_sha256':sha(ep),'exact_equal_fields':FIELDS,'sections':16,'annexes':6,'contract_preamble_removed':True,'three_preamble_paragraphs_transferred_verbatim_once_in_order':True,'paragraph_positions_in_email':positions,'all_six_financial_table_rows_identical_to_audited_R06':True,'base_net_eur':eur(net),'vat20_eur':eur(net*Decimal('.20')),'base_gross_eur':eur(net*Decimal('1.20')),'six_options_net_eur':eur(opt),'six_options_gross_eur':eur(opt*Decimal('1.20')),'package_if_all_six_net_eur':eur(net+opt),'package_if_all_six_gross_eur':eur((net+opt)*Decimal('1.20')),'to':mail['to'],'cc':mail['cc'],'source_recipient_verified':True,'email_status':mail['status'],'no_other_provider_in_email':True,'published_pdf_pending':item['PDF_expected'],'original_offer_attachment_expected':item['offer_original_copy'],'original_offer_sha_expected':item['offer_sha256']})

report={'date':'2026.10.13','title':'Audit independent R08: identitatea contractului, transferul preambulului și protecția prețurilor','status':'PASS pentru sursele JSON și corpul emailurilor','registry_sha256':sha(regp),'providers':records,'findings':[],'limitations':['Acesta este un control al mutării preambulului, nu o nouă analiză comercială sau juridică integrală.','Sections, annexes, signatures și presentation sunt identice cu R07 final; toate rândurile financiare sunt identice și cu R06 auditat.','TXT/EML și PDF-urile publicate sunt încă în curs de export. Identitatea atașamentelor efective și absența preambulului în PDF necesită readback separat al publicației.','Emailurile sunt drafturi locale netrimise; nu a fost creat niciun draft în EVA și nu există comandă, semnare sau plată confirmată.'],'edits_to_contract_sources':0,'emails_sent':0,'eva_drafts_created':0}
rp=OUT/'2026.10.13 Audit independent transfer preambul R08.json'
rp.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['2026.10.13 — Audit independent transfer preambul R08','PASS pentru sursele JSON și corpul emailurilor; fără constatări deschise în această etapă.','']
for r in records:
 lines += [r['provider']+' — R08 SHA '+r['R08_sha256'],'R07 final SHA '+r['R07_sha256'],'Email sursă SHA '+r['R08_email_sha256'],'Identitate exactă R07→R08: sections, annexes, signatures, presentation; 16 capitole și 6 anexe.','Preambul: eliminat din sursa contractului; toate cele 3 alineate transferate textual, integral, o singură dată, în aceeași ordine și ca paragrafe separate în email.','Toate cele 6 tabele financiare: rânduri identice cu R06 auditat; onorariul, regia, retenția, alocările, cele 7 rate și opțiunile sunt păstrate.','Bază: '+r['base_net_eur']+' EUR net + '+r['vat20_eur']+' TVA = '+r['base_gross_eur']+' brut.','6 opțiuni: '+r['six_options_net_eur']+' net / '+r['six_options_gross_eur']+' brut; total condiționat: '+r['package_if_all_six_net_eur']+' net / '+r['package_if_all_six_gross_eur']+' brut.','Destinatari confirmați din mesajul original arhivat: '+', '.join(r['to'])+'; CC '+(', '.join(r['cc']) or '—')+'.','Emailul nu numește celălalt prestator; cere verificare, observații ori contrapropunere și păstrează semnarea separată.','']
lines += ['Limită: '+v for v in report['limitations']]
(OUT/'2026.10.13 Audit independent transfer preambul R08.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'status':'PASS surse','report':str(rp.relative_to(BASE)),'sha256':sha(rp)},ensure_ascii=True))
