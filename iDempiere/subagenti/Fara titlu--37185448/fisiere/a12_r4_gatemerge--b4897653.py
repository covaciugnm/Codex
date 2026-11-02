from a12_r3_survey import *
from pathlib import Path
p=Path(__file__).parent/'a12_r4_run.py';s=p.read_text(encoding='utf8');s=s.replace("from a12_r4_recovery_map import dec","from a12_r4_recovery_map import dec\nfrom a12_r4_dependencies import dep")
s=s.replace("t1=rd(R/'Java/executii.json');t2=rd(R/'Java/executii2.json');tr=t1+t2;","t1=rd(R/'Java/executii.json');t2=rd(R/'Java/executii2.json');scan=rd(R/'Java/scaner.json');scal=rd(R/'Java/scan_calibrat/observat.json');tr=t1+t2+scan;")
s=s.replace("('Java/executii2.json',t2),('Java/retry/executii.json',retry)","('Java/executii2.json',t2),('Java/scaner.json',scan),('Java/retry/executii.json',retry)")
s=s.replace("f=fam(c);actor,fixture,steps,negative,surface=families[f]","f=fam(c);actor,fixture,steps,negative,surface=families[f];dd=dep(k,c)")
s=s.replace("'requires_external_or_hardware':bool(re.search('terminal fizic|telefon fizic|scanner fizic|cont partener real|aprobare.+proprietar|consultantul confirmă',c['normative_content'],re.I))","'requires_external_or_hardware':dd['requires_external_or_hardware'],'resource_split':dd")
s=s.replace("obs=[]\n for fp in ['Reverificare_inchidere_GL_doua_scheme.json'","obs=[]\n for fp in ['Reverificare_inchidere_GL_doua_scheme.json'")
s=s.replace("if k=='T259':\n  ds=[]","""if k=='T328' and id in ('T328-R2-002','T328-R2-003','T328-R2-004'):
  cc=rd(R/'Java/scan_calibrat/observat.json');ids=[efile('Java/scan_calibrat/observat.json','/0..1',cc,'TEST_PROIECT_ORIGINAL_CALIBRARE','Runner Windows al parserului javap: LF normalizat ca în proiect. Leagă bytecode și cazuri simulate, nu scanner hardware sau interacțiune ZK reală.')]
  for n in ('git','instalat'):
   candidates=[(j,z) for j,z in enumerate(scal) if z['target']==n];j,z=candidates[0];pth=R/'Java/scan_calibrat'/z['log'];lines=pth.read_text(encoding='utf8').splitlines();als=[(i,l[:230])for i,l in enumerate(lines,1)if re.search('legatura:|REZULTAT|cartela .* (S2|necunoscut|ambiguu|ostil)',l)];ids.append(efile('Java/scan_calibrat/'+z['log'],'asis:15/15 and individual cards',{'sample':als[:6]+als[-2:],'total_matching_assertions':len(als)},'SCANARE_COMPONENTĂ'))
  attach(c,'COMPONENTĂ_SCANARE_DOVEDITĂ_HARDWARE_NEEXECUTAT','TestScanareCod 98/0 pe ambele JAR. TestScanareEcrane original: 296/27 în Windows inițial; cu LF pentru parserul javap, 327/0 și legături 15/15 în ambele JAR. Cartela de cazuri valide/necunoscute/ambigue/ostile este exercitată de test. Competența cu scanerul fizic, focus real și Enter rămâne distinctă; T328 nu e integral extern.',ids);return
 if k=='T351' and id.endswith('002'):
  vs=suite_rows.get('TestT22Stripe',[]);ids=[]
  for ds,j,rec in vs:
   l=(R/'Java'/rec['log']).read_text(encoding='utf8').splitlines();hits=[(i,v[:290])for i,v in enumerate(l,1)if re.search('C-351.01|terminal/readers|terminal/locations|refuz LOCAL',v,re.I)and re.match(r'^\\s*OK',v)][:6];ids.append(efile('Java/'+rec['log'],'allowlist read-only',hits,'TEST_DE_CONTRACT_COMPONENTĂ','Citire și allowlist; nici decontare la POS, nici activare autorizată de proprietar.'))
  if ids:attach(c,'CONTRACT_LOCAL_PROBAT_POS_REAL_NEEXECUTAT','Suita Git/instalat dovedește doar cele 9 căi admise, inclusiv citirile Terminal locations/readers, și refuzul gazdelor/verbului nedefinit. Nu s-a făcut plată, activarea este amânată de proprietar; cont sandbox/dispozitiv pentru porțiunea de acceptare externă.',ids)
  return
 if k=='T259':
  ds=[]""")
s=s.replace("w['R4_technical_scope_and_routes']=nativecase;", "w['R4_technical_scope_and_routes']=nativecase;w['R4_resource_boundaries']=[{'criterion':c['id'],**dep(k,c)}for c in allc if dep(k,c)['external_or_physical_part_only'] or k in ('T328','T335','T336','T338','T351')];")
s=s.replace("'archive_paths_inspected_by_name':", "'archive_paths_inspected_by_name':")
s=s.replace("'unit_calibrations':len(retry),","'unit_calibrations':len(retry)+len(scal),'initial1868_requiring_external_portion_only':sum(v['requires_external_or_hardware'] for v in plans if v['original_NEEXECUTAT_R3']),'initial1868_resource_categories':dict(Counter(v['resource_split']['classification']for v in plans if v['original_NEEXECUTAT_R3'])),")
p.write_text(s,encoding='utf8')

