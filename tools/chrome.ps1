# A headless Chrome that belongs to the tools, never to you.
#
#   pwsh -File tools/chrome.ps1 start [port] [-W 1280] [-H 720] [-Url ...]   start one, print its pid
#   pwsh -File tools/chrome.ps1 stop            stop ours, and only ours
#   pwsh -File tools/chrome.ps1 status
#
# Three rules this script exists to enforce:
#   * the profile lives OUTSIDE the repo — a profile inside it gets copied into
#     the Android assets by android/build.ps1;
#   * stop matches the "hl-chrome" marker in the command line, so it can never
#     take your own browser down with it. `Get-Process chrome | Stop-Process`
#     does exactly that, and did, once;
#   * stdio is redirected to the profile dir. Started detached with no handles,
#     headless Chrome here prints "DevTools listening" and then exits at once,
#     which looks exactly like a dead debugging port.
param([Parameter(Position = 0)][string]$Action = 'status', [Parameter(Position = 1)][int]$Port = 9222,
    [int]$W = 1280, [int]$H = 720, [string]$Url = 'about:blank')

$ErrorActionPreference = 'Stop'

$chrome = @(
    'C:\Program Files\Google\Chrome\Application\chrome.exe',
    'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
    (Join-Path $env:LOCALAPPDATA 'Google\Chrome\Application\chrome.exe')
) | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $chrome) { throw 'chrome.exe not found' }

$profileDir = Join-Path $env:TEMP "hl-chrome-$Port"
# one instance per port, so `stop 9223` can't take the 9222 one (or your browser) with it.
# (%TEMP% can come back as an 8.3 short name, so match on the marker, not the whole path.)
$marker = "hl-chrome-$Port"

function Ours {
    Get-CimInstance Win32_Process -Filter "Name='chrome.exe'" |
        Where-Object { $_.CommandLine -and $_.CommandLine -like "*$marker*" }
}

switch ($Action) {
    'start' {
        if (Ours) { 'already running:'; Ours | ForEach-Object { "  pid $($_.ProcessId)" }; break }
        New-Item -ItemType Directory -Force -Path $profileDir | Out-Null
        $chromeArgs = @(
            '--headless=new', "--remote-debugging-port=$Port", "--user-data-dir=$profileDir",
            "--window-size=$W,$H", '--lang=zh-CN', '--accept-lang=zh-CN',
            '--enable-unsafe-swiftshader', '--hide-scrollbars', '--no-first-run',
            '--disable-extensions', $Url
        )
        $p = Start-Process -FilePath $chrome -ArgumentList $chromeArgs -PassThru `
            -RedirectStandardOutput (Join-Path $profileDir 'chrome.out.log') `
            -RedirectStandardError (Join-Path $profileDir 'chrome.err.log')
        Start-Sleep -Seconds 3
        if ($p.HasExited) {
            "exited at once (code $($p.ExitCode)) — see $(Join-Path $profileDir 'chrome.err.log')"
            break
        }
        "started pid $($p.Id) on port $Port (profile $profileDir)"
        "check it with: node tools/cdp.mjs url"
    }
    'stop' {
        $k = Ours
        if (-not $k) { 'not running'; break }
        $k | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
        "stopped $(($k | Measure-Object).Count) process(es)"
    }
    'status' {
        $k = Ours
        if (-not $k) { 'not running'; break }
        $k | ForEach-Object { $c = $_.CommandLine; "pid $($_.ProcessId)  $($c.Substring(0, [Math]::Min(110, $c.Length)))" }
    }
    default { throw "usage: chrome.ps1 start|stop|status [port]" }
}
