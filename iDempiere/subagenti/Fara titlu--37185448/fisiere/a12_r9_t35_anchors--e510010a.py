from a12_r9_orig import *
d='Documentatie/echipa-2026-10-09/T35-cadru-platforme-vanzari/'
for fp,pat in [(d+'08-L3_arhitect_spec.md',r'\| C[0-9]|T22.*semnat|semnat.*T22|ACORD|A-T22-21|Rev. 5.1'),(d+'09-L3_auditor_verdict_spec.md',r'A-T22-21|ACORD|semnat|contract.*TabelaFisaCanal'),(d+'11-L3b_implementator_raport.md',r'\| .*?[a-f0-9]{7,12}.*\| |comit|T10'),(d+'LOG_MODIFICARI.md',r'L3b backend|L3b BE|L3 §C|ACORD.*T22')]:
 oid,data=getp(fp);ls=data.decode().splitlines();matches=[(i,line[:320])for i,line in enumerate(ls,1)if re.search(pat,line,re.I)]
 print(fp.split('/')[-1],oid,len(matches));print(matches[:4],matches[-2:])
y=git('ls-tree -r --name-only '+BASE+' -- Documentatie/echipa-2026-10-09/COORDONARE_SESIUNI.md COORDONARE_SESIUNI.md').decode();print(y)

