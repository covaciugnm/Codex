import getpass, json, pathlib, sys
import paramiko

root = pathlib.Path(__file__).resolve().parent
client = paramiko.SSHClient()
client.load_host_keys(str(pathlib.Path.home()/'.ssh'/'known_hosts'))
client.connect('192.168.100.166', username='cesirothor', password=getpass.getpass('SSH password: '), timeout=15, look_for_keys=False, allow_agent=False)
print('READY', flush=True)
for line in sys.stdin:
    try:
        req=json.loads(line)
        if req['action']=='exec':
            _, out, err=client.exec_command(req['command'], timeout=90)
            result={'stdout':out.read().decode('utf-8','replace'),'stderr':err.read().decode('utf-8','replace'),'exit':out.channel.recv_exit_status()}
            if req.get('save'):
                (root/req['save']).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
            print(json.dumps(result,ensure_ascii=False),flush=True)
        elif req['action']=='source':
            sftp=client.open_sftp()
            _,out,_=client.exec_command('cd /home/cesirothor/openfyxer && git ls-files -z')
            names=out.read().decode().split('\0')
            count=0
            for name in names:
                p=pathlib.PurePosixPath(name)
                if not name or p.is_absolute() or '..' in p.parts or any(x.startswith('.env') for x in p.parts): continue
                if p.suffix.lower() in {'.png','.jpg','.jpeg','.ico','.mp3','.mp4','.pdf','.zip','.gz','.apk','.keystore','.jks','.pem','.key','.dump','.sql'}: continue
                remote='/home/cesirothor/openfyxer/'+name
                try:
                    if sftp.stat(remote).st_size>4_000_000: continue
                    local=root/'source'/name
                    local.parent.mkdir(parents=True,exist_ok=True)
                    sftp.get(remote,str(local)); count+=1
                except OSError: pass
            sftp.close()
            print(json.dumps({'copied':count}),flush=True)
    except Exception as e: print(json.dumps({'error':str(e)}),flush=True)
