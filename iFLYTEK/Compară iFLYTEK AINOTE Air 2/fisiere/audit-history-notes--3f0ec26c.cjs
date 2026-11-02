const fs=require('fs'),path=require('path'),crypto=require('crypto');
const root=path.resolve(__dirname,'..'),software=path.resolve(root,'..');
const files=[
  'Cercetare_SDK_2026-10-30/Raport_SDK.txt',
  'Cercetare_SDK_2026-10-30/Raport_Bluetooth_extins.txt',
  'Biblioteca_Glasses/Cercetare/Raport_SDK.txt',
  'Biblioteca_Glasses/Cercetare/Raport_Bluetooth_extins.txt'
];
const changed=[];
for(const file of files){
  const target=path.join(software,file);if(!fs.existsSync(target))continue;
  let text=fs.readFileSync(target,'utf8');
  if(text.startsWith('NOTĂ DE ETAPĂ ISTORICĂ'))continue;
  const rel=path.relative(path.dirname(target),root).replaceAll('\\','/');
  const note='NOTĂ DE ETAPĂ ISTORICĂ — actualizare de orientare, 30.10.2026\n'+
    'Textul de mai jos descrie stadiul cercetării la momentul redactării lui.\n'+
    'Etapele ulterioare au decompilat componentele Android din APK 1.0.3899 și au identificat UUID-uri GATT, constructori de comenzi și parseri.\n'+
    'Afirmațiile de mai jos despre lipsa decompilării / a UUID-urilor / a unui protocol documentat trebuie citite numai în contextul acelei etape.\n'+
    'Rezultatul actual este o reconstrucție experimentală din APK, cu limite explicite; nu este un SDK oficial și nu a fost validat pe ochelari sau în cloud.\n'+
    'Catalog actual: '+rel+'/catalog-parametri-functii/INDEX.html\n'+
    'Protocol: '+rel+'/protocol-comunicare/INDEX.html\n'+
    'Firmware: '+rel+'/firmware-analiza/INDEX.html\n'+
    'Audit și corectări: '+rel+'/audit-calitate/INDEX.html\n\n'+
    '--- RAPORTUL ETAPEI INIȚIALE ---\n\n';
  fs.writeFileSync(target,note+text);changed.push(file);
}
const manifestUpdates=[];
for(const name of ['manifest.json','manifest-complet.json']){
  const filename=path.join(software,'Biblioteca_Glasses',name),manifest=JSON.parse(fs.readFileSync(filename,'utf8'));
  for(const row of manifest.filter(x=>/^Cercetare\/Raport_(SDK|Bluetooth_extins)\.txt$/.test(x.file||''))){
    const bytes=fs.readFileSync(path.join(software,'Biblioteca_Glasses',row.file));
    row.historicalOriginal=row.historicalOriginal||{bytes:row.bytes,sha256:row.sha256,note:'Conținutul inițial este păstrat după nota de etapă adăugată în audit.'};
    row.bytes=bytes.length;row.sha256=crypto.createHash('sha256').update(bytes).digest('hex').toUpperCase();
    row.scope='Raport istoric al cercetării; notă de orientare adăugată la auditul din 30.10.2026. Vezi catalogul APK actual.';
    manifestUpdates.push(name+':'+row.file);
  }
  fs.writeFileSync(filename,JSON.stringify(manifest,null,2));
}
console.log(JSON.stringify({historicalReportsAnnotated:changed,manifestUpdates}));
