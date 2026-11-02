from a12_r8_arch import *
import a12_r8_arch as arch
root='Documentatie/echipa-2026-10-09/'
patterns=['T22-*','T211-*','T212-*','T213-*','T214-*','T216-*','T310-*','T351-*']
sub=git('ls-tree -d --name-only '+BASE+':'+root.rstrip('/')).decode().splitlines()
dirs=[root+z for z in sub if any(PurePosixPath(z).match(pt)for pt in patterns)]
target=Path('D:/CodexWork/a12-r8-morearchive');target.mkdir(exist_ok=True);arch.pool=target;arch.folders=lambda:dirs
if __name__=='__main__':arch.build()

