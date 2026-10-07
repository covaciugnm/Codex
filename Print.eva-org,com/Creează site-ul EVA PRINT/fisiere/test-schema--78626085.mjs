import {PGlite} from './validation_runtime/package/dist/index.js';
import fs from 'node:fs/promises';
const root='EVA_PRINT_WEBSITE_BRIEF_2026-10-02';
const db=new PGlite();
for(const f of ['schema.sql','002_dynamic_fields.sql']){await db.exec(await fs.readFile(root+'/07_DATABASE/'+f,'utf8'));console.log('Applied '+f);}
await db.close();
