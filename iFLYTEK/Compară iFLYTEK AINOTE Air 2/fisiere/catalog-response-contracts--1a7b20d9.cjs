// Verified receive contracts. Keep wire reads separate from local Java model fields.
module.exports = function (ctx) {
  const {allFunctions, paramMap, functionMap, get, resolve, evidence, addParam, link, schemaLinks, typeClass, corefile} = ctx;
  const parserFile = 'com/iflytek/easytrans/headset/bluetooth/bean/common/DeviceInfoParsers.java';
  const parser = get(parserFile), core = get(corefile);
  const receives = allFunctions.filter(f => f.kind === 'recepție BLE');
  function source(file, needle) {
    const d = get(file), at = d.s.indexOf(needle);
    if (at < 0) throw Error('Missing receive evidence: ' + file + ' ' + needle);
    return evidence(file, d.s.slice(0, at).split('\n').length, needle, 'parser / transformare verificată');
  }
  function wire(f, key, type, profile, condition, method, extra = {}) {
    const name = key.startsWith('"') ? JSON.parse(key) : resolve(key, parserFile);
    if (typeof name !== 'string') throw Error('Unresolved parser key ' + key);
    const m = parser.methods.find(x => x.name === method);
    if (!m || !m.body.includes(key)) throw Error('Missing parser key ' + method + ' ' + key);
    const at = m.body.indexOf(key);
    const p = addParam({scope:f.id + ':response:' + profile, name, javaType:type, valueClass:typeClass(type),
      direction:'răspuns BLE / ' + profile, profile, wirePath:name,
      format:'cheie JSON citită din mesajul dispozitivului',
      description:'Citită în ' + method + '. ' + condition, confidence:'citire în parser verificată static',
      evidence:[evidence(parserFile, parser.s.slice(0,m.bodyStart + at).split('\n').length, m.body.trim(), 'parser profil ' + profile)], ...extra});
    link(f,p,'output');
    (f.schemaPaths ||= []).push({path:name,parameterId:p.id,direction:'output',profile,condition,representation:'JSON primit / parser de profil'});
    return p;
  }
  const profiles = {
    62001:['System', 'parseSystemInfo', ['"sn"','"mac"'], ['aa4.b3','aa4.c3','aa4.d3','aa4.e3','aa4.f3'], 'String', 'Prezența snL sau snR selectează varianta headset. Modelul este dedus local din seria extrasă.'],
    62002:['Version', 'parseVersionInfo', ['"version"'], ['aa4.h3','aa4.i3','aa4.j3'], 'String', 'Prezența verL sau verR selectează varianta headset.'],
    62003:['Battery', 'parseBatteryInfo', ['"bat"','GPassEventReporter.MODULE_BATTERY','"batChanging"','"charging"'], ['aa4.k3','aa4.l3','aa4.m3','aa4.n3','aa4.o3','aa4.p3'], 'int', 'Prezența batL sau batR selectează varianta headset. Pentru ochelari: bat are fallback battery; batChanging are fallback charging.'],
    62004:['State', 'parseStateInfo', ['"state"'], ['aa4.q3','aa4.r3','"master"'], 'String', 'Prezența stateL sau stateR selectează varianta headset; pentru ochelari se citește state.']
  };
  for (const f of receives) {
    const opt = f.opt[0], def = profiles[opt === 61001 ? 62004 : opt === 61002 ? 62003 : opt];
    if (def) {
      const [kind,method,glassKeys,headsetKeys,type,condition] = def;
      for (const [profile,keys] of [['glasses',glassKeys],['headset',headsetKeys]]) {
        for (const key of keys) wire(f,key,type,profile,condition,method,
          kind==='State' && key!=='"master"' ? {parserFallback:'unknown'} : {});
        schemaLinks(f,'com.iflytek.easytrans.headset.bluetooth.bean.' + profile + '.' + (profile==='glasses'?'Glasses':'Headset') + kind + 'Info',parserFile,f.owner,'model');
      }
      f.evidence.push(source(parserFile,'public final Base' + kind + 'Info ' + method));
      f.notes.push(condition, 'CoreBluetoothDevice poate transmite JSON-ul mai departe către callback. Contractul de câmpuri de aici provine din DeviceInfoParsers și adaptoarele *Info.Companion, nu dintr-un test pe firmware.');
      const adapter = 'com/iflytek/easytrans/headset/bluetooth/bean/' + kind + 'Info.java';
      f.evidence.push(source(adapter,'DeviceInfoParsers.INSTANCE.' + method));
      if (kind==='System') f.notes.push('appendModelField() adaugă local model. Câmpul model din obiectul Java nu dovedește un câmp primit de la ochelari.');
      if (kind==='State') f.notes.push('StateInfo.Companion.create() adaptează GlassesStateInfo prin toLegacy(). stateL, stateR și master din modelul legacy nu sunt chei dovedite ale mesajului pentru ochelari.');
      for (const pid of f.outputParameterIds) {
        const p=paramMap.get(pid);
        if(p.profile==='glasses' && kind==='Battery') {
          if(p.name==='bat') p.parserFallback={expression:'jSONObject.optInt("battery")', finalFallback:0};
          if(p.name==='batChanging') p.parserFallback={expression:'jSONObject.optInt("charging")', finalFallback:0};
          if(['battery','charging'].includes(p.name)) {p.parserFallback=0;p.requirement='Cheie alternativă de fallback; parserul preferă '+(p.name==='battery'?'bat':'batChanging')+'.';}
        }
      }
    }
    if ([62007,61005].includes(opt)) {
      f.notes.push('Transformare locală: WorkState.state = JSON.workState; WorkState.msg = v6(workState); WorkState.type = optInt("type",0). msg nu este citit de pe fir.');
      for(const pid of f.outputParameterIds){const p=paramMap.get(pid);p.wirePath=p.name;(f.schemaPaths ||= []).push({path:p.name,parameterId:pid,direction:'output',representation:'JSON primit'});}
    }
    if (opt===70400) {
      f.notes.push('data acceptă JSONArray sau String care conține un tablou JSON. name, fileType și fileList apar în fiecare obiect data[].',
        'FileListResponse.pageSize este calculat local ca arrayList.size(). Alte câmpuri DeviceFileInfo primesc zero / valori implicite; nu sunt chei citite de acest parser.',
        'errCode=32301 este tratat ca succes numai când wifiFileList=1; modelul local normalizează atunci errCode la 0.');
      for (const pid of f.outputParameterIds) {
        const p=paramMap.get(pid), nested=['name','fileType','fileList'].includes(p.name);
        p.wirePath=(nested?'data[].':'')+p.name;
        p.description='Citire JSON verificată la '+p.wirePath+'. '+(nested?'Obiectele provin din tabloul data sau din decodarea șirului JSON data.':'Câmp al obiectului rădăcină.');
        if(p.name==='data'){p.javaType='JSONArray | String';p.valueClass='uniune JSON';p.format='tablou JSON sau șir ce codifică un tablou JSON';p.rule='Se încearcă optJSONArray; dacă rezultatul este null se parsează optString; șirul gol produce tablou gol.';}
        (f.schemaPaths ||= []).push({path:p.wirePath,parameterId:pid,direction:'output',representation:'JSON primit / cale verificată'});
      }
    }
    if(f.evidence.some(e=>e.file===corefile && /FileTransferCtrlResponse[\s\S]*fromJson\(/.test(e.excerpt||''))) {
      const file='com/iflytek/easytrans/headset/bluetooth/bean/FileTransferCtrlResponse.java';
      f.evidence.push(source(file,'new Gson().fromJson(str, FileTransferCtrlResponse.class)'));
      schemaLinks(f,'FileTransferCtrlResponse',file,f.owner,'output','',new Set(),0,'JSON prin Gson.fromJson confirmat');
    }
    for (const fid of f.relatedFunctionIds) {
      const command=functionMap.get(fid);
      if (!command || command.kind!=='comandă BLE') continue;
      for(const pid of f.outputParameterIds) link(command,paramMap.get(pid),'output');
      for(const pid of f.localModelParameterIds||[]) link(command,paramMap.get(pid),'model');
      command.schemaPaths=[...(command.schemaPaths||[]),...(f.schemaPaths||[]).filter(x=>x.direction==='output')];
      command.localModelPaths=[...(command.localModelPaths||[]),...(f.localModelPaths||[])];
      command.notes.push('Răspunsul și modelele locale sunt descrise separat în parserul corelat '+f.id+'.');
    }
  }
  const ota=allFunctions.find(f=>f.kind==='Flutter MethodChannel' && f.name==='startGlassOTA');
  if(!ota) throw Error('Missing startGlassOTA');
  const otaFile='com/example/recorde_translate_plugin/glass/wifip2p/WifiManagerPlugin.java';
  ota.resultContract={channel:'wifi_manager_plugin',kind:'MethodChannel.Result.success',value:{},meaning:'ACK imediat după apelul startOTA; nu confirmă finalizarea actualizării.'};
  ota.eventChannel='wifi_manager_plugin_event';
  ota.eventContracts=[
    {callback:'onOTAStartConnectDevice',fields:{type:'status',status:0}},
    {callback:'onOTAStart',fields:{type:'status',status:1}},
    {callback:'onOTACheckSuccess',fields:{type:'status',status:3}},
    {callback:'onOTAEnterError',fields:{type:'status',status:-1}},
    {callback:'onOTACheckError',fields:{type:'status',status:'argumentul int status'}},
    {callback:'onOTAProgress',fields:{type:'ota_progress',progress:'argumentul int progress'}},
    {callback:'onOTAFailed',fields:{type:'error',message:'errorMsg, numai dacă nu este null / gol'}},
    {callback:'onOTASuccess',fields:{type:'success'}}
  ];
  for(const [name,type,desc,extra,needle] of [
    ['type','String','Discriminatorul evenimentului asincron.',{observedValues:['status','ota_progress','error','success']},'map.put("type", "ota_progress")'],
    ['status','int','Cod de etapă / eroare, prezent când type=status. onOTACheckError retransmite codul primit; lista codurilor nu este închisă.',{values:[{value:0,meaning:'începe conectarea'},{value:1,meaning:'începe OTA'},{value:3,meaning:'verificarea a reușit'},{value:-1,meaning:'eroare la intrarea în OTA'}]},'map.put("status", Integer.valueOf(status))'],
    ['progress','int','Progres retransmis din callback; unitatea și intervalul nu sunt stabilite de acest adaptor.',{},'map.put("progress", Integer.valueOf(progress))'],
    ['message','String','Mesaj de eroare opțional la type=error.',{requirement:'omis dacă TextUtils.isEmpty(errorMsg)'},'map.put("message", errorMsg)']
  ]){
    const p=addParam({scope:ota.id+':event',name,javaType:type,valueClass:typeClass(type),format:'Map Flutter / EventChannel wifi_manager_plugin_event',direction:'ieșire asincronă Flutter',description:desc,confidence:'callback implementat în Java',evidence:[source(otaFile,needle)],...extra});
    link(ota,p,'output');
  }
  ota.returns='Result.success({}) este ACK. Etapele și rezultatul OTA sunt trimise separat prin EventChannel.';
  ota.notes.push('Callbackurile folosesc mEventSink.success(map), inclusiv la type=error; acestea nu sunt MethodChannel.Result.error. Nu confundați status=3 (check success) cu evenimentul final type=success.');
  ota.errors.push('onOTAEnterError → eveniment {type:"status",status:-1}.','onOTACheckError(status) → eveniment {type:"status",status}.','onOTAFailed(errorMsg) → eveniment {type:"error"}, cu message numai dacă există text.');
  ota.evidence.push(source(otaFile,'public void onOTACheckError(final int status)'));
};
