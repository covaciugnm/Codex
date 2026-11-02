'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const root=path.resolve(__dirname,'..'),read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const fold=s=>s.normalize('NFC').toUpperCase(),sha=b=>crypto.createHash('sha256').update(b).digest('hex');
function verifyTree(manifestRelative,destination){
 const m=read(path.join(root,manifestRelative)),mapping=read(path.join(destination,'PATH-MAP.json')),source=read(path.join(destination,'SOURCE-MANIFEST.json'));
 if(mapping.sourceSha256!==m.source.sha256||source.source.sha256!==m.source.sha256||mapping.variant!==m.variant)throw Error('Wrong source identity '+destination);
 const expected=new Map();function add(logical,r,kind,component){if(expected.has(logical))throw Error('Duplicate expected logical name');expected.set(logical,{record:r,kind,component,path:r.path});}
 for(const r of m.entries)add('raw/'+r.component+'/'+r.path,r,'raw',r.component);for(const r of m.outerEntries)if(r.storage!=='source-zip-entry')add('xapk/'+r.path,r,'xapk-sidecar',null);
 for(const c of m.decompilation.components||[]){const d=read(path.join(root,c.manifest));for(const r of d.entries)add('decompiled/'+c.component+'/'+r.path,r,'decompiled',c.component);for(const r of d.logs)add('logs/'+c.component+'/'+r.path.replace(/.*\//,''),r,'log',c.component);}
 const logicalSeen=new Set(),physicalSeen=new Set();let bytes=0,mapped=0;
 for(const p of mapping.paths){const row=expected.get(p.logical),r=row?.record;if(!r||r.sha256!==p.sha256||r.bytes!==p.bytes||logicalSeen.has(p.logical)||row.path!==p.path||row.component!==p.component||row.kind!==p.kind)throw Error('Wrong logical mapping');logicalSeen.add(p.logical);
  if(p.physical.includes('\\')||p.physical.startsWith('/')||p.physical.split('/').some(s=>!s||s==='.'||s==='..'))throw Error('Unsafe physical mapping');
  const key=fold(p.physical);if(physicalSeen.has(key))throw Error('Case-insensitive file overwrite');physicalSeen.add(key);
  const target=path.resolve(destination,p.physical);if(!target.startsWith(path.resolve(destination)+path.sep))throw Error('Physical path escape');
  const b=fs.readFileSync(target);if(b.length!==r.bytes||sha(b)!==r.sha256)throw Error('Materialized byte mismatch '+m.variant+':'+p.logical);bytes+=b.length;if(p.physical!==p.logical)mapped++;
 }
 if(logicalSeen.size!==expected.size)throw Error('Incomplete logical mapping');
 const actual=new Set();function walk(folder,rel=''){for(const e of fs.readdirSync(folder,{withFileTypes:true})){const name=rel?rel+'/'+e.name:e.name;if(e.isDirectory())walk(path.join(folder,e.name),name);else {const key=fold(name);if(actual.has(key))throw Error('Unexpected physical filesystem alias');actual.add(key);}}}walk(destination);
 const permitted=new Set([...physicalSeen,'PATH-MAP.JSON','SOURCE-MANIFEST.JSON']);if(actual.size!==permitted.size||[...actual].some(p=>!permitted.has(p)))throw Error('Missing/stale physical files '+m.variant);
 const result={variant:m.variant,sourceSha256:m.source.sha256,logicalContentFiles:expected.size,physicalContentFiles:physicalSeen.size,metadataFiles:2,totalFilesystemFiles:actual.size,independentlyRereadBytes:bytes,mappedPaths:mapped,status:'PASS'};console.log('Verified physical tree',m.variant,result.logicalContentFiles);return result;
}
function option(name){const i=process.argv.indexOf(name);return i<0?null:process.argv[i+1];}
if(require.main===module){const manifest=option('--manifest'),destination=option('--destination');let result;
 if(manifest&&destination)result={checkedAt:new Date().toISOString(),status:'PASS',versions:[verifyTree(manifest,destination)]};
 else {const runs=read(path.join(root,'materialization-runs.json')),catalog=read(path.join(root,'catalog.json'));if(runs.versions.length!==catalog.versions.length||runs.versions.some(r=>r.status!=='verified'))throw Error('Bulk materialization incomplete');const versions=[];for(const v of catalog.versions){const r=runs.versions.find(x=>x.manifest===v.manifest);if(!r)throw Error('Missing version run');versions.push(verifyTree(v.manifest,r.destination));}result={checkedAt:new Date().toISOString(),status:'PASS',versions,totalContentFiles:versions.reduce((n,r)=>n+r.logicalContentFiles,0),totalFilesystemFiles:versions.reduce((n,r)=>n+r.totalFilesystemFiles,0),independentlyRereadBytes:versions.reduce((n,r)=>n+r.independentlyRereadBytes,0)};}
 const output=manifest?'full-translate-mapped-results.json':'all-materialized-tree-results.json';fs.writeFileSync(path.join(__dirname,output),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));
}
module.exports={verifyTree};
