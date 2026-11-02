from a12_r8_cases import *
if __name__=='__main__':
 for k in ['T216-','T214-','T213-','T310-','T351-','T212-']:
  rr=[(x['file'].split('/',3)[-1],x['size'])for x in a if ('/'+k)in x['file'] and x['size']<60000];print(k,len(rr));subset=[x for x in rr if re.search(r'rezult|factur|comenzi|pl[aă]t|incas|r49|mont|cui|orig|buton|decizi|proba|verdict',x[0],re.I)];print('\n'.join(z for z,n in (subset if len(subset)<35 else subset[:8]+subset[-26:])))

