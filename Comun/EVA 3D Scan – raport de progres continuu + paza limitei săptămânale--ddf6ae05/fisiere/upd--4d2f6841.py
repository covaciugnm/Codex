import json,re,io
p='progres_server.json'
d=json.load(open(p,encoding='utf-8'))
d['actualizat']='2026-10-07 08:15'; d['utilizare_saptamanala_procent']=76
for c in d['componente']:
    i=c['id']
    if i=='SRV-006/B05':
        c['procent']=89; c['audit']+= [9.3,9.4,9.4]
        c['etapa']='audit r4 9,3 → r5 9,4 → r6 9,4 (merge_ready); singura constatare rămasă e de coordonare: rezervarea 018 trebuie comisă pe main (patch livrat în Site/docs/patches/main-PROTOCOL-rezervare-018.patch) înainte de merge'
    if i=='SRV-009/B15':
        c['procent']=88; c['audit'].append(9)
        c['etapa']='audit r3 9 (merge_ready, 3 minore: TOCTOU rezidual în offsite-sync, ordine §8, raportare JSON); remediere r3 în curs'
    if i=='SRV-001':
        c['procent']=88; c['audit'].append([9.4,10,'în curs'])
        c['etapa']='remediere r2 gata (ffe4fa6, toate cele 12 constatări); audit r3: 9,4 (2 minore) și 10 (securitate, 0 constatări), al treilea auditor în curs; E2E 112/112'
    if i=='SRV-013':
        c['etapa']='audit r1 8,5 / 7,5 / 7,5; remedierea r1 are commit-uri pe branch (507835f, 08:08: ordine popover WCAG 1.3.2, tasta ?), rezultatul încă nescris în jurnal; traducerea wf_d2c65ea3-1e8: niciun rezultat în jurnal de la 05:41 (necunoscut)'
d['total_server_procent']=61; d['total_proiect_procent']=58
json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=2); open(p,'a').write('\n')

m=open('PROGRES_SERVER.md',encoding='utf-8').read()
R=[('2026-10-07 07:45 (Europe','2026-10-07 08:15 (Europe'),
('proiect ~57% · server ~60%','proiect ~58% · server ~61%'),
('actualizare: **74%**','actualizare: **76%**'),
('| SRV-006 / B05 | Verificarea C07 + T02 | 86 | remediere r3 | 8,5 → 9,3 → **10** → (reluat) 6 → 8,5 → 8,5 (merge_ready dacă 018 e rezervat pe main) |',
 '| SRV-006 / B05 | Verificarea C07 + T02 | 89 | gata de merge după rezervarea 018 pe main | 8,5 → 9,3 → **10** → (reluat) 6 → 8,5 → 8,5 → 9,3 → 9,4 → 9,4 (merge_ready; rămâne doar 018 pe main, patch livrat) |'),
('| SRV-009 / B15 | Operare, backup | 82 | remediere r2 | 7 → 7,5 → 9 → 9 → 9 → (reluat) 7 → 8 |',
 '| SRV-009 / B15 | Operare, backup | 88 | remediere r3 | 7 → 7,5 → 9 → 9 → 9 → (reluat) 7 → 8 → 9 (merge_ready, 3 minore) |'),
('| SRV-001 | /admin/ live | 80 | remediere r2 | arh. 7/8 → 8,5/8,5 → 8,3/8,6 → 8/8,5; audit r1 8,5/7,5/7,5; audit r2 8,5/9,3/8,5 (fără blocante) |',
 '| SRV-001 | /admin/ live | 88 | audit r3 (2 din 3 gata) | arh. 7/8 → 8,5/8,5 → 8,3/8,6 → 8/8,5; audit r1 8,5/7,5/7,5; audit r2 8,5/9,3/8,5; audit r3 9,4 / **10** / în curs (E2E 112/112) |'),
('| SRV-013 | Help server + aplicație | 60 | remediere r1 |','| SRV-013 | Help server + aplicație | 60 | remediere r1 (commit-uri pe branch, 507835f) |'),
('help +24, admin +16, scenă +16, modele +14, b15 +7, b05 +6,','help +25, admin +17, scenă +17, modele +14, b05 +9, b15 +8,'),
]
for a,b in R:
    assert a in m, a[:50]; m=m.replace(a,b)
m=re.sub(r'- \*\*Audituri noi de la 07:13:\*\*[^\n]*','- **Audituri noi de la 07:45:** admin r3 9,4 și 10 (al treilea în curs); B05 r4 9,3, r5 9,4, r6 9,4 (merge_ready); B15 r3 9 (merge_ready). **Remedieri:** admin r2 gata (ffe4fa6, 12/12), B05 r5 parțial (rămâne 018 pe main), B15 r3 și help r1 în curs.',m)
open('PROGRES_SERVER.md','w',encoding='utf-8').write(m)

r=open('RELUARE_SERVER.md',encoding='utf-8').read()
R2=[('| B01 reaudit r6 9,4; B05 audit r3 8,5 → remediere r3; B15 audit r2 8 → remediere r2; B09 și B12 în audit r1 |','| B01 reaudit r6 9,4; B05 audit r6 9,4 (merge_ready, așteaptă 018 pe main); B15 audit r3 9 → remediere r3; B09 și B12 în audit r1 |'),
('| audit r2 complet (8,5 / 9,3 / 8,5) → remediere r2 |','| remediere r2 gata (ffe4fa6) → audit r3: 9,4 / 10 / în curs |'),
('| audit r1 (8,5 / 7,5 / 7,5) → remediere r1 |','| audit r1 (8,5 / 7,5 / 7,5) → remediere r1 (commit-uri pe branch, 08:08) |')]
for a,b in R2:
    assert a in r, a[:50]; r=r.replace(a,b)
open('RELUARE_SERVER.md','w',encoding='utf-8').write(r)
print('ok')
