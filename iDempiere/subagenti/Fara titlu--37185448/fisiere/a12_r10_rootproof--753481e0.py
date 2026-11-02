from a12_r10_base import *
exec((Path(__file__).parent/'a12_r10_receipt.py').read_text(encoding='utf8').split("j=P10/")[0]);p=E/'R10_pregatire/T216_corelare/Comparatie_cititori_T216.json';f=rd(p);assert sha(p)=='c9bdb90413f8c8df9b1faee3a7e30529839910b9b41c23435ff1ab91b20e7e64'and sha(E/f['input_synthetic_A07']['path'])==f['input_synthetic_A07']['sha256']
for c in ['T216-R2-001','T216-R2-007']:
 add(c,'COORDONATOR · comparație de cititori existenți pe aceeași origine A07','Două căi trebuie distinse între citirea articolelor și proiectarea pentru reconciliere; păstrați funcția T22 reutilizabilă și identitatea fiecărei linii.',{'same_origin_readers':f['rows'],'reuse':'DetaliuComanda.din recuperează Oak, 2 × 12,10 lei și separă SKU, cantitatea și lipsa articolelor. SursaCesiro1.comanda/detaliu răspunde totalului și nu transportă diferența liniilor.'},f['change_controls'],f['decision_scope'],[jr(p,'/rows'),jr(p,'/change_controls'),jr(p,'/input_synthetic_A07')],'context_only')
dest=P10/'T216_comparator_de_reutilizare.json';wr(dest,{'utc':now(),'independent_review_status':'În revizuire A11 la intrarea probei în dosar.','no_new_criterion_awarded':True,'receipts':out});print(sha(dest))

