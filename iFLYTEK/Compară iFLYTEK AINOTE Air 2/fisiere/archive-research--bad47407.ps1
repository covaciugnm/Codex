$ErrorActionPreference='Stop'
$root=$PSScriptRoot
$dest=Join-Path $root 'Biblioteca_Glasses'
New-Item -ItemType Directory -Force -Path $dest | Out-Null
$items=@(
@('Documentatie','Politica aplicatiei iFLYTEK','https://saas-public.ioss.xfinfr.com/private/config/privacy-policy.html','politica.html','Oficial; ochelari si casti'),
@('Documentatie','Lista SDK din aplicatie','https://saas-public.ioss.xfinfr.com/private/config/third-party.html','sdk-terti.html','Oficial'),
@('Documentatie','Pagina descarcare Translation','https://m.iflytranslate.com/','translation.html','Oficial; pagina dinamica, folositi APK-ul local'),
@('Documentatie','AINOTE Skill - producator','https://theainote.com/en-ca/pages/ainote-skill','ainote-producator.html','Oficial; Air 2 si AINOTE 2'),
@('Documentatie','Loomy - pagina oficiala','https://loomy.xunfei.cn/','loomy.html','Oficial; aplicatie partenera GlassClaw'),
@('Documentatie','Loomy - modificari versiuni','https://loomy.xunfei.cn/changelog','loomy-changelog.html','Oficial'),
@('Documentatie','Loomy - MCP toolbox','https://loomy.xunfei.cn/docs/user-guide/toolbox','loomy-mcp.html','Oficial'),
@('Documentatie','AIKIT SDK - prezentare','https://aikit.xfyun.cn/docs/sdk/overview/','aikit-prezentare.html','Oficial; AI, nu driver XF'),
@('Documentatie','AIKIT SDK Android','https://aikit.xfyun.cn/docs/sdk/android/','aikit-android.html','Oficial; AI, nu driver XF'),
@('Documentatie','AIKIT SDK iOS','https://aikit.xfyun.cn/docs/sdk/ios/','aikit-ios.html','Oficial; AI, nu driver XF'),
@('Documentatie','AIKIT SDK C/C++','https://aikit.xfyun.cn/docs/sdk/c-cpp/','aikit-c-cpp.html','Oficial; AI, nu driver XF'),
@('Documentatie','AIUI SDK','https://doc.iflyos.cn/aiui/sdk/','aiui.html','Oficial; AI, nu driver XF'),
@('Documentatie','XFyun CLI','https://www.xfyun.cn/xfyun-cli/doc','xfyun-cli.html','Oficial; servicii cloud'),
@('Documentatie','Glance Android SDK','https://www.oneglance.cn/docs/sdk/android/intro.html','glance.html','Alt producator; compatibilitate XF neconfirmata')
)
$repos=@(
@('iflyink/ainote','Oficial; integrare AINOTE'),
@('lianshuang-photo/s1-voice-bridge','Comunitate; microfon S1/T8, nu ochelari XF'),
@('yinzixu03/bluetooth-mouse-mic','Comunitate; mouse cu microfon, compatibilitate XF neconfirmata'),
@('GuoZhuang-cn/HuaweiEyewearLiveTranscribe','Comunitate; Huawei, compatibilitate XF neconfirmata'),
@('ebowwa/HeyCyanSmartGlassesSDK','Comunitate; HeyCyan, nu SDK XF'),
@('wingsfly/glassclaw','Comunitate; RayNeo, nu GlassClaw iFLYTEK'),
@('sctg-development/ai-smart-glasses-e09','Comunitate; Eyevue E09, nu XF'),
@('buildwithfenna/rokid-docs','Comunitate; Rokid, nu XF')
)
foreach($r in $repos){$items+=,@('Cod_sursa',$r[0],('https://codeload.github.com/'+$r[0]+'/zip/HEAD'),($r[0].Replace('/','--')+'.zip'),$r[1])}
$jobs=$items | ForEach-Object -Parallel {
 $a=$_; $dir=Join-Path $using:dest $a[0]; New-Item -ItemType Directory -Force -Path $dir | Out-Null
 $path=Join-Path $dir $a[3]; $status='descarcat'; $err=''; $hash=''; $bytes=0
 try { if(!(Test-Path -LiteralPath $path)){Invoke-WebRequest -Uri $a[2] -OutFile ($path+'.part') -TimeoutSec 70; Move-Item -LiteralPath ($path+'.part') -Destination $path -Force}; $bytes=(Get-Item -LiteralPath $path).Length; $hash=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash } catch {$status='indisponibil'; $err=$_.Exception.Message}
 [pscustomobject]@{category=$a[0];title=$a[1];url=$a[2];file=($a[0]+'/'+$a[3]);scope=$a[4];status=$status;bytes=$bytes;sha256=$hash;error=$err}
} -ThrottleLimit 6
$list=[Collections.Generic.List[object]]::new(); foreach($j in $jobs){$list.Add($j)}
$appDir=Join-Path $dest 'Aplicatii'; New-Item -ItemType Directory -Force $appDir | Out-Null
$source=Join-Path $root 'Cercetare_SDK_2026-10-30/iflytranslate-official.apk'
$target=Join-Path $appDir 'iflytranslate-official.apk'
if(!(Test-Path -LiteralPath $target)){Copy-Item -LiteralPath $source -Destination $target}
$list.Add([pscustomobject]@{category='Aplicatii';title='iFLYTEK Translation Android';url='https://m.iflytranslate.com/download/android/FY10010010';file='Aplicatii/iflytranslate-official.apk';scope='Aplicatia oficiala; include componenta Bluetooth pentru ochelari';status='descarcat';bytes=(Get-Item $target).Length;sha256=(Get-FileHash $target -Algorithm SHA256).Hash;error=''})
$list.Add([pscustomobject]@{category='Aplicatii';title='iFLYTEK Translation iOS';url='https://apps.apple.com/app/id6739250870';file='';scope='Instalare din App Store; nu a fost identificat IPA public';status='doar link oficial';bytes=0;sha256='';error=''})
$research=Join-Path $dest 'Cercetare'; New-Item -ItemType Directory -Force $research | Out-Null
Get-ChildItem (Join-Path $root 'Cercetare_SDK_2026-10-30') -File | Where-Object Extension -ne '.apk' | ForEach-Object {
 Copy-Item -LiteralPath $_.FullName -Destination $research -Force
 $list.Add([pscustomobject]@{category='Cercetare';title=$_.Name;url='';file=('Cercetare/'+$_.Name);scope='Referinte si rezultate ale analizei; fisierele de cod nu sunt executate';status='descarcat';bytes=$_.Length;sha256=(Get-FileHash $_.FullName -Algorithm SHA256).Hash;error=''})
}
$list | ConvertTo-Json -Depth 6 | Set-Content (Join-Path $dest 'manifest.json') -Encoding utf8
Write-Output ($list | Select-Object title,status,bytes,error | ConvertTo-Json -Depth 3)
