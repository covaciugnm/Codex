import fs from 'node:fs/promises';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const base='D:/CodexWork/a02-historic-r6';
const x=await SpreadsheetFile.importXlsx(await FileBlob.load(base+'/INVENTAR_IDEMPIERE_SAGA_EVA_2026-10-08.xlsx'));
const rows={};for(const s of x.worksheets.items){const name=s.name;console.log(name);if(name.includes('invers')||name.includes('instalabile')||name==='Sinteză')rows[name]=s.getRange(`A1:M${name.includes('invers')?620:name.includes('instalabile')?480:160}`).values;}
await fs.writeFile(base+'/xlsx-values.json',JSON.stringify(rows));
