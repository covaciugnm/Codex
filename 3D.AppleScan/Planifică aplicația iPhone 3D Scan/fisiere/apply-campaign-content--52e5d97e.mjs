import {withPool,transaction,readSeeds,fail} from './shared.mjs';
import {setVariable} from './set-variable.mjs';
try {
 const seeds=await readSeeds();
 await withPool(db=>transaction(db,async client=>{
  let changed=0;
  for(const [locale,messages] of Object.entries(seeds))for(const [key,value] of Object.entries(messages)){
   if(!key.startsWith('campaign.')&&!['hero.title','hero.description','hero.eyebrow','footer.copyright'].includes(key))continue;
   const result=await client.query(`INSERT INTO content_messages(locale,key,value) VALUES($1,$2,$3)
    ON CONFLICT(locale,key) DO UPDATE SET value=excluded.value,updated_at=now()
    WHERE content_messages.value IS DISTINCT FROM excluded.value`,[locale,key,value]);changed+=result.rowCount;
  }
  const brand=await setVariable(client,'product','EVA-3dScan');
  console.log(JSON.stringify({event:'campaign_content_applied',changed,brandChanged:brand.changed,scope:'campaign.*, three hero keys and footer brand only; other editorial values preserved'}));
 }));
}catch(error){fail(error);}
