'use strict';
// Manual body-only reconstruction proposal. No APK or generated code is executed.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process');
const {buildCandidate}=require('./prepare-material-repair-candidates-20261101.cjs');
const repo=path.resolve(__dirname,'..'),work='D:/Codex-iflytek-decompilation-repair-20261101',old='D:/Codex-iflytek-apk-analysis-20261101',group='3ea33623b7ddbb57cd1fc08a9efe8dcf9d77d3ce8113df41218ef282db79f088';
const hash=b=>crypto.createHash('sha256').update(b).digest('hex'),read=p=>JSON.parse(fs.readFileSync(p));
const body=`{
        /* Body-only reconstruction from original DEX La/b;->l(AISummaryResponse)V.
           Unapproved candidate; requires independent semantic review. */
        if (!com.iflytek.fanyi.blc.manager.BlcUtils.isSuccess(r9.f18384c)) {
            p057f6.c.b("AISummary-Session", new StringBuilder()
                    .append("响应失败: c=").append(r9.f18384c)
                    .append(", d=").append(r9.f18385d).toString());
            if (this.mCallback != null) {
                this.mCallback.onError(r9, Integer.parseInt(r9.f18384c), r9.f18385d, null);
            }
            return;
        }
        if (this.mCallback != null) {
            this.mCallback.onTranslate(r9);
        }
        if (r9.isEnd()) {
            if (this.mCallback != null) {
                this.mCallback.onComplete();
            }
        } else {
            p117l6.g stream = this.mTransStream;
            if (stream != null) {
                stream.d(1);
            }
        }
        java.util.Map<String, Object> data = new java.util.HashMap<>();
        String payload = r9.f18387r;
        int length = payload != null ? payload.length() : 0;
        data.put("data_length", Integer.valueOf(length));
        data.put("c", r9.f18384c);
        data.put("l", Boolean.valueOf(r9.f18386l));
        p157p6.b.h().c(this.mMethodName, "summary", data, null, null);
    }`;
