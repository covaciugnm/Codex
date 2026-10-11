// Retrage numai permisiuni; nu sterge, muta sau modifica continutul fisierelor.
const CONT_ASTEPTAT = 'covaciu.gnm@gmail.com';
const MIME_FOLDER = 'application/vnd.google-apps.folder';

function verificaPartajari() { audit_(); }
function verificaSurse() { surse_(); }
function retragePartajari() { retrage_(); }
function limiteazaSurse() { limiteaza_(); }

function cont_() {
  const email = Drive.About.get({fields:'user(emailAddress)'}).user.emailAddress;
  if (email.toLowerCase() !== CONT_ASTEPTAT) throw new Error('Cont diferit: ' + email);
}
function externe_(permissions) {
  return (permissions || []).filter(p => p.role !== 'owner' && p.view !== 'metadata' &&
    (p.emailAddress || '').toLowerCase() !== CONT_ASTEPTAT);
}
function permisiuni_(id) {
  let token = '', result = [];
  do {
    const opts = {pageSize:100, fields:'nextPageToken,permissions(id,type,role,emailAddress,domain,view,permissionDetails(inherited,inheritedFrom))'};
    if (token) opts.pageToken = token;
    const page = Drive.Permissions.list(id,opts);
    result.push(...(page.permissions || [])); token = page.nextPageToken || '';
  } while(token);
  return externe_(result);
}
function inventar_(doarFoldere) {
  const deadline = Date.now()+210000;
  let token='', files=[];
  do {
    if(Date.now()>deadline) throw new Error('Inventarul nu s-a terminat in timpul disponibil. Nicio confirmare de rezultat.');
    const opts={q:"'me' in owners and trashed=false"+(doarFoldere ? " and mimeType='"+MIME_FOLDER+"'" : ''),
      pageSize:1000, fields:'nextPageToken,incompleteSearch,files(id,name,mimeType,parents,ownedByMe,shared,inheritedPermissionsDisabled,permissions(id,type,role,emailAddress,domain,view))'};
    if(token) opts.pageToken=token;
    const page=Drive.Files.list(opts);
    if(page.incompleteSearch) throw new Error('Rezultat incomplet al cautarii.');
    files.push(...(page.files||[])); token=page.nextPageToken||'';
  } while(token);
  return files;
}
function eticheta_(f) { return {id:f.id,nume:f.name,parinti:f.parents||[]}; }
function audit_() {
  cont_(); const files=inventar_(false);
  const shared=files.filter(f=>f.permissions ? externe_(f.permissions).length : f.shared===true);
  const uncertain=files.filter(f=>!f.permissions && f.shared!==false);
  const folders=files.filter(f=>f.mimeType===MIME_FOLDER);
  const result={total:files.length,foldere:folders.length,documente:files.length-folders.length,
    elementeCuAccesExtern:shared.length,permisiuniExterne:files.reduce((n,f)=>n+externe_(f.permissions).length,0),
    permisiuniNedisponibile:uncertain.length,permisiuniDoarMetadate:files.reduce((n,f)=>n+(f.permissions||[]).filter(p=>p.view==='metadata').length,0)};
  console.log('AUDIT FINAL: '+JSON.stringify(result));
  shared.slice(0,12).forEach(f=>console.log('EXEMPLU ACCES: '+JSON.stringify({...eticheta_(f),acces:externe_(f.permissions)})));
  console.log(shared.length===0 && uncertain.length===0 ? 'CONFIRMAT: fara partajari pe elementele proprii active. Cosul si fisierele altor proprietari nu sunt incluse.' : 'Mai exista acces extern sau elemente neverificate.');
}
function surse_() {
  cont_(); const folders=inventar_(true); const ids=new Set(folders.map(f=>f.id));
  const roots=folders.filter(f=>!(f.parents||[]).some(id=>ids.has(id)));
  console.log('FOLDERE PROPRII: '+folders.length+'; RADACINI: '+roots.length);
  roots.forEach(f=>{
    const permissions=permisiuni_(f.id);
    console.log('SURSA: '+JSON.stringify({...eticheta_(f),permisiuni:permissions}));
    (f.parents||[]).forEach(id=>{
      if(!ids.has(id)) {
        try {console.log('PARINTE SURSA: '+JSON.stringify(Drive.Files.get(id,{fields:'id,name,ownedByMe,owners(emailAddress),parents'})));}
        catch(e) {console.log('PARINTE NECITIBIL: '+id+' '+e.message);}
      }
    });
  });
}
function retrage_() {
  const lock=LockService.getUserLock();
  if(!lock.tryLock(1000)) throw new Error('Exista deja o retragere activa.');
  try {
    cont_(); const start=Date.now(); const files=inventar_(false);
    const byId=new Map(files.map(f=>[f.id,f]));
    const shared=new Map(files.filter(f=>f.permissions ? externe_(f.permissions).length : f.shared!==false).map(f=>[f.id,f]));
    // Se trateaza mai intai sursa cea mai de sus a partajarii. Dupa propagare se ruleaza din nou.
    function areStramosPartajat(f) {
      let parents=f.parents||[], seen=new Set();
      while(parents.length) {
        const id=parents[0]; if(seen.has(id)) return false; seen.add(id);
        if(shared.has(id)) return true;
        const parent=byId.get(id); if(!parent) return false; parents=parent.parents||[];
      }
      return false;
    }
    const candidates=[...shared.values()].filter(f=>!areStramosPartajat(f));
    candidates.sort((a,b)=>(a.mimeType===MIME_FOLDER?0:1)-(b.mimeType===MIME_FOLDER?0:1));
    const stats={totalInventariat:files.length,partajate:shared.size,surse:candidates.length,procesate:0,retrase:0,mostenite:0,erori:0,pauza:false};
    console.log('PLAN RETRAGERE: '+JSON.stringify(stats));
    for(const f of candidates) {
      if(Date.now()-start>240000) {stats.pauza=true;break;}
      try {
        const current=Drive.Files.get(f.id,{fields:'id,name,ownedByMe,trashed'});
        if(!current.ownedByMe || current.trashed) continue;
        for(const p of permisiuni_(f.id)) {
          const label={...eticheta_(f),acces:p.emailAddress||p.domain||p.type,rol:p.role};
          const details=p.permissionDetails||[];
          if(details.length && details.every(d=>d.inherited===true)) {
            stats.mostenite++; console.log('MOSTENITA NEREZOLVATA: '+JSON.stringify({...label,detalii:details})); continue;
          }
          try {Drive.Permissions.remove(f.id,p.id);stats.retrase++;console.log('RETRASA: '+JSON.stringify(label));}
          catch(e) {stats.erori++;console.log('EROARE RETRAGERE: '+JSON.stringify(label)+' '+e.message);}
        }
        stats.procesate++;
      } catch(e) {stats.erori++;console.log('EROARE FISIER: '+f.id+' '+e.message);}
    }
    console.log('REZULTAT RETRAGERE: '+JSON.stringify(stats));
    console.log('Ruleaza verificaPartajari pentru confirmare. Daca mai exista partajari, poate fi necesara inca o trecere dupa propagare.');
  } finally {lock.releaseLock();}
}

