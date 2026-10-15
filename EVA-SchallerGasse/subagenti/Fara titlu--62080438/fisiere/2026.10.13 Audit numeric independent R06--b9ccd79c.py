from pathlib import Path
from decimal import Decimal as D, ROUND_HALF_UP
import json,hashlib
work=Path.cwd()/'00.Proiect/09. Vertraege/2026.10.13 Reorganizare juridica si audit'
source=work/'2026.10.13 Propunere economica comuna R06.json'
d=json.loads(source.read_text(encoding='utf-8-sig'))
errors=[];checks=0
def q(x):return x.quantize(D('.01'),rounding=ROUND_HALF_UP)
def check(label,actual,expected):
 global checks
 checks+=1
 if actual!=expected:errors.append({'id':label,'actual':str(actual),'expected':str(expected)})
def amount_block(label,b,expected_net):
 net=q(expected_net);vat=q(net*D('.20'));ret=q(net*D('.05'))
 values={'net_eur':net,'tva_20_eur':vat,'brut_eur':net+vat,'retentie_5_net_eur':ret,
 'net_dupa_retentie_eur':net-ret,'plata_bruta_dupa_retentie_eur':net+vat-ret}
 for k,v in values.items():check(label+'.'+k,D(b[k]),v)
 for k,v in b['afisare'].items():
  key=k+'_eur' if k not in ['retentie_5_net','plata_bruta_dupa_retentie'] else k+'_eur'
  display=format(values[key],',.2f').translate(str.maketrans(',.','.,'))
  check(label+'.display.'+k,v,display)
bases={'berger':D('45000'),'pech':D('69300')}
fractions=[10,20,25,15,10,10,10]
check('fractions',[x['procent_pachet'] for x in d['repere_plati']],fractions)
check('sum_fractions',sum(fractions),100)
for row,pct in zip(d['repere_plati'],fractions):
 for party,base in bases.items():amount_block(row['id']+'.'+party,row[party],base*D(pct)/100)
originals={'berger':[D(x) for x in ['13000','20000','2000','10000']],
 'pech':[D(x) for x in ['42000','6000','5000','800','14000','1500']]}
for party,base in bases.items():
 amount_block('total.'+party,d['totaluri'][party],base)
 grid=d['alocare_interna_propusa'][party]
 check('originals.'+party,[D(x) for x in grid['totaluri_originale_net_eur']],originals[party])
 for i,row in enumerate(grid['randuri']):
  vals=[D(x) for x in row['valori_net_eur']]
  check(party+'.allocation.'+row['reper'],sum(vals),base*D(fractions[i])/100)
  check(party+'.rowtotal.'+row['reper'],D(row['total_net_eur']),sum(vals))
  for j,x in enumerate(vals):check(party+'.cellformat.'+row['reper']+'.'+str(j),row['valori_net_afisate'][j],format(x,',.2f').translate(str.maketrans(',.','.,')))
 for col,target in enumerate(originals[party]):
  check(party+'.column.'+str(col),sum(D(x['valori_net_eur'][col]) for x in grid['randuri']),target)
 for k in ['net_eur','tva_20_eur','brut_eur','retentie_5_net_eur','plata_bruta_dupa_retentie_eur']:
  check(party+'.rate_sum.'+k,sum(D(x[party][k]) for x in d['repere_plati']),D(d['totaluri'][party][k]))
 check(party+'.D1D5',sum(D(x[party]['net_eur']) for x in d['repere_plati'][:5]),base*D('.80'))
check('option_counts',[x['numar_vizite_suplimentare'] for x in d['optiuni_0_6']],list(range(7)))
for row in d['optiuni_0_6']:
 n=row['numar_vizite_suplimentare']
 additions={'berger':q(D(n)*D('2000')/D(12)),'pech':D(n)*D('450')}
 for party,addon in additions.items():
  amount_block('option.'+str(n)+'.'+party,row[party],addon)
  amount_block('optiontotal.'+str(n)+'.'+party,row['total_cu_baza_'+party],bases[party]+addon)
early=d['control_80_procente']['fara_avans_PI']['repartizare_early_PI']
for i,row in enumerate(early):
 for party,col in [('berger',3),('pech',4)]:
  value=D(d['alocare_interna_propusa'][party]['randuri'][i]['valori_net_eur'][col])
  check('earlyPI.'+party+'.'+str(i),D(row[party+'_parte_PI_net_eur']),value)
  check('earlyPlan.'+party+'.'+str(i),D(row[party+'_parte_planificare_net_eur'])+value,D(d['repere_plati'][i][party]['net_eur']))
check('earlyPI_B',sum(D(x['berger_parte_PI_net_eur']) for x in early),D('3000'))
check('earlyPI_P',sum(D(x['pech_parte_PI_net_eur']) for x in early),D('2440'))
check('ground800_once',sum(D(x['valori_net_eur'][3]) for x in d['alocare_interna_propusa']['pech']['randuri']),D('800'))
result={'date':'2026.10.13','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'method':'Independent Decimal calculations, ROUND_HALF_UP to cent; no float arithmetic',
 'checks':checks,'errors':errors,'pass':not errors,
 'original_position_totals':{p:[str(x) for x in v] for p,v in originals.items()},
 'option_final_net':{'berger':'1000.00','pech':'2700.00'},
 'E6_cumulative_examples':{str(k):{'berger':str(q(D(k)*D('4500')/12)),
  'pech_visits':str(q(D(k)*D('6130')/12)),'pech_ground_only_after_complete_befund':'800.00'} for k in range(13)}}
(work/'2026.10.13 Audit numeric independent R06.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='E6_cumulative_examples'},ensure_ascii=False,indent=2))
