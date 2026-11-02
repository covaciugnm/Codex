from a03_r8_jvm import *
def main():
 d=work/'trace58';d.mkdir(exist_ok=True)
 n='TestT58Inchidere';src=plug/'test'/(n+'.java');original=src.read_text(encoding='utf8');s=original.replace('static void chk(String m, boolean c) {','static void chk(String m, boolean c) {\n        System.out.println("R8 " + (c ? "OK " : "FAIL ") + m);',1)
 assert len(s)-len(original)==len('\n        System.out.println("R8 " + (c ? "OK " : "FAIL ") + m);');f=d/(n+'.java');f.write_text(s,encoding='utf8');res=[]
 for lab,jar in [('git','cod-master-contab.jar'),('installed','com.eva.ro.contab_13.0.0.jar')]:
  dst=d/(lab+"-clean");dst.mkdir(exist_ok=True);cp=os.pathsep.join(str(q) for q in [dst,work/lab,P('D:/CodexWork/a03-r4-runtime')/lab,sec/jar,sec/'org.adempiere.base_13.0.0.202603090043.jar',sec/'org.adempiere.base.process_13.0.0.202603090043.jar',P('D:/CodexWork/a05-support-jars/*'),P('D:/CodexWork/eva-a01-java/lib/*'),plug/'src'])
  c=sp.run([jdk/'javac.exe','-proc:none','-encoding','UTF8','-sourcepath','','-cp',cp,'-d',dst,f],cwd=plug,capture_output=True);assert c.returncode==0,c.stderr
  rr=sp.run([jdk/'java.exe','-Dstdout.encoding=UTF-8','-Dfile.encoding=UTF-8','-Djava.security.manager','-Djava.security.policy=='+(work/'R8.policy').as_uri(),'-cp',cp,n],cwd=plug,capture_output=True,timeout=55);b=rr.stdout+rr.stderr;l=out/'log'/('trace-'+lab+'-'+n+'.txt');l.write_bytes(b);lines=b.decode('utf8',errors='replace').splitlines();res.append({'jar':jar,'jar_sha256':H((sec/jar).read_bytes()),'rc':rr.returncode,'raw':str(l.relative_to(out)),'raw_sha256':H(b),'assertions':[x for x in lines if x.startswith('R8 ')],'tail':[x for x in lines if 'REZULTAT' in x]});print(lab,rr.returncode,res[-1]['tail'])
 J(out/'Trasare_T58_254_asertiuni.json',{'utc':UTC(),'sha':sha,'fixture_path':str(src.relative_to(root)),'fixture_sha':H(src.read_bytes()),'instrumented_sha':H(f.read_bytes()),'change':'O instrucțiune System.out.println adăugată în metodă chk a unei copii de laborator a TESTULUI, pentru vizibilitatea cazului; predicatul original, condiția, codul de terminare și JAR-ul nu sunt modificate. Comparat cu rularea R4 nemodificată.','results':res})
if __name__=='__main__':main()

