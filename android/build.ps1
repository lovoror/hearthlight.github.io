# Builds android/Hearthlight.apk out of this checkout with nothing but the
# Android SDK's own tools — no Gradle, no Android Studio, no network, no
# dependencies to install. Everything it needs is listed in android/README.md.
#
#   powershell -ExecutionPolicy Bypass -File android/build.ps1
#
# The game itself is copied straight from the repository root into the APK's
# assets/ (same files the website serves), with one edit: config.js points the
# relay at the public server, so Party Mode on a phone joins the same rooms as
# the browser build.
param(
  [string]$Sdk = $env:ANDROID_HOME,
  [string]$JavaHome = $env:JAVA_HOME,
  [string]$Relay = 'wss://vps-ec093ef6.vps.ovh.ca/ws',
  [string]$Pad = 'https://vps-ec093ef6.vps.ovh.ca/pad.html',
  [string]$Stats = '',
  [string]$Out = ''
)

$ErrorActionPreference = 'Stop'
$here = $PSScriptRoot
$root = Split-Path -Parent $here
if (-not $Sdk) { $Sdk = 'D:\sdk' }
# Any JDK 11+ will do; JAVA_HOME is not always trustworthy, so check for the real
# binary and fall back to the usual install spots before giving up.
$cands = @($JavaHome, $env:JAVA_HOME,
  (Join-Path $env:LOCALAPPDATA 'Programs\Android Studio\jbr'),
  'C:\Program Files\Android\Android Studio\jbr')
$JavaHome = $cands | Where-Object { $_ -and (Test-Path (Join-Path $_ 'bin\java.exe')) } | Select-Object -First 1
if (-not $JavaHome) { throw 'no JDK found — pass -JavaHome <jbr folder>' }
$BT = Join-Path $Sdk 'build-tools\35.0.0'
$Jar = Join-Path $Sdk 'platforms\android-35\android.jar'
$env:JAVA_HOME = $JavaHome
$env:PATH = (Join-Path $JavaHome 'bin') + ';' + $env:PATH

foreach ($tool in @('aapt2.exe', 'd8.bat', 'zipalign.exe', 'apksigner.bat')) {
  if (-not (Test-Path (Join-Path $BT $tool))) { throw "no $tool in $BT — install build-tools;35.0.0" }
}
if (-not (Test-Path $Jar)) { throw "no $Jar — install platforms;android-35" }
if (-not (Get-Command java -ErrorAction SilentlyContinue)) { throw "no java on PATH (JAVA_HOME=$JavaHome)" }

$build = Join-Path $here 'build'
$assets = Join-Path $build 'assets'
$gen = Join-Path $build 'gen'
$classes = Join-Path $build 'classes'
$dex = Join-Path $build 'dex'
if (-not $Out) { $Out = Join-Path $here 'Hearthlight.apk' }
if (Test-Path $build) { Remove-Item -Recurse -Force $build }
foreach ($d in @($build, $assets, $gen, $classes, $dex)) { New-Item -ItemType Directory -Force -Path $d | Out-Null }

function Step($n, $what) { Write-Host "`n[$n/8] $what" -ForegroundColor Cyan }
function Run($exe, [string[]]$argv) {
  & $exe @argv
  if ($LASTEXITCODE -ne 0) { throw "$exe failed (exit $LASTEXITCODE)" }
}

Step 1 'assets: the game, straight from the checkout'
python (Join-Path $root 'tools\android-icon.py')
robocopy $root $assets /E /NFL /NDL /NJH /NJS /NP `
  /XD .git .github .claude node_modules tools docs screenshots android server desktop `
  /XF *.md .gitignore .* | Out-Null
if ($LASTEXITCODE -ge 8) { throw "robocopy failed ($LASTEXITCODE)" }
# Whatever hidden working directory happens to sit in the checkout (a browser
# profile, a cache…) has no business inside the APK.
Get-ChildItem -Path $assets -Force -Directory | Where-Object { $_.Name.StartsWith('.') } |
  ForEach-Object { Write-Host "dropping $($_.Name) from assets"; Remove-Item -Recurse -Force $_.FullName }
