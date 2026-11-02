from a12_r3_survey import *
from pathlib import Path
p=Path(__file__).parent/'a12_r4_run.py';s=p.read_text(encoding='utf8')
s=s.replace("def native(c,k):","""android_inputs=rd(R/'probe/Android_snapshot_R4.json')
def androidsnap(c,k):
 old=c['current'];ids=old.get('evidence_ids',[]);candidate=[]
 for eid in ids:
  e=ev.get(eid,{});data=e.get('content_or_observation')or{};aid=data.get('id') if isinstance(data,dict)else None
  if aid in android_inputs and k in android_inputs[aid]['aliases']:candidate.append(aid)
 if not candidate:return
 used=[]
 for aid in set(candidate):
  d=android_inputs[aid];ee=efile('inputs/android/'+d['file'],'/observed și /observed_server /observed_accessibility',{'id':aid,'state':d['status'],'observed':d['observed'],'instrumentation_finished':d['finished'],'passing_subset':d['passing_subset_in_card'],'server_interpretation':d['server_basis'],'hardware':d['hardware'],'limits':d['limit']},'ANDROID_POST_R3_EXECUTAT','Snapshot nou al aceluiași card după instrumentare. AVD/DAO/server/hardware sunt distincte; nu echivala clasa sau numărul de teste cu respectarea întregului task.')
  used.append(ee)
  if aid=='AND04' and c['id']in ('T333-R2-005','T334-R2-006'):
   obs='Pe aceeași firmă cu rol numai citire: cheia nouă primește 403, dar aceeași cheie deja în jurnal primește 409. Zero efecte străine în acest caz; răspunsul dezvăluie existența cheii. Caz separat de acces cu dispozitiv revocat și de izolarea fizică între cabinete.'
  elif aid=='AND06':obs='Manifestul și registrul delimitează interoperabilitatea Android WMS C17 de iOS WMS C18 și ERP general C19/C20. Aceste alte trei suprafețe nu au dovadă runtime. Nu se transferă un PASS de clasificare către o funcție din task.'
  else:obs=d['observed']+' Instrumentare finalizată; teste reușite aferente cardului '+str(d['passing_subset_in_card'])+'. '+(d['server_basis']or'')+' '+d['hardware']+' Starea integrală a cardului: '+d['status']+'. Un defect al cardului se verifică în oracolul concret, nu se copiază automat pe fiecare task din capitol.'
  attach(c,'PARȚIAL_ANDROID_POST_R3' if aid!='AND04' or c['id'] not in ('T333-R2-005','T334-R2-006') else 'CONTRAEXEMPLU_AND04_REPLAY_AUTORIZARE',obs,[ee]+old.get('evidence_ids',[]))
def native(c,k):""")
s=s.replace("native(c,k);gl_update(c,k)","native(c,k);gl_update(c,k);androidsnap(c,k)")
s=s.replace("attach(c,'PROBĂ_NATIVĂ_MULTISTADIU_LIMITATĂ'","""if (IN/'Reverificare_SAGA_schema_secundara.json').exists():
   sd=rd(IN/'Reverificare_SAGA_schema_secundara.json');ds.append(ent('Reverificare_SAGA_schema_secundara.json','/observations',sd['observations'],sd['boundary']))
  attach(c,'PROBĂ_NATIVĂ_MULTISTADIU_LIMITATĂ'""")
s=s.replace("Cele 2 note fidele din schema 101 nu dovedesc distribuție echivalentă în toate schemele native, iar toate intrările G1–G6 nu sunt certificate.","La import nativ L8 existau patru rânduri în schemele 101 și 200000; L12 a înlocuit ambele perechi cu doar două rânduri în schema 101. Repetarea a păstrat cele două ID. Este diferență măsurată multi-schemă, separată de protecția reușită a notelor. Toate intrările G1–G6 nu sunt certificate.")
s=s.replace("w['A11_score_R4']=None","""w['A11_score_R4']=None
 w['active_R4_outcome']={'status':'EVALUAT_INDIVIDUAL_PARȚIAL','source_owner_accepted':False if newcase else 'vezi categoria și autoritatea fiecărei cerințe','unknown_functional_execution_for_new_alias':('Documentarea sau reconstituirea unui obiectiv identifică scopul, fără a proba automat funcția.' if newcase else None),'closure_vs_current':'Câmpurile decision_at_closure și decision_current au fost copiate ca istoric R2, iar current din fiecare criteriu și acest bloc sunt active pentru R4.','open_requirements':[c['id']for c in allc if c['current']['status']=='NEEXECUTAT'],'R4_score_independent':None}
 w['R4_control_register']={key:{'baseline_R3':v['baseline'],'area':key,'source':w['R4_source_identity']['primary_sha'],'status_R4':'CONTROL_INVENTAR_VERIFICAT' if key in ('A12-CK-01','A12-CK-02','A12-CK-30','A12-CK-35','A12-CK-36')else 'AVIZ_A11_IN_AȘTEPTARE' if key=='A12-CK-34'else 'REZULTATE_LIMITATE_LA_CERINȚE','criteria_with_R4_specific_results':[c['id']for c in allc if c.get('current_R3_before_R4')and c['id']in v.get('r3_related_criteria',[])],'complete_product':False}for key,v in w['control_register_R3'].items()}""")
s=s.replace("'Devalidarea","'Devalidarea")
s=s.replace("'records':rows});print(counts","'readable_index':'Audit_individual_P01_R4.html','findings_requiring_decision':[{'case':'T352-R04','observation':'Implicit N este conform; Y cu stoc 8 și furnizor 7 ori 25% rămâne 8 pe calculatorul Git, față de 15/33 în contractul condițional. Clasa nu este montată.'},{'case':'T257','observation':'După import L12, numai 2 note fidele schema 101 înlocuiesc 4 în două scheme; protecții și replay dovedite, politica schemei secundare necesită decizie.'},{'case':'T333/T334','observation':'Rol de citire, cheie existentă 409 versus cheie nouă 403; nu a divulgat valori și nu a modificat documentul.'},{'case':'T08.03','observation':'79 TSV păstrează markerul de ciornă; aprobarea consultantului la închidere este neconfirmată.'},{'case':'T157/închidere contabilă','observation':'Procesul a postat 120 în schema EUR din 100 USD + 20 EUR în fixture. Stornarea a fost verificată separat.'},{'case':'T259','observation':'Forma reală 4/4 pe două roluri; există test Playwright versionat și raport istoric 0→1→0.'}],'records':rows});print(counts")
p.write_text(s,encoding='utf8')