function main(){
 const baseline=read(path.join(repo,'apk-analysis-2026-11-01/decompilation',group,'manifest.json')),base=path.join(old,'jadx-output',group),get=logical=>{const r=baseline.entries.find(e=>e.path===logical);if(!r)throw Error('Missing baseline '+logical);const b=fs.readFileSync(path.join(base,logical));if(hash(b)!==r.sha256||b.length!==r.bytes)throw Error('Changed baseline '+logical);return{record:r,bytes:b,text:b.toString('utf8')};};
 const original=get('sources/p000a/b.java'),response=get('sources/com/iflytek/fanyi/blc/service/bean/AISummaryResponse.java'),aliases=[['c','f18384c','String'],['d','f18385d','String'],['r','f18387r','String'],['l','f18386l','boolean']];
 for(const [raw,alias,type] of aliases)if(!new RegExp('renamed from: '+raw+',[\\s\\S]{0,180}public '+type+' '+alias+';').test(response.text))throw Error('Response field alias not verified');
 const dependencies=['sources/p057f6/c.java','sources/p117l6/g.java','sources/p157p6/b.java'].map(p=>get(p).record);
 const exported=read(path.join(repo,'decompilation-repair-2026-11-01/correlation/reference-export-results.json')),rows=fs.readFileSync(path.join(exported.run,'references.ndjson'),'utf8').trim().split('\n').map(l=>JSON.parse(l)),raw=rows.find(r=>r.descriptor==='La/b;');if(!raw||raw.validationErrors)throw Error('Validated class reference required');const smali=Buffer.from(raw.smaliBase64,'base64');if(hash(smali)!==raw.smaliSha256||smali.length!==raw.smaliBytes)throw Error('Smali changed');
 const lines=smali.toString('utf8').split(/\r?\n/),start=lines.indexOf('.method public l(Lcom/iflytek/fanyi/blc/service/bean/AISummaryResponse;)V'),end=lines.findIndex((l,i)=>i>start&&l==='.end method');if(start<0||end<start)throw Error('Raw callback method missing');const method=lines.slice(start,end+1),instructions=method.map(l=>l.trim()).filter(l=>l&&!/^[.#:]/.test(l));if(instructions.filter(l=>/^if-/.test(l)).length!==7||method.some(l=>l.trim().startsWith('.catch')))throw Error('Unexpected callback control flow');
 const synthetic='class Callback {\n public void onPerformStreamCallback(com.iflytek.fanyi.blc.service.bean.AISummaryResponse r9) '+body+'\n}',built=buildCandidate(original.text,synthetic,'onPerformStreamCallback',{}),folder=path.join(work,'manual-callback');fs.mkdirSync(folder,{recursive:true});const file=path.join(folder,'b.java');fs.writeFileSync(file,built.candidate);
 const fixture=fs.mkdtempSync(path.join(folder,'syntax-')),sources=[],put=(name,text)=>{const p=path.join(fixture,name);fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,text);sources.push(p);};
 put('check/CallbackBody.java','package check; class CallbackBody { Callback mCallback; p117l6.g mTransStream; String mMethodName; interface Callback { void onError(Object o,int n,String s,Throwable t); void onTranslate(Object o); void onComplete(); } public void onPerformStreamCallback(com.iflytek.fanyi.blc.service.bean.AISummaryResponse r9) '+body+' }');
 put('com/iflytek/fanyi/blc/service/bean/AISummaryResponse.java','package com.iflytek.fanyi.blc.service.bean; public class AISummaryResponse { public String f18384c,f18385d,f18387r; public boolean f18386l; public boolean isEnd(){return false;} }');
 put('com/iflytek/fanyi/blc/manager/BlcUtils.java','package com.iflytek.fanyi.blc.manager; public class BlcUtils { public static boolean isSuccess(String c){return false;} }');
 put('p057f6/c.java','package p057f6; public class c { public static void b(String a,String b){} }');put('p117l6/g.java','package p117l6; public class g { public g d(int n){return this;} }');put('p157p6/b.java','package p157p6; public class b { public static b h(){return null;} public void c(String m,String s,java.util.Map a,java.util.Map b,String t){} }');
 const compile=cp.spawnSync('C:/Program Files/Java/jdk-21/bin/javac.exe',['-proc:none','-encoding','UTF-8','-d',path.join(fixture,'classes'),...sources],{encoding:'utf8',timeout:60000,windowsHide:true});
 const report={schemaVersion:1,generatedAt:new Date().toISOString(),generatorSha256:hash(fs.readFileSync(__filename)),status:'UNAPPROVED-CANDIDATE',group,descriptor:'La/b;->l(Lcom/iflytek/fanyi/blc/service/bean/AISummaryResponse;)V',displayedJavaMethod:'p000a.b.onPerformStreamCallback(AISummaryResponse)',logicalPath:original.record.path,baseline:{sha256:original.record.sha256,bytes:original.record.bytes},candidate:{file,sha256:hash(built.candidate),bytes:Buffer.byteLength(built.candidate)},proof:built.proof,responseAliasSource:{path:response.record.path,sha256:response.record.sha256,bytes:response.record.bytes,fields:aliases},dependencyAliasSources:dependencies.map(r=>({path:r.path,sha256:r.sha256,bytes:r.bytes})),smali:{classSha256:raw.smaliSha256,methodSha256:hash(method.join('\n')),methodStartLine:start+1,methodEndLine:end+1,instructions:instructions.length,branches:instructions.filter(l=>/^if-/.test(l)),catches:[]},syntax:{status:compile.status===0?'PASS':'FAIL',exitCode:compile.status,error:compile.error?.message||null,stdout:compile.stdout,stderr:compile.stderr,fixture,sources:sources.map(p=>({file:p,sha256:hash(fs.readFileSync(p))})),generatedCodeExecuted:false},authorStaticReview:[
  'Raw l(AISummaryResponse) is reconstructed, not the synthetic IResponse bridge. Existing displayed method name is preserved.',
  'Failure logs the ordered StringBuilder result before callback checking, parses the response code only for a nonnull callback, calls onError then returns without telemetry.',
  'Callback checks and invocations reread mCallback separately, as in DEX; no local snapshot silently changes concurrent field reads.',
  'Success calls onTranslate before isEnd. End invokes onComplete only when callback exists; non-end reads mTransStream once and invokes d(1) only if nonnull.',
  'Map allocation follows callback/stream effects; payload is read once before length. data_length, c, l insertions preserve key/value boxing and order.',
  'Telemetry singleton h() is evaluated before reading mMethodName; c(methodName,summary,map,null,null) retains argument order.',
  'All seven branches and both returns accounted for; no try/catch, null guard, default error code, swallowed exception or new network operation introduced.'
 ],limitations:'Compilation uses inert type stubs and establishes syntax only. Manual static comparison is by author and still needs independent semantic approval. No generated class or APK executed.'};
 fs.writeFileSync(path.join(folder,'candidate.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({file,candidateSha256:report.candidate.sha256,syntax:report.syntax.status,instructions:instructions.length}));if(compile.status!==0)throw Error(compile.stderr||'Syntax check failed');
}
if(require.main===module)main();
