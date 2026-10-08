from research_bi import ROOT
import pathlib,subprocess,json,re,hashlib
G=r'C:/Users/User/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/cmd/git.exe'
R=pathlib.Path(__file__).parent/'eva-bi-docs';SHA='1c039193e0c1626cb03fb8ca37f9980a1703fd0c'
def git(*a):return subprocess.check_output([G,'-C',str(R),*a])
paths=git('ls-tree','-r','--name-only',SHA).decode().splitlines()
out=ROOT/'03_Audit_Eva_Accounting';out.mkdir(parents=True,exist_ok=True)
selected=['README.md','AGENTS.md','backend/app/routers/reports.py','backend/app/ai_assistant/catalog.py','backend/app/ai_assistant/service.py','backend/app/ai_assistant/gateway.py','backend/app/routers/fiscal_profile.py','backend/docs/AI_ASSISTANT_INTEGRATION.md','backend/app/ai/client.py']
selected += [p for p in paths if p.startswith('idempiere/plugins/com.eva.ro.contab/src/') and re.search('Dashboard|Profil|AI[A-Z]|Balanta|Bilant|Situati|Indicator|Cash|Analiz',p)]
records=[]
for p in selected:
 try:
  data=git('show',SHA+':'+p);dest=out/'cod_verificat'/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
  records.append({'path':p,'sha256':hashlib.sha256(data).hexdigest(),'url':f'https://github.com/cesiroproduction/Eva-Accounting/blob/{SHA}/{p}'})
 except subprocess.CalledProcessError:pass
(out/'commit_si_fisiere.json').write_text(json.dumps({'branch':'fix/116-remediere-izolare-multifirma','commit':SHA,'files':records},indent=2),encoding='utf-8')
(out/'inventar_cai_aplicatie.txt').write_text('\n'.join(p for p in paths if p.startswith(('backend/app/','idempiere/plugins/com.eva.ro.contab/src/','frontend/portal/'))),encoding='utf-8')
print('\n'.join(x['path'] for x in records))
