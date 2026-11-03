from pathlib import Path
import json,hashlib,datetime
O=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_G3_nativ_lot04')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
d=json.loads((O/'Identitati_lectura_G3_v1.json').read_text(encoding='utf8'))
m={
 'RezervareStoc.java':('disponibil/suma/SQL_STOC/SQL_REZ_NATIVA/SQL_REZ_T22','cititor business original','Gestionar→alocare/validare→disponibil; harness intră la metoda disponibil','SO2 fărăPO→8','SO2+PO5→3; PO15→-7; filtre/rollback','citire DB fără scrieri; rezervările create prin modelul nativ'),
 'FisaCanalProces.java':('sursa/stoc/surse.brut/stocCuSet/stocArticol','cititor business original și record persistent','Fișa canal→stoc→surse originale→formula; harness începe la sursa/stoc','stoc10/SO2/PO0→8','PO5→3; PO15→0; filtre/ASI','citire DB; nu doIt/proces integral/HTTP'),
 'FisaCanalCalcul.java':('stocCalculat','formulă originală apelată de stocArticol','stocArticol→stocCalculat→RegulaStocCanal','8.50→floor8','negativ→0; PO n-ar trebui dedus','calcul pur, nicio persistență proprie'),
 'RegulaStocCanal.java':('cantitateOferita','calea fără reguli a formulei','FisaCanalCalcul.stocCalculat→cantitateOferita(reguli={})','cantitate păstrată fără reguli','orice regulă nezero în fixture invalidează izolarea','nu credit pentru celelalte reguli/configurații'),
 'SetLista.java':('esteSet/stare/citeste/cerereComponenta','cititor auxiliar original, non-BOM și cererezero','FisaCanalProces și RezervareStoc→SetLista','produs non-BOM; cerere0','hook nonnull ori cerere nezero invalidează proba','fără credit pentru BOM/S1/S2/comenzi set'),
 'TabelaFisaCanal.java':('reguliStoc','calea canal null','surse.reguli→reguliStoc(ctx,client,sursa,null,trx)','harta goală originală','niciun adaptor fals al regulilor','fără activare tabele canal/HTTP/admin'),
 'DomeniiT22.java':('REZERVAT/EXCLUS','constante de filtru','cititori→constante T22','termeni site0','linii neprevăzute invalidează proba','nu credit pentru workflow T22'),
 'FluxTabele.java':('constante de nume','metadata/citire statică','dependențe cititor','tabelele există','mismatch metadata blochează','nu execuție independentă creditată'),
 'TipGestiune.java':('SQL_FARA_NC','citire statică doar în această parametrizare','gestiuni(*) exclude NC; fixture folosește ID explicit','gestiune contabilă normală','nu se atribuie agregare wildcard','fără execuție necesară a ramurii wildcard'),
 'EvaWmsGardaEvents.java':('initialize/doHandleEvent/decide, ramuri warehouse/source','gardă originală la fixture PO','PO.saveEx→EventManager→garda','warehouse/source valid','refuz neașteptat setup se păstrează, nu defect','nu credit pentru restul gardelor WMS'),
 'EvaStocEvents.java':('initialize; eventual PO_BEFORE_CHANGE warehouse','binding original, fixture doar după topic real','PO warehouse→event dacă aplicabil','niciun handler relevant omis','topic/class diferit invalidează','nu credit pentru costare/postare'),
 'EvaAuditPostareEvents.java':('initialize','binding auxiliar posibil, fără business postare','activare manuală originală pentru gardă, nu EvaActivator întreg','serviciu original dacă păstrat','inventar de excluderi explicit','zero credit Fact_Acct'),
 'EvaActivator.java':('lista handlerelor','lectură de bootstrap','start→bindEventManager numai ca model de configurare','inventar nominal complet','omisiune handler relevant oprește','EvaActivator întreg nu rulează')}
rows=[]
for s in d['sources']:
 n=Path(s['path']).name;method,role,path,pos,neg,effect=m[n]
 rows.append(dict(**s,method_scope=method,role=role,actor='user101/role102/client11/org11; nu login',normal_path=path,positive=pos,counterexample=neg,persistent_effect=effect,result='PLAN_ONLY_NOT_EXECUTED',limit='Nu fișier integral, nu task închis, nu UI; '+effect))
f=O/'Fise_plan_G3_v1.json';assert not f.exists();f.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
s={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'protocol_v2':{'path':'Protocol_G3_nativ_v2.json','sha256':sha(O/'Protocol_G3_nativ_v2.json')},'fiches':{'path':f.name,'sha256':sha(f)},'runtime_started':False}
f2=O/'SIGILIU_fise_plan_G3_v1.json';assert not f2.exists();f2.write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'fiches':len(rows),'sha256':sha(f),'seal_sha256':sha(f2)}))
