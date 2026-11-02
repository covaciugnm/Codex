from readgit import *
i=json.loads((w/'hits.json').read_text(encoding='utf8'))
for k,patt in [('T22-doc','adresaZoom|Record_UU|Action=Zoom|R7|linkul|fereastră nouă'),('T22-chan','valoarea efectivă|valoare efectivă|suprascris|nesuprascris|moștenir|nativă')]:
 print(k)
 ct=0
 for v in i[k]:
  for pos,l in v['hits']:
   if re.search(patt,l,re.I) and ct<16:
    j=re.search(patt,l,re.I);print(v['path'].split('/')[-1],pos,l[max(0,j.start()-35):j.start()+155]);ct+=1

