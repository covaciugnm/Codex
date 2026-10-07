const fs=require('fs'),p=require('path'),crypto=require('crypto'),{Readable}=require('stream'),{pipeline}=require('stream/promises');
const root='\\\\192.168.100.169\\Comun\\00.Roboti\\EVA.Pro\\Learn\\EVA_LEARN_DB_35';
const name=process.argv[2]||'dictionary',plan=p.join(root,'00_Administrare','downloads_'+name+'.json'),jobs=JSON.parse(fs.readFileSync(plan,'utf8'));
const log=p.join(root,'00_Administrare','download_'+name+'.log');
let cursor=0,done=jobs.filter(j=>j.status==='downloaded').length,errors=0,bytes=0;
function save(){fs.writeFileSync(plan,JSON.stringify(jobs,null,2),'utf8');}
function message(t){const line=new Date().toISOString()+' '+t;console.log(line);fs.appendFileSync(log,line+'\n');}
async function one(j){
 if(j.status==='downloaded'&&fs.existsSync(p.join(root,j.path)))return;
 const dest=p.join(root,j.path);fs.mkdirSync(p.dirname(dest),{recursive:true});j.status='downloading';
 for(let attempt=0;attempt<2;attempt++){
 try{
  const r=await fetch(j.url,{headers:{'User-Agent':'EVA-Learn-offline-collection/1.0','Accept-Encoding':'identity'},signal:AbortSignal.timeout(name==='models'?1800000:300000)});
  if(!r.ok)throw Error('HTTP '+r.status);
  const type=r.headers.get('content-type')||'';
  if(type.includes('text/html'))throw Error('Server returned HTML instead of file');
  const declared=Number(r.headers.get('content-length')||0),hash=crypto.createHash('sha256');let count=0,first=Buffer.alloc(0);
  const destStream=fs.createWriteStream(dest+'.part');
  const source=Readable.fromWeb(r.body);
  source.on('data',chunk=>{if(first.length<32)first=Buffer.concat([first,chunk.subarray(0,32-first.length)]);hash.update(chunk);count+=chunk.length;});
  await pipeline(source,destStream);
  if(declared&&count!==declared)throw Error('Incomplete file '+count+'/'+declared);
  if(!count)throw Error('Empty file');
  if(/\.zip$/i.test(dest)&&first.subarray(0,2).toString()!=='PK')throw Error('Wrong ZIP signature');
  if(/\.pdf$/i.test(dest)&&!first.toString('latin1').startsWith('%PDF'))throw Error('Wrong PDF signature');
  if(/\.gz$/i.test(dest)&&!(first[0]===31&&first[1]===139))throw Error('Wrong GZIP signature');
  if(/\.bz2$/i.test(dest)&&first.subarray(0,3).toString()!=='BZh')throw Error('Wrong BZIP2 signature');
  if(/\.xz$/i.test(dest)&&first.subarray(0,6).toString('hex')!=='fd377a585a00')throw Error('Wrong XZ signature');
  j.sha256=hash.digest('hex');if(j.expectedSha256&&j.sha256!==j.expectedSha256)throw Error('SHA256 mismatch');
  fs.renameSync(dest+'.part',dest);j.status='downloaded';j.bytes=count;j.contentType=type;j.completedAt=new Date().toISOString();j.error='';done++;bytes+=count;
  if(done%10===0||name==='models')message('Completed '+done+'/'+jobs.length+'; '+(bytes/1e9).toFixed(2)+' GB; '+p.basename(dest));
  return;
 }catch(e){j.error=String(e.message||e);if(/HTTP (401|403|404|429)|HTML|Wrong.*signature/.test(j.error))break;}
 }
 j.status='failed';errors++;if(errors%10===0)message('Unavailable '+errors+'; latest '+j.error);
}
async function work(){while(cursor<jobs.length){const j=jobs[cursor++];await one(j);if((done+errors)%10===0)save();}}
(async()=>{message('Starting '+jobs.length+' jobs');const timer=setInterval(save,15000);try{await Promise.all(Array.from({length:name==='models'?4:6},work));}finally{clearInterval(timer);save();}message('FINISHED downloaded='+jobs.filter(j=>j.status==='downloaded').length+' failed='+jobs.filter(j=>j.status==='failed').length);})();
