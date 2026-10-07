const fs=require('fs'),p=require('path'),crypto=require('crypto');
const root='\\\\192.168.100.169\\Comun\\00.Roboti\\EVA.Pro\\Learn\\EVA_LEARN_DB_35',name=process.argv[2]||'dictionary';
const cache=p.join(__dirname,'eva_download_cache',name);fs.mkdirSync(cache,{recursive:true});
const plan=p.join(root,'00_Administrare','downloads_'+name+'.json'),jobs=JSON.parse(fs.readFileSync(plan,'utf8'));
let cursor=0,done=jobs.filter(j=>j.status==='downloaded').length,failed=0;
function save(){fs.writeFileSync(plan,JSON.stringify(jobs,null,2),'utf8');}
function log(s){console.log(new Date().toISOString()+' '+s);}
async function one(j){
 if(j.status==='downloaded'&&fs.existsSync(p.join(root,j.path)))return;
 if(j.status==='failed'&&/HTTP (401|403|404)/.test(j.error||'')){failed++;return;}
 const dest=p.join(root,j.path),part=p.join(cache,j.id+'.part');
 fs.mkdirSync(p.dirname(dest),{recursive:true});
 if(!fs.existsSync(part)&&fs.existsSync(dest+'.part'))fs.copyFileSync(dest+'.part',part);
 j.status='downloading';let total=j.totalBytes||0,retries=0,offset=fs.existsSync(part)?fs.statSync(part).size:0;
 try{
  while(!total||offset<total){
   const requestedEnd=offset+16*1024*1024-1;
   try{
    const response=await fetch(j.url,{headers:{'User-Agent':'EVA-Learn-offline-collection/1.0','Accept-Encoding':'identity','Range':'bytes='+offset+'-'+requestedEnd},signal:AbortSignal.timeout(180000)});
    if(!response.ok)throw Error('HTTP '+response.status);
    const type=response.headers.get('content-type')||'';
    if(type.includes('text/html'))throw Error('HTML instead of a file');
    const cr=response.headers.get('content-range');
    if(response.status===206){
      const m=cr?.match(/^bytes (\d+)-(\d+)\/(\d+)$/);
      if(!m||Number(m[1])!==offset)throw Error('Incorrect Content-Range: '+cr);
      total=Number(m[3]);j.totalBytes=total;
      const b=Buffer.from(await response.arrayBuffer());
      if(b.length!==Number(m[2])-Number(m[1])+1)throw Error('Incomplete range');
      fs.appendFileSync(part,b);offset+=b.length;
    }else{
      if(offset){await response.body.cancel();fs.writeFileSync(part,Buffer.alloc(0));offset=0;throw Error('Server ignores range; restart full file');}
      const declared=Number(response.headers.get('content-length')||0);
      const b=Buffer.from(await response.arrayBuffer());
      if(declared&&declared!==b.length)throw Error('Incomplete file');
      fs.writeFileSync(part,b);offset=b.length;total=b.length;j.totalBytes=total;
    }
    if(!offset)throw Error('Empty file');
    j.receivedBytes=offset;j.contentType=type;retries=0;
   }catch(e){
    j.error=e.message;
    if(/HTTP (401|403|404|429)|HTML/.test(j.error))throw e;
    if(++retries>5)throw e;
    await new Promise(r=>setTimeout(r,1500*retries));
   }
  }
  const fd=fs.openSync(part,'r'),first=Buffer.alloc(32);fs.readSync(fd,first,0,32,0);fs.closeSync(fd);
  if(/\.zip$/i.test(dest)&&first.subarray(0,2).toString()!=='PK')throw Error('Wrong ZIP signature');
  if(/\.pdf$/i.test(dest)&&!first.toString('latin1').startsWith('%PDF'))throw Error('Wrong PDF signature');
  if(/\.gz$/i.test(dest)&&!(first[0]===31&&first[1]===139))throw Error('Wrong GZIP signature');
  if(/\.bz2$/i.test(dest)&&first.subarray(0,3).toString()!=='BZh')throw Error('Wrong BZIP2 signature');
  if(/\.xz$/i.test(dest)&&first.subarray(0,6).toString('hex')!=='fd377a585a00')throw Error('Wrong XZ signature');
  if(/\.safetensors$/i.test(dest)){const n=first.readBigUInt64LE(0);if(n<2n||n>100000000n||first[8]!==123)throw Error('Wrong SafeTensors header');}
  const sha=crypto.createHash('sha256'),md5=crypto.createHash('md5');
  for await(const b of fs.createReadStream(part)){sha.update(b);md5.update(b);}
  j.sha256=sha.digest('hex');j.md5=md5.digest('hex');
  if(j.expectedSha256&&j.sha256!==j.expectedSha256)throw Error('SHA256 mismatch');
  if(j.expectedMd5&&j.md5!==j.expectedMd5)throw Error('MD5 mismatch');
  fs.copyFileSync(part,dest);
  if(fs.statSync(dest).size!==total)throw Error('Copy size mismatch');
  fs.unlinkSync(part);
  if(fs.existsSync(dest+'.part'))fs.unlinkSync(dest+'.part');
  j.status='downloaded';j.bytes=total;j.error='';j.completedAt=new Date().toISOString();done++;
  if(done%10===0||name==='models')log('Completed '+done+'/'+jobs.length+' '+p.basename(dest)+' '+(total/1e6).toFixed(1)+' MB');
 }catch(e){j.status='failed';j.error=e.message;j.receivedBytes=fs.existsSync(part)?fs.statSync(part).size:0;failed++;if(failed%10===0||name==='models')log('Unavailable '+j.id+' '+j.error);}
}
async function work(){while(cursor<jobs.length){await one(jobs[cursor++]);if((done+failed)%10===0)save();}}
(async()=>{log('START resumable '+name+' '+jobs.length);const timer=setInterval(save,20000);try{await Promise.all(Array.from({length:name==='models'?6:10},work));}finally{clearInterval(timer);save();}log('FINISHED downloaded='+jobs.filter(j=>j.status==='downloaded').length+' failed='+jobs.filter(j=>j.status==='failed').length);})();
