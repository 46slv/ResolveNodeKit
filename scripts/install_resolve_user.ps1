[CmdletBinding()]
param(
    [switch]$Uninstall,
    [string]$FusionRoot = "",
    [string]$RepoRoot = "",
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Marker = "ResolveNodeKit - Arrange"
$ManifestName = "install_manifest.json"

if ([string]::IsNullOrWhiteSpace($RepoRoot)) {
    $RepoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
}
if ([string]::IsNullOrWhiteSpace($FusionRoot)) {
    $appData = $env:APPDATA
    if ([string]::IsNullOrWhiteSpace($appData)) {
        throw "APPDATA is not available; a per-user Resolve installation cannot be located."
    }
    $FusionRoot = Join-Path $appData "Blackmagic Design\DaVinci Resolve\Support\Fusion"
}

$entrySource = Join-Path $RepoRoot "scripts\Fusion\ResolveNodeKit_Arrange.py"
$packageSource = Join-Path $RepoRoot "src\resolve_node_kit"
$ownDir = Join-Path $FusionRoot "ResolveNodeKit"
$packageTarget = Join-Path $ownDir "src\resolve_node_kit"
$compDir = Join-Path $FusionRoot "Scripts\Comp"
$entryTarget = Join-Path $compDir "ResolveNodeKit_Arrange.py"
$manifestPath = Join-Path $ownDir $ManifestName

function Write-Utf8NoBom {
    param([Parameter(Mandatory = $true)][string]$Path, [Parameter(Mandatory = $true)][string]$Content)
    $encoding = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $encoding)
}

function Get-Sha256 {
    param([Parameter(Mandatory = $true)][string]$Path)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $stream = [System.IO.File]::OpenRead($Path)
        try {
            $bytes = $sha.ComputeHash($stream)
        } finally {
            $stream.Close()
        }
    } finally {
        $sha.Dispose()
    }
    return ([System.BitConverter]::ToString($bytes)).Replace("-", "").ToLowerInvariant()
}

function Test-OwnedEntry([Parameter(Mandatory = $true)][string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return $false }
    return (Get-Content -LiteralPath $Path -Raw).Contains($Marker)
}

function Get-RepoCommit([Parameter(Mandatory = $true)][string]$Root) {
    try {
        $out = & git -C $Root rev-parse HEAD 2>$null
        if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace($out)) { return $out.Trim() }
    } catch { }
    return "unknown"
}

function Remove-DirIfEmptyTree {
    param([Parameter(Mandatory = $true)][string]$Top)
    if (-not (Test-Path -LiteralPath $Top -PathType Container)) { return }
    $dirs = @($Top)
    Get-ChildItem -LiteralPath $Top -Recurse -Directory -Force -ErrorAction SilentlyContinue |
        ForEach-Object { $dirs += $_.FullName }
    foreach ($d in ($dirs | Sort-Object Length -Descending)) {
        if ((Test-Path -LiteralPath $d -PathType Container) -and
            (@(Get-ChildItem -LiteralPath $d -Force | Select-Object -First 1).Count -eq 0)) {
            Remove-Item -LiteralPath $d -Force
        }
    }
}

