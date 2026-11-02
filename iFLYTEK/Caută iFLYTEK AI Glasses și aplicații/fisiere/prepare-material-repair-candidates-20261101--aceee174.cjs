'use strict';
// Constructs unapproved text candidates only. Does not alter or promote baseline code.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const repo=path.resolve(__dirname,'..'),baseline='D:/Codex-iflytek-apk-analysis-20261101',work='D:/Codex-iflytek-decompilation-repair-20261101';
const group='3ea33623b7ddbb57cd1fc08a9efe8dcf9d77d3ce8113df41218ef282db79f088';
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
function methodSpan(text,name){
 if(!/^[A-Za-z_$][A-Za-z0-9_$]*$/.test(name))throw Error('Invalid method selector');
 const re=new RegExp('^[ \\t]*(?:(?:public|private|protected|static|final|synchronized)\\s+)*[\\w.$<>\\[\\]]+\\s+'+name+'\\s*\\([^;{}]*?\\)\\s*\\{','gm'),matches=[...text.matchAll(re)];
 if(matches.length!==1)throw Error('Expected unique method declaration: '+name);const open=matches[0].index+matches[0][0].lastIndexOf('{');let level=0,state='code';
 for(let i=open;i<text.length;i++){const c=text[i],n=text[i+1];if(state==='line'){if(c==='\n')state='code';continue;}if(state==='block'){if(c==='*'&&n==='/'){state='code';i++;}continue;}if(state==='string'||state==='char'){if(c==='\\'){i++;continue;}if(c===(state==='string'?'"':"'"))state='code';continue;}
  if(c==='/'&&n==='/'){state='line';i++;continue;}if(c==='/'&&n==='*'){state='block';i++;continue;}if(c==='"'){state='string';continue;}if(c==="'"){state='char';continue;}if(c==='{')level++;if(c==='}'&&!--level)return{declaration:matches[0].index,open,end:i+1};}
 throw Error('Unclosed method body');
}
function renameTokens(text,names){
 let out='',state='code';for(let i=0;i<text.length;){const c=text[i],n=text[i+1];if(state==='line'){out+=c;i++;if(c==='\n')state='code';continue;}if(state==='block'){out+=c;i++;if(c==='*'&&n==='/'){out+='/';i++;state='code';}continue;}if(state==='string'||state==='char'){out+=c;i++;if(c==='\\'){out+=text[i++]||'';continue;}if(c===(state==='string'?'"':"'"))state='code';continue;}
  if(c==='/'&&(n==='/'||n==='*')){out+=c+n;i+=2;state=n==='/'?'line':'block';continue;}if(c==='"'||c==="'"){out+=c;i++;state=c==='"'?'string':'char';continue;}
  if(/[A-Za-z_$]/.test(c)){let j=i+1;while(j<text.length&&/[A-Za-z0-9_$]/.test(text[j]))j++;const token=text.slice(i,j);out+=Object.hasOwn(names,token)?names[token]:token;i=j;}else{out+=c;i++;}}
 return out;
}
function buildCandidate(original,upstream,name,renames,notice=''){
 const oldSpan=methodSpan(original,name),upstreamSpan=methodSpan(upstream,name),oldBody=original.slice(oldSpan.open,oldSpan.end),sourceBody=upstream.slice(upstreamSpan.open,upstreamSpan.end);
 if(!/Method not decompiled:/.test(oldBody))throw Error('Target is not the expected generated stub');
 const renamed=renameTokens(sourceBody,renames),replacement=notice?'{\n'+notice+'\n'+renamed.slice(1):renamed,prefix=original.slice(0,oldSpan.open),suffix=original.slice(oldSpan.end),candidate=prefix+replacement+suffix;
 if(candidate.slice(0,prefix.length)!==prefix||candidate.slice(prefix.length+replacement.length)!==suffix)throw Error('Outside-body modification');
 return{candidate,proof:{oldSpan:{start:oldSpan.open,end:oldSpan.end,sha256:hash(oldBody),bytes:Buffer.byteLength(oldBody)},upstreamSpan:{start:upstreamSpan.open,end:upstreamSpan.end,sha256:hash(sourceBody)},replacement:{sha256:hash(replacement),bytes:Buffer.byteLength(replacement)},unchangedPrefixSha256:hash(prefix),unchangedSuffixSha256:hash(suffix),offsetUnit:'UTF-16 string offsets; span bytes and SHA-256 independently recorded',renames}};
}
function main(){
 const report=JSON.parse(fs.readFileSync(path.join(repo,'apk-analysis-2026-11-01/decompilation',group,'manifest.json'))),sourceRoot=path.join(repo,'decompilation-repair-2026-11-01/upstream-candidates/material-1.13.0'),provenance=JSON.parse(fs.readFileSync(path.join(sourceRoot,'provenance.json')));
 const definitions=[{name:'CarouselStrategyHelper',sub:'carousel',method:'createCenterAlignedKeylineState',descriptor:'Lcom/google/android/material/carousel/CarouselStrategyHelper;->createCenterAlignedKeylineState(Landroid/content/Context;FILcom/google/android/material/carousel/Arrangement;)Lcom/google/android/material/carousel/KeylineState;',renames:{context:'r19',childHorizontalMargins:'r20',availableSpace:'r21',arrangement:'r22',min:'Math.min',getChildMaskPercentage:'CarouselStrategy.getChildMaskPercentage'}},{name:'ShadowDrawableWrapper',sub:'shadow',method:'drawShadow',descriptor:'Lcom/google/android/material/shadow/ShadowDrawableWrapper;->drawShadow(Landroid/graphics/Canvas;)V',renames:{canvas:'r19'}}],results=[];
 for(const d of definitions){const logical='sources/com/google/android/material/'+d.sub+'/'+d.name+'.java',record=report.entries.find(r=>r.path===logical);if(!record)throw Error('Missing baseline entry');const b=fs.readFileSync(path.join(baseline,'jadx-output',group,logical));if(hash(b)!==record.sha256||b.length!==record.bytes)throw Error('Baseline SHA mismatch');const original=b.toString('utf8');if(!Buffer.from(original).equals(b))throw Error('Non-roundtrippable baseline UTF-8');
  const source=fs.readFileSync(path.join(sourceRoot,d.name+'.java')),expected=provenance.files.find(r=>r.file===d.name+'.java');if(source.length!==expected.bytes||hash(source)!==expected.sha256)throw Error('Upstream source mismatch');const upstreamText=source.toString('utf8'),license=upstreamText.match(/^\/\*[\s\S]*?\*\//)?.[0];if(!license)throw Error('Upstream copyright/license notice missing');const notice=license+'\n/* Modified body-only repair candidate. NOT semantically approved. Source: '+expected.url+' */',result=buildCandidate(original,upstreamText,d.method,d.renames,notice),folder=path.join(work,'manual-material',d.name);fs.mkdirSync(folder,{recursive:true});fs.writeFileSync(path.join(folder,d.name+'.java'),result.candidate);
  results.push({status:'UNAPPROVED-CANDIDATE',semanticValidation:'pending independent Smali/CFG and individual audit; syntax compilation alone is insufficient',group,logicalPath:logical,descriptor:d.descriptor,baseline:{sha256:record.sha256,bytes:record.bytes},upstream:expected,candidate:{file:path.join(folder,d.name+'.java'),sha256:hash(result.candidate),bytes:Buffer.byteLength(result.candidate)},proof:result.proof});
 }
 const out=path.join(work,'manual-material/candidates.json');fs.writeFileSync(out,JSON.stringify({schemaVersion:1,generatedAt:new Date().toISOString(),generator:{script:'tools/prepare-material-repair-candidates-20261101.cjs',sha256:hash(fs.readFileSync(__filename)),command:['node','tools/prepare-material-repair-candidates-20261101.cjs']},status:'UNAPPROVED-CANDIDATES-NO-BASELINE-MODIFIED',candidates:results},null,2)+'\n');console.log(JSON.stringify({file:out,candidates:results.map(r=>({class:r.logicalPath,sha256:r.candidate.sha256,status:r.status}))}));
}
if(require.main===module)main();
module.exports={methodSpan,renameTokens,buildCandidate};
