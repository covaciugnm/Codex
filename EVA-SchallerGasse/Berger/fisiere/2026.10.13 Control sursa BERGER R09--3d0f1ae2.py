from pathlib import Path
import json,copy,hashlib,shutil,re
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent;DATE='2026.10.13'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rp=OUT/f'{DATE} Registru modificari BERGER R09.json';r=json.loads(rp.read_text(encoding='utf-8'))
src=ROOT/r['source_R09'];s=json.loads(src.read_text(encoding='utf-8'))
label=s['annexes'][0]['tables'][0]['rows'][5][0]
assert label=='Baugrubensicherung / Verbau — bauseits'
s['annexes'][0]['tables'][0]['rows'][5][0]=label.replace('—','-')
r['changes'].append({'path':['annexes',0,'tables',0,'rows',5,0],'before':label,'after':label.replace('—','-'),'instruction':'ASCII hyphen typography only'})
src.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');shutil.copy2(src,ROOT/r['public_folder']/src.name)
r['source_R09_sha256']=sha(src);rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
old=json.loads((ROOT/r['source_R08']).read_text(encoding='utf-8'));replay=copy.deepcopy(old)
for c in r['changes']:
    t=replay
    for k in c['path'][:-1]:t=t[k]
    assert t[c['path'][-1]]==c['before'],c['path']
    t[c['path'][-1]]=copy.deepcopy(c['after'])
assert replay==s
assert sha(ROOT/r['source_R08'])==r['source_R08_sha256']
assert sha(ROOT/r['PECH_frozen']['path'])==r['PECH_frozen']['sha256']
assert sha(ROOT/r['original_offer'])==r['original_offer_sha256']
assert s['annexes'][3]['tables'][0]==old['annexes'][3]['tables'][0]
assert s['annexes'][3]['tables'][1]==old['annexes'][3]['tables'][4]
text=json.dumps(s,ensure_ascii=False)
for bad in ['0,1 Prozent','fünf Prozent','dreißig Kalendertage','10/20/25','E1-E7','E6-Rate','EUR 166,67','bis zu sechs zusätzliche','sechs zusätzliche physische','zwölf physische','zwölf enthaltenen','zusätzlich zu den zwölf','PECH','Vertragsvorschlag','Vorbemerkung']:assert bad not in text,bad
assert sum(float(x[1].replace('.','').replace(',','.')) for x in s['annexes'][3]['tables'][0]['rows'][:-1])==45000
assert s['annexes'][3]['tables'][2]['rows'][1][2:] == ['46.000,00','55.200,00']
assert s['annexes'][3]['tables'][2]['rows'][2][2:] == ['47.000,00','56.400,00']
email=json.loads((ROOT/r['email_source']).read_text(encoding='utf-8'))
assert email['body_de'].endswith('Mit freundlichen Grüßen\n') and 'PECH' not in email['body_de']
out=OUT/f'{DATE} Control integritate sursa BERGER R09.json';assert not out.exists()
out.write_text(json.dumps({'data':DATE,'status':'PASS','source_sha256':sha(src),'replay_changes_exact':len(r['changes']),'base_positions_and_regie_original_identical':True,'PECH_frozen':r['PECH_frozen'],'original_offer_unchanged':True,'payment_days':14,'no_contractual_AG_retention':True,'no_contractual_penalty':True,'extra_pack_net':1000,'extra_pack_visits':4,'extras_examples_math':'PASS','no_obsolete_12visits_6options_terms':True,'trimiteri':0},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'PASS','source_sha256':sha(src),'changes_exact':len(r['changes']),'PECH_untouched':True},ensure_ascii=False))
