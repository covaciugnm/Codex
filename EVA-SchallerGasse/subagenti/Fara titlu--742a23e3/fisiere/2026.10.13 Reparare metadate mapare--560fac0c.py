import json,pathlib,hashlib,re,sys
sys.stdout.reconfigure(encoding='utf-8')
W=pathlib.Path(__file__).parent
O=W.parent/'2026.10.13 Baza comuna negociere BERGER PECH'
P=W/'2026.10.13 Cerinte comune negociere matrice.json';Q=O/P.name;T=W/'2026.10.13 Cerinte comune negociere matrice.txt'
oldbytes=P.read_bytes();assert hashlib.sha256(oldbytes).hexdigest()=='8ad0abd035fb0a55ae18052f621bdd24ebe42b63968bf7fbec9c4effb69f2154'
assert Q.read_bytes()==oldbytes
J=json.loads(oldbytes);before=json.loads(oldbytes);M={r['id']:r for r in J['matrice']}
SRC={};hashes={}
for v in ['BERGER','PECH']:
    f=W/f'2026.10.13 Werkvertrag {v} R05.json';hashes[v]=hashlib.sha256(f.read_bytes()).hexdigest();c=json.loads(f.read_text(encoding='utf-8'));s={}
    for sec in c['sections']:
        for k,tx in enumerate(sec['paragraphs'],1):s[f"§ {sec['number']}({k})"]=tx
    for an in c['annexes']:
        for k,tx in enumerate(an.get('paragraphs',[]),1):s[f"Anexa {an['number']}, alineat {k}"]=tx
        for t,table in enumerate(an.get('tables',[]),1):
            for r,row in enumerate(table['rows'],1):s[f"Anexa {an['number']}, tabel {t}, rând {r}"]=' | '.join(map(str,row))
    SRC[v]=s
assert sum(map(len,SRC.values()))==401
oldinvalid=[]
for r in J['matrice']:
    for v,s in SRC.items():
        d=r[v.lower()]
        oldinvalid += [{'criteriu':r['id'],'prestator':v,'referinta':ref}for ref in d['referinte_selectate']if ref not in s]
        # Liste independente, reconstruite pornind numai de la citatele publice ale ACESTUI prestator.
        d['referinte_selectate']=[x['referinta']for x in d['referinte_r05']]
        for x in d['referinte_r05']:assert x['citat']==s[x['referinta']],(r['id'],v,x['referinta'])

def add(v,ref,ids):
    assert ref in SRC[v]
    for i in ids:
        a=M[i][v.lower()]['referinte_selectate']
        if ref not in a:a.append(ref)

# Numerele tabelelor și rândurilor financiare se tratează separat pentru fiecare firmă.
for v,s in SRC.items():
    for ref in s:
        if any(ref in r[v.lower()]['referinte_selectate']for r in J['matrice']):continue
        ids=[]
        if ref.startswith('Anexa 2, tabel'):ids=['N002']
        elif ref=='Anexa 3, alineat 1':ids=['N049','N051']
        elif ref.startswith('Anexa 3, tabel 1, rând '):
            k=int(ref.rsplit(' ',1)[1]);ids={3:['N043'],4:['N051'],5:['N044'],11:['N018'],16:['N032']}[k]
        elif ref.startswith('Anexa 4, alineat '):
            k=int(ref.rsplit(' ',1)[1]);ids=({'BERGER':{5:['N034','N038'],7:['N037']},'PECH':{3:['N034','N038'],4:['N037']}}[v][k])
        elif ref.startswith('Anexa 4, tabel 2, rând '):
            k=int(ref.rsplit(' ',1)[1]);ids=['N069']
            if v=='PECH':
                if k in [6,7]:ids+=['N007']
                if k in [8,9]:ids+=['N010']
                if k==10:ids+=['N042']
                if k==15:ids+=['N026','N032','N061']
                if k==16:ids+=['N062']
            else:
                if k==6:ids+=['N036']
                if k==7:ids+=['N026','N061']
                if k==8:ids+=['N062']
        elif ref.startswith('Anexa 4, tabel 3, rând '):
            k=int(ref.rsplit(' ',1)[1])
            if v=='PECH':ids=['N066']
            else:ids=['N063']if k==8 else(['N036','N069']if k==6 else(['N061','N069']if k==7 else['N069']))
        elif(v=='BERGER'and ref.startswith('Anexa 4, tabel 5'))or(v=='PECH'and ref.startswith('Anexa 4, tabel 4')):ids=['N038']
        elif ref=='Anexa 6, alineat 1':ids=['N082','N083']
        elif ref=='Anexa 6, alineat 3'and v=='BERGER':ids=['N084']
        elif ref.startswith('Anexa 6, tabel 1, rând '):
            k=int(ref.rsplit(' ',1)[1]);ids={1:['N003'],2:['N003'],9:['N075'],10:['N091']}[k]
        elif ref.startswith('Anexa 6, tabel 2, rând '):
            k=int(ref.rsplit(' ',1)[1]);ids={1:['N001'],2:['N020','N026'],3:['N050','N051'],4:['N064'],5:['N068','N074'],6:['N056','N058'],7:['N034','N038'],8:['N088']}[k]
        if not ids:raise ValueError('Componentă fără asociere proprie '+v+' '+ref)
        add(v,ref,ids)

