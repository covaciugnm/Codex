'use strict';
// Restores historical source/plan bytes after an acknowledged premature draft overwrite.
// Every reconstructed byte sequence must match a SHA recorded before the overwrite.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const repo=path.resolve(__dirname,'..'),meta=path.join(repo,'decompilation-repair-2026-11-01/jadx-null-const'),work='D:/Codex-iflytek-decompilation-repair-20261101/jadx-null-const',hash=b=>crypto.createHash('sha256').update(b).digest('hex');
function main(){
 const previousFile=path.join(meta,'V1-PRESERVATION.json');if(fs.existsSync(previousFile)){const prior=JSON.parse(fs.readFileSync(previousFile));for(const r of Object.values(prior.restored))if(hash(fs.readFileSync(r.file))!==r.sha256)throw Error('Previously preserved historical bytes changed');console.log(JSON.stringify({status:prior.status,verifiedExistingArchive:true}));return;}
 const currentFile=path.join(repo,'tools/jadx-null-const-experiment-20261101.cjs'),current=fs.readFileSync(currentFile,'utf8'),ssa=`    if (result) {
      RegisterArg assignment = InsnArg.reg(0, current);
      SSAVar variable = new SSAVar(0, 0, assignment);
      variable.setType(current);
      if (!assignment.getType().equals(current)) throw new IllegalStateException("Fixture SSA type setup failed");
      insn.setResult(assignment);
    }`;
 if(current.split(ssa).length!==2)throw Error('Expected exactly the acknowledged v2 edit');
 const historical=current.replace('import jadx.core.dex.instructions.args.RegisterArg;\n','').replace('import jadx.core.dex.instructions.args.SSAVar;\n','').replace(ssa,'    if (result) insn.setResult(InsnArg.reg(0, current));').replace("path.join(work,'preflight-v2')","path.join(work,'preflight-v1')"),expectedRunner='653da2b1f0a6a75b0f1725d03da792345730a769c479dcb7d24eb693c0e4ec4a';
 if(hash(historical)!==expectedRunner)throw Error('Historical runner reconstruction does not match its independently recorded SHA');
 const literal=/const fixture=(`[^]*?`);/.exec(historical)?.[1];if(!literal||literal.includes('${'))throw Error('Expected own static fixture literal');const historicalFixture=Function('return '+literal)(),expectedFixture='fbba38fc8953b9a8551c187e1ebabd9407ee7cf5695b3e4766fe1c3f7c79799c';if(hash(historicalFixture)!==expectedFixture||Buffer.byteLength(historicalFixture)!==2610)throw Error('Historical fixture hash mismatch');
 const draftFile=path.join(meta,'PREFLIGHT-PLAN.json'),draftBytes=fs.readFileSync(draftFile),draft=JSON.parse(draftBytes),old=JSON.parse(JSON.stringify(draft).replaceAll('preflight-v2','preflight-v1'));old.upstream.retrievedAt='2026-11-01T17:16:56.683Z';old.sources.fixture.sha256=expectedFixture;old.sources.fixture.bytes=2610;const oldBytes=Buffer.from(JSON.stringify(old,null,2)+'\n'),expectedPlan='336d266a1c4883f2f9fb35872ad47cedcd87f554d28c58df98598bbf68133342';if(hash(oldBytes)!==expectedPlan)throw Error('Historical plan reconstruction does not match exact pre-existing audit SHA');
 const archive=path.join(work,'provenance/v1');fs.mkdirSync(archive,{recursive:true});const writeExact=(file,b)=>{if(fs.existsSync(file)){if(!fs.readFileSync(file).equals(Buffer.from(b)))throw Error('Existing archive differs');}else fs.writeFileSync(file,b);};
 writeExact(path.join(archive,'runner.cjs'),historical);writeExact(path.join(archive,'NullConstGuardFixture.java'),historicalFixture);writeExact(path.join(archive,'PREFLIGHT-PLAN.json'),oldBytes);writeExact(path.join(archive,'superseded-unexecuted-v2-draft-plan.json'),draftBytes);
 const fixturePath=old.sources.fixture.file,newFixtureBytes=fs.readFileSync(fixturePath),newFixturePath=path.join(work,'source/fixture-v2/jadx/core/dex/visitors/typeinference/NullConstGuardFixture.java');fs.mkdirSync(path.dirname(newFixturePath),{recursive:true});writeExact(newFixturePath,newFixtureBytes);fs.writeFileSync(fixturePath,historicalFixture);fs.writeFileSync(draftFile,oldBytes);
 const report={schemaVersion:1,status:'EXACT-HISTORICAL-BYTES-RESTORED-BY-RECORDED-SHA',cause:'v2 draft preparation prematurely overwrote the shared v1 plan and fixture-source path; execution logs/classfiles/results stayed intact',restored:{plan:{file:draftFile,sha256:expectedPlan},fixture:{file:fixturePath,sha256:expectedFixture,bytes:2610},runnerArchive:{file:path.join(archive,'runner.cjs'),sha256:expectedRunner}},evidence:'Expected runner/plan SHA and fixture SHA/bytes were recorded by the independent auditor before overwrite. The original upstream retrievedAt value was recovered from the auditor previous complete read. No timestamp was invented.',v2SourceSeparated:{file:newFixturePath,sha256:hash(newFixtureBytes),bytes:newFixtureBytes.length},executionArtifactsModified:false};fs.writeFileSync(path.join(meta,'V1-PRESERVATION.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
}
if(require.main===module)main();
