<#  make-zip.ps1
    Clean archive from Git + (optionally) dist/*.whl,*.tar.gz

    Usage
	From the repo root:
      .scripts/make-zip.ps1
      .scripts/make-zip.ps1 -Ref v0.9.0 -ZipName obk-0.9.0.zip
      .scripts/make-zip.ps1 -NoWheels
#>

param(
  [string]$Ref = "HEAD",
  [string]$ZipName = "",
  [switch]$NoWheels
)

$ErrorActionPreference = "Stop"

function Require-Cmd($name) {
  if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
    throw "Required command not found: $name"
  }
}

# Ensure we're in a Git repo and the ref exists
Require-Cmd git
git rev-parse --verify $Ref > $null 2>&1

# Default zip name: obk_<ref>.zip (sanitize ref), or obk_clean.zip for HEAD
if ([string]::IsNullOrWhiteSpace($ZipName)) {
  $refSafe = ($Ref -replace '[^A-Za-z0-9._-]', '_')
  $ZipName = $(if ($Ref -eq "HEAD") { "obk_clean.zip" } else { "obk_$refSafe.zip" })
}

# 1) Base archive from Git (tracked files only; respects .gitignore)
Write-Host "Creating base archive from $Ref -> $ZipName"
git archive --format=zip --output "$ZipName" $Ref

# Helper: add files to an existing zip with either Compress-Archive -Update or 7z
function Add-ToZip {
  param(
    [string]$Zip,
    [string[]]$Paths
  )
  $Paths = $Paths | Where-Object { Test-Path $_ }
  if (-not $Paths -or $Paths.Count -eq 0) { return }

  $compress = Get-Command Compress-Archive -ErrorAction SilentlyContinue
  if ($compress -and ($compress.Parameters.ContainsKey("Update"))) {
    Write-Host "Adding $($Paths.Count) item(s) via Compress-Archive -Update"
    Compress-Archive -Path $Paths -DestinationPath $Zip -Update
    return
  }

  $sevenZ = Get-Command 7z -ErrorAction SilentlyContinue
  if ($sevenZ) {
    Write-Host "Adding $($Paths.Count) item(s) via 7-Zip"
    & 7z a "$Zip" $Paths | Out-Null
    return
  }

  throw "Neither Compress-Archive -Update nor 7z is available to update the zip."
}

# 2) Optionally include wheels/sdists from dist/
if (-not $NoWheels) {
  $wheelPaths = @()
  if (Test-Path ".\dist") {
    $wheelPaths += Get-ChildItem .\dist\*.whl -ErrorAction SilentlyContinue | ForEach-Object { $_.FullName }
    $wheelPaths += Get-ChildItem .\dist\*.tar.gz -ErrorAction SilentlyContinue | ForEach-Object { $_.FullName }
  }
  if ($wheelPaths.Count -gt 0) {
    Write-Host "Including dist artifacts: $($wheelPaths.Count)"
    $relWheelPaths = $wheelPaths | ForEach-Object { Resolve-Path -Relative $_ }
    Add-ToZip -Zip $ZipName -Paths $relWheelPaths
  } else {
    Write-Host "No dist/*.whl or *.tar.gz found; skipping wheels."
  }
} else {
  Write-Host "Skipping wheels/sdists by request (-NoWheels)."
}

Write-Host ""
Write-Host "Done -> $ZipName"
Write-Host "Tip: verify contents with 'Expand-Archive $ZipName -DestinationPath _zipcheck -Force'"
