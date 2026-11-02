param([string]$Jdk='C:\Program Files\Java\jdk-21')
$ErrorActionPreference='Stop'
$root=$PSScriptRoot
if(!$root){$root=(Get-Item '.\iFLYTEK_XF-AIGlasses-01_Documentatie\Software\SDK_Experimental').FullName}
$classes=Join-Path $root 'build/classes';$tests=Join-Path $root 'build/tests';$dist=Join-Path $root 'dist'
New-Item -ItemType Directory -Force $classes,$tests,$dist | Out-Null
$sources=@(Get-ChildItem (Join-Path $root 'src') -Recurse -Filter '*.java' | ForEach-Object FullName)
& (Join-Path $Jdk 'bin/javac.exe') --release 8 -encoding UTF-8 -d $classes $sources
if($LASTEXITCODE){throw 'SDK compilation failed'}
& (Join-Path $Jdk 'bin/jar.exe') --create --file (Join-Path $dist 'ifly-glasses-experimental-0.1.0.jar') -C $classes .
if($LASTEXITCODE){throw 'JAR packaging failed'}
$testSources=@(Get-ChildItem (Join-Path $root 'tests') -Recurse -Filter '*.java' | ForEach-Object FullName)
$testSources+=Join-Path $root 'examples/BatteryQuery.java'
& (Join-Path $Jdk 'bin/javac.exe') --release 8 -encoding UTF-8 -cp $classes -d $tests $testSources
if($LASTEXITCODE){throw 'Test compilation failed'}
$cp=$classes+';'+$tests
$results=foreach($test in @('CodecTest','BridgeTest','BatteryQuery')){& (Join-Path $Jdk 'bin/java.exe') -cp $cp $test;if($LASTEXITCODE){throw "Failed: $test"}}
$results | Set-Content (Join-Path $root 'test-results.txt') -Encoding utf8
$results
