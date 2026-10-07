const fs=require('fs'),path=require('path'),crypto=require('crypto');const root=path.resolve(__dirname,'..');
const target=process.argv[2];if(!target||path.basename(target)!=='Cercetare_si_arhitectura_robotica_2026-10-02')throw Error('Unexpected destination');
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const manifest=JSON.parse(fs.readFileSync(path.join(root,'MANIFEST_SHA256.json'),'utf8'));
for(const f of manifest.files)if(hash(path.join(root,f.path))!==f.sha256)throw Error('Source changed '+f.path);
fs.mkdirSync(target,{recursive:true});
for(const f of [...manifest.files.map(x=>x.path),'MANIFEST_SHA256.json']){const dest=path.join(target,f);fs.mkdirSync(path.dirname(dest),{recursive:true});fs.copyFileSync(path.join(root,f),dest);}
const walk=d=>fs.readdirSync(d,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(d,e.name)):[path.relative(target,path.join(d,e.name)).replaceAll('\\','/')]);
const mismatches=manifest.files.filter(f=>!fs.existsSync(path.join(target,f.path))||hash(path.join(target,f.path))!==f.sha256).map(f=>f.path);
const tracked=new Set([...manifest.files.map(f=>f.path),...manifest.excludes]);const extra=walk(target).filter(p=>!tracked.has(p));
const mh=hash(path.join(root,'MANIFEST_SHA256.json'));if(hash(path.join(target,'MANIFEST_SHA256.json'))!==mh)mismatches.push('MANIFEST_SHA256.json');
const proof={at:new Date().toISOString(),status:mismatches.length||extra.length?'failed':'verified',source:root,destination:target,files_checked:manifest.files.length,manifest_sha256:mh,mismatches,extra,scope:'Identitatea si completitudinea copiei; nu validare fizica sau aplicatie'};
for(const d of [root,target])fs.writeFileSync(path.join(d,'LIVRARE_CONFIRMATA.json'),JSON.stringify(proof,null,2)+'\n','utf8');console.log(JSON.stringify(proof));if(proof.status!=='verified')process.exitCode=1;
