import csv,os,sys,collections,json
sp=sys.argv[1]
done=set()
import glob
donefiles=set()
for fn in glob.glob(os.path.join(sp,'results_files*.tsv')):
    for l in open(fn,encoding='utf-8'):
        q=l.rstrip(chr(10)).split(chr(9))
        if len(q)>1 and q[0] in ('OK','ALREADY'): donefiles.add(q[1])
for fn in glob.glob(os.path.join(sp,'results_[0-9].tsv'))+glob.glob(os.path.join(sp,'results2_*.tsv')):
    for l in open(fn,encoding='utf-8'):
        p=l.rstrip('\n').split('\t')
        if p[0] in('OK','ALREADY','ERROR'): done.add(p[3].split(' (')[0])
def gone(p): 
    parts=p.split('/')
    return any('/'.join(parts[:k]) in done for k in range(1,len(parts)))
rows=[r for r in list(csv.reader(open(os.path.join(sp,'comparatie.csv'),encoding='utf-8-sig'),delimiter=';'))[1:] if not gone(r[1]) and r[4] not in donefiles]
c=collections.Counter(); g=collections.Counter()
for r in rows: c[r[0]]+=1; g[r[0]]+=float(r[2])
for k in c: print(f"RAMAS {k}: {c[k]} fisiere, {g[k]/1000:.2f} GB")
bad=collections.Counter(); size=collections.Counter(); cnt=collections.Counter(); samp={}
for st,p,mb,lp,i in rows:
    parts=p.split('/')
    for k in range(1,len(parts)):
        f='/'.join(parts[:k]); size[f]+=float(mb); cnt[f]+=1
        if st!='EXISTA_LOCAL': bad[f]+=1
        if f not in samp or p.count('/')<samp[f][0].count('/'): samp[f]=(p,i)
full={f for f in size if bad[f]==0 and f.count('/')>=1}  # nu stergem radacini (My PC, Contul meu Drive)
maxi=[f for f in full if '/'.join(f.split('/')[:-1]) not in full]
loose=[(p,float(mb),i) for st,p,mb,lp,i in rows if st=='EXISTA_LOCAL' and not any('/'.join(p.split('/')[:k]) in full for k in range(1,p.count('/')+1))]
tasks=[{"folder":f,"title":f.split('/')[-1],"gb":size[f]/1000,"sample_file_id":samp[f][1],"hops_up_from_parent":samp[f][0].count('/')-f.count('/')-1} for f in sorted(maxi,key=lambda f:-size[f])]
json.dump(tasks,open(os.path.join(sp,'tasks3.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=0)
json.dump([{"id":i,"gb":mb/1000,"path":p} for p,mb,i in sorted(loose,key=lambda x:-x[1])],open(os.path.join(sp,'files3.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=0)
print("foldere de sters:",len(tasks),f"{sum(t['gb'] for t in tasks):.2f} GB")
print("fisiere izolate:",len(loose),f"{sum(x[1] for x in loose)/1000:.2f} GB")
