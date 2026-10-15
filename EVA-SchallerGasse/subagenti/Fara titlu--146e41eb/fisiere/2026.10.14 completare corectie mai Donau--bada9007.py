from pathlib import Path
r=Path('05. Asigurari/Asigurare cladire/2026.10.14 Analiza juridica Donau')
one=r/'2026.10.14 01 Incetarea politei Donau.txt'
two=r/'2026.10.14 02 Neplata si acoperirea Donau.txt'
t=one.read_text(encoding='utf8')
t=t.replace('mandatul de primire și data accesului.','mandatul de primire, data accesului și data la care DONAU a cunoscut înstrăinarea, inclusiv în raport cu § 69 alin. 3.')
one.write_text(t,encoding='utf8')
src=next(s for s in t.splitlines() if s.startswith('P9. '))[4:]
t=two.read_text(encoding='utf8')
t=t.replace('\nL1. VersVG','\nP5. '+src+'\n\nL1. VersVG')
t=t.replace('§§ 1, 36, 38, 39, 39a, 40, 41a, 41b, 42, 68, 91,','§§ 1, 36, 38, 39, 39a, 40, 41a, 41b, 42, 68, 69, 91,')
t=t.replace('Somația din 2026.06.05, p. 1, privește','§ 69 alin. 3 leagă opozabilitatea înstrăinării față de asigurător, în privința creanțelor întemeiate împotriva sa prin asigurare, de cunoașterea acesteia. Extras: „Der Versicherer hat die Veräußerung in Ansehung der durch das Versicherungsverhältnis gegen ihn begründeten Forderungen erst dann gegen sich gelten zu lassen, wenn er von ihr Kenntnis erlangt”. Se cere deci data la care DONAU a cunoscut transferul și dovada notificării, împreună cu mandatele Hofhans și traseul comunicării. Numele fostului titular pe scrisoare nu permite, singur, declararea somației ca ineficace; nici alin. 3 nu dovedește automat valabilitatea ei în toate celelalte privințe. [L1 § 69 alin. 3]\n\nSomația din 2026.06.05, p. 1, privește')
two.write_text(t,encoding='utf8')
p=r/'2026.10.14 Cerere documente Donau NETRIMIS.txt';t=p.read_text(encoding='utf8')
t=t.replace('des maßgeblichen Zugangs und Fristbeginns','des Zeitpunkts Ihrer Kenntnis vom Eigentumsübergang (§ 69 Abs. 3 VersVG), des maßgeblichen Zugangs und Fristbeginns')
p.write_text(t,encoding='utf8')
p=r/'2026.10.14 Registru documente necesare.txt';t=p.read_text(encoding='utf8')
t=t.replace('Expediere, acces A&C, efectul retransmiterii','Data cunoașterii transferului de către DONAU (§ 69 alin. 3), expediere, acces A&C, efectul retransmiterii')
p.write_text(t,encoding='utf8')
print('Correction complete.')
