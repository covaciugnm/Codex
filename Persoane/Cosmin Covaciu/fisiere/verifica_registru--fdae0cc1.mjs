import fs from 'node:fs/promises';
import {createRequire} from 'node:module';
const req=createRequire('C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/package.json');
const {FileBlob,SpreadsheetFile}=await import(req.resolve('@oai/artifact-tool'));
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(process.argv[2]));
console.log((await wb.inspect({kind:'region',sheetId:'Persoane',range:'A26:H26',maxChars:2200})).ndjson);
console.log(wb.help('workbook.render',{include:'index,examples,notes',maxChars:2600}).ndjson);
const preview=await wb.render({sheetName:'Persoane',range:'A24:H27',scale:1,format:'png'});
await fs.writeFile(process.argv[3],new Uint8Array(await preview.arrayBuffer()));
