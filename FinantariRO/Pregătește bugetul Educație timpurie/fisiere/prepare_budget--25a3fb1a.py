import json
from pathlib import Path
rows=[]
def add(code,owner,desc,unit,qmin,qmax,rate,kind='Real',base=1,theme=0,just='Estimare de proiectare; necesită două oferte comparabile și analiza nevoii.'):
 rows.append(dict(code=code,owner=owner,desc=desc,unit=unit,qmin=qmin,qmax=qmax,rate=rate,kind=kind,base=base,theme=theme,just=just))
# Tarifele salariale sunt cost total angajator; CAM/taxe se reconciliază la contractare.
p='Cost total angajator estimat/oră; pontaj, fișă post și verificare salariu net plafon PEO. Fără dublare barem.'
add('M','Lider','Manager proiect','ore',480,2400,110,'Personal',0,0,p)
add('M','Lider','Responsabil financiar','ore',240,1440,90,'Personal',0,0,p)
add('M','Lider','Responsabil achiziții','ore',120,720,90,'Personal',0,0,p)
add('M','ONG','Coordonator partener','ore',192,960,90,'Personal',0,0,p)
add('A1.1','Lider','Expert educație: analiză de nevoi','ore',120,800,100,'Personal',1,0,p)
add('A1.2','Lider','Același expert: strategie și plan de acțiune','ore',100,640,100,'Personal',1,0,p)
add('A1.3','Lider','Același expert: operaționalizare servicii','ore',60,400,100,'Personal',1,0,p)
add('A1.4','Lider','Formare curriculum incluziv personal servicii noi','participanți',8,120,500)
add('A1.5','Lider','Același expert: studiu de impact','ore',60,480,100,'Personal',1,0,p)
add('A2.1-3','Lider','Servicii standard antepreșcolari (ED01)','copil-lună',63,3240,1641.50,'Barem',1,0,'GSCS p43–45: 1.641,50 lei/copil/lună, TVA inclusă; 7/270 copii ×9/12 luni. Include personal, hrană, materiale și funcționare. Categorii de vârstă verificate lunar.')
add('A2.1-3','Lider','Servicii standard preșcolari (ED02)','copil-lună',306,15120,906.55,'Barem',1,0,'GSCS p43–45: 906,55 lei/copil/lună, TVA inclusă; 34/1260 copii ×9/12 luni. Include personal, hrană, materiale și funcționare.')
add('A2.1','Lider','Educator serviciu complementar, program 4 ore/zi','ore',1680,8400,75,'Personal',1,0,p+' 2/10 grupe de 12 copii, 84 ore/lună ×10 luni; calificare obligatorie.')
add('A2.1','Lider','Îngrijire și supraveghere directă copii complementar','ore',840,4200,45,'Personal',1,0,p+' 42 ore/lună/grupă ×10 luni; exclude curățenie administrativă. Încadrarea directă/auxiliară, programul și înlocuirile se validează cu operatorul/juristul.')
add('A2.2','Lider','Hrană exclusiv copii serviciu complementar','porții',5040,25200,15,'Real',1,0,'24/120 copii ×21 zile ×10 luni, porție estimată cu taxe. Fără copii/luni deja acoperite prin ED01/ED02.')
add('A2.3','Lider','Consumabile didactice serviciu complementar','copil-lună',240,1200,35)
add('A2.2','Lider','Utilități și igienă serviciu complementar','grupă-lună',20,100,650,'Real',1,0,'Alocare exclusiv spațiului serviciului complementar; chei verificabile, fără dublare cheltuieli indirecte.')
add('A2.4','Lider','Mobilier inițial pentru locuri noi','loc',24,300,1800,'FEDR')
add('A2.4','Lider','Echipament psihomotor exterior','set inventariat',1,20,14000,'FEDR')
add('A2.4','Lider','Echipamente siguranță inițială','locație',1,20,4000,'FEDR')
add('A3.1/5/6','ONG','Expert social: recrutare, planuri, parentală, cooperare','ore',420,7200,85,'Personal',1,1,p+' Volume defalcate în planul de lucru; 1/5 persoane, atribuții compatibile și fără atribuții de management.')
add('A3.3','ONG','Logoped/psihopedagog autorizat','ore',100,4200,100,'Personal',1,1,p+' 10/210 copii ×10/20 ore; nevoia și calificarea se confirmă individual.')
add('A3.1/4','ONG','Mediator comunitar: acces și desegregare','ore',200,4200,70,'Personal',1,1,p)
add('A3.4','ONG','Sprijin lingvistic distinct de curriculum standard','ore',60,1400,90,'Personal',1,1,p)
add('A3.2','Lider','Transport copii vulnerabili','copil-lună',300,4200,160,'Real',1,1,'30/350 copii ×10/12 luni; tarif estimat, trasee și prețuri de confirmat. Nu reprezintă închiriere auto pe zi.')
add('A3.2','Lider','Îmbrăcăminte și încălțăminte','copil',35,850,400,'Real',1,1,'Pachet unic pe copil conform planului individual; articolele și ofertele se detaliază separat la fundamentare.')
add('A3.3','Lider','Tehnologie asistivă individuală','copil CES',2,60,2500,'FEDR',1,1)
add('A3.3','Lider','Echipare cameră resursă','cameră',1,15,10000,'FEDR',1,1)
add('A3.5','ONG','Materiale ateliere parentale','părinte',20,500,100,'Real',1,1)
add('A3.4','Lider','Ateliere diversitate cu grupuri mixte','atelier',4,120,750,'Real',1,1,'Numai conținut distinct desegregare; fără excursii/tabere/hrană acoperite de barem. Personalul deja bugetat nu se refacturează.')
add('A3.6','Lider','Cooperare educație-social-sănătate','atelier',4,30,500,'Real',1,0,'Logistică atelier; spațiu public pus la dispoziție gratuit; fără remunerarea repetată a experților.')
add('A1.3','Lider','Documentație și avize operaționalizare','serviciu',1,5,1500,'Real',1,0,'Estimare pentru 1/5 servicii noi; documentație/avize efectiv eligibile de verificat, fără lucrări de construcție.')
add('A3.3','Lider','Specialiști itineranți pentru incluziune CES','ore',0,6720,100,'Personal',1,1,p+' 5 specialiști ×56 ore/lună ×24 luni; 224 copii ×30 ore sprijin. Distinct de logopedie, fără suprapuneri de pontaj.')
add('M','ONG','Responsabil financiar partener','ore',96,480,90,'Personal',0,0,p+' Funcție obligatorie conform GSCG3.4, persoană distinctă de coordonator.')
def calc(key):
 direct=sum(r[key]*r['rate'] for r in rows)
 personal=sum(r[key]*r['rate'] for r in rows if r['kind']=='Personal')
 total=direct+personal*.15
 own={x:sum(r[key]*r['rate']*(1.15 if r['kind']=='Personal' else 1) for r in rows if r['owner']==x) for x in ['Lider','ONG']}
 return dict(direct=direct,personal=personal,indirect=personal*.15,total=total,euro=total/5.2584,byOwner=own,FEDR=sum(r[key]*r['rate'] for r in rows if r['kind']=='FEDR'),theme=sum(r[key]*r['rate'] for r in rows if r['theme']))
Path('budget_rows.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:calc(k) for k in ['qmin','qmax']},indent=2))