function limiteaza_() {
  const lock=LockService.getUserLock();
  if(!lock.tryLock(1000)) throw new Error('Alta operatiune activa.');
  try {
    cont_(); const start=Date.now(); const folders=inventar_(true);
    const ids=new Set(folders.map(f=>f.id));
    const roots=folders.filter(f=>!(f.parents||[]).some(id=>ids.has(id)));
    const stats={radacini:roots.length,limitate:0,permisiuniDirecteRetrase:0,erori:0,pauza:false};
    for(const f of roots) {
      if(Date.now()-start>240000) {stats.pauza=true;break;}
      try {
        const current=Drive.Files.get(f.id,{fields:'ownedByMe,trashed,inheritedPermissionsDisabled,capabilities(canDisableInheritedPermissions)'});
        if(!current.ownedByMe || current.trashed) continue;
        let permissions=permisiuni_(f.id);
        const inherited=permissions.some(p=>(p.permissionDetails||[]).some(d=>d.inherited));
        if(inherited && !current.inheritedPermissionsDisabled) {
          if(!current.capabilities.canDisableInheritedPermissions) throw new Error('Nu permite limitarea mostenirii.');
          Drive.Files.update({inheritedPermissionsDisabled:true},f.id);
          stats.limitate++;console.log('LIMITAT: '+JSON.stringify(eticheta_(f)));
          permissions=permisiuni_(f.id);
        }
        for(const p of permissions) {
          const details=p.permissionDetails||[];
          if(details.length && details.every(d=>d.inherited)) {
            stats.erori++;console.log('MOSTENIRE RAMASA: '+f.id+' '+JSON.stringify(p));continue;
          }
          Drive.Permissions.remove(f.id,p.id);stats.permisiuniDirecteRetrase++;
          console.log('DIRECTA RETRASA: '+f.id+' '+(p.emailAddress||p.type));
        }
      } catch(e) {stats.erori++;console.log('EROARE LIMITARE: '+f.id+' '+e.message);}
    }
    console.log('REZULTAT LIMITARE: '+JSON.stringify(stats));
  } finally {lock.releaseLock();}
}

