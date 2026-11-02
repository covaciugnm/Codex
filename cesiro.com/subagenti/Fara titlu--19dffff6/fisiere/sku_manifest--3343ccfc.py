import openpyxl,collections,json,pathlib,re
out=pathlib.Path(r"Z:\00.Roboti\cesiro.com\work_nomexp\audit_date")
src=r"Z:\00.Roboti\cesiro.com\NOMEXP_v9_ultimate.(2).xlsx"
wv=openpyxl.load_workbook(src,read_only=True,data_only=True)
wf=openpyxl.load_workbook(src,read_only=True,data_only=False)
names=['NOMEXP02','SORTAT','ARS','GLAZ','BISC','CRUD']
rs={n:list(wv[n].iter_rows(values_only=True)) for n in names}
fs={n:list(wf[n].iter_rows(values_only=True)) for n in names}
changes=[]; issues=[]; candidates=[]
def add(sheet,row,col,new,reason,evidence):
    old=fs[sheet][row-1][col-1]
    if old!=new:changes.append({'sheet':sheet,'cell':f'{openpyxl.utils.get_column_letter(col)}{row}','old':old,'new':new,'reason':reason,'evidence':evidence})
def normalize(s):
    if not isinstance(s,str):return s
    return re.sub(r'(?<=\d)\s+(?=[LMA](?:_|$))','',s.strip())
for n,rows in rs.items():
    suffix={'SORTAT':'S','ARS':'A','GLAZ':'G','BISC':'B','CRUD':'C'}.get(n)
    for i,r in enumerate(rows[1:],2):
        sku=r[0]
        if not isinstance(sku,str):continue
        cleaned=normalize(sku)
        if re.match(r'^394_',cleaned):
            cleaned='0'+cleaned
        if n=='BISC' and cleaned=='0394_4010__B':cleaned='0394_4010_B'
        if cleaned!=sku:
            add(n,i,1,cleaned,'Normalizare format SKU fără schimbarea componentelor','Modelul 0394 existent în NOMEXP02/FINAL_NOMEXP; glazurile sunt coduri fără spații.')
        if n=='NOMEXP02':
            for j in (6,24,32):
                v=r[j-1]
                if isinstance(v,str) and re.fullmatch(r'\d{3}\s+[LMA]',v):
                    add(n,i,j,normalize(v),'Eliminare spațiu interior din cod glazură','Aceeași glazură în SKU și în dicționarele de glazuri.')
            parts=cleaned.split('_')
            if len(parts)==4:
                source=[r[14],r[20],r[8],r[5]]
                for pos,v in enumerate(source):
                    if v in (None,'',0,'0') or str(v).startswith('#'):
                        issues.append({'sheet':n,'row':i,'sku':sku,'type':'componenta_sursa_lipsa','component':['BEN','MODEL','FORMA','GLAZURA'][pos],'value':v})
                    elif str(v)!=parts[pos] and not (pos==1 and str(v).zfill(4)==parts[pos]):
                        issues.append({'sheet':n,'row':i,'sku':sku,'type':'componenta_diferita','component':['BEN','MODEL','FORMA','GLAZURA'][pos],'source':v,'sku_component':parts[pos]})
        elif n in ['SORTAT','ARS','GLAZ']:
            if isinstance(r[2],str) and re.fullmatch(r'\d{3}\s+[LMA]',r[2]):
                add(n,i,3,normalize(r[2]),'Eliminare spațiu interior din cod glazură','Codul normalizat păstrează toate caracterele alfanumerice originale.')
            if not re.fullmatch(r'^\d{4}_\d{4}_[A-Za-z0-9]+_[SAG]$',cleaned):
                issues.append({'sheet':n,'row':i,'sku':sku,'type':'sku_trunchiat','description':r[1],'color':r[2],'weight':r[4],'cost':r[5]})
            else:
                parts=cleaned.split('_')
                if int(parts[1])>=9001:
                    issues.append({'sheet':n,'row':i,'sku':sku,'type':'cod_forma_set_in_semifabricat','description':r[1],'note':'Codul formei de set apare pe o descriere de piesă componentă; necesită identificarea modelului și formei componente.'})
                if parts[2]!=normalize(r[2]):
                    issues.append({'sheet':n,'row':i,'sku':sku,'type':'glazura_diferita','sku_color':parts[2],'column_color':r[2]})

# Fix exact form lookup failure, with two independent exact-label mapping tables.
add('NOMEXP02',2747,9,"=IFERROR(VLOOKUP(D2747,'ADAUGARE FORME 1'!$A$2:$C$869,3,FALSE),VLOOKUP(D2747,'Codificare forme'!$A$4:$C$205,3,FALSE))",
    'Recuperare cod formă prin denumire exactă existentă',
    "Codificare forme!A182:C182 și Adaugare forme!A195:C195: SET 6 BOL13 2996 = 9049; NOMEXP02!D1487/I1487 confirmă. A2747 devine 5250_2996_9049_S002 după recalculare.")

# Exact duplicate data matching is a candidate, not proof of the lost physical identity.
for n in ['SORTAT','ARS','GLAZ']:
    d=collections.defaultdict(list)
    for i,r in enumerate(rs[n][1:],2):
        sku=normalize(r[0])
        if isinstance(sku,str) and re.fullmatch(r'\d{4}_\d{4}_[A-Za-z0-9]+_[SAG]',sku) and int(sku.split('_')[1])<9001:
            key=(r[1],normalize(r[2]),r[4],r[5])
            d[key].append((i,sku))
    for issue in issues:
        if issue['sheet']!=n or issue['type']!='sku_trunchiat':continue
        key=(issue['description'],normalize(issue['color']),issue['weight'],issue['cost'])
        matches=d.get(key,[])
        unique=set(sku for _,sku in matches)
        if unique:
            candidates.append({**issue,'candidate_skus':sorted(unique),'matching_rows':matches,
                'confidence':'CANDIDAT: identitatea nu este confirmată doar de descriere/culoare/greutate/cost. Nu aplica automat.'})

for n in names:
    groups=collections.defaultdict(list)
    edits={c['cell']:c['new'] for c in changes if c['sheet']==n}
    for i,r in enumerate(rs[n][1:],2):
        sku=edits.get('A'+str(i),r[0])
        if isinstance(sku,str) and '_' in sku:groups[sku].append(i)
    for sku,ix in groups.items():
        if len(ix)>1:issues.append({'sheet':n,'sku':sku,'rows':ix,'type':'sku_duplicat_dupa_normalizare'})

manifest={'source':src,'scope':names,'certain_cell_changes':changes,
          'issues':issues,'recovery_candidates_do_not_autoapply':candidates,
          'note':'Coliziunile nu se elimină automat. Păstrează rândurile și sufixele manuale. Regulile nu completează prețuri sau greutăți lipsă.'}
(out/'sku_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
print('CHANGES',len(changes),dict(collections.Counter(c['sheet'] for c in changes)))
print('ISSUES',len(issues),dict(collections.Counter(x['type'] for x in issues)))
print('CANDIDATES',len(candidates),'unique',sum(len(x['candidate_skus'])==1 for x in candidates))
print('SOURCE DIFFERENCES',[x for x in issues if x['type']=='componenta_diferita'][:15])
