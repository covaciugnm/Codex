from a12_r10_lease import *
w=current();pro=ssh('cd '+w+' && test -f supervisor-log && test ! -e A12-ui-restore.private && touch finish');pro.check_returncode()
for it in range(35):
 s=ssh("cd "+w+" && tail -5 supervisor-log; docker ps -a -q --filter label=eva.sesiune=eva-contab-codex-p01a12r10t06")
 if 'CLEANED'in s.stdout.decode():break
 time.sleep(2)
dat=ssh('cd '+w+' && tail -12 supervisor-log; printf "owned containers count=";docker ps -a -q --filter label=eva.sesiune=eva-contab-codex-p01a12r10t06 | wc -l; test ! -e db-secret && echo "secret file removed"');v=dat.stdout.decode('utf8','replace');f=P10/'T06_laborator_restituit.txt';f.write_text(v,encoding='utf8');print(sha(f),v[-620:]);assert 'CLEANED'in v and 'owned containers count=0'in v and 'secret file removed'in v

