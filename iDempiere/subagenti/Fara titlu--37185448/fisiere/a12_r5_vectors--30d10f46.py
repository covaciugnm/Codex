from a12_r5_calibrated import *
from lxml import etree
import json,zipfile,datetime
o=E/'R5/vectors';o.mkdir(exist_ok=True);src=o/'VecteursP01.java'
body='''import java.math.*; import java.time.*; import java.util.*; import com.eva.ro.contab.corelare.*; import com.eva.ro.contab.reges.RegesXsd;
public class VecteursP01 {
 static BigDecimal b(String x){return new BigDecimal(x);} static void r(String id,Object x){System.out.println(id+"\\t"+x);}
 public static void main(String[]args){LocalDate d=LocalDate.of(2026,11,30); for(String n:new String[]{"10","0","-1","abc","36501"}){try{r("days/"+n,Fefo.termenDinZile(d,n));}catch(RuntimeException e){r("days/"+n,e.getClass().getSimpleName());}}
 var lots=List.of(new LoturiArticole.Lot(41,"EX",d.minusDays(1),b("9")),new LoturiArticole.Lot(42,"TODAY",d,b("3")),new LoturiArticole.Lot(43,"TOMORROW",d.plusDays(1),b("4")),new LoturiArticole.Lot(44,"NO_DATE",null,b("10")));for(String qty:new String[]{"2","4","9","11","0"}){var lot=Fefo.propus(lots,b(qty),d);r("lot/"+qty,lot==null?"NONE":lot.asi());}for(var c:Fefo.Cale.values()){r("expires/"+c,Fefo.decizieExpirat(c,d.minusDays(1),d,false,false));r("reverse/"+c,Fefo.decizieExpirat(c,d.minusDays(1),d,true,false));}
 for(String n:List.of("NivelStudii","TipActIdentitate")){var v=new TreeSet<>(RegesXsd.valori(n));r("xsd/"+n,String.join("|",v));}
 r("stock/basic", FisaCanalCalcul.stocCalculat(List.of(b("10"),b("15")),b("4"),b("3"),2,Map.of()));r("stock/rule", FisaCanalCalcul.stocCalculat(List.of(b("10"),b("15")),b("4"),b("3"),2,Map.of(RegulaStocCanal.PROCENT,"50")));r("stock/no-negative",FisaCanalCalcul.stocCalculat(List.of(b("3")),b("4"),b("3"),2,Map.of()));r("gross/add-tax",FisaCanalCalcul.pretBrut(b("10.01"),b("0.21"),false));r("gross/includes-tax",FisaCanalCalcul.pretBrut(b("10.01"),b("0.21"),true)); r("gross/null",FisaCanalCalcul.pretBrut(null,b("0.21"),false));}}
''';src.write_text(body,encoding='utf8');ex={'days/10':'2026-12-10',**{'days/'+n:'Refuz'for n in ['0','-1','abc','36501']},'lot/2':'42','lot/4':'43','lot/9':'44','lot/11':'NONE','lot/0':'NONE','expires/VANZARE':'REFUZ','expires/CONSUM':'AVERTISMENT','expires/TRANSFER':'AVERTISMENT','expires/INVENTAR':'AVERTISMENT','expires/INTRARE':'OK',**{'reverse/'+n:'OK'for n in ['VANZARE','CONSUM','TRANSFER','INVENTAR','INTRARE']},'stock/basic':'16','stock/rule':'8','stock/no-negative':'0','gross/add-tax':'12.11','gross/includes-tax':'10.01','gross/null':'null'}
xsd=plug/'META-INF/reges/reges2025.xsd';tree=etree.parse(str(xsd));ns={'xs':'http://www.w3.org/2001/XMLSchema'}
for n in ['NivelStudii','TipActIdentitate']:
 vals=tree.xpath("//xs:simpleType[@name=$n]//xs:enumeration/@value",n=n,namespaces=ns);assert len(vals)in (13,16);ex['xsd/'+n]='|'.join(sorted(vals))
# Save oracle before compilation or observation, distinct from the evidence and its adapter.
wr(o/'oracole.json',{'reference_date':'2026-11-30','warehouse_fixture':{'positive_stock':[10,15],'reserved':4,'orders':3,'reserve':2,'rule':'first 16, then 50% = 8'},'xsd_source':str(xsd.relative_to(repo)),'xsd_sha256':sha(xsd),'expected':ex})
res=[]
for tag,jar in [('git',sec/'cod-master-contab.jar'),('instalat',sec/'com.eva.ro.contab_13.0.0.jar')]:
 dest=temp/('vectors_'+tag);dest.mkdir(exist_ok=True);cp=';'.join([str(dest),str(jar),str(base),str(next(sec.glob('org.adempiere.base.process_*.jar'))),'D:/CodexWork/eva-a01-java/lib/*','D:/CodexWork/a05-support-jars/*',str(plug/'src')]);cc=cmd([java/'javac.exe','-encoding','UTF-8','-proc:none','-sourcepath','','-cp',cp,'-d',dest,src]);assert not cc.returncode,cc.stdout
 qq=cmd([java/'java.exe','-Dline.separator=\n','-Djava.security.manager','-Djava.security.policy=='+pol.as_uri(),'-Dfile.encoding=UTF-8','-Dstdout.encoding=UTF-8','-Dstderr.encoding=UTF-8','-cp',cp,'VecteursP01']);lo=o/(tag+'.log');lo.write_text(qq.stdout,encoding='utf8');obs={s.split('\t',1)[0]:s.split('\t',1)[1]for s in qq.stdout.splitlines()if '\t'in s and s.split('\t',1)[0]in ex};assert not qq.returncode and set(obs)==set(ex),(qq.stdout[-300:],set(ex)-set(obs));res.append({'target':tag,'jar_sha':sha(jar),'source_sha':sha(src),'exit':qq.returncode,'log':lo.name,'log_sha':sha(lo),'observed':{k:{'expected':val,'observed':obs[k],'matches_independent_oracle':val==obs[k]}for k,val in ex.items()}})
wr(o/'rezultate.json',res);print([(v['target'],len(v['observed']),[k for k,x in v['observed'].items()if not x['matches_independent_oracle']])for v in res])

