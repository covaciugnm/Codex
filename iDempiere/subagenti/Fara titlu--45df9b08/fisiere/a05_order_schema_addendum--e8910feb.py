from pathlib import Path
import json,subprocess,os,hashlib,datetime,sys
sys.path.insert(0,'D:/CodexWork/eva-a01-fixture-deps');import psycopg
O=Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere/A05_Comanda_rezervare_lot05');H='df85d33c1648ce2b2df130a60a05ef696e2e5480';G='D:/CodexWork/eva-audit-p01-src-20261101';E=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0');sha=lambda b:hashlib.sha256(b).hexdigest()
ss=[]
for n in ['setup/EvaMetadata.java','corelare/CorelareTabele.java','corelare/OperatiiCanale.java','corelare/VanzariPeCanal.java']:
 p='idempiere/plugins/com.eva.ro.contab/src/com/eva/ro/contab/'+n;oid=subprocess.check_output(['git','-C',G,'rev-parse',H+':'+p],env=E).decode().strip();b=subprocess.check_output(['git','-C',G,'cat-file','blob',oid],env=E);assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid;d=O/'surse_df85'/n;d.parent.mkdir(parents=True,exist_ok=True);assert not d.exists();d.write_bytes(b);ss.append(dict(path=p,oid=oid,sha256=sha(b),owner='A05',peer='A11',state='LECTURĂ_PENTRU_RECONCILIERE',task='SHARED'))
rows={}
with psycopg.connect(host='127.0.0.1',port=56455,user='a05lab',password='[CREDENTIAL_REDACTED]',dbname='idempiere',autocommit=True) as conn:
 with conn.cursor(row_factory=psycopg.rows.dict_row) as c:
  c.execute('SET search_path=adempiere,pg_catalog');c.execute('SET default_transaction_read_only=on')
  def q(n,s,p=None):c.execute(s,p);rows[n]=c.fetchall()
  q('missing_structure',"SELECT to_regclass('adempiere.eva_canalgrupa')::text AS grupa,to_regclass('adempiere.eva_canalfunctie')::text AS functie,(SELECT count(*) FROM information_schema.columns WHERE table_schema='adempiere' AND table_name='eva_canalvanzare' AND column_name='c_campaign_id') AS campaign_col")
  q('native_channels','SELECT c_channel_id,ad_client_id,name,isactive FROM c_channel ORDER BY 1')
  q('business_before','SELECT (SELECT count(*) FROM eva_canalvanzare) AS channels,(SELECT count(*) FROM eva_sursasite) AS sources,(SELECT count(*) FROM c_order) AS orders,(SELECT count(*) FROM m_storagereservationlog) AS reservation_logs,(SELECT count(*) FROM fact_acct) AS facts')
  q('period_candidates',"SELECT p.c_period_id,p.name,p.startdate,p.enddate FROM c_period p WHERE p.ad_client_id=11 AND EXISTS(SELECT 1 FROM c_periodcontrol q WHERE q.c_period_id=p.c_period_id AND q.docbasetype='SOO' AND q.periodstatus='O') AND EXISTS(SELECT 1 FROM c_periodcontrol q WHERE q.c_period_id=p.c_period_id AND q.docbasetype='MMS' AND q.periodstatus='O') ORDER BY p.enddate DESC LIMIT 2")
  q('b2b_structural_count',"SELECT (SELECT count(*) FROM information_schema.tables WHERE table_schema=current_schema() AND table_name='eva_canalgrupa') + (SELECT count(*) FROM information_schema.columns WHERE table_schema=current_schema() AND table_name='eva_canalvanzare' AND column_name IN ('eva_tipcanal','c_campaign_id','c_paymentterm_id','m_discountschema_id','eva_limitacredit')) AS found")
doc=dict(schema='A05.schema.reconciliation.proposal.v1',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),head=H,state='PROPUS A11, NEAPLICAT',source_schema_sha256=sha((O/'Schema_comanda_inainte_v2.json').read_bytes()),sources=ss,rows=rows,
 diagnosis='Seedul are4/6 obiecte ale SQL_STRUCTURA: lipsesc EVA_CanalGrupa și EVA_CanalVanzare.C_Campaign_ID; migrarea T211 mai creează EVA_CanalFunctie. Fără ele handlerul B2B ar ieși devreme. Nu confundăm această ieșire cu verificarea pe schemă completă.',
 proposed_steps=['Păstrează clona izolată; runtime numai Equinox dormant și canari conform gate, înaintea oricărei clase de migrare.',
 'Înregistrează CodeSource/clasele originale și context separat de instalare System client0/org0/user100/role0 verificat în seed; aceasta este instalare de laborator, nu actorul comercial.',
 'Apelează reflectiv metodele originale package-private EvaMetadata.ensureT214(ctx,null,Rezultat) și ensureT211Canale(ctx,null,Rezultat), în această ordine, fără ensureAll și fără EvaActivator. Null trx este calea originală admisă pentru tranzacții locale de metadate; toate schimbările se măsoară independent.',
 'ensureT214 asigură C_Channel original pe fiecare client sintetic; ensureT211 folosește ensureTabelaSpec → AD_Table/AD_Column + CreateTable/ColumnSync, indexuri originale protejeazaT211 și jurnal. Tabelele de canal au0 rânduri înainte, deci completeazaCanale nu ar trebui să creeze campanii comerciale.',
 'Codul original ensureT214 conține set_ValueNoCheck pentru clientul C_Channel; nu este un bypass introdus de harness și nu se folosește la fixturea business. Acest detaliu cere acceptare explicită a auditorului pentru migrarea exactă.',
 'Consemnează Rezultat.log și count, diff AD_Table/AD_Column/AD_Sequence/AD_ChangeLog/schema/indexuri și C_Channel/C_Campaign plus business_before. Nu accepta doar metoda returnată: nicio lipsă structurală, niciun mesaj de eroare nemotivat. A doua apelare originală cere0 obiecte noi și nicio schimbare de rând business.',
 'Oprește JVM de migrare și repornește JVM business cu GardenAdmin101/role102 și toate handler-ele originale. Repetă schema/readiness, SQL_STRUCTURA=6 și canalPartenernull pentru grupa BP aleasă. Niciun cache patch.',
 'Dacă helperul original are dependențe suplimentare sau alterări nereconciliate, oprește înainte de A/B și propune addendum; fără SQL DDL improvizat.'],
 scope='Numai migrarea nominală T214/T211 în clonă sintetică proprie; nu implementare de produs, nu migrare operațională, nu recepție T211/T214/T316 integrală.',
 runtime_business_started=False,operational_writes=0)
f=O/'Propunere_reconciliere_schema_T211_v1.json';assert not f.exists();f.write_text(json.dumps(doc,default=str,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(dict(sha256=sha(f.read_bytes()),missing=rows['missing_structure'],b2b=rows['b2b_structural_count'])))
