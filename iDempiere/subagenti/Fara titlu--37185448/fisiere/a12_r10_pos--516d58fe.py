from a12_r10_base import *
from a12_r10_jvm import *
exec((Path(__file__).parent/'a12_r10_receipt.py').read_text(encoding='utf8').split("j=P10/")[0]);import subprocess
des=P10/'Zone_A08';j.J=des;j.T8=Path('D:/CodexWork/a12-r10-local/jvm')
rdir='Documentatie/echipa-2026-10-09/T351-stripe-pos-card/'
s0=rdir+'00_cerinta_proprietar.md';s1=rdir+'01b_decizii_orchestrator_r0.md';s2=rdir+'11g_decizii_orchestrator_cod_B_r2.md'
def snippet(path,matcher):
 z=subprocess.run(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151','git -C /home/saga-server/Documents/EvA-Contab show '+BASE+':'+path],capture_output=True,timeout=20);z.check_returncode();b=z.stdout;return {'repo_path':path,'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),'sha256':hashlib.sha256(b).hexdigest(),'lines':[{'n':i,'line':l[:1600],'line_sha256':hashlib.sha256(l.encode()).hexdigest()}for i,l in enumerate(b.decode().splitlines(),1)if re.search(matcher,l,re.I)][:4]}
ls=[snippet(s0,r'^\- (Sursa taskului|Cuvântul de pornire)'),snippet(s1,r'D-T351-01.*Varianta'),snippet(s2,r'10/10|montare|montat')];assert len(ls[0]['lines'])==2
def present(z):return all(k in z for k in ['P01.C10.T0027','P01.C10.T0028'])and re.search(r'(?i)se[cq]ven|pe rand',z)is not None
line=ls[0]['lines'][1]['line'];assert present(line)and not present(line.replace('P01.C10.T0027','P01.C10.T0026'))
with ThreadPoolExecutor(max_workers=2)as px:res=list(px.map(j.go,[(x,'TestT22Stripe')for x in ['git','instalat']]))
pdf=des/'T351_gates_si_suita.json';wr(pdf,{'utc':now(),'cutoff':BASE,'git':ls,'control_comparator':{'names_target_plus_next':present(line),'swap_first_target_to_T0026':present(line.replace('P01.C10.T0027','P01.C10.T0026'))},'suite':res,'limitation':'Authorisation to work appears as owner quotation transcribed in historical artifact; no direct replay of the author’s terminal; component test has synthetic sources.'})
h=[]
for k in ['git','instalat']:
 h+=lines(des/(k+'_TestT22Stripe.log'),r'^\s*(OK|FAIL).*(0 POST|card.present|card_present|terminal POS|cititor|sursa.*POS|POS.*[Ff])')[:9]
add('T351-R2-001','Confrontarea celor două decizii datate și porții de scriere','Cerința inițială 23.10 «ulterior», urmată 30.10 de pornirea explicită a taskurilor T0027/T0028 în ordine, cu deblocarea scrierilor externe distinctă.',{'source_lines':ls[0]['lines'],'disposition':ls[1]['lines'],'gate_pairs_replay':{'names_and_order':True,'swapped_first_task':False}},'Substituirea lui T0027 cu T0026 în text nu mai autorizează partida de față.','Citatul este consemnat în decizia istorică, nu o nouă instrucțiune de pornire primită astăzi. Nu este autorizarea unei plăți Stripe live.',[jr(pdf,'/git/0'),jr(pdf,'/git/1'),jr(pdf,'/control_comparator')],'documentary_or_test')
if h:add('T351-R2-002','Stripe POS, suite proprii proiectului pe două JAR și etaloane nominale','Marchează citirea card-present și blocarea scrierilor la partener; păstrează distinct încasarea, captura și rambursarea externă.',{'suite_outcomes':[(w['target'],w['exit'])for w in res],'nominal':[z['text']for z in h]},'Expedierile către Stripe nu au fost autorizate în acest audit. Suita lucrează cu obiectul de transport sintetic.','Niciun POS fizic și nicio tranzacție Stripe reală în acest test. O aterizare a comenzii pe clientul comercial și legarea plății reale nu sunt demonstrate.',[jr(pdf,'/suite')]+h,'subcase')
fp=des/'T351_receptie.json';wr(fp,{'utc':now(),'receipts':out});print(sha(fp),[(w['target'],w['exit'])for w in res])
