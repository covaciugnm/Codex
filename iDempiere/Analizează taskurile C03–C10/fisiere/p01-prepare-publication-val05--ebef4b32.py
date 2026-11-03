from pathlib import Path
import json
D=Path('D:/CodexWork')
source=(D/'p01-publish-r12-val04.py').read_text(encoding='utf-8')
replacements={
 'Publicare_R12_Val04':'Publicare_R12_Val05',
 'r12-lot04':'r12-lot05',
 "else '<!--r12-lot03-->'":"else '<!--r12-lot04-->'",
 '2026-11-03 01:43 UTC':'2026-11-03 02:45 UTC',
 '8c0695de36b50ede569c6d318715db0af11fcbff':'c594a93a1d4e606f8c2e432108a29e97244d692e',
 'serverului8c0695':'serverului c594a93a',
 "d['latest_G3_native']=cfg['G3_native'];d['latest_frontend_catalog']=cfg['frontend_catalog']":"d['latest_native_order']=cfg['native_order'];d['latest_backend_catalog_pagination']=cfg['backend_catalog_pagination']",
}
for old,new in replacements.items():
 assert old in source,old
 source=source.replace(old,new)
out=D/'p01-publish-r12-val05.py'
assert not out.exists()
out.write_text(source,encoding='utf-8')
qa=(D/'p01-r12-qa-val04.py').read_text(encoding='utf-8').replace('Publicare_R12_Val04','Publicare_R12_Val05').replace('r12-lot04','r12-lot05')
out=D/'p01-r12-qa-val05.py';assert not out.exists();out.write_text(qa,encoding='utf-8')
print(json.dumps({'prepared_only':['p01-publish-r12-val05.py','p01-r12-qa-val05.py'],'published':False}))
