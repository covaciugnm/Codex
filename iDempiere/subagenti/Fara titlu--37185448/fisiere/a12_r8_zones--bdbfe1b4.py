from a12_r8_cov import *
def attach(obs):
 z=E/'R4_zone/A03/dovezi/Registru_subcriterii_R4.json';d=rd(z);dmap=collections.Counter()
 for i,a in enumerate(d['claims']):
  c=a['criterion_id'];st=a['R4_classification'];phase='current'if st.startswith('PASS')or st.startswith('PARȚIAL')or st.startswith('PARTIAL')else'context';dmap[st]+=1
  obs[c].append(zmake(c,st+'_ANTERIOR_A03','old_current_evidence','Corelare cu registrul nominal A03 R4: se păstrează tipul și oracolul. Nu este o nouă execuție R8.',a['R6_oracle'],a['observed_and_expected'],z,'/claims/'+str(i),a.get('limits')or a.get('limit')or 'Valabil numai la metoda și stratul din fișa A03.','historic_assertion_limited'))
 # UX and currency: only if authentic target row.
 z=E/'R6_supliment/A12_UX_NIR_provenienta.json';data=rd(z)
 for k,y in data['by_criterion'].items():
  obs[k].append(zmake(k,'ZK_FORMULAR_DOUĂ_ROLURI','old_context','Confirmarea deja realizată în R6 pentru deschiderea meniurilor; fără o nouă sesiune R8.', 'Forma se deschide pentru cele două roluri de test.',{'form_rows':y},z,'/by_criterion/'+esc(k),'Nu validează totaluri, drepturi de operație, emitere sau plăți.'))
 c='T354-R2-021';p=E/'R8_pregatire/A05/T354_nativ_complet.json'
 if p.exists():
  groups=rd(p);ii,ix,v=next((ii,i,l)for ii,m in enumerate(groups)for i,l in enumerate(m['lines'])if l.startswith('CRIT C-20 |'));obs[c].append(zmake(c,'PROCES_NATIV_AUTO_C20_A05','current','Aceeași proba operatorului A05 din clasificarea C20, fără a număra o nouă execuție A12.','Stoc A6 vs5; două comenzi site S×1 REZERVAT, cerere totală A4.',v,p,'/'+str(ii)+'/lines/'+str(ix),'Primele două comenzi au rânduri de staging persistente şi ord=0, numai a treia generează C_Order 1000089 în cazul A6. Evenimente secvențiale din același scenariu, nu două tranzacții ERP simultane; nici două C_Order pentru primele două.','complete_at_staging_criterion_only'))
 c='T354-R2-027';p=E/'Reverificare_G3_rezervare_canal.json';m=rd(p)
 for i in [0,1,2]:
  val=m['observations'][i];obs[c].append(zmake(c,'PUBLICARE_G3_DOUĂ_G1_SQL','old_current_evidence','Analiză mai veche, validată pe două warehouse-uri pe calea canalului.', '10+10−7=13 pe două G1; PO de 4 nu este vânzare.',val,p,'/observations/'+str(i),'13 pe vânzare; cu PO IsSOTrx=N, 9 în loc de 13. Suma celor două disponibilități operative nu este apelul real de publicare.'))
 ixp=E/'R8_pregatire/Index_883_relectura_surse.json';au=E/'R8_pregatire/A11';peer=E/'R8_pregatire/T159';named=[p for p in (E/'R8_pregatire').rglob('*')if p.is_file()and re.search('M.B4|159.*050|receptie.*a03',p.name,re.I)]
 c='T159-R2-050';oldz=next(q for q in obs[c]if q['kind']=='CONFORM_ORACOL_EXECUTAT_A03');oldz['coverage']='vacuous_cli_only';oldz['qualification']+=' Rezerva A11: 302 chei MUTA/TEXT înghețate; zero comparabile din ele în clasificarea actuală, deci «0 reclasificate» nu dovedește conservarea.';oldz['id']=stripped_id({k:v for k,v in oldz.items()if k!='id'})
 p=next((n for n in named if n.suffix=='.json'and '050'in n.name),None)
 if p is None:p=E/'R8_pregatire/A03/Registru_A03_R8_final.json';pointer='/r8/'+str(next(i for i,a in enumerate(rd(p)['r8'])if a['criterion']==c))
 else:pointer=''
 obs[c].append(zmake(c,'REZULTAT_VID_FĂRĂ_DOVADA_CONSERVĂRII','correction','Verificare semantică A11 a intersecției comparate.', 'Cele 302 chei inițiale (224+78) trebuie urmărite chiar dacă dispar.','302 chei inițiale, 0 în MUTA/TEXT în sursa curentă, intersecție 0; CLI 0 reclasificate. Conservarea rămâne neprobată.',p,pointer,'Metoda originală examinează intersecția. Nicio cheie comună nu poate constitui rezultat pozitiv privind disparițiile.', 'audit_semantic_limit'))
 a11=E/'A11_control_suplimente_R7_R8.json';pw='/A03/T159_R2_050_own_secondary_witness';tv=ptr(rd(a11),pw)
 obs[c].append(zmake(c,'MARTOR_INDEPENDENT_A11','correction','Martor static auditor: cazul inițial și cheie readăugată / clasificare divergentă.', 'Urmărește 302 chei și diferența observată realmente pe domeniu comun.',tv,a11,pw,'Acest experiment al auditorului validează limita scriptului, nu conservarea reală a tuturor deciziilor.','audit_semantic_limit'))
 c='T04.06-R3-001'; exp=E/'R8_pregatire/T04.06/EVA_Export_CESIRO1_readonly.json';rv=rd(exp);obs[c].append(zmake(c,'CLIENT_PYTHON_CESIRO1_5_ACCEPTATE_7_REFUZATE_5_ACCEPTĂRI_SUPLIMENTARE','current','Transport fără socket pe implementarea de referință CESIRO1.', 'Căile permise funcționează iar orice altă cale sau schemă nepermisă se respinge înainte de transport.',rv['counts'],exp,'/counts','Clientul Python admite cinci cereri suplimentare față de lista închisă. Nu este încă verificată implementarea conectorului de export în pluginul ERP pentru aceste șapte cazuri.'))
 a11=E/'A11_control_T04_06_oracol_R8.json';r=rd(a11);obs[c].append(zmake(c,'CORELARE_A11_EXPORT_ȘI_EMAG','correction','Adjudecare independentă a codurilor JAR și a clientului CESIRO1.', 'Acordă separat eMAG, referința export și pluginul iDempiere.',r['disposition'],a11,'/disposition','Rezultatul se limitează la contractul simulat, fără transfer real.','audit_semantic_limit'))
 c='T06-R2-001';p=P/'T06_denominatori_AD_reconciliati.json';v=rd(p);obs[c].append(zmake(c,'READBACK_EVA_40_DIN_50_TOTAL','current','În ambele capturi se numără distinct toate coloanele și numai prefixul EVA_.',v['oracle'],{'actual':dict(zip(v['current_labels'],v['current_counts'])),'historical_recomputed':v['historical_blob']['lines']},p,'','Numărătoarea are aceleași rezultate în ambele epoci; nu s-a identificat o creștere de 10 coloane.'))
 return {'historical_A03':dmap,'semantic_A11_T159_inputs':named}
if __name__=='__main__':
 os.environ['A12_R8_PREVIEW']='1';o,_=sources();print(attach(o))

