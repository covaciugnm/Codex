$root=(Get-Item '.\iFLYTEK_XF-AIGlasses-01_Documentatie\Software\Biblioteca_Glasses').FullName
$base='https://a2sgp-ota-ap1.iflyoversea.com/a2-sg-bucket/62caabf368613a33146a964ab862bec3/attachment/'
$tasks=@(@('AINOTE macOS',($base+'AINOTE.dmg'),'AINOTE.dmg'),@('AINOTE Windows',($base+'AINOTE.exe'),'AINOTE.exe'),@('AINOTE Android',($base+'app-release.apk'),'AINOTE-Android.apk'),@('AINOTE Screen Casting macOS',($base+'EinkMirrorTool.pkg'),'EinkMirrorTool.pkg'),@('AINOTE Screen Casting Windows',($base+'EinkMirrorTool.zip'),'EinkMirrorTool.zip'),@('Loomy Android','https://loomy.xunfei.cn/api/download?platform=android','Loomy-Android.apk'))
$rows=$tasks | ForEach-Object -Parallel {
 $t=$_; $p=Join-Path $using:root ('Aplicatii/'+$t[2]); $status='descarcat';$err='';$bytes=0;$hash=''
 try {Invoke-WebRequest $t[1] -OutFile ($p+'.part') -TimeoutSec 240 -ErrorAction Stop; Move-Item -LiteralPath ($p+'.part') -Destination $p -Force; $bytes=(Get-Item $p).Length; $hash=(Get-FileHash $p -Algorithm SHA256).Hash}catch{$status='indisponibil';$err=$_.Exception.Message}
 [pscustomobject]@{category='Aplicatii';title=$t[0];url=$t[1];file=('Aplicatii/'+$t[2]);scope='Aplicatie oficiala; descarcata, nu instalata';status=$status;bytes=$bytes;sha256=$hash;error=$err}
} -ThrottleLimit 6
$rows | ConvertTo-Json -Depth 4 | Set-Content (Join-Path $root 'manifest-aplicatii.json') -Encoding utf8
$rows | Select-Object title,status,bytes,error | ConvertTo-Json
