import pathlib,json,hashlib,collections,decimal,datetime,xml.etree.ElementTree as ET
O=pathlib.Path(__file__).parent;E=O.parent;R=E.parent
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2,default=str),encoding='utf8')
res=rd(O/'integrity.json');a=rd(E/res['A01']['path']);files={p:h(E/'R2_zone/A01'/p) for p in a['local_artifacts']};assert all(v==a['local_artifacts'][k]['sha256'] for k,v in files.items());res['A01']['local_artifacts']=files;res['A01']['evidence_hashes']+=len(files)
p=E/'A09_raport_R2.json';assert h(p)=='18c36baf10a9c965cefb50a5324026126b02f2ffdb812f885967e91cf301f47e';j=rd(p);Q=rd(R/'Index_trasabilitate.json');cs={v['control_id'] for v in j['controls']};ps={v['pipeline_id'] for v in j['pipelines']};c0={v['id']for v in Q['controls'] if v['zone']=='A09'};p0={v['id']for v in Q['pipelines'] if v['zone']=='A09'}; errors=[];details=[]
for label,items in [('evidence',j['evidence_index']),('sheet',j['individual_sheets']),('AND',j['android_cards'])]:
 for v in items:
  actual=h(R/v['path']) if (R/v['path']).is_file() else None
  if v['sha256']!=actual:errors.append([label,v['path'],v['sha256'],actual])
  details.append({'kind':label,'path':v['path'],'matched':v['sha256']==actual})
res['A09']={'path':p.name,'report_sha256':h(p),'controls':len(cs),'pipelines':len(ps),'control_missing':sorted(c0-cs),'control_extra':sorted(cs-c0),'pipeline_missing':sorted(p0-ps),'pipeline_extra':sorted(ps-p0),'evidence_hashes':len(j['evidence_index']),'extra_individual_sheets':len(j['individual_sheets']),'extra_ANDROID_cards':len(j['android_cards']),'hash_errors':errors,'findings':len(j['findings']),'statuses':j['counts']['by_status'],'evidence_checks':details}
wr(O/'integrity_extended.json',res);print([(z,r['evidence_hashes'],len(r['hash_errors'])) for z,r in res.items()],errors[:1])
d=decimal.Decimal; obs={};p31=rd(E/'Staging_proxy_CUI_31s.json');obs['A01_p31']=[[k,v,n]for(k,v),n in collections.Counter((a['phase'],a['http'])for a in p31['rows']).items()]
sc=[]
for a in rd(E/'R2_zone/A05/barriers-confirmed.json'):
 curr=[d(a['final']['g1']),d(a['final']['g2'])];again=[d(a['after_repeat']['g1']),d(a['after_repeat']['g2'])];assert curr==again==([18,20] if a['mode']=='overlap' else [18,18]);assert sum(d(x[4]) for x in a['final']['transactions'])==-2
 sc.append({'case':a['mode'],'result':curr,'repeat':again,'commit_or_interleaving_events':[x['event'] for x in a['events']],'g1_transactions':a['final']['transactions'],'mirror_rows':len(a['final']['mirror'])})
obs['A05_native_barriers']=sc
w=[x for x in rd(E/'R2_zone/A05/recipe-cost-cycle.json') if 'g2' in x]; qty=[d(x['g2']['1000005']) for x in w]; movements=[len(x['wms_moves']) for x in w];assert qty==[0,1,2,3,2] and movements==[2,5,8,11,14] and all(x['g1']==w[0]['g1']for x in w)
obs['A05_packing']={'set_qty':qty,'G2_movements':movements,'G1_inventory_unchanged':True,'limit':'Compensation is a new operation, not demonstrated reversal linked to source.'}
q=rd(E/'A09/F01_queue_R2.json');mnt=rd(E/'A09/native_actions_R2.json');assert q['exit']==0 and any('eliberat' in t for t in q['stderr']) and 'read only' in str(q['sql']).lower() and h(E/'A09/F01_queue_R2.json')==mnt['queue_sha256']; assert len(mnt['cases'])==236 and all(not x['type_match'] and not x['object_match'] for x in mnt['cases'])
obs['A09_menu']={'cases':236,'wrong_type_and_object':236,'native_types':dict(collections.Counter(x['native_type']for x in mnt['cases'])),'queue_and_handler_match':mnt['git_handler_sha']==mnt['live_handler_sha']}
dir=E/'A09/android_R2';relay=rd(dir/'relay-outcome.json');a,b=relay['first'],relay['repeat'];r=relay['independent_native_readback'];assert h(R/r['file'])==r['sha256'];x=r['observed'];st=x['state']
assert a['http']==b['http']==200 and a['body_request_sha256']==b['body_request_sha256'] and a['canonical_body_hash']==b['canonical_body_hash']==x['payload_sha256'] and a['canonical_body_hash']!=a['body_request_sha256']; assert len(x['key_journal'])==len(x['line_rows'])==1 and list(map(d,x['line_rows'][0][4:6]))==[20,18] and not st['facts'] and not st['transactions'] and st['inventory'][0][0]=='DR'
obs['Android_wire_and_DB']={'key_suffix':'0021','qty_book_count':[20,18],'durable_keys':1,'lines':1,'DR':True,'facts':0,'transactions':0,'notice':'Distinct from server fixture K0011 with CO/posted E. Emulator run used debug/test relay, not physical hardware.'}
l=rd(dir/'mobile-label.json');src=pathlib.Path('D:/CodexWork/a09-android-560fd59')/l['source_path'];nso='{http://schemas.android.com/apk/res/android}';assert h(src)==l['xml_sha256'];xm=ET.parse(src);nd=next(t for t in xm.iter() if t.get(nso+'id')=='@+id/cantitate');labs=[t for t in xm.iter() if t.get(nso+'labelFor','').endswith('/cantitate')]; assert not labs and nd.get(nso+'hint');png=E/'A09'/l['screen_png'];assert h(png)==l['screen_sha256'];obs['A09_F06']={'resource':'cantitate','hint':nd.get(nso+'hint'),'explicit_labelFor':0,'screenshot':h(png),'direct_visual_observation':'Lot and prior count are shown, entered value 2 has no persistent label before SALVEZ; retry/offline message remains visible.'}
zk=rd(E/'A09/zk_volume_R2.json');assert all(len([v for v in zk['raw'] if v['rows']==x])==7 for x in [100,10001]);obs['ZK_laboratory']=zk['stats']
so=rd(E/'R2_zone/A06/dovezi/so-native-retry.json');assert sorted(v['http'] for v in so['compete'])==[200,500] and any('m_storagereservation_pkey' in (v.get('summary')or '').lower() for v in so['compete']);obs['A06_SO']=[(x['http'],x['status']) for x in so['compete']]
wr(O/'underlying_observations.json',obs);print('observations',list(obs))