new=[]
for v,s in SRC.items():
    for ref,tx in s.items():
        ids=[r['id']for r in J['matrice']if ref in r[v.lower()]['referinte_selectate']]
        assert ids,(v,ref)
        new.append({'prestator':v,'referinta_r05':ref,'criterii':ids,'citat_exact_r05':tx})
oldmap={(x['prestator'],x['referinta_r05']):set(x['criterii'])for x in J['acoperire_401_componente']}
linkchanges=[]
for x in new:
    a=oldmap[(x['prestator'],x['referinta_r05'])];b=set(x['criterii'])
    if a!=b:linkchanges.append({'prestator':x['prestator'],'referinta':x['referinta_r05'],'criterii_eliminate':sorted(a-b),'criterii_adaugate':sorted(b-a)})
J['acoperire_401_componente']=new
for r0,r1 in zip(before['matrice'],J['matrice']):
    assert r0['cerinta_comuna']==r1['cerinta_comuna']
    assert r0['celule_publice']==r1['celule_publice']
    assert r0['pozitie_negociere']==r1['pozitie_negociere']
    for v in SRC:
        assert r0[v.lower()]['referinte_r05']==r1[v.lower()]['referinte_r05']
        assert set(r1[v.lower()]['referinte_selectate']).issubset(SRC[v])
assert len(oldinvalid)==13
J['verificare']['referinte_invalide']=[]
J['validare_mapare_proprie']={'data':'2026.10.13','rezultat':'PASS','componente':401,'criterii':100,'surse_r05_sha256':hashes,'referinte_invalide_dupa':0,'public_schimbat':False,'rectificare':'Afirmația anterioară zero referințe invalide se referea la selecția dinaintea completării mapării. Au fost identificate 13 referințe orientative propagate între firme. Acestea și asocierile interne sunt acum reconstruite din fiecare JSON R05 propriu. Citatele și celulele publice rămân identice.','referinte_invalide_anterioare':oldinvalid,'asocieri_corectate':linkchanges}
data=json.dumps(J,ensure_ascii=False,indent=2)+'\n';P.write_text(data,encoding='utf-8');Q.write_text(data,encoding='utf-8')
sha=hashlib.sha256(P.read_bytes()).hexdigest()
report=J['validare_mapare_proprie']|{'json_initial_sha256':hashlib.sha256(oldbytes).hexdigest(),'json_corectat_sha256':sha}
(O/'2026.10.13 Validare metadate si mapare 401.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['2026.10.13 — VALIDARE METADATE ȘI MAPARE R05','PASS: 100 criterii; 401 componente reconstruite din JSON-ul R05 al fiecărui prestator; toate citatele exacte; zero referințe invalide după corecție.','JSON corectat SHA-256: '+sha,report['rectificare'],'Nicio cerință, celulă publică, citat public sau fișier R05 nu a fost modificat.','']
for x in linkchanges:lines.append(f"{x['prestator']} {x['referinta']}: eliminate {', '.join(x['criterii_eliminate'])or'—'}; adăugate {', '.join(x['criterii_adaugate'])or'—'}")
(O/'2026.10.13 Validare metadate si mapare 401.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
append=['','2026.10.13 — Rectificarea metadatelor și maparea proprie a celor 401 componente',report['rectificare']]
for x in new:append.append(f"{x['prestator']} {x['referinta_r05']} → {', '.join(x['criterii'])}")
T.write_text(T.read_text(encoding='utf-8')+'\n'.join(append)+'\n',encoding='utf-8')
print('PASS',len(new),'componente,',len(linkchanges),'grupuri de asocieri corectate; 13 selecții inexistente eliminate.')
print('JSONSHA',sha);print('TXTSHA',hashlib.sha256(T.read_bytes()).hexdigest())
