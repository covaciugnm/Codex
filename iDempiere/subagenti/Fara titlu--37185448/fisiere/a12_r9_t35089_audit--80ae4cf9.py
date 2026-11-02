from a12_r9_orig import *
d='Documentatie/echipa-2026-10-09/T35-cadru-platforme-vanzari/'
regpath='Documentatie/echipa-2026-10-09/COORDONARE_SESIUNI.md';ro,buf=getp(regpath);lines=buf.decode().splitlines();print('registry size',len(lines),ro)
hits=[(i,l[:400])for i,l in enumerate(lines,1)if re.search(r'((§C|TabelaFisaCanal).{0,110}(semnat|acord)|(semnat|acord).{0,110}(§C|TabelaFisaCanal))',l,re.I)]
print('reg',len(hits),hits[:10])
for f in ['11-L3b_implementator_raport.md','LOG_MODIFICARI.md','09-L3_auditor_verdict_spec.md']:
 o,b=getp(d+f);v=b.decode().splitlines();print(f,len(v));print([(i,n[:245])for i,n in enumerate(v,1)if (f.startswith('11')and re.search(r'(comit|\bT10\b|M-[0-9])',n,re.I) or f.startswith('LOG')and re.search(r'(inclu|integrare|comit|F-[0-9]).{0,35}L3b|L3b.{0,100}comit',n,re.I)or f.startswith('09')and re.search(r'C.K4|semn[aă]|semnat|angajament',n,re.I))][:11])

