import json,sys,os
for wf in sys.argv[1:]:
    lab={};ev=[]
    for l in open(os.path.join(wf,'journal.jsonl'),encoding='utf-8'):
        try:e=json.loads(l)
        except:continue
        t=e.get('type')
        if t=='started': lab[e['agentId']]=e.get('label'); ev.append(('S',e.get('label'),'',e['agentId']))
        elif t in('result','error','failed'):
            r=e.get('result'); s=''
            if isinstance(r,dict):
                for k in('score','scor','nota','verdict','status','merge_ready','commit','summary'):
                    if k in r: s+=f"{k}={str(r[k])[:140]} "
                f=r.get('findings')
                if isinstance(f,list): s+=f"findings={len(f)}"
            else: s=str(r or e)[:160]
            ev.append((t[0].upper(),lab.get(e.get('agentId'),'?'),s,e.get('agentId')))
        else: ev.append((t,'','',''))
    print('=====',wf,len(ev))
    done={x[3] for x in ev if x[0] in 'RE'}
    for x in ev[-14:]: print(' ',x[0],x[1],'|',x[2])
    print('  PENDING:',[lab[a] for a in lab if a not in done][-6:])
