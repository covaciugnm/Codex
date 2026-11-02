from pathlib import Path
p=Path(__file__).with_name('a12_r10_publish.py');s=p.read_text(encoding='utf8');marker=" extra=[v for v in reg if v['cohorts']['external_38']]"
pre=""" afr=[q['id']for q in read(E/'A11_control_A12_R9.json')['remaining_reaudit']];assert len(afr)==5
 stage['five_A11_actions_receipt']={
 'R9-Q1':{'asked':afr[0],'intake_distinct':[164,873,167],'direct_or_documentary_in_164':q['in_164_receipted'],'pending_from_intake_164':sorted(v['criterion']for v in reg if v['R10_entry_cohorts']['164']and v['R10']=='NEEXECUTAT'),'lookups':['Registru_reexecutare_R10.json','A12_raport.json#/all_ten_zones']},
 'R9-Q2':{'asked':afr[1],'bounds':S(p07),'metadata_crosscheck':S(P10/'T216_metadate_R9_corectate.json'),'result':'Originea proprie a ajuns la antet, dar conversia s-a oprit înaintea unui C_Order eligibil. Factura, numărul, încasarea și returul din aceeași comandă rămân neprobate. TVA 21% este condiție diferită.'},
 'R9-Q3':{'asked':afr[2],'independent':S(E/'A11_control_supliment_G3_C20_postR9.json'),'ids':['T354-R2-004','T354-R2-021','T354-R2-027'],'result':'Au fost separate documentele persistente cu produse primare, refuzul setului în calea manuală, repetarea creării POST și repetarea CO pe documentul existent.'},
 'R9-Q4':{'asked':afr[3],'handoff_A05':zone.get('A05'),'ids':['T329-R2-012','T330-R2-025'],'rule':'Controlul costului pe schemă și ASI și numitorul suitei de la export nu sunt interschimbabile.'},
 'R9-Q5':{'asked':afr[4],'routers_873':S(histfile),'comparator_on_intake_873':q['in_873_receipted'],'example_signed_references':[S(P10/'Registru_documentar_A12.json'),S(P10/'T210_auth_trace_routes.json'),S(P10/'T227_mutanti_nominali.json'),S(P10/'Zone_A02_A10/T254_bytecode.json')],'limit':'Documentul autoritativ, sursa unei implementări, un rezultat istoric și o măsurare refăcută sunt nivele distincte.'}}
"""
assert marker in s;s=s.replace(marker,pre+marker);p.write_text(s,encoding='utf8')
