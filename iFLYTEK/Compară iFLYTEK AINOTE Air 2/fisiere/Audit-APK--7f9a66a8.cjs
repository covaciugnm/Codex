'use strict';
// Checks the complete ZIP payload independently of Apktool and apksigner.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const zlib = require('node:zlib');
const sha = b => crypto.createHash('sha256').update(b).digest('hex');
function apk(file) {
  const b = fs.readFileSync(file);
  let end = -1;
  for (let i = b.length - 22; i >= Math.max(0, b.length - 65557); i--) {
    if (b.readUInt32LE(i) === 0x06054b50 && i + 22 + b.readUInt16LE(i + 20) === b.length) { end = i; break; }
  }
  if (end < 0) throw Error('Missing ZIP end record: ' + file);
  const count = b.readUInt16LE(end + 10);
  if (count === 65535 || b.readUInt32LE(end + 16) === 0xffffffff) throw Error('ZIP64 is not supported by this verifier');
  let at = b.readUInt32LE(end + 16);
  const entries = new Map();
  for (let i = 0; i < count; i++) {
    if (b.readUInt32LE(at) !== 0x02014b50) throw Error('Invalid central directory');
    const method = b.readUInt16LE(at + 10), size = b.readUInt32LE(at + 24), packed = b.readUInt32LE(at + 20);
    const n = b.readUInt16LE(at + 28), x = b.readUInt16LE(at + 30), c = b.readUInt16LE(at + 32);
    const name = b.toString('utf8', at + 46, at + 46 + n), local = b.readUInt32LE(at + 42);
    at += 46 + n + x + c;
    if (name.endsWith('/')) continue;
    if (entries.has(name)) throw Error('Duplicate ZIP entry: ' + name);
    if (b.readUInt32LE(local) !== 0x04034b50) throw Error('Invalid local header: ' + name);
    const start = local + 30 + b.readUInt16LE(local + 26) + b.readUInt16LE(local + 28);
    const data = b.subarray(start, start + packed);
    const raw = method === 0 ? data : method === 8 ? zlib.inflateRawSync(data) : null;
    if (!raw || raw.length !== size) throw Error('Invalid compressed payload: ' + name);
    const entry = {name, bytes: size, sha256: sha(raw), method};
    if (/^classes(?:\d+)?\.dex$/.test(name)) {
      if (raw.subarray(0,4).toString() !== 'dex\n') throw Error('Invalid DEX header');
      entry.classes = raw.readUInt32LE(96);
      entry.methodReferences = raw.readUInt32LE(88);
      entry.fieldReferences = raw.readUInt32LE(80);
    }
    entries.set(name, entry);
  }
  return {file: path.resolve(file), bytes:b.length, sha256:sha(b), entries};
}
const [originalPath, rebuiltPath, outputPath] = process.argv.slice(2);
if (!originalPath || !rebuiltPath || !outputPath) throw Error('Usage: node Audit-APK.cjs original.apk rebuilt.apk report.json');
const original = apk(originalPath), rebuilt = apk(rebuiltPath);
const differences = [], additions = [], failures = [], relocatedCompiledResources = [];
const signature = n => /^META-INF\/(?:MANIFEST\.MF|[^/]+\.(?:SF|RSA|DSA|EC))$/i.test(n);
const compiled = n => n === 'AndroidManifest.xml' || n === 'resources.arsc' || n.startsWith('res/');
let native = 0, assets = 0, identical = 0;
for (const [name, entry] of original.entries) {
  const other = rebuilt.entries.get(name);
  if (signature(name)) continue;
  if (!other) {
    // AAPT2 expands obfuscated res/ filenames. Resource equivalence must be
    // checked by decoding both APKs, not by equating archive paths.
    if (name.startsWith('res/')) relocatedCompiledResources.push(name);
    else failures.push('Missing entry: ' + name);
    continue;
  }
  if (entry.sha256 !== other.sha256) {
    differences.push({name, original:entry.sha256, rebuilt:other.sha256});
    if (!compiled(name) && !/^classes(?:\d+)?\.dex$/.test(name)) failures.push('Changed preserved payload: ' + name);
  } else {
    identical++;
    if (name.startsWith('lib/') && name.endsWith('.so')) native++;
    if (name.startsWith('assets/')) assets++;
  }
  if (entry.classes !== undefined && entry.classes !== other.classes) failures.push('DEX class count changed: ' + name);
  if (entry.classes !== undefined && entry.methodReferences !== other.methodReferences) failures.push('DEX method references changed: ' + name);
  if (entry.classes !== undefined && entry.fieldReferences !== other.fieldReferences) failures.push('DEX field references changed: ' + name);
}
for (const name of rebuilt.entries.keys()) {
  if (!original.entries.has(name) && !signature(name)) additions.push(name);
}
const dex = a => [...a.entries.values()].filter(e => e.classes !== undefined);
const summary = a => ({file:a.file,bytes:a.bytes,sha256:a.sha256,entries:a.entries.size,dex:dex(a)});
const result = {schemaVersion:1, original:summary(original),rebuilt:summary(rebuilt),
  identicalEntries:identical, identicalNativeLibraries:native, identicalAssets:assets,
  changedEntries:differences, addedEntries:additions,relocatedCompiledResources,failures,
  nativeAbis:[...new Set([...original.entries.keys()].filter(n=>n.startsWith('lib/')).map(n=>n.split('/')[1]))],
  status:failures.length?'FAIL':'PASS',
  scope:'Preserved binary payload, ZIP structure and DEX class counts. Compiled Android resources require the separate decoded-resource check.',
  limitation:'This does not test device behavior. A PASS here alone does not validate the rebuilt application.'};
fs.mkdirSync(path.dirname(outputPath), {recursive:true});
fs.writeFileSync(outputPath, JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({status:result.status,identicalEntries:identical,nativeLibraries:native,assets,
  dexFiles:result.rebuilt.dex.length,classes:result.rebuilt.dex.reduce((s,d)=>s+d.classes,0),
  changedEntries:differences.length,addedEntries:additions.length,relocatedCompiledResources:relocatedCompiledResources.length,
  nativeAbis:result.nativeAbis,failureCount:failures.length,failureExamples:failures.slice(0,8)},null,2));
if (failures.length) process.exitCode=1;
