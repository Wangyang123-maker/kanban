$ErrorActionPreference = 'Stop'
$base = 'http://127.0.0.1:8017'
$paths = @('/', '/api/status', '/index.html', '/demo.html', '/upload.html', '/data.json', '/inventory.json', '/demo.json')
$failed = @()
foreach ($path in $paths) {
  try { $r = Invoke-WebRequest -UseBasicParsing -Uri ($base + $path) -TimeoutSec 10; Write-Host ("{0,-20} {1}" -f $path, $r.StatusCode); if ($r.StatusCode -ne 200) { $failed += $path } }
  catch { Write-Host ("{0,-20} ERROR" -f $path) -ForegroundColor Red; $failed += $path }
}
if ($failed.Count) { throw "Health check failed: $($failed -join ', ')" }
Write-Host 'Local dashboard health check passed.' -ForegroundColor Green
