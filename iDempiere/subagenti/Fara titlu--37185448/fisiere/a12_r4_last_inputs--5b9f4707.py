from pathlib import Path
t=Path(__file__).parent;p=t/'a12_r4_dependencies.py';s=p.read_text(encoding='utf8').replace('LOCAL_AVEC_PREUVE_HISTORIQUE','LOCAL_CU_PROVENIENȚĂ_ISTORICĂ').replace('LOCAL_CORPUS_OU_LABORATOR','LOCAL_CORPUS_SAU_LABORATOR');p.write_text(s,encoding='utf8')
p=t/'a12_r4_run.py';s=p.read_text(encoding='utf8')
s=s.replace("for z in ['A01','A02','A03','A04','A07','A08','A09','A10']:", """for z in ['A05','A06','A09']:
 p3=E/'R3_zone'/z/(z+'_raport.json')
 if p3.exists():shu(p3,IN/(z+'_consolidare_R3.json'))
if (E/'A09_raport_R2.json').exists():shu(E/'A09_raport_R2.json',IN/'A09_R2_semnat.json')
for z in ['A01','A02','A03','A04','A07','A08','A09','A10']:""")
s=s.replace("d=android_inputs[aid];ee=efile","""d=android_inputs[aid];cc9=rd(IN/'A09_consolidare_R3.json')['revision_consolidated'];v3=ent('A09_consolidare_R3.json','/revision_consolidated/changes',cc9['changes'],'Predare consolidată A09, distinctă de manifest, debug și hardware.');cc5=rd(IN/'A05_consolidare_R3.json')['revision_consolidated'];v5=ent('A05_consolidare_R3.json','/revision_consolidated/changes',cc5['changes'],'E9 1000023 este DR, o cheie, zero M_Transaction/GL. Alte documente CO cu Posted E sunt alt caz.');ee=efile""")
s=s.replace("used.append(ee)\n  if aid=='AND04'", "used.append(ee)\n  if aid=='AND04'")
s=s.replace("obs=d['observed']+' Instrumentare finalizată;", "obs=d['observed']+' Pentru E9, documentul 1000023 a rămas DR cu QtyBook 20, QtyCount 18, o cheie și 0 M_Transaction/Fact_Acct. Alte documente CO cu Posted=E nu reprezintă aceeași fixtură. Instrumentare finalizată;" )
s=s.replace("obs,[ee]+old.get('evidence_ids',[]))","obs,[ee,v3]+([v5] if aid in ('AND03','AND04')else [])+old.get('evidence_ids',[]))")
s=s.replace("attach(c,s,obs,ds);return","""if (IN/'A06_consolidare_R3.json').exists() and id in ('T352-R02','T352-R04','T352-R08','T352-R09'):
   zz=rd(IN/'A06_consolidare_R3.json')['revision_consolidated'];ds.append(ent('A06_consolidare_R3.json','/revision_consolidated/changes',zz['changes'],'Verdictele A06-F09/F10 și integrarea cesiro.com nu se extind dincolo de componentele probate.'))
  attach(c,s,obs,ds);return""")
s=s.replace("ds=[ent('A05_R2.json','/T366_handoff',C5,'ERP r57, apel autentificat la metoda din bundle pe DB native; nu este click ZK.')]","""ds=[ent('A05_R2.json','/T366_handoff',C5,'ERP r57, apel autentificat la metoda din bundle pe DB native; nu este click ZK.')]
  if id=='T366-R05' and (IN/'A05_consolidare_R3.json').exists():
   zz=rd(IN/'A05_consolidare_R3.json')['revision_consolidated'];ds.append(ent('A05_consolidare_R3.json','/revision_consolidated/changes',zz['changes'],'F10 la activarea concurentă este alt scenariu decât perechile deja conectate la validarea T366.'))""")
s=s.replace("'current_input_hashes':{p.name:sha(p)for p in sorted(IN.glob('*.json'))}", "'current_input_hashes':{p.name:sha(p)for p in sorted(IN.glob('*.json'))},'android_card_hashes':{pp.name:sha(pp)for pp in sorted((IN/'android').glob('AND*.json'))}")
p.write_text(s,encoding='utf8')

