import openpyxl,collections,json,pathlib,re
out=pathlib.Path(r"Z:\00.Roboti\cesiro.com\work_nomexp\audit_date")
src=r"Z:\00.Roboti\cesiro.com\NOMEXP_v9_ultimate.(2).xlsx"
w=openpyxl.load_workbook(src,read_only=True,data_only=True)
data={s.title:list(s.iter_rows(values_only=True)) for s in w}
rows=[(i,r) for i,r in enumerate(data['NOMEXP02'][1:],2) if isinstance(r[0],str) and r[0].startswith('5900_')]
defs={int(r[2]):(i,r[0]) for i,r in enumerate(data['ADAUGARE FORME 1'],1) if len(r)>2 and isinstance(r[2],(int,float)) and isinstance(r[0],str)}
glazes=collections.defaultdict(list)
for n,start in [('Codificare 1 Glazuri',4),('COD CULOARE COD',2)]:
    for i,r in enumerate(data[n][start-1:],start):
        if r[0] is not None:glazes[str(r[0])].append({'sheet':n,'row':i,'description':r[1]})
changes=[];issues=[];records=[]
for i,rr in rows:
    r=list(rr)
    color=re.sub(r'\s+','',str(r[5]))
    model=2345 if int(r[8])==9043 else r[20]
    sku=f'5900_{model}_{r[8]}_{color}'
    pc=int(re.match(r'SET\s+(\d+)',defs[int(r[8])][1],re.I).group(1))
    for col,value,reason in [
        ('A',sku,'SKU din client5900, model confirmat, cod formă și glazură fără spații.'),
        ('F',color,'Cod glazură fără spații.'),
        ('O',5900,'Cod client recuperat din prefixul SKU5900.'),
        ('U',model,'Modelul formei9043 confirmat concordant în trei dicționare de forme.'),
        ('X',color,'Cod glazură fără spații.'),
        ('AE',pc,'Numărul declarat de piese din definiția formei.'),
        ('AF',color,'Cod glazură fără spații.'),
    ]:
        j=openpyxl.utils.column_index_from_string(col)-1
        if r[j]!=value:
            changes.append({'sheet':'NOMEXP02','cell':f'{col}{i}','old_value':r[j],'new_value':value,'reason':reason,
             'evidence':f"ADAUGARE FORME 1!A{defs[int(r[8])][0]}:C{defs[int(r[8])][0]} = {defs[int(r[8])][1]}" if col in ('U','AE') else f'NOMEXP02!A{i},F{i},I{i},U{i}'})
        r[j]=value
    if not glazes[color]:
        issues.append({'row':i,'sku':sku,'type':'cod_glazura_absent_dictionare','color':color,'source_description':r[6]})
    else:
        if len(set(x['description'] for x in glazes[color]))>1:
            issues.append({'row':i,'sku':sku,'type':'cod_glazura_ambiguu','color':color,'matches':glazes[color]})
        known={str(x['description']).strip().upper().replace(' ','') for x in glazes[color]}
        got=str(r[6]).strip().upper().replace(' ','')
        if got not in known:
            issues.append({'row':i,'sku':sku,'type':'descriere_glazura_diferita','source_description':r[6],'matches':glazes[color]})
    records.append({'source_row':i,'normalized_sku':sku,'values':r[:32]})
groups=collections.defaultdict(list)
for item in records:groups[item['normalized_sku']].append(item)
dups=[]
for sku,its in groups.items():
    if len(its)>1:
        # Only report exact equality once codes/model/pieces/BEN normalization is applied.
        differentcols=[openpyxl.utils.get_column_letter(j+1) for j in range(32) if len(set(str(it['values'][j]) for it in its))>1]
        dups.append({'sku':sku,'rows':[it['source_row'] for it in its],'different_columns':differentcols,'identical_after_corrections':not differentcols})
manifest={'source':src,'scope':'DOAR NOMEXP02 SKU prefix5900','source_rows':len(rows),'proposed_unique_sku':len(groups),
 'changes':changes,'duplicates_after_correction':dups,'color_issues':issues,
 'records_after_certain_corrections':records,
 'do_not_fill':['Pret unitar','Cost Standard','Greutate Net','Greutate Brut','PRET','COD','NRART'],
 'basis':'BEN din SKU; NRPIESE din numărul explicit SET; model2345 pentru forma9043 confirmat concordant; prețurile altor clienți nu se transferă.'}
(out/'sku5900_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
print('CHANGES',len(changes),dict(collections.Counter(re.sub(r'\d+','',x['cell']) for x in changes)))
print('DUPLICATES',dups)
print('COLOR ISSUES',len(issues),dict(collections.Counter(x['type'] for x in issues)))
print('COLOR EXAMPLES',issues[:15])
print('PIECES',dict(collections.Counter(it['values'][30] for it in records)))
