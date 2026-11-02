'use strict';
const fs=require('node:fs'),fsp=fs.promises,path=require('node:path'),zlib=require('node:zlib'),{spawnSync}=require('node:child_process');
const {fileHash}=require('./package-apk-analysis-20261101.cjs');
const root=path.resolve(__dirname,'../apk-analysis-2026-11-01');
const opt=process.argv.indexOf('--store-dir'),storeRoot=opt<0?root:path.resolve(process.argv[opt+1]||'');
async function unpack(p,pack,targetRoot=root){
 const expected=new Map(pack.objects.map(o=>[o.sha256,o]));let buffer=Buffer.alloc(0),entry=null,count=0,fd=null,target=null,remaining=0,pad=0,zeroBlocks=0;
 try{for await(const chunk of fs.createReadStream(p).pipe(zlib.createGunzip())){
  buffer=buffer.length?Buffer.concat([buffer,chunk]):chunk;
  while(true){
   if(pad){const n=Math.min(pad,buffer.length);buffer=buffer.subarray(n);pad-=n;if(pad||!buffer.length)break;}
   if(!entry){if(buffer.length<512)break;const h=buffer.subarray(0,512);buffer=buffer.subarray(512);if(h.every(v=>v===0)){zeroBlocks++;continue;}if(zeroBlocks)throw Error('Nonzero data after TAR footer');
    const check=parseInt(h.subarray(148,156).toString().replace(/\0/g,'').trim(),8);let sum=0;for(let j=0;j<512;j++)sum+=j>=148&&j<156?32:h[j];if(check!==sum)throw Error('TAR header checksum mismatch');
    const name=h.subarray(0,100).toString().split('\0')[0],size=parseInt(h.subarray(124,136).toString().replace(/\0/g,'').trim(),8);
    if(!/^cas\/[a-f0-9]{64}$/.test(name)||h[156]!==48)throw Error('Unexpected archive entry');const hash=name.slice(4);entry=expected.get(hash);if(!entry||entry.bytes!==size)throw Error('Unlisted archive object');remaining=size;pad=(512-size%512)%512;
    // Padding is consumed after the object, not before its body.
    entry={...entry,padding:pad};pad=0;target=path.join(targetRoot,name);await fsp.mkdir(path.dirname(target),{recursive:true});fd=await fsp.open(target+'.partial','w');
   }
   const n=Math.min(remaining,buffer.length);if(n){await fd.writeFile(buffer.subarray(0,n));buffer=buffer.subarray(n);remaining-=n;}
   if(remaining)break;
   await fd.close();fd=null;if(await fileHash(target+'.partial')!==entry.sha256)throw Error('Restored object hash mismatch');
   if(fs.existsSync(target)){if(await fileHash(target)!==entry.sha256)throw Error('Existing object differs '+target);await fsp.unlink(target+'.partial');}else await fsp.rename(target+'.partial',target);
   expected.delete(entry.sha256);pad=entry.padding;entry=null;count++;
  }
 }}finally{if(fd)await fd.close();}
 if(entry||expected.size||pad||buffer.length||zeroBlocks<2)throw Error('Incomplete archive '+pack.name);return count;
}
async function main(){
 const manifest=JSON.parse(await fsp.readFile(path.join(root,'release-packs.json'),'utf8'));let count=0;
 for(const pack of manifest.packs){
  let all=true;for(const o of pack.objects){const p=path.join(storeRoot,'cas',o.sha256);if(!fs.existsSync(p)||(await fsp.stat(p)).size!==o.bytes||await fileHash(p)!==o.sha256){all=false;break;}}
  if(all){count+=pack.objects.length;continue;}
  const folder=path.join(storeRoot,'packs'),p=path.join(folder,pack.name);await fsp.mkdir(folder,{recursive:true});
  if(!fs.existsSync(p)){
   if(process.argv.includes('--local-only'))throw Error('Missing pack '+pack.name);
   const r=spawnSync('gh',['release','download',manifest.releaseTag,'--repo',manifest.repository,'--pattern',pack.name,'--dir',folder],{stdio:'inherit',windowsHide:true});if(r.status!==0)throw Error('Download failed');
  }
  if((await fsp.stat(p)).size!==pack.bytes||await fileHash(p)!==pack.sha256)throw Error('Pack integrity mismatch '+pack.name);
  count+=await unpack(p,pack,storeRoot);console.log('Restored',pack.name);
 }
 console.log('Verified/restored',count,'CAS objects. Use the per-version materialization tool to reconstruct logical directories.');
}
if(require.main===module)main().catch(e=>{console.error(e);process.exitCode=1;});
module.exports={unpack};
