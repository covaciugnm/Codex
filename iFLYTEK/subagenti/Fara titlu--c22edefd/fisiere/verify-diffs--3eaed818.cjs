'use strict';
const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..'),read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const diffs=read(path.join(root,'VERSION-DIFFS.json'));
function entries(info){const m=read(path.join(root,info.manifest));if(m.source.sha256!==info.sourceSha256)throw Error('Wrong comparison source');const map=new Map(m.entries.map(r=>[(r.component===m.package+'.apk'?'base.apk':r.component)+'/'+r.path,r]));if(map.size!==info.files)throw Error('Wrong source file count');return map;}
const results=[];
for(const pair of diffs.comparisons){const before=entries(pair.from),after=entries(pair.to),seen=new Set(),counts={added:0,changed:0,removed:0,identical:0};
 for(const [kind,list] of Object.entries(pair.lists))for(const r of list){if(seen.has(r.key))throw Error('Repeated comparison key');seen.add(r.key);const b=before.get(r.key),a=after.get(r.key),expected=!b?'added':!a?'removed':b.sha256===a.sha256&&b.bytes===a.bytes?'identical':'changed';if(expected!==kind)throw Error('Wrong diff status '+r.key);for(const [actual,claimed] of [[b,r.before],[a,r.after]])if(claimed&&(!actual||claimed.sha256!==actual.sha256||claimed.bytes!==actual.bytes))throw Error('Wrong before/after hash');counts[kind]++;}
 const union=new Set([...before.keys(),...after.keys()]);if(seen.size!==union.size||[...union].some(k=>!seen.has(k)))throw Error('Incomplete diff');
 for(const key of Object.keys(counts))if(counts[key]!==pair.counts[key])throw Error('Wrong diff totals');
 const categories=Object.values(pair.categories);for(const key of Object.keys(counts))if(categories.reduce((n,c)=>n+c[key],0)!==counts[key])throw Error('Wrong category aggregate');
 results.push({from:pair.from.variant,to:pair.to.variant,counts,status:'PASS'});
}
if(results.length!==10)throw Error('Wrong comparison coverage');
const result={checkedAt:new Date().toISOString(),comparisons:results,status:'PASS'};fs.writeFileSync(path.join(__dirname,'diff-results.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));
