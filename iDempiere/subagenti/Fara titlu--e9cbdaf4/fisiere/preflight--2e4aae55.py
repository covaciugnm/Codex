import pathlib,json,collections,datetime
O=pathlib.Path(__file__).parent;E=O.parent;F=E/'R3'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
ctr=collections.Counter();ex={};types=collections.Counter();repeat=collections.Counter();n=0;recovered=collections.Counter();un=[];oldchange=[];fc={};not_exec=collections.Counter()
for rr in rd(F/'A12_raport.json')['records']:
 d=rd(F/rr['file']);j2=None if d['task']=='T352' else rd(E/'R2'/rr['file']);raw=d['R3_new_criteria'];group=collections.Counter(c['kind'] for c in raw);n+=len(raw)
 if rr['unknown_R2'] and raw:recovered.update([tuple(sorted(set(group)))])
 if d['functional_criteria_unidentified']:un.append(d['task'])
 if j2:
  o={c['id']:c for c in j2['operative_criteria_and_audit_criteria']}
  for c in d['operative_criteria_and_audit_criteria']:
   if c!=o[c['id']]:oldchange.append([c['id'],[k for k in set(c)|set(o[c['id']]) if c.get(k)!=o[c['id']].get(k)]])
 for c in raw:
  k=(c['kind'],c['current']['status']);ctr[k]+=1
  ex.setdefault(k,[]);ex[k].append((c['id'],str(c['normative_content'])[:110])); repeat['oracle_equal']+=c['expected_oracle'].strip()==c['normative_content'].strip();repeat['no_current_evidence']+=not c['current']['evidence_ids'];not_exec[c.get('next_action','')]+=1
print('new',n,'oldchanged',oldchange,'recovered',recovered,'25unknown',un)
for k,n in ctr.most_common():print(n,k,ex[k][:2])
print('counters',repeat)

