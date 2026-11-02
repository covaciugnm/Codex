from a12_r8_arch_survs import *
for k,pat in [('06',r'/dovezi-40-audit/proba_finala/C-(?:01|14_|15_|16_|18_|19_|22_|25_)'),('204',r'/dovezi-08-cod/auto-verificare/C-(?:04|05|14|17|18|20|21|22|23_final|24)'),('204',r'/dovezi-13-cod/auto-verificare/C-(?:07|08|12|19)'),('227',r'/dovezi-06/auto-verificare/K-12a'),('314',r'/dovezi-10a-lotA/auto-verificare/K-(?:09|14|18|20|21|22|23|24|25|26_|27)'),('220',r'/dovezi-02/defect_|/dovezi-12-k12/k12')]:
 for z in a:
  if not re.search('/T'+k+'-',z['file']) or not re.search(pat,z['file']):continue
  lines=txt(z).splitlines();print('\n'+z['file'].split('/',3)[-1]+' '+str(len(lines)));print(('\n'.join(lines[:3]+lines[-4:]))[:700])

