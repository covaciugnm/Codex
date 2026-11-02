from a12_r10_base import *
a=Path(__file__).parent/'a12_r10_receipt.py';exec(a.read_text(encoding='utf8').split("j=P10/")[0])
f=P10/'R10_documentar_supliment/Rezultat.json';q=rd(f);assert sha(f)=='e0f8650fbc2a89cceec9e81e1fa8d72d2c4e36866761685ea40d46d09ae0569c';g=f.parent/'T22_15_hashuri_etalon.json'
assert sha(g)=='733c355900f4e45fe494362e17d8db450ebfc8ca642a1b44fe43e04a2b571a01'
for i,z in enumerate(q['rows']):
 for rr in z['references']:
  pp=B/rr['file'];assert sha(pp)==rr['sha256']
  if 'pointer'in rr:
   from a12_r9_publish import ptr
   assert ptr(rd(pp),rr['pointer'])is not None
 additional=[jr(g)]if z['criterion'].startswith('T22.15')else []
 add(z['criterion'],z['kind'],z['expected'],z['observed'],z['negative_or_control']if not additional else{'corrected_hash_comparator':rd(g),'other_negative':z['negative_or_control']},z['limit'],[jr(f,'/rows/'+str(i))]+additional,'documentary_or_test')
dest=P10/'Registru_documentar_A12.json';wr(dest,{'utc':now(),'independent_source':jr(f),'receipts':out});print(sha(dest))