function verificaDestinatie() {
  cont_();
  try {console.log('DESTINATIE VECHE: '+JSON.stringify(Drive.Files.get('1ltgo4ImgXLsA1WeuAd9ecrD6bWvY5UMT',{fields:'id,name,ownedByMe,trashed,parents,owners(emailAddress),capabilities'})));}
  catch(e) {console.log('DESTINATIE VECHE: '+e.message);}
  const list=Drive.Files.list({q:"'me' in owners and trashed=false and mimeType='application/vnd.google-apps.folder' and name='Comun.7'",fields:'files(id,name,parents,ownedByMe)',pageSize:100});
  console.log('COMUN PROPRIU: '+JSON.stringify(list));
  console.log('EXEMPLU DOCUMENT: '+JSON.stringify(Drive.Files.get('1RI1KqoQQKzSwKDwQZeHPARMoANuRLI8Oi7Ax5rk__2s',{fields:'id,name,mimeType,ownedByMe,parents,capabilities(canAddMyDriveParent,canMoveItemWithinDrive),permissions(id,type,role,emailAddress)'})));
}

function destinatieComun_() {
  const props=PropertiesService.getUserProperties();
  let id=props.getProperty('comun7_destinatie');
  if(!id) {
    const page=Drive.Files.list({q:"'me' in owners and trashed=false and mimeType='application/vnd.google-apps.folder' and name='Comun.7'",fields:'files(id)',pageSize:100});
    if((page.files||[]).length>1) throw new Error('Mai multe destinatii Comun.7; oprire.');
    id=page.files?.[0]?.id;
    if(!id) id=Drive.Files.create({name:'Comun.7',mimeType:MIME_FOLDER,parents:['root']},null,{fields:'id'}).id;
    props.setProperty('comun7_destinatie',id);
  }
  const dest=Drive.Files.get(id,{fields:'id,name,ownedByMe,trashed'});
  if(!dest.ownedByMe || dest.trashed || dest.name!=='Comun.7') throw new Error('Destinatie nevalida.');
  if(permisiuni_(id).length) throw new Error('Destinatia are partajari; oprire.');
  return id;
}
function mutaExempluComun() {
  cont_(); const dest=destinatieComun_();
  console.log('COMUN PRIVAT: '+dest);
  const id='1RI1KqoQQKzSwKDwQZeHPARMoANuRLI8Oi7Ax5rk__2s';
  const f=Drive.Files.get(id,{fields:'id,name,ownedByMe,parents,trashed'});
  if(!f.ownedByMe || f.trashed) throw new Error('Fisier neeligibil.');
  if(!(f.parents||[]).includes(dest)) {
    const opts={addParents:dest,enforceSingleParent:true,fields:'id,name,parents'};
    if(f.parents?.length) opts.removeParents=f.parents.join(',');
    console.log('MUTAT: '+JSON.stringify(Drive.Files.update({},id,null,opts)));
  }
  console.log('VERIFICARE DUPA MUTARE: '+JSON.stringify({fisier:Drive.Files.get(id,{fields:'id,name,parents,ownedByMe'}),permisiuni:permisiuni_(id)}));
}

function mutaInComun() {
  const lock=LockService.getUserLock();
  if(!lock.tryLock(1000)) throw new Error('Alta operatiune activa.');
  try {
    cont_(); const dest=destinatieComun_(); const start=Date.now();
    let token='', files=[];
    do {
      const opts={q:"'me' in owners and trashed=false",pageSize:1000,fields:'nextPageToken,incompleteSearch,files(id,name,ownedByMe,parents,mimeType)'};
      if(token) opts.pageToken=token;
      const page=Drive.Files.list(opts);
      if(page.incompleteSearch) throw new Error('Inventar incomplet.');
      files.push(...(page.files||[]));token=page.nextPageToken||'';
      if(Date.now()-start>180000) throw new Error('Inventarierea a depasit timpul disponibil.');
    } while(token);
    const ids=new Set(files.map(f=>f.id));
    const roots=files.filter(f=>f.ownedByMe && f.id!==dest && !(f.parents||[]).some(id=>ids.has(id)));
    roots.sort((a,b)=>(a.mimeType===MIME_FOLDER?0:1)-(b.mimeType===MIME_FOLDER?0:1));
    const stats={destinatie:dest,total:files.length,deMutat:roots.length,mutate:0,erori:0,pauza:false};
    console.log('PLAN MUTARE: '+JSON.stringify(stats));
    for(const f of roots) {
      if(Date.now()-start>240000 || stats.mutate>=180) {stats.pauza=true;break;}
      try {
        const current=Drive.Files.get(f.id,{fields:'ownedByMe,trashed,parents'});
        if(!current.ownedByMe || current.trashed || (current.parents||[]).includes(dest)) continue;
        const opts={addParents:dest,enforceSingleParent:true,fields:'id,parents'};
        if(current.parents?.length) opts.removeParents=current.parents.join(',');
        const moved=Drive.Files.update({},f.id,null,opts);
        if(!(moved.parents||[]).includes(dest)) throw new Error('Parintele nu a fost confirmat.');
        stats.mutate++;
        console.log('MUTAT COMUN: '+JSON.stringify({...eticheta_(f),parintiAnteriori:current.parents||[],destinatie:dest}));
      } catch(e) {stats.erori++;console.log('EROARE MUTARE: '+f.id+' '+e.message);}
    }
    console.log('REZULTAT MUTARE: '+JSON.stringify(stats));
    console.log('Reia mutaInComun pana la deMutat=0; apoi verificaPartajari.');
  } finally {lock.releaseLock();}
}

