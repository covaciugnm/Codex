'use strict';
// Packages only new content-addressed objects; no input APKs are copied here.
const fs=require('node:fs'),fsp=fs.promises,path=require('node:path'),crypto=require('node:crypto'),zlib=require('node:zlib');
const {Readable}=require('node:stream'),{pipeline}=require('node:stream/promises');
const option=(name,fallback)=>{const i=process.argv.indexOf(name);return i<0?fallback:path.resolve(process.argv[i+1]||'');};
const root=option('--analysis-root',path.resolve(__dirname,'../apk-analysis-2026-11-01'));
const casDir=option('--cas-dir',path.join(root,'cas')),packDir=option('--pack-dir',path.join(root,'packs'));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
async function fileHash(p){const h=crypto.createHash('sha256');for await(const b of fs.createReadStream(p))h.update(b);return h.digest('hex');}
function header(name,size){const b=Buffer.alloc(512);b.write(name,0,100,'utf8');const oct=(v,p,n)=>b.write(v.toString(8).padStart(n-1,'0')+'\0',p,n,'ascii');oct(420,100,8);oct(0,108,8);oct(0,116,8);oct(size,124,12);oct(0,136,12);b.fill(32,148,156);b[156]=48;b.write('ustar\0',257,6,'ascii');b.write('00',263,2,'ascii');let sum=0;for(const v of b)sum+=v;b.write(sum.toString(8).padStart(6,'0')+'\0 ',148,8,'ascii');return b;}
async function main(){
 await fsp.mkdir(packDir,{recursive:true});const indexPath=path.join(root,'cas-index.json');
 const index=JSON.parse(await fsp.readFile(indexPath,'utf8'));if(!Array.isArray(index.objects))throw Error('Missing objects index');const declared=new Map();
 for(const o of index.objects){if(!/^[a-f0-9]{64}$/.test(o.sha256)||!Number.isSafeInteger(o.bytes)||o.bytes<0||declared.has(o.sha256))throw Error('Invalid/duplicate CAS index entry');declared.set(o.sha256,o.bytes);}
 const files=[...declared.keys()].sort();
 const objects=[];for(const hash of files){const p=path.join(casDir,hash),s=await fsp.stat(p);if(!s.isFile()||s.size!==declared.get(hash)||await fileHash(p)!==hash)throw Error('CAS integrity mismatch '+hash);objects.push({sha256:hash,bytes:s.size});}
 const groups=[];let group=[],size=0;for(const o of objects){if(group.length&&size+o.bytes>256*1024*1024){groups.push(group);group=[];size=0;}group.push(o);size+=o.bytes;}if(group.length)groups.push(group);
 const manifest={schema:1,repository:'covaciugnm/iFLYTEK',releaseTag:'iflytek-apk-analysis-2026-11-01',format:'POSIX ustar gzip; entries cas/<sha256>; deterministic mtime=0',objects:objects.length,objectBytes:objects.reduce((n,o)=>n+o.bytes,0),packs:[]};
 for(let i=0;i<groups.length;i++){
  const list=groups[i],temp=path.join(packDir,'part-'+String(i+1).padStart(4,'0')+'.tar.gz');
  async function* tar(){for(const o of list){yield header('cas/'+o.sha256,o.bytes);for await(const b of fs.createReadStream(path.join(casDir,o.sha256)))yield b;const pad=(512-o.bytes%512)%512;if(pad)yield Buffer.alloc(pad);}yield Buffer.alloc(1024);}
  await pipeline(Readable.from(tar()),zlib.createGzip({level:6}),fs.createWriteStream(temp));const hash=await fileHash(temp),name='cas-'+String(i+1).padStart(4,'0')+'-'+hash.slice(0,16)+'.tar.gz',dest=path.join(packDir,name);
  if(fs.existsSync(dest)){if(await fileHash(dest)!==hash)throw Error('Existing pack differs');await fsp.unlink(temp);}else await fsp.rename(temp,dest);
  manifest.packs.push({name,bytes:(await fsp.stat(dest)).size,sha256:hash,objects:list,downloadUrl:'https://github.com/'+manifest.repository+'/releases/download/'+manifest.releaseTag+'/'+name});console.log('Packed',i+1,groups.length,name);
 }
 await fsp.writeFile(path.join(root,'release-packs.json'),JSON.stringify(manifest,null,2)+'\n');console.log('Objects',manifest.objects,'bytes',manifest.objectBytes);
}
if(require.main===module)main().catch(e=>{console.error(e);process.exitCode=1;});
module.exports={fileHash,header,sha};
