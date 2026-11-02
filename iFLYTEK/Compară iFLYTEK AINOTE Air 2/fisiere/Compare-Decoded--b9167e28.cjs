'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {normalizeSmali,normalizeAttrs}=require('./normalization.cjs');
const [originalDir, rebuiltDir, reportPath]=process.argv.slice(2);
if(!reportPath) throw Error('Usage: node Compare-Decoded.cjs original-decoded rebuilt-decoded report.json');
function inventory(root) {
  const map=new Map();
  function walk(dir, prefix='') {
    for(const entry of fs.readdirSync(dir,{withFileTypes:true})) {
      const rel=prefix+entry.name, full=path.join(dir,entry.name);
      if(entry.isSymbolicLink()) throw Error('Unexpected symbolic link: '+full);
      if(entry.isDirectory()) walk(full,rel+'/');
      else if(entry.isFile()) map.set(rel,crypto.createHash('sha256').update(fs.readFileSync(full)).digest('hex'));
    }
  }
  for(const entry of fs.readdirSync(root,{withFileTypes:true})) {
    if(entry.isDirectory() && (/^smali(?:_classes\d+)?$/.test(entry.name) || entry.name==='res')) walk(path.join(root,entry.name),entry.name+'/');
    if(entry.name==='AndroidManifest.xml') map.set(entry.name,crypto.createHash('sha256').update(fs.readFileSync(path.join(root,entry.name))).digest('hex'));
  }
  return map;
}
const original=inventory(originalDir), rebuilt=inventory(rebuiltDir);
const changed=[],missing=[],added=[],equivalent=[];
let smali=0,resources=0;
for(const [name,digest] of original) {
  if(!rebuilt.has(name)) missing.push(name);
  else if(rebuilt.get(name)!==digest) changed.push(name);
  else if(name.endsWith('.smali')) smali++;
  else resources++;
}
for(const name of rebuilt.keys()) if(!original.has(name)) added.push(name);
for(const name of changed) {
  const a=fs.readFileSync(path.join(originalDir,name),'utf8');
  const b=fs.readFileSync(path.join(rebuiltDir,name),'utf8');
  if(name.endsWith('.smali') && normalizeSmali(a)===normalizeSmali(b)) equivalent.push({name,reason:'Default static initial values and/or merging adjacent identical exception ranges; instruction text and per-instruction handler coverage verified'});
  else if(name==='res/values/attrs.xml' && normalizeAttrs(a)===normalizeAttrs(b)) equivalent.push({name,reason:'Order of enum/flag declarations only'});
}
const known=new Set(equivalent.map(e=>e.name));
const unresolved=[...missing,...changed.filter(n=>!known.has(n)),...added];
const codeChanges=unresolved.filter(n=>n.endsWith('.smali'));
const resourceChanges=unresolved.filter(n=>!n.endsWith('.smali'));
const report={schemaVersion:1,originalDir:path.resolve(originalDir),rebuiltDir:path.resolve(rebuiltDir),
  identicalSmaliFiles:smali,identicalResourceFiles:resources,changed,missing,added,equivalent,unresolved,
  codeStatus:codeChanges.length?'FAIL':'PASS',resourceStatus:resourceChanges.length?'FAIL':'PASS',
  status:unresolved.length?'FAIL':'PASS',allFilesIdentical:!changed.length&&!missing.length&&!added.length,
  limitation:'Canonical disassembly equality checks instructions, declarations and debug metadata; it is not a device runtime test.'};
fs.mkdirSync(path.dirname(reportPath),{recursive:true});
fs.writeFileSync(reportPath,JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({codeStatus:report.codeStatus,identicalSmaliFiles:smali,identicalResourceFiles:resources,
  resourceStatus:report.resourceStatus,equivalent:equivalent.length,unresolved:unresolved.length,
  changed:changed.length,missing:missing.length,added:added.length,examples:unresolved.slice(0,8)},null,2));
if(unresolved.length) process.exitCode=1;
