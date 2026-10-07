import {readFile,writeFile,appendFile} from 'node:fs/promises';
import path from 'node:path';
const root=path.resolve(import.meta.dirname,'..'),now=new Date().toISOString();
const statusFile=path.join(root,'docs/STATUS.json');const status=JSON.parse(await readFile(statusFile,'utf8'));
status.recorded_at=now;status.phase='website_redesign';status.status='completed_local_preview';status.deployment.migrations=['001','002','003','004','005'];
status.redesign={brand:'EVA-3dScan',campaign_images:5,locales:7,keys_per_locale:190,tests:{backend:4,browser:117,redesign:42,live_variable:1},audit:'accepted_scoped',report:'REDESIGN_LIVRAT.md',existing_auth_projects:'preserved'};
await writeFile(statusFile,JSON.stringify(status,null,2));
const events=[
 {task:'BRAND-01',owner:'manager',result:'App icon SVG+1024/180/32PNG; separate animated symbol and full logo; copied to Aplicație identity folder'},
 {task:'BRAND-02',owner:'campaign_assets',result:'5 built-in image generations, 5 saved PNG originals and5 WebP; prompts and provenance saved'},
 {task:'BRAND-03',owner:'site_translations',result:'51 new campaign keys in7locales;190keys each; copy simplified after visual review'},
 {task:'BRAND-04',owner:'manager',result:'Clear homepage3modules/input-process-output/audience; accessible5framecarousel; existing auth/projectintegration restored and preserved after stale copy detected; localtransfer repaired withverifiedSHA256'},
 {task:'BRAND-05',owner:'auditor_final',result:'6findings closed including localtransfer integrity; scope documented; noopenfindings'},
 {task:'BRAND-06',owner:'manager',result:'4backend,117browser,42campaign,1livevariable checks passed;5originals+identityfiles persisted; updateappliedtoDocker'}
 ];
for(const event of events)await appendFile(path.join(root,'docs/manager-events.jsonl'),JSON.stringify({recorded_at:now,event:'redesign_completed',timing:'retrospective_summary_current_turn',...event})+'\n');
const readme=path.join(root,'README.md');let text=await readFile(readme,'utf8');text=text.replace('cont de citire pentru runtime','citire pentru conținutul public și permisiuni dedicate funcțiilor de cont/proiect existente');if(!text.includes('## Identitate și redesign'))text+='\n## Identitate și redesign\n\nMarca curentă este **EVA-3dScan**. Prima pagină explică trei module și include cinci imagini de campanie într-un carusel, cu siglă animată. Ghid: `docs/IDENTITATE_EVA-3dScan.md`. Livrare și verificări: `docs/REDESIGN_LIVRAT.md`. Audit: `docs/AUDIT_REDESIGN.md`. Iconița pentru aplicație are copie în `../Aplicație/Identitate EVA-3dScan`.\n';await writeFile(readme,text);
console.log('Redesign status and logs saved');
