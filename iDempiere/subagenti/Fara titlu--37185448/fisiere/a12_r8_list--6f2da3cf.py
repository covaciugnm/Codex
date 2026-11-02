from a12_r8_review import *
tr=rd(E/'R7_pregatire/A12/Clasificare_nominala_1587.json')['records'];reg={r['criterion']:r for r in rd(R7/'Registru_reexecutare_R7.json')['records']};own=['A01','A04','A06','A07','A09'];rows=[x for x in tr if x['category']=='FIXTURĂ_EXECUTABILĂ' and reg[x['criterion']]['R7_state']=='NEEXECUTAT' and x['owner']in own]
assert len(rows)==93
if __name__=='__main__':
 for x in rows:
  w=r7w(x['task']);c=next(c for c in criteria(w)if c['id']==x['criterion'])
  print(x['owner'],x['criterion'],c['normative_content'][:540].replace('\n',' '))
 wr(P/'Lista_93.json',{'R7_report':source(R7/'A12_raport.json'),'counts':collections.Counter(x['owner']for x in rows),'records':rows})

