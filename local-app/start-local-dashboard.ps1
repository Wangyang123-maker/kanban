$ErrorActionPreference = 'Stop'
$Source = Join-Path $env:USERPROFILE 'Documents\kimi\workspace\retail-site'
$Port = 8017
$Health = "http://127.0.0.1:$Port/api/status"

if (-not (Test-Path (Join-Path $Source 'serve.py'))) {
  Write-Host "Dashboard source not found: $Source" -ForegroundColor Red
  Read-Host 'Press Enter to exit'
  exit 1
}

function Find-Python {
  $candidates = @(
    (Join-Path $env:APPDATA 'kimi-desktop\daimon-share\daimon\runtime\python\.venv\Scripts\python.exe'),
    (Join-Path $env:APPDATA 'kimi-desktop\daimon-bundle\runtime\python\cpython-3.12\python.exe'),
    'python.exe'
  )
  foreach ($candidate in $candidates) {
    if ($candidate -eq 'python.exe') { $cmd = Get-Command python.exe -ErrorAction SilentlyContinue; if ($cmd) { return $cmd.Source } }
    elseif (Test-Path $candidate) { return $candidate }
  }
  return $null
}

function Test-Service {
  try { $r = Invoke-WebRequest -UseBasicParsing -Uri $Health -TimeoutSec 4; return $r.StatusCode -eq 200 }
  catch { return $false }
}

$python = Find-Python
if (-not $python) { Write-Host 'Python runtime not found.' -ForegroundColor Red; Read-Host 'Press Enter to exit'; exit 1 }

if (-not (Test-Service)) {
  Write-Host 'Starting dashboard service...' -ForegroundColor Cyan
  Start-Process -FilePath $python -ArgumentList @('-X','utf8','serve.py') -WorkingDirectory $Source -WindowStyle Hidden
  $ready = $false
  1..20 | ForEach-Object { Start-Sleep -Milliseconds 500; if (Test-Service) { $ready = $true; return } }
  if (-not $ready) { Write-Host 'Service failed to start.' -ForegroundColor Red; Read-Host 'Press Enter to exit'; exit 1 }
}

Write-Host ''
Write-Host 'Dashboard service is running.' -ForegroundColor Green
Write-Host "Local: http://127.0.0.1:$Port/" -ForegroundColor White

$ips = @(& ipconfig | Select-String -Pattern 'IPv4.*:') | ForEach-Object {
  if ($_.Line -match '([0-9]{1,3}(\.[0-9]{1,3}){3})') { $Matches[1] }
} | Where-Object { $_ -notlike '127.*' -and $_ -notlike '169.254.*' } | Select-Object -Unique
foreach ($ip in $ips) { Write-Host "Same Wi-Fi: http://${ip}:$Port/" -ForegroundColor Yellow }

$tailscale = Get-Command tailscale.exe -ErrorAction SilentlyContinue
if ($tailscale) {
  $tsip = (& $tailscale.Source ip -4 2>$null | Select-Object -First 1).Trim()
  if ($tsip) { Write-Host "Tailscale: http://${tsip}:$Port/" -ForegroundColor Magenta }
}

Start-Process "http://127.0.0.1:$Port/"
Write-Host ''
Write-Host 'Open the Wi-Fi address on your phone, then add it to the home screen.' -ForegroundColor Gray
Write-Host 'Closing this window does not stop the service.' -ForegroundColor Gray
Read-Host 'Press Enter to close this message'
