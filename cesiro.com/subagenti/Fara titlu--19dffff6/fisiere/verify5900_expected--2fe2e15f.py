import json,pathlib,re,collections
p=pathlib.Path(r"Z:\00.Roboti\cesiro.com\work_nomexp\audit_date")
m=json.loads((p/'sku5900_manifest.json').read_text(encoding='utf-8'))
dedup={}
for r in m['records_after_certain_corrections']:
    dedup.setdefault(r['normalized_sku'],r)
rows=list(dedup.values())
errors=[]
for it in rows:
    r=it['values']; sku=it['normalized_sku']; parts=sku.split('_')
    if not re.fullmatch(r'5900_\d{4}_\d{4}_[A-Z0-9]+',sku):errors.append([sku,'invalid_format'])
    if str(r[20])!=parts[1] or str(r[8])!=parts[2] or str(r[5])!=parts[3]:errors.append([sku,'component_mismatch'])
    if r[14]!=5900:errors.append([sku,'wrong_client'])
    if r[7]!='PF.C':errors.append([sku,'wrong_category',r[7]])
    if r[29]!='SET':errors.append([sku,'wrong_unit',r[29]])
    if r[27]!='EUR':errors.append([sku,'wrong_currency',r[27]])
    if r[30] not in [4,6,12,16,18,24]:errors.append([sku,'invalid_piece_count'])
    if any(r[j] is not None for j in [10,11,12,13,28]):errors.append([sku,'unexpected_price_weight'])
result={'source_rows':367,'expected_unique_sku_count':len(rows),'duplicate_removed_source_row':3520,
        'errors':errors,'models':dict(collections.Counter(r['values'][20] for r in rows)),
        'forms':dict(collections.Counter(r['values'][8] for r in rows)),
        'colors':dict(collections.Counter(r['values'][5] for r in rows)),
        'piece_counts':dict(collections.Counter(r['values'][30] for r in rows)),
        'expected_sku_sorted':sorted(dedup)}
(p/'sku5900_expected_control.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print({k:v for k,v in result.items() if k!='expected_sku_sorted'})
