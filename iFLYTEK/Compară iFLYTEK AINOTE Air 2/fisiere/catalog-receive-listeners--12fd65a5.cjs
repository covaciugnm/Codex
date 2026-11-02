// Manually traced receive -> listener -> Flutter producer chains, APK 1.0.3899.
module.exports=function({allFunctions,get,evidence,addParam,link,typeClass}){
 const plugin='com/example/recorde_translate_plugin/b.java',bridge='com/alipay/verifyiotidentity/obfuscated/i04.java';
 const d=get(plugin),b=get(bridge),reviews=[];
 const proof=(file,line,end,role)=>{const s=get(file).s;return evidence(file,line,s.split('\n').slice(line-1,end).join('\n'),role);};
 function method(file,name){const m=get(file).methods.find(m=>m.name===name&&m.owner===(file===plugin?'com.example.recorde_translate_plugin.b':'com.alipay.verifyiotidentity.obfuscated.i04'));if(!m)throw Error('Missing listener helper '+name);return evidence(file,m.line,m.body,'helper urmărit '+name);}
 for(const opt of [61117,70811,61119,61120]){
  const f=allFunctions.find(f=>f.kind==='recepție BLE'&&f.opt.includes(opt));if(!f)throw Error('Missing receive '+opt);
  const chain=opt===61117?['CoreBluetoothDevice → i04.o3 / nd4.a → b.t.a → b.u3',method(bridge,'o3'),proof(plugin,2125,2132,'nd4 → u3'),method(plugin,'u3')]:opt===70811?['CoreBluetoothDevice → gc4.a → b.u.a → b.q3',proof(plugin,2190,2197,'gc4 → q3'),method(plugin,'q3')]:opt===61119?['CoreBluetoothDevice → i04.r3 → kj4.a → b.z.a → b.u2',method(bridge,'r3'),proof(plugin,2500,2508,'kj4 → u2'),method(plugin,'u2')]:['CoreBluetoothDevice → i04.q3 → oi4.a → b.a0.a → b.F3 → b.C2',method(bridge,'q3'),proof(plugin,332,340,'oi4 → F3'),method(plugin,'F3'),method(plugin,'C2')];
  const fields=opt===61117?[
   ['data','JSONArray | String',6215,6219,'data; alternativ șir JSON, parsată numai dacă începe cu ['],
   ['filePath','String',6233,6233,'valoare de rezervă pentru numele grupului; fallback parser șir gol'],
   ['fileType','int',6234,6234,'fallback parser 0; nu enumerare completă'],
   ['data[].fileType','int',6244,6246,'fallback din fileType de la rădăcină'],
   ['data[].name','String',6247,6247,'fallback din filePath de la rădăcină'],
   ['data[].fileList','JSONArray | String',6248,6252,'str5 = IBluetoothProtocol.KEY_FILE_LIST; alternativ șir JSON'],
   ['data[].fileList[].file','String',6266,6280,'nume de fișier citit din obiectul element'],
   ['data[].fileList[].size','long',6282,6282,'valoarea 0 provoacă marcarea locală FILE_DELETED; nu garantăm semantica tuturor firmware-urilor']
  ]:opt===70811?[
   ['events','JSONArray | String',5725,5736,'cheia g.ax = events; încercare JSONArray, apoi șir JSON. Fallbackul new JSONArray(events) este precedat de new JSONObject(events); o rădăcină array nu este confirmată acceptată.']
  ]:[];
  if(opt===61117){const c='com/example/recorde_translate_plugin/glass/wifip2p/wifi/protocol/IBluetoothProtocol.java',s=get(c).s,needle='KEY_FILE_LIST = "fileList"';if(!s.includes(needle))throw Error('File-list key changed');f.evidence.push(proof(c,s.slice(0,s.indexOf(needle)).split('\n').length,s.slice(0,s.indexOf(needle)).split('\n').length,'constanta fileList'));f.evidence.push(proof(plugin,6200,6201,'aliasuri str5/str6 pentru cheile JSON'));}
  if(opt===70811){const c='com/umeng/analytics/pro/g.java';if(!get(c).s.includes('ax = "events"'))throw Error('Event key changed');f.evidence.push(proof(c,64,64,'constanta events'));}
  for(const [wire,type,line,end,description] of fields){
   const ev=proof(plugin,line,end,'parser de notificare în listener; cale '+wire);
   const p=addParam({scope:f.id+':response',name:wire,javaType:type,valueClass:typeClass(type),direction:'răspuns BLE',format:'cale JSON în notificare',description,confidence:'parser urmărit static prin listener; fără trafic real',evidence:[ev]});
   link(f,p,'output');(f.schemaPaths||=[]).push({path:wire,parameterId:p.id,direction:'output',representation:'JSON primit; parser în plugin Android'});
  }
  f.evidence.push(...chain.slice(1));
  const detail=opt===61117?'Notificarea este ignorată dacă FileListSyncManager sau FileDataSyncManager sincronizează. glass_media_notify și contoarele construite local nu sunt câmpuri wire. Ramurile complexe decompilate nu reprezintă o validare dinamică.':opt===70811?'Produce onGlassEventNotify; structura elementelor events rămâne dinamică, fără enum sau intervale inventate.':opt===61119?'Nu citește payload. Dacă sincronizarea de fișiere este activă, o oprește și produce onWifiError cu reason=wifi_error și code local. Acestea nu sunt câmpuri citite din pachet.':'C2 iterează cheile JSONObject dinamic; F3 le transmite în onTransDisplaySettingChanged. La eroare, pune textul original în data. Nu există o listă fixă de chei demonstrată.';
  f.listenerTrace={chain:chain[0],detail,status:fields.length?'campuri_wire_urmarite':opt===61119?'notificare_fara_payload_citit':'obiect_json_cu_chei_dinamice'};
  f.notes.push(detail);reviews.push({id:f.id,opt,fields:fields.map(x=>({path:x[0],javaType:x[1]})),...f.listenerTrace,evidence:chain.slice(1)});
 }
 return reviews;
};
