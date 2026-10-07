@echo off
 echo Dracula Design: http://127.0.0.1:4181/
 echo Dracula Food:   http://127.0.0.1:4183/
 echo Lasa aceasta fereastra deschisa pentru acces la server.
 "%WINDIR%\System32\OpenSSH\ssh.exe" -o ExitOnForwardFailure=yes -N -L 4181:127.0.0.1:4181 -L 4183:127.0.0.1:4183 saga-server@192.168.100.151
 pause
