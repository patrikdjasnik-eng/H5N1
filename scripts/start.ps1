$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$backend = Join-Path $root "backend"
$frontend = Join-Path $root "frontend"
$venvPython = Join-Path $backend ".venv\Scripts\python.exe"

try {
  if (-not (Test-Path $venvPython)) {
    Write-Host "Vytvarim virtualni prostredi Python..."
    Push-Location $backend
    py -3 -m venv .venv
    Pop-Location
  }

  & $venvPython -m pip show h5n1-drone-safety 2>$null | Out-Null
  if ($LASTEXITCODE -ne 0) {
    Write-Host "Instaluji Python zavislosti..."
    & $venvPython -m pip install -e $backend
    if ($LASTEXITCODE -ne 0) { throw "Instalace Python balicku selhala" }
  }

  if (-not (Test-Path (Join-Path $frontend "node_modules"))) {
    Write-Host "Instaluji frontend..."
    Push-Location $frontend
    npm install
    if ($LASTEXITCODE -ne 0) { throw "Instalace npm selhala" }
    Pop-Location
  }

  Write-Host "Spoustim H5N1 backend na http://127.0.0.1:8765"
  Start-Process -FilePath $venvPython -ArgumentList @("-m", "uvicorn", "h5n1.api:app", "--host", "127.0.0.1", "--port", "8765") -WorkingDirectory $backend

  Write-Host "Spoustim H5N1 dashboard na http://127.0.0.1:5174"
  Start-Process -FilePath "npm.cmd" -ArgumentList @("run", "dev") -WorkingDirectory $frontend
  Write-Host "Simulace spustena. H5N1 neovlada skutecne drony."
} catch {
  Write-Error ("Spusteni se nepodarilo: " + $_.Exception.Message)
  exit 1
}