function Get-RelativePath {
    param([Parameter(Mandatory = $true)][string]$Base, [Parameter(Mandatory = $true)][string]$Target)
    $separator = [System.IO.Path]::DirectorySeparatorChar
    $baseFull = [System.IO.Path]::GetFullPath($Base).TrimEnd($separator) + $separator
    $targetFull = [System.IO.Path]::GetFullPath($Target)
    if (-not $targetFull.StartsWith($baseFull, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Path is not under base: $Target"
    }
    return $targetFull.Substring($baseFull.Length)
}

if ($Uninstall) {
    $removed = @()
    if (Test-Path -LiteralPath $manifestPath -PathType Leaf) {
        $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
        foreach ($file in $manifest.files) {
            $target = Join-Path $ownDir $file.path
            if (Test-Path -LiteralPath $target -PathType Leaf) {
                Remove-Item -LiteralPath $target -Force
                $removed += $file.path
            }
        }
        if (Test-Path -LiteralPath $manifestPath -PathType Leaf) {
            Remove-Item -LiteralPath $manifestPath -Force
            $removed += $ManifestName
        }
        Remove-DirIfEmptyTree -Top $ownDir
    } else {
        Write-Output "No install manifest; limited uninstall."
    }
    if (Test-Path -LiteralPath $entryTarget -PathType Leaf) {
        if (Test-OwnedEntry -Path $entryTarget) {
            Remove-Item -LiteralPath $entryTarget -Force
            $removed += "Scripts/Comp/ResolveNodeKit_Arrange.py"
        } else {
            Write-Output "Comp entry is not ResolveNodeKit-owned; left untouched: $entryTarget"
        }
    }
    if ((-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) -and (Test-Path -LiteralPath $ownDir -PathType Container)) {
        if ($Force) {
            Remove-Item -LiteralPath $ownDir -Recurse -Force
            $removed += "ResolveNodeKit/ (forced)"
        } else {
            Write-Output "ResolveNodeKit dir kept (no manifest); rerun with -Force to remove it."
        }
    }
    Write-Output "UNINSTALL DONE removed=$($removed.Count)"
    foreach ($item in $removed) { Write-Output "  - $item" }
    return
}

if (-not (Test-Path -LiteralPath $entrySource -PathType Leaf)) { throw "Entry source was not found: $entrySource" }
if (-not (Test-Path -LiteralPath $packageSource -PathType Container)) { throw "Package source was not found: $packageSource" }

$packageFiles = Get-ChildItem -LiteralPath $packageSource -Recurse -File -Filter "*.py" |
    Where-Object { $_.FullName -notmatch "__pycache__" } | Sort-Object FullName
if ($packageFiles.Count -eq 0) { throw "No package files found under: $packageSource" }

New-Item -ItemType Directory -Force -Path $packageTarget | Out-Null
New-Item -ItemType Directory -Force -Path $compDir | Out-Null
New-Item -ItemType Directory -Force -Path $ownDir | Out-Null

$stamp = (Get-Date).ToUniversalTime().ToString("yyyyMMdd-HHmmss")
$backupRoot = Join-Path $ownDir "backup\$stamp"

if ((Test-Path -LiteralPath $entryTarget -PathType Leaf) -and (-not (Test-OwnedEntry -Path $entryTarget))) {
    throw "Comp entry exists and is not ResolveNodeKit-owned; refusing to overwrite: $entryTarget"
}
if ((Test-Path -LiteralPath $entryTarget -PathType Leaf) -and (-not $Force)) {
    if ((Get-Sha256 -Path $entryTarget) -ne (Get-Sha256 -Path $entrySource)) {
        $backupEntry = Join-Path $backupRoot "Scripts\Comp\ResolveNodeKit_Arrange.py"
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $backupEntry) | Out-Null
        Copy-Item -LiteralPath $entryTarget -Destination $backupEntry -Force
        Write-Output "Backed up previous entry to: $backupEntry"
    }
}
Copy-Item -LiteralPath $entrySource -Destination $entryTarget -Force

$expected = @()
foreach ($file in $packageFiles) {
    $relative = Get-RelativePath -Base $packageSource -Target $file.FullName
    $destination = Join-Path $packageTarget $relative
    $parent = Split-Path -Parent $destination
    if (-not (Test-Path -LiteralPath $parent -PathType Container)) {
        New-Item -ItemType Directory -Force -Path $parent | Out-Null
    }
    Copy-Item -LiteralPath $file.FullName -Destination $destination -Force
    $info = Get-Item -LiteralPath $destination
    $expected += [pscustomobject]@{
        path   = ("src\resolve_node_kit\" + $relative)
        sha256 = (Get-Sha256 -Path $destination)
        bytes  = $info.Length
    }
}

$stale = Get-ChildItem -LiteralPath $packageTarget -Recurse -File -Filter "*.py" |
    Where-Object { $_.FullName -notmatch "__pycache__" -and $_.FullName -notmatch "\\backup\\" }
$keep = @{}
foreach ($item in $expected) { $keep[(Join-Path $ownDir $item.path)] = $true }
foreach ($item in $stale) {
    if (-not $keep.ContainsKey($item.FullName)) {
        Remove-Item -LiteralPath $item.FullName -Force
        Write-Output "Removed stale installed file: $($item.FullName)"
    }
}

$manifest = [pscustomobject]@{
    tool         = "ResolveNodeKit Semantic Arrange"
    version      = 1
    repo_commit  = (Get-RepoCommit -Root $RepoRoot)
    installed_at = (Get-Date).ToUniversalTime().ToString("o")
    files        = @($expected | Sort-Object path)
}
Write-Utf8NoBom -Path $manifestPath -Content ($manifest | ConvertTo-Json -Depth 6)

$mismatched = @()
foreach ($item in $expected) {
    $target = Join-Path $ownDir $item.path
    if (-not (Test-Path -LiteralPath $target -PathType Leaf)) { $mismatched += ($item.path + " (missing)"); continue }
    if ((Get-Sha256 -Path $target) -ne $item.sha256) { $mismatched += ($item.path + " (hash)") }
}
if ((Get-Sha256 -Path $entryTarget) -ne (Get-Sha256 -Path $entrySource)) { $mismatched += "Scripts/Comp/ResolveNodeKit_Arrange.py (hash)" }
if ($mismatched.Count -gt 0) { throw ("Install verification failed: " + ($mismatched -join ", ")) }

Write-Output "INSTALL VERIFIED files=$($expected.Count + 1) commit=$($manifest.repo_commit)"
Write-Output "  entry : $entryTarget"
Write-Output "  package root : $packageTarget"
Write-Output "  manifest : $manifestPath"
