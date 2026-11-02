'use strict';
// Reproducible evidence index accompanying the author's manual static review.
// Instruction/branch counters alone do not establish semantic equivalence.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {methodSpan}=require('./prepare-material-repair-candidates-20261101.cjs');
const repo=path.resolve(__dirname,'..'),root=path.join(repo,'decompilation-repair-2026-11-01'),work='D:/Codex-iflytek-decompilation-repair-20261101';
const hash=b=>crypto.createHash('sha256').update(b).digest('hex'),read=p=>JSON.parse(fs.readFileSync(p));
function main(){
 const candidates=read(path.join(work,'manual-material/candidates.json')),exported=read(path.join(root,'correlation/reference-export-results.json'));
 const rows=fs.readFileSync(path.join(exported.run,'references.ndjson'),'utf8').trim().split('\n').map(x=>JSON.parse(x)),results=[];
 for(const c of candidates.candidates){const [descriptor,signature]=c.descriptor.split('->'),r=rows.find(x=>x.descriptor===descriptor);if(!r||r.validationErrors)throw Error('Validated original ClassDef required');const raw=Buffer.from(r.smaliBase64,'base64');if(raw.length!==r.smaliBytes||hash(raw)!==r.smaliSha256)throw Error('Smali mismatch');const lines=raw.toString('utf8').split(/\r?\n/),starts=lines.flatMap((l,i)=>l.startsWith('.method ')&&l.endsWith(signature)?[i]:[]);if(starts.length!==1)throw Error('Method identity is not unique');const end=lines.findIndex((l,i)=>i>starts[0]&&l==='.end method');if(end<0)throw Error('Missing end method');const method=lines.slice(starts[0],end+1),instructions=method.map(l=>l.trim()).filter(l=>l&&!/^[.#:]/.test(l)),branches=instructions.filter(l=>/^if-/.test(l)),catches=method.filter(l=>l.trim().startsWith('.catch'));
  const text=fs.readFileSync(c.candidate.file);if(hash(text)!==c.candidate.sha256||text.length!==c.candidate.bytes)throw Error('Candidate changed');const name=signature.slice(0,signature.indexOf('(')),span=methodSpan(text.toString('utf8'),name),body=text.toString('utf8').slice(span.open,span.end);
  if(catches.length||branches.length!==(name==='drawShadow'?6:4)||/Method not decompiled:/.test(body))throw Error('Unexpected reviewed method shape');
  results.push({descriptor:c.descriptor,candidate:c.candidate,baseline:c.baseline,originalSmali:{dexEntry:r.dexEntry,classSha256:r.smaliSha256,classBytes:r.smaliBytes,methodSha256:hash(method.join('\n')),lineEndingForMethodHash:'LF',methodStartLine:starts[0]+1,methodEndLine:end+1},instructionCount:instructions.length,conditionalBranches:branches,catches,calls:instructions.filter(l=>l.startsWith('invoke-')),fieldReads:instructions.filter(l=>/^iget/.test(l)),returnInstructions:instructions.filter(l=>l.startsWith('return')),authorReview:{status:'AUTHOR-REVIEW-COMPLETE; INDEPENDENT-SEMANTIC-ACCEPTANCE-PENDING',method:'Full static comparison of the original symbolic Smali and adapted upstream method body; not inferred from counts or compilation alone',observations:name==='drawShadow'?[
    'Canvas save/rotation precede all geometry. cornerRadius is cached as shadowOffset; edgeShadowTop = -cornerRadius - shadowSize.',
    'width - 2*shadowOffset > 0 and height - 2*shadowOffset > 0 match cmpl-float + if-lez, including false branches for NaN.',
    'Raw shadow offsets preserve the ordered float operations with .25f, .5f and 1f; subtraction by the value times 1f is preserved rather than replaced by zero.',
    'LT/RB/LB/RT save, translate, scale, drawPath, optional edge drawRect and restore order agrees. RB/LB/RT rotations are 180/270/90 degrees.',
    'Horizontal edge tests guard LT/RB; vertical edge tests guard LB/RT. The inverse scale uses horizontal/bottom/top scale in the corresponding block.',
    'RB rectangle bottom is -cornerRadius + shadowSize; all other edge rectangle bottoms are -cornerRadius. Final restore uses the original outer save token.',
    'No try/catch/finally exists in the original method or the source body. Call exceptions stop the same remaining operations; no handler was introduced.'
   ]:[
    'Extra-small width is Math.min(getExtraSmallSize(context)+margins, largeSize); head = 0f-width/2f. Math.min remains the float overload.',
    'First small and medium halves use int-to-float, /2f, promotion to double, Math.floor and cast to int. Position helper call order and repeated field reads agree.',
    'Large range uses largeCount; second medium half uses ceil(count/2f). Tail anchor converts the availableSpace int to float before adding width/2f.',
    'Masks are calculated in extra-small/small/medium order with the same three float arguments; Builder constructor retains (float,int), not (float,float).',
    'Four independent if count>0 branches guard small-floor, medium-floor, medium-ceil and small-ceil ranges. Counts are read at each corresponding source point.',
    'Central range uses zero float mask and true focal boolean. Range ordering, final tail anchor and returned Builder.build() value agree.',
    'No try/catch/finally exists in either method body. Static helper and builder calls are preserved rather than replaced by assumed values.'
   ]}});
 }
 const report={schemaVersion:1,reviewer:'root / author; requires independent auditor acceptance',reviewedAt:new Date().toISOString(),generatorSha256:hash(fs.readFileSync(__filename)),sourceReferenceExportSha256:hash(fs.readFileSync(path.join(root,'correlation/reference-export-results.json'))),status:'NOT-PROMOTED',methods:results};
 fs.writeFileSync(path.join(work,'manual-material/static-review.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(results.map(r=>({method:r.descriptor,instructions:r.instructionCount,branches:r.conditionalBranches.length,smaliMethodSha256:r.originalSmali.methodSha256}))));
}
if(require.main===module)main();
