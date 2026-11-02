'use strict';
const fs=require('node:fs'),zlib=require('node:zlib');
function zipEntries(b){
 let end=b.length-22;while(end>=Math.max(0,b.length-65557)&&b.readUInt32LE(end)!==0x06054b50)end--;
 if(end<0)throw Error('Missing ZIP directory');
 const count=b.readUInt16LE(end+10),offset=b.readUInt32LE(end+16),entries=[];let p=offset;
 for(let i=0;i<count;i++){
  if(b.readUInt32LE(p)!==0x02014b50)throw Error('Invalid ZIP directory');
  const method=b.readUInt16LE(p+10),size=b.readUInt32LE(p+20),uncompressed=b.readUInt32LE(p+24),nl=b.readUInt16LE(p+28),el=b.readUInt16LE(p+30),cl=b.readUInt16LE(p+32),local=b.readUInt32LE(p+42),name=b.toString('utf8',p+46,p+46+nl);
  entries.push({name,size,uncompressed,read(){const start=local+30+b.readUInt16LE(local+26)+b.readUInt16LE(local+28);const data=b.subarray(start,start+size);const out=method===0?data:method===8?zlib.inflateRawSync(data):(()=>{throw Error('Unsupported compression')})();if(out.length!==uncompressed)throw Error('ZIP size mismatch');return out;}});p+=46+nl+el+cl;
 }return entries;
}
function axml(b){let strings=[],result={};
 for(let p=8;p+8<=b.length;){const type=b.readUInt16LE(p),header=b.readUInt16LE(p+2),size=b.readUInt32LE(p+4);if(size<8||p+size>b.length)throw Error('Invalid AXML chunk');
  if(type===1){const n=b.readUInt32LE(p+8),utf8=!!(b.readUInt32LE(p+16)&256),start=p+b.readUInt32LE(p+20);
   strings=Array.from({length:n},(_,i)=>{let q=start+b.readUInt32LE(p+header+i*4);const len8=()=>{let n=b[q++];if(n&128)n=((n&127)<<8)|b[q++];return n;};if(utf8){len8();const n=len8();return b.toString('utf8',q,q+n);}let n=b.readUInt16LE(q);q+=2;if(n&32768){n=((n&32767)<<16)|b.readUInt16LE(q);q+=2;}return b.toString('utf16le',q,q+n*2);});
  }else if(type===0x102){const name=strings[b.readUInt32LE(p+20)];if(name==='manifest'){const start=p+16+b.readUInt16LE(p+24),step=b.readUInt16LE(p+26),n=b.readUInt16LE(p+28);for(let i=0;i<n;i++){const a=start+i*step,key=strings[b.readUInt32LE(a+4)],raw=b.readUInt32LE(a+8),dtype=b[a+15],data=b.readUInt32LE(a+16);if(['package','versionName','versionCode'].includes(key))result[key]=raw!==0xffffffff?strings[raw]:dtype===3?strings[data]:data;}return result;}}
  p+=size;
 }return result;
}
function inspect(file){const b=fs.readFileSync(file),entries=zipEntries(b),meta=entries.find(e=>e.name==='manifest.json');if(meta){const x=JSON.parse(meta.read().toString('utf8'));const apks=entries.filter(e=>e.name.endsWith('.apk'));const details=apks.map(e=>{const sub=zipEntries(e.read());return {file:e.name,...axml(sub.find(x=>x.name==='AndroidManifest.xml').read())};});return {format:'XAPK',manifest:x,apks:details,entries:entries.length};}const m=entries.find(e=>e.name==='AndroidManifest.xml');if(!m)throw Error('Missing AndroidManifest.xml');return {format:'APK',...axml(m.read()),entries:entries.length};}
if(require.main===module)for(const f of process.argv.slice(2))console.log(JSON.stringify({file:f,...inspect(f)}));
module.exports={zipEntries,inspect};
