'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const {normalizeSmali:n}=require('./normalize-smali.cjs');
const base=`.class public Lfixture/A;
.super Ljava/lang/Object;
.source "A.java"
.field public value:I
.method public run(I)V
.registers 3
.line 10
const-string v0, "text # literal"
iget v1, v2, Lfixture/A;->value:I
invoke-static {v1}, Lfixture/Helper;->use(I)V
:try_start_0
packed-switch v1, :switch_data_0
:try_end_0
.catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0
:catch_0
return-void
:case_0
return-void
:switch_data_0
.packed-switch 0x1
:case_0
.end packed-switch
:array_data_0
.array-data 0x1
0x1t
.end array-data
.annotation runtime Lfixture/Anno;
value = "annotation"
.end annotation
.end method
`;
const results=[];function test(name,fn){try{fn();results.push({name,status:'PASS'});}catch(e){results.push({name,status:'FAIL',error:e.message});}}
const same=s=>assert.equal(n(base).classSha256,n(s).classSha256);
const different=s=>assert.notEqual(n(base).classSha256,n(s).classSha256);
test('01 CRLF equivalence',()=>same(base.replace(/\n/g,'\r\n')));
test('02 debug line equivalence',()=>same(base.replace('.line 10','.line 900')));
test('03 local debug equivalence',()=>same(base.replace('.line 10','.local v0, "local":I\n.end local v0\n.restart local v0')));
test('04 full comment equivalence',()=>same('# metadata\n'+base));
test('05 hash inside string preserved',()=>different(base.replace('text # literal','text # changed')));
test('06 string value preserved',()=>different(base.replace('text # literal','other')));
test('07 symbolic field reference preserved',()=>different(base.replace('->value:I','->other:I')));
test('08 symbolic method reference preserved',()=>different(base.replace('->use(I)V','->other(I)V')));
test('09 method prototype preserved',()=>different(base.replace('run(I)V','run(J)V')));
test('10 class field context rejects donor',()=>{const other=base.replace('.field public value:I','.field private value:J');assert.notEqual(n(base).contextSha256,n(other).contextSha256);different(other);});
test('11 catch type preserved',()=>different(base.replace('.catch Ljava/lang/Exception;','.catch Ljava/lang/Throwable;')));
test('12 switch key preserved',()=>different(base.replace('.packed-switch 0x1','.packed-switch 0x2')));
test('13 switch target preserved',()=>different(base.replace('\n:case_0\n.end packed-switch','\n:catch_0\n.end packed-switch')));
test('14 array payload preserved',()=>different(base.replace('0x1t','0x2t')));
test('15 register differences not normalized',()=>different(base.replace('iget v1, v2','iget v0, v2')));
test('16 labels not arbitrarily normalized',()=>different(base.replace(/:case_0/g,':case_1')));
test('17 runtime annotation preserved',()=>different(base.replace('value = "annotation"','value = "other"')));
test('18 unterminated method rejected',()=>assert.throws(()=>n(base.replace('.end method','')),/Unterminated method/));
test('19 duplicate method rejected',()=>assert.throws(()=>n(base+base.slice(base.indexOf('.method '))),/Duplicate method/));
test('20 source filename ignored',()=>same(base.replace('"A.java"','"Other.java"')));
test('21 literal internal spaces preserved',()=>different(base.replace('text # literal','text  # literal')));
test('22 instructions preserved',()=>different(base.replace('return-void','throw v0')));
// Additional fail-closed cases are independent of the 22 required fixtures.
test('23 unknown directive rejected',()=>assert.throws(()=>n(base+'\n.unknown-directive\n'),/Unknown Smali directive/));
test('24 method access flags preserved',()=>different(base.replace('.method public run','.method private run')));
test('25 class descriptor context preserved',()=>different(base.replace('.class public Lfixture/A;','.class public Lfixture/B;')));
test('26 method signature fully qualified',()=>assert.equal(n(base).methods[0].descriptor,'Lfixture/A;->run(I)V'));
test('27 no silent source method discard',()=>assert.equal(n(base).methodCount,1));
test('28 unknown end directive rejected',()=>assert.throws(()=>n(base+'\n.end unknown\n'),/Unknown Smali end directive/));
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const output={schemaVersion:1,date:new Date().toISOString(),implementationSha256:hash(path.join(__dirname,'normalize-smali.cjs')),testSha256:hash(__filename),cases:results.length,passed:results.filter(x=>x.status==='PASS').length,failed:results.filter(x=>x.status==='FAIL').length,results,scope:'Normalizer fixtures only; no proof of Java equivalence and no APK execution'};
fs.writeFileSync(path.join(__dirname,'fixture-results.json'),JSON.stringify(output,null,2)+'\n');console.log(JSON.stringify(output));if(output.failed)process.exitCode=1;