$cfgPath = Join-Path $assets 'config.js'
$cfg = [IO.File]::ReadAllText($cfgPath)
$cfg = $cfg -replace "(?<![A-Za-z])relay:\s*'[^']*'", "relay: '$Relay'"
$cfg = $cfg -replace "(?<![A-Za-z])pad:\s*'[^']*'", "pad: '$Pad'"
# (the installer itself says nothing to the relay's counters unless asked to;
# pass -Stats https://…/hello to match the website's hello-on-boot)
if ($Stats) { $cfg = $cfg -replace "(?<![A-Za-z])stats:\s*'[^']*'", "stats: '$Stats'" }
[IO.File]::WriteAllText($cfgPath, $cfg, (New-Object Text.UTF8Encoding($false)))
Write-Host $cfg.Trim()
$mb = [math]::Round((Get-ChildItem $assets -Recurse -File | Measure-Object Length -Sum).Sum / 1MB, 2)
Write-Host "assets: $mb MB"

Step 2 'aapt2 compile (resources)'
Run (Join-Path $BT 'aapt2.exe') @('compile', '--dir', (Join-Path $here 'res'), '-o', (Join-Path $build 'res.zip'))

Step 3 'aapt2 link (resources + assets + manifest -> apk)'
Run (Join-Path $BT 'aapt2.exe') @(
  'link', '-o', (Join-Path $build 'app-unsigned.apk'),
  '-I', $Jar,
  '--manifest', (Join-Path $here 'AndroidManifest.xml'),
  '-R', (Join-Path $build 'res.zip'),
  '--java', $gen,
  '-A', $assets,
  '--min-sdk-version', '24', '--target-sdk-version', '35',
  '--auto-add-overlay')

Step 4 'javac (MainActivity + the R class aapt2 generated)'
$java = @(Get-ChildItem -Recurse -Filter *.java (Join-Path $here 'java') | ForEach-Object FullName)
$java += @(Get-ChildItem -Recurse -Filter *.java $gen | ForEach-Object FullName)
Run 'javac' (@('-nowarn', '-encoding', 'UTF-8', '-source', '8', '-target', '8', '-bootclasspath', $Jar, '-d', $classes) + $java)

Step 5 'd8 (java bytecode -> dex, desugared down to API 24)'
$class = @(Get-ChildItem -Recurse -Filter *.class $classes | ForEach-Object FullName)
Run (Join-Path $BT 'd8.bat') (@('--lib', $Jar, '--min-api', '24', '--output', $dex) + $class)

Step 6 'package (fold classes.dex into the apk)'
python (Join-Path $root 'tools\apkzip.py') (Join-Path $build 'app-unsigned.apk') $dex (Join-Path $build 'app-withdex.apk')
if ($LASTEXITCODE -ne 0) { throw 'apkzip failed' }

Step 7 'zipalign'
Run (Join-Path $BT 'zipalign.exe') @('-p', '-f', '4', (Join-Path $build 'app-withdex.apk'), (Join-Path $build 'app-aligned.apk'))

Step 8 'sign'
$ks = Join-Path $here 'hearthlight.keystore'
if (-not (Test-Path $ks)) {
  Write-Host 'no keystore yet — making one (hearthlight / hearthlight)'
  Run 'keytool' @('-genkeypair', '-keystore', $ks, '-alias', 'hearthlight', '-keyalg', 'RSA',
    '-keysize', '2048', '-validity', '10950', '-storepass', 'hearthlight', '-keypass', 'hearthlight',
    '-dname', 'CN=Hearthlight, O=Hearthlight, C=CA')
}
Run (Join-Path $BT 'apksigner.bat') @('sign', '--ks', $ks,
  '--ks-pass', 'pass:hearthlight', '--key-pass', 'pass:hearthlight', '--out', $Out,
  (Join-Path $build 'app-aligned.apk'))
Run (Join-Path $BT 'apksigner.bat') @('verify', '--print-certs', $Out)

Write-Host ''
Write-Host ("done: {0}  ({1} MB)" -f $Out, [math]::Round((Get-Item $Out).Length / 1MB, 2)) -ForegroundColor Green