function continuaMutarea() {
  const lock=LockService.getUserLock();
  if(!lock.tryLock(1000)) throw new Error('Alta mutare activa.');
  try {
    cont_();const dest=destinatieComun_();const props=PropertiesService.getUserProperties();const start=Date.now();
    let state=JSON.parse(props.getProperty('mutare_comun_coada_v1')||'null');
    if(!state) {
      let token='', files=[];
      do {
        const opts={q:"'me' in owners and trashed=false",pageSize:1000,fields:'nextPageToken,incompleteSearch,files(id,ownedByMe,parents,mimeType)'};
        if(token) opts.pageToken=token;
        const page=Drive.Files.list(opts);
        if(page.incompleteSearch) throw new Error('Inventar incomplet.');
        files.push(...(page.files||[]));token=page.nextPageToken||'';
        if(Date.now()-start>180000) throw new Error('Inventar prea lent.');
      } while(token);
      const ids=new Set(files.map(f=>f.id));
      const roots=files.filter(f=>f.ownedByMe && f.id!==dest && !(f.parents||[]).some(id=>ids.has(id)));
      roots.sort((a,b)=>(a.mimeType===MIME_FOLDER?0:1)-(b.mimeType===MIME_FOLDER?0:1));
      const pending=roots.map(f=>f.id);
      for(let i=0;i<pending.length;i+=100) props.setProperty('mutare_comun_ids_'+Math.floor(i/100),JSON.stringify(pending.slice(i,i+100)));
      state={dest,total:pending.length,index:0,mutate:0,erori:0};props.setProperty('mutare_comun_coada_v1',JSON.stringify(state));
    }
    if(state.dest!==dest) throw new Error('Destinatia s-a schimbat.');
    console.log('PROGRES INITIAL: '+JSON.stringify(state));
    let cachedBlock=-1, ids=[];
    for(;state.index<state.total;state.index++) {
      if(Date.now()-start>270000) break;
      const block=Math.floor(state.index/100);
      if(block!==cachedBlock){ids=JSON.parse(props.getProperty('mutare_comun_ids_'+block));cachedBlock=block;}
      const id=ids[state.index%100];
      try {
        const f=Drive.Files.get(id,{fields:'id,name,ownedByMe,trashed,parents'});
        if(!f.ownedByMe || f.trashed) throw new Error('Nu mai este eligibil.');
        if(!(f.parents||[]).includes(dest)) {
          const opts={addParents:dest,enforceSingleParent:true,fields:'id,parents'};
          if(f.parents?.length) opts.removeParents=f.parents.join(',');
          const result=Drive.Files.update({},id,null,opts);
          if(!(result.parents||[]).includes(dest)) throw new Error('Parinte neconfirmat.');
          state.mutate++;
          console.log('MUTAT: '+JSON.stringify({...eticheta_(f),destinatie:dest}));
        }
      } catch(e) {state.erori++;props.setProperty('mutare_eroare_'+id,e.message);console.log('EROARE MUTARE: '+id+' '+e.message);}
      props.setProperty('mutare_comun_coada_v1',JSON.stringify({...state,index:state.index+1}));
    }
    props.setProperty('mutare_comun_coada_v1',JSON.stringify(state));
    console.log('PROGRES FINAL: '+JSON.stringify(state));
    console.log(state.index>=state.total ? 'COADA TERMINATA. Verifica inventarul si partajarile.' : 'PAUZA. Reia continuaMutarea.');
  } finally {lock.releaseLock();}
}
