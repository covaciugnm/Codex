exec(open('C:/Users/User/AppData/Local/Temp/a11_r5_108.py',encoding='utf8').read().split('print(len(ls))')[0])
for c,t in ls:
 sc=c['R5_measured_scenarios'];txts=[i['result'] for i in sc]; print(c['id']+' '+c['normative_content'][:88]+' ⇒ '+' | '.join(txts[:2])[:130])

