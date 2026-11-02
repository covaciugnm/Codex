from a12_r8_static import *
tail=script.split('echo "T204_C20"',1)[1];src=script[:script.index('for k in old head')]+'''BB=ae18abdfd7; VV=2eac815f7a
echo "T204_C20"'''+tail
p=subprocess.run(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151','bash','-s'],input=src.encode(),capture_output=True,timeout=65);q=P/'T204_T171_predicate_tail.log';q.write_bytes(p.stdout+p.stderr);print(p.returncode,p.stdout.decode())

