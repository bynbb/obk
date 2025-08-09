param(
  [string]$Ref = "HEAD",
  [string]$ZipName = "",
  [switch]$IncludeLinuxWheels
)

$ErrorActionPreference = "Stop"

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location (git rev-parse --show-toplevel)

# Build + vendor (optionally include Linux wheels)
pwsh -File "$here/build-and-vendor.ps1" @($IncludeLinuxWheels ? "-IncludeLinuxWheels" : $null)

# Zip (forward optional ref/name)
$zipArgs = @()
if ($Ref)    { $zipArgs += @("-Ref", $Ref) }
if ($ZipName){ $zipArgs += @("-ZipName", $ZipName) }
pwsh -File "$here/make-zip.ps1" @zipArgs
