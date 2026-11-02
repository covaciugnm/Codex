const fs=require('fs'),cp=require('child_process'),path=require('path'),crypto=require('crypto');
const repo='D:/CodexWork/eva-audit-p01-src-20261101', out='D:/CodexWork/eva-audit-p01-readonly-20261101';
const docsOnly=process.argv.includes('--docs');
const env={...process.env,GIT_SSH_COMMAND:'ssh -i C:/Users/User/.ssh/eva_accounting_docs_20261008 -o IdentitiesOnly=yes -o BatchMode=yes',GIT_LFS_SKIP_SMUDGE:'1'};
const git=(args,opt={})=>cp.execFileSync('git',['-C',repo,...args],{env,maxBuffer:300*1024*1024,...opt});
const sha=git(['rev-parse','HEAD']).toString().trim();
const tree=git(['ls-tree','-r','-z',sha]).toString('utf8').split('\0').filter(Boolean).map(s=>{const [a,p]=s.split('\t');const [mode,type,oid]=a.split(' ');return{mode,type,oid,path:p};});
const roots=new Set(['backend','frontend','idempiere','database','proxy','scripts','tools','import-bridge','provisioner','bootstrap','Spree','mail','mirror']);
const docs=new Set(['Documentatie/echipa-2026-10-09/00_REGULI_SI_ROLURI.md','Documentatie/echipa-2026-10-09/00_CORESPONDENTA_COD_CAPITOL.json','Documentatie/09.10.2026-octombrie/00-comun/00_REGULI_SI_ROLURI.md']);
const selected=[],excluded=[];
for(const e of tree){let include=docsOnly ? /^Documentatie\/echipa-2026-10-09\/(00[^/]+\.(json|jsonl|md)|00_TEMPLATE\/[^/]+|agenti\/[^/]+)$/.test(e.path) : (roots.has(e.path.split('/')[0])||docs.has(e.path)||['AGENTS.md','README.md','docker-compose.yml','.gitignore'].includes(e.path));
 if(!include)continue;
 let reason='';if(e.type!=='blob'||e.mode==='120000')reason='nonregular';
 else if(/(^|\/)(node_modules|\.git|vendor\/bundle)(\/|$)/i.test(e.path))reason='vendored dependencies';
 else if(/\.(jar|war|zip|tar|gz|png|jpe?g|gif|ico|pdf|woff2?|ttf|mp4|db|sqlite|bak|exe|dll|p12|pfx|pem|key)$/i.test(e.path))reason='binary or credential-like extension';
 else if(/(^|\/)\.env($|\.)/.test(e.path)&&!/example|sample|template/.test(e.path))reason='environment file';
 else if(e.path.split('/').some(p=>/[<>:"|?*]/.test(p)||/^(con|prn|aux|nul|com[1-9]|lpt[1-9])(\.|$)/i.test(p)))reason='Windows-incompatible path';
 if(reason)excluded.push({...e,reason});else selected.push(e);
}
fs.mkdirSync(out,{recursive:true});
fs.writeFileSync(path.join(out,docsOnly?'DOCS_INVENTORY.json':'SOURCE_INVENTORY.json'),JSON.stringify({sha,tree_count:tree.length,selected_count:selected.length,selected,excluded},null,2));
const required=selected.filter(e=>docs.has(e.path)||['AGENTS.md','README.md','docker-compose.yml'].includes(e.path));
const ordered=[...required,...selected.filter(e=>!required.includes(e))];
const chunk=250;
for(let offset=0;offset<ordered.length;offset+=chunk){const entries=ordered.slice(offset,offset+chunk),ids=[...new Set(entries.map(e=>e.oid))];
 git(['-c','fetch.negotiationAlgorithm=noop','fetch','--no-tags','--no-write-fetch-head','--recurse-submodules=no','--filter=blob:none','origin','--stdin'],{input:ids.join('\n')+'\n',stdio:['pipe','pipe','pipe']});
 const buf=git(['cat-file','--batch'],{input:entries.map(e=>e.oid).join('\n')+'\n'});let cursor=0;
 for(const e of entries){const nl=buf.indexOf(10,cursor),header=buf.subarray(cursor,nl).toString(),parts=header.split(' '),len=Number(parts[2]);if(parts[1]!=='blob'||!Number.isFinite(len))throw Error(header);const bytes=buf.subarray(nl+1,nl+1+len);cursor=nl+1+len+1;const verified=crypto.createHash('sha1').update(Buffer.from('blob '+len+'\0')).update(bytes).digest('hex');if(verified!==e.oid)throw Error('Object mismatch '+e.path);const target=path.join(out,...e.path.split('/'));fs.mkdirSync(path.dirname(target),{recursive:true});fs.writeFileSync(target,bytes);e.bytes=len;e.sha256=crypto.createHash('sha256').update(bytes).digest('hex');}
 console.log(JSON.stringify({materialized:Math.min(offset+chunk,ordered.length),total:ordered.length}));
}
const manifest={repo:'cesiroproduction/Eva-Accounting',branch:'master',sha,captured_at_utc:new Date().toISOString(),tree_count:tree.length,materialized_count:selected.length,method:'Git blob objects verified by SHA1, no checkout; excluded files remain explicit, not audited',files:selected,excluded};
fs.writeFileSync(path.join(out,docsOnly?'DOCS_MANIFEST.json':'SOURCE_MANIFEST.json'),JSON.stringify(manifest,null,2));
console.log(JSON.stringify({done:true,sha,files:selected.length,excluded:excluded.length,out}));
