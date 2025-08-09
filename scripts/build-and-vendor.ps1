<# scripts/build-and-vendor.ps1
    Build obk (wheel + sdist) and vendor runtime dependency wheels into dist/
    - Default: download native (Windows) wheels
    - With -IncludeLinuxWheels: also download manylinux x86_64 wheels for CPython 3.11 (ChatGPT runtime)

    Usage:
      pwsh -File scripts/build-and-vendor.ps1
      pwsh -File scripts/build-and-vendor.ps1 -IncludeLinuxWheels
#>

param(
  [switch]$IncludeLinuxWheels
)

$ErrorActionPreference = "Stop"

function Require-Cmd($name) {
  if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
    throw "Required command not found: $name"
  }
}

Require-Cmd git
Require-Cmd python

# Go to repo root
$repoRoot = (& git rev-parse --show-toplevel).Trim()
Set-Location $repoRoot

# Ensure dist/
New-Item -ItemType Directory -Force -Path dist | Out-Null

# Isolated build venv
$venv = Join-Path $repoRoot ".venv_build"
if (-not (Test-Path $venv)) { python -m venv $venv }
$py  = Join-Path $venv "Scripts" "python.exe"
$pip = Join-Path $venv "Scripts" "pip.exe"

& $py -m pip install -U pip wheel build | Out-Null

Write-Host "🛠️  Building (wheel + sdist) ..."
& $py -m build

# Extract [project].dependencies from pyproject.toml via temp script
$reqFile = Join-Path $repoRoot "dist" "runtime-requirements.txt"
$tmpPy   = Join-Path $env:TEMP ("extract_deps_{0}.py" -f ([guid]::NewGuid().ToString("N")))

$pyCode = @'
import sys
try:
    import tomllib as toml  # Python 3.11+
except ModuleNotFoundError:
    import toml  # type: ignore

with open("pyproject.toml", "rb") as f:
    data = toml.load(f)

deps = (data.get("project", {}) or {}).get("dependencies", []) or []
for d in deps:
    d = str(d).strip()
    if d:
        print(d)
'@

$pyCode | Set-Content -Encoding UTF8 $tmpPy
try {
  $deps = & $py $tmpPy
} finally {
  if (Test-Path $tmpPy) { Remove-Item $tmpPy -Force }
}

$deps | Set-Content -Encoding UTF8 $reqFile
Write-Host "📦 Found dependencies:" ($deps -join ", ")

# Helper to run pip download with extra args
function Invoke-PipDownload {
  param([string[]]$ExtraArgs)
  if ((Get-Content $reqFile | Where-Object { $_.Trim() }) -ne $null) {
    Write-Host "⬇️  pip download -> dist/ $($ExtraArgs -join ' ')"
    & $pip download --only-binary=:all: --dest dist -r $reqFile @ExtraArgs
  } else {
    Write-Host "ℹ️  No runtime deps found in [project].dependencies."
  }
}

# 1) Native (Windows) wheels
Invoke-PipDownload @()

# 2) Optional Linux wheels for ChatGPT (manylinux x86_64, CPython 3.11)
if ($IncludeLinuxWheels) {
  Invoke-PipDownload @(
    "--platform", "manylinux2014_x86_64",
    "--implementation", "cp",
    "--python-version", "311",
    "--abi", "cp311"
  )
}

Write-Host ""
Write-Host "✅ dist/ ready:"
Get-ChildItem dist | Select-Object Name, Length
