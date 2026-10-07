const fs=require('fs'),path=require('path');const root=path.resolve(__dirname,'..');
function edit(p,pairs){let s=fs.readFileSync(path.join(root,p),'utf8');for(const [a,b]of pairs){if(!s.includes(a))throw Error('Missing text '+a);s=s.replaceAll(a,b);}fs.writeFileSync(path.join(root,p),s,'utf8');}
edit('01_cercetare/piata_feedback_ux.md',[
 ['test de utilizabilitate cu minimum 15 persoane diferite','pilot formativ cu 5 persoane și evaluare de acceptare cu minimum 20 persoane diferite'],
 ['minimum 14/15 participanți aleg modul corect în ≤15 secunde','minimum 18/20 participanți aleg modul corect în ≤10 secunde'],
 ['12/15 începători','16/20 începători'],['10⁻⁶ × lungime','10⁻⁵ × lungime în mm'],['30/30 sesiuni B','50/50 sesiuni B'],
 ['Proiect test cu 12 camere și 2 niveluri','Fixture sintetic pentru persistența modelului de date, cu 12 camere și 2 niveluri (captura reală multi-etaj rămâne P2)'],
 ['14/15 participanți','18/20 participanți'],['12/15 utilizatori','16/20 utilizatori'],['14/15 utilizatori','18/20 utilizatori'],
 ['≥15 participanți, rezultate U01/U03/U21/U27','pilot 5 + acceptare 20 participanți, rezultate U01/U03/U21/U27']
]);
fs.appendFileSync(path.join(root,'01_cercetare/piata_feedback_ux.md'),'\n\n## Armonizare după audit\n\n[Criteriile canonice](../05_validare/CRITERII_CANONICE.md) stabilesc pragurile și etapele. Interviurile de explorare, pilotul formativ și evaluarea de acceptare sunt loturi distincte. Cele 30 sesiuni de teren din UX-06 sunt pilot; nu înlocuiesc cele 50 sesiuni de confidențialitate sau lotul metrologic. Captura multi-etaj reală este P2; fixture-ul U15 verifică numai persistența structurii de date. Toate acestea sunt teste propuse, neexecutate.\n');
edit('02_specificatie/01_VIZIUNE_SI_SPECIFICATIE.md',[
 ['export minim testat;','export minim testat (3MF, STL, PLY, USDZ, DXF 2D cotat și manifest JSON);'],
 ['Pierdere maximă propusă 5 s de date deja eligibile pentru checkpoint în testele persistente','Zero pierdere de date confirmate; ≤5 s numai metadate/fluxuri persistente controlate de aplicație; stări opace RoomPlan/Object Capture best effort cu recaptură posibilă']
]);
fs.appendFileSync(path.join(root,'02_specificatie/01_VIZIUNE_SI_SPECIFICATIE.md'),'\n\n## Referința normativă pentru acceptare\n\n[CRITERII_CANONICE.md](../05_validare/CRITERII_CANONICE.md) fixează pragurile, domeniile, eșantioanele și prioritățile după audit. Acesta este documentul de referință când un experiment exploratoriu folosește un lot mai mare sau un domeniu mai larg.\n');
console.log('Remedieri manager aplicate');
