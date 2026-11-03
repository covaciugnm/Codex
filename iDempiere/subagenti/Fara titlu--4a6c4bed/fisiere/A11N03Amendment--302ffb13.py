import pathlib,json,hashlib,datetime
R=pathlib.Path('Z:/00.Roboti/EVA.Pro/Eva-contab/Audit_P01_2026-11-01/executie/R12_fisiere')
B=R/'A05_N05_lot03'; O=R/'A11/Val03_preflight'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p): return {'path':str(p),'sha256':sha(p)}
def save(name,x):
 p=O/name
 assert not p.exists(),p
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 return ref(p)
core=pathlib.Path('D:/CodexWork/a05-r12-native-cache/org.adempiere.base_13.0.0.202603090043.jar')
assert sha(core)=='86c82f54299f55e8f5089e0c48f13dc29432fdecec205a51560eb48dc54ac8c3'
assert sha(B/'Addendum_N03_nativ_v1.json')=='f2e538a546bdb8a381a9bbb288d9a0e3d6401aa4d52d064632ca2b35016f8797'
assert sha(B/'Readback_independent_dupa_business_v1.json')=='169e259af482179fcc41bfe2bbacc5a0957729773da4a3307d5e25c8b00668cb'
evidence=[ref(B/n) for n in ['Addendum_N03_nativ_v1.json','MPInstance_bytecode_native13.txt','business_v1.stdout.txt','business_v1.stderr.txt','business_v1.A05N05Probe.java','Readback_independent_dupa_business_v1.json','Protocol_N05_nativ_v2.json']]+[ref(core)]
r=save('Amendament_A11_N03_refuz_nativ_v1.json',{
 'reviewer':'A11 independent','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':'df85d33c1648ce2b2df130a60a05ef696e2e5480',
 'disposition':'ACCEPTAT amendament nominal de oracol; continuare N03/R01/C01 autorizată în domeniul protocolului, fără notă de produs',
 'evidence':evidence,
 'independent_method':'Lectură independentă bytecode MPInstance din core original rehashuit, stack efectiv și readback al executorului. Nicio conectare A11 la PG, nicio reproducere business proprie revendicată.',
 'correction':'Prima identificare comunicată ProcessAccess/processItPermission era inexactă. Stackul și bytecode-ul indică CannotAccessProcess în MPInstance.setAD_Process_ID, invocat din constructorul MPInstance prin MProcess.processIt și ProceseEcran. AD_PInstance=0. Nicio modificare retroactivă a jurnalelor.',
 'oracle':['ProceseEcran.ok=false și mesaj complet exact al CannotAccessProcess, formatat cu numele procesului și al rolului conform limbii contextului; bytecode-ul include traducere + / + Name în limba ne-bază.','Numărul de instanțe persistente rămâne neschimbat; stocul G2, jurnalul, stocul nativ și Fact_Acct aferente fixturii rămân identice.','Rolul permis are baseline pozitiv distinct; rolul Web Service Execution refuzat rămâne context injectat de laborator, fără autentificare UI demonstrată.'],
 'interpretation':'Refuzul nativ anterior este comportament corect pentru cerința de acces. Oprirea business_v1 este nepotrivirea oracolului EVA prea îngust, nu defect de produs. Nu se ocolește protecția nativă pentru a atinge garda EVA.',
 'readback_limit':'Readback-ul din conexiune SQL separată este o probă a executorului verificată documentar de A11, nu o conexiune independentă a lui A11. Patru instanțe seriale, cinci mișcări incluzând inițializarea, 10 piese/0 seturi, BOM2, nativeQty10, zero Fact_Acct.',
 'no_credit':['NotaSetWmsProces.R_DREPT nu este atins de N03','Nu se dovedește login/ZK/RBAC integral','Nu se închid N05/T355/C03/C10 ori vreunul din cele 17 contracte'],
 'next':['Păstrează business_v1 și protocolul v2 imuabile; probe noi în ediție nouă.','Revalidează identitățile și starea fixturii seriale; nu repeta S01/S02/N01/N02 fără motiv.','Execută N03 cu oracolul corect și fixturi noi pentru rollback/retry și concurență, cu aceleași canarii, binding real, SurseTest=null, PID/Trx și invizibilitate înainte de barieră.','Recepția finală cere sigiliul executorului, efecte persistente și cleanup raportat.']})
s=save('SIGILIU_Amendament_A11_N03_v1.json',{'files':[r],'algorithm':'SHA256','immutable':True})
print(json.dumps({'report':r,'seal':s},ensure_ascii=False))
