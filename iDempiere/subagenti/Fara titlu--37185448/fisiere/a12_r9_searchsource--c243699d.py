from a12_r9_orig import *
p=r7map['T04.07-R3-001']['source_row']['source_file'];oid=r7map['T04.07-R3-001']['source_row']['sha_or_git_blob'];ls=fetch_oid(oid).decode('utf8').splitlines()
for j,line in enumerate(ls,1):
 if re.search(r'EVA_DocPartener|EVA_DecontCurier|EVA_CorelareDecont|CititorTabelar|foaia|antet.*(patru|[0-9]|rând)|DE_LAMURIT|fără potrivire|Ramburs',line,re.I)and j not in [63,64,65,66,67,68]:print(j,line[:420])
pdir='Documentatie/echipa-2026-10-09/T35-cadru-platforme-vanzari'
alist=git('ls-tree -r --name-only '+BASE+' -- '+pdir).decode().splitlines()
print('named root',[(x.split('/')[-1])for x in alist if x.count('/')==3 and re.search('08-L3|09-L3|COORDONARE|log|L3b',x,re.I)][:100])
if __name__=='__main__':pass

