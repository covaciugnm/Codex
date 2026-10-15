from pathlib import Path
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent;DATE='2026.10.13'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
record_path=OUT/f'{DATE} Registru aplicare editoriala R07.json'
record=read(record_path);history=OUT/f'{DATE} Istoric R07 inainte ultima neutralizare'
assert not history.exists();history.mkdir();shutil.copy2(record_path,history/record_path.name)
old_text='Eine alte interne Baukostenschätzung oder Prozentmethode des Angebots ist keine Zusage über die tatsächlichen Baukosten und kein automatischer Index für dieses Honorar. Der vollständige beauftragte Umfang wird im jeweiligen Paketpreis und nicht nur in einer einzelnen wirtschaftlichen Originalposition übernommen.'
new_text='Eine interne Baukostenschätzung oder Prozentmethode ist keine Zusage über die tatsächlichen Baukosten und kein automatischer Index für dieses Honorar. Der vollständige beauftragte Umfang wird im vereinbarten Paketpreis und nicht nur in einer einzelnen Honorarposition übernommen.'
delta=[]
for index,operation in enumerate(record['operatiuni'],84):
    provider=operation['provider'];src=ROOT/operation['R07'];public=ROOT/operation['public_source'];pdf=ROOT/operation['PDF_expected']
    assert sha(src)==operation['R07_sha256']==sha(public)
    old=read(src);new=read(src);assert new['sections'][2]['paragraphs'][6]==old_text
    for p in [src,pdf,OUT/f'{DATE} QA text {provider} R07.json']:
        assert p.exists();saved=history/p.name;assert not saved.exists();shutil.copy2(p,saved);assert sha(p)==sha(saved)
    new['sections'][2]['paragraphs'][6]=new_text
    src.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    shutil.copy2(src,public);assert sha(src)==sha(public)
    assert old['annexes']==new['annexes'] and old['presentation']==new['presentation']
    expected=read(history/src.name);expected['sections'][2]['paragraphs'][6]=new_text;assert new==expected
    change={'id':f'E{index:03d}','pointer':'/sections/2/paragraphs/6','before':old_text,'after':new_text,'reason':'Final editorial neutralization; no prices, scope, rights or schedule altered'}
    operation['applied_editorial_changes'].append(change);operation['R07_sha256']=sha(src)
    delta.append({'provider':provider,'previous_source_sha256':sha(history/src.name),'final_source_sha256':sha(src),'previous_pdf_sha256':sha(history/pdf.name),'exact_only_pointer_changed':change['pointer'],'financial_annex_exact':True})
    # Free only our newly-created PDF/QA output names; preserve all originals.
    assert pdf.resolve().is_relative_to(ROOT.resolve()) and pdf.name.endswith(f'{provider} R07.pdf')
    pdf.unlink();(OUT/f'{DATE} QA text {provider} R07.json').unlink()
record['additional_neutralization']={'data':DATE,'delta':delta,'editorial_changes_total':85}
record_path.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/f'{DATE} Delta final §3 R07.json').write_text(json.dumps({'data':DATE,'delta':delta},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(delta,ensure_ascii=False))
