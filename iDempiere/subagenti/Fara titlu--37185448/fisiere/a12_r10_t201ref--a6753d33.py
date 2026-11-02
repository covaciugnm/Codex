from a12_r10_base import *
s=git('log --all --format=%h%x09%s -i --grep='+shlex.quote('T201.*[Ii]ntegra')+' -20').decode();print(s[:2400])

