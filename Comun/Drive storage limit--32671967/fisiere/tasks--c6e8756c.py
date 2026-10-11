import csv,sys,os,json
sp=sys.argv[1]; N=int(sys.argv[2])
fold=[l.rstrip('\n').split('\t') for l in open(os.path.join(sp,'plan_foldere.tsv'),encoding='utf-8')]
rows=list(csv.reader(open(os.path.join(sp,'comparatie.csv'),encoding='utf-8-sig'),delimiter=';'))[1:]
# native google docs in local mirror
mirror=r'C:\Users\User\My Drive (covaciu.gnm@gmail.com)'
nat=set()
for dp,dn,fn in os.walk(mirror):
    if any(f.lower().rsplit('.',1)[-1] in ('gdoc','gsheet','gslides','gform','gdraw','gmap','gsite','gjam') for f in fn):
        rel=os.path.relpath(dp,mirror).replace(chr(92),'/')
        parts=[] if rel=='.' else rel.split('/')
        for k in range(len(parts)+1): nat.add('/'.join(['Contul meu Drive']+parts[:k]))
best={}
for r in rows:
    for f,_,_ in [(x[0],0,0) for x in []]: pass
idx={f[0]:None for f in fold[:N]}
for r in rows:
    p=r[1]; parts=p.split('/')
    for k in range(1,len(parts)):
        f='/'.join(parts[:k])
        if f in idx and (idx[f] is None or p.count('/')<idx[f][0].count('/')): idx[f]=(p,r[4])
tasks=[];skip=[]
for f,gb,cnt in fold[:N]:
    if f in nat: skip.append(f); continue
    p,i=idx[f]
    tasks.append({"folder":f,"title":f.split('/')[-1],"gb":float(gb),"sample_file_id":i,"hops_up_from_parent":p.count('/')-f.count('/')-1})
json.dump(tasks,open(os.path.join(sp,'tasks.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(len(tasks),"taskuri",sum(t['gb'] for t in tasks),"GB; sarite (au Google Docs native):",skip)
