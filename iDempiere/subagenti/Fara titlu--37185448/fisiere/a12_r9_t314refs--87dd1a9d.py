from a12_r9_orig import *
p='Documentatie/echipa-2026-10-09/T314-meniu-vanzari-canale-comenzi-facturare';o,t=getp(p+'/LOG_MODIFICARI.md');a=t.decode().splitlines();print([(i,l[:205])for i,l in enumerate(a,1)if 'K-25' in l or ('INTEGRA' in l and 'master' in l)][-6:])
f=git('log --all --format=%h%x09%s -i --grep='+shlex.quote('T314.*integrare')+' -12');print(f.decode()[:950]);print([x[:245]for x in a[-4:]])

