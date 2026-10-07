import {readdir,readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import path from 'node:path';
const root=path.resolve(import.meta.dirname,'..');
const target='docs/FILES.sha256.json';
const hash=buffer=>createHash('sha256').update(buffer).digest('hex');
if(process.argv.includes('--check')){
 const manifest=JSON.parse(await readFile(path.join(root,target),'utf8'));const failures=[];
 for(const file of manifest.files){try{if(hash(await readFile(path.join(root,file.path)))!==file.sha256)failures.push(file.path);}catch{failures.push(file.path);}}
 console.log(JSON.stringify({checked:manifest.files.length,failures}));if(failures.length)process.exitCode=1;
}else{
 const files=[];
 async function walk(relative=''){for(const item of await readdir(path.join(root,relative),{withFileTypes:true})){if(['node_modules','.git','backups'].includes(item.name)||item.name==='.env'||(item.name.startsWith('.env.')&&item.name!=='.env.example'))continue;const rel=path.posix.join(relative,item.name);if(item.isDirectory())await walk(rel);else if(item.isFile()&&rel!==target){const body=await readFile(path.join(root,rel));files.push({path:rel,bytes:body.length,sha256:hash(body)});}}}
 await walk();files.sort((a,b)=>a.path.localeCompare(b.path));await writeFile(path.join(root,target),JSON.stringify({created:new Date().toISOString(),scope:'Delivery snapshot; secrets, node_modules, backups and this manifest excluded. Regenerate after intentional changes.',files},null,2));console.log(JSON.stringify({files:files.length}));
}
