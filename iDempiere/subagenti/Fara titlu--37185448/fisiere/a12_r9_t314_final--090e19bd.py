from a12_r9_git_controls import shell
from a12_r9_orig import *
lines=shell.splitlines()
pre=shell[:shell.index('echo "START T06"')]
tail=shell[shell.index('echo "START T314"'):];tail=tail.replace('for target in 11c03ac3e1 "$cut";do',"""for target in d01ab3d2c2b 6e83fd73fa6;do 
 parent=$(git rev-parse "$target^1"); z=0; git merge-base --is-ancestor "$target" "$cut" || z=$?; echo "candidate=$target ancestor-of-cut=$z parent=$parent";""").replace('"$target" 4f3614927d','"$target" "$parent"')
s=pre+tail
r=subprocess.run(['ssh','-o','BatchMode=yes','saga-server@192.168.100.151','bash','-s'],input=s.encode(),capture_output=True,timeout=160);p=P9/'T314_final_integrare_A.log';p.write_bytes(r.stdout+r.stderr);print(sha(p),r.returncode);print([ln for ln in r.stdout.decode().splitlines()if 'ancestor-of-cut'in ln or 'K-25 rânduri'in ln or 'arbor'in ln])

