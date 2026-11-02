from a12_r8_cases import *
if __name__=='__main__':
 for frag in ['/BAZA-PB-93/','/BAZA-PB-91/','/BAZA-PB-95/']:
  z=next((x for x in a if '/T216-'in x['file'] and frag in x['file'] and x['file'].endswith(('PB-93_auto_confirma_trimis.txt','PB-95_tipar_factura_site.txt','PB-91_confirm_fara_trimitere.txt'))),None)
  if z:print(z['file'],txt(z)[:1700])
 matches=[]
 for z in a:
  if '/T216-' not in z['file'] and '/T22-'not in z['file']:continue
  if z['size']>90000 or z['file'].endswith(('.sh','.py','.json','.md')):continue
  ts=txt(z);l=ts.splitlines();found=[(i,q[:190])for i,q in enumerate(l,1)if re.search('serie.{0,30}număr|serie.{0,15}numar|pl[aă]ti? .{0,30}potrivi|număr.{0,25}pe site|ar[aă]tat.{0,20}site|alocare.{0,20}factur',q,re.I)and not q.startswith('##')]
  if found:matches.append((z['file'].split('/',3)[-1],found[:2]))
 print('candidates',len(matches));print('\n'.join(str(x)for x in matches[:12]))

