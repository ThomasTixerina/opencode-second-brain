<#
.SYNOPSIS
    Register wiki automation tasks in Windows Task Scheduler.

.DESCRIPTION
    Creates three scheduled tasks:
      - wiki-lint:     Runs lint-wiki.py daily at 06:00
      - wiki-compact:  Runs compact_memory.py weekly on Sunday at 07:00
      - wiki-watch:    Runs wiki-watch.py at user logon (background)

.NOTES
    Run as Administrator.
    Example:
        powershell -ExecutionPolicy Bypass -File scripts\setup-automation.ps1
#>

$ScriptDir = Split-Path -Parent $PSScriptRoot
$VaultRoot = Split-Path -Parent $ScriptDir
$Python = (Get-Command python).Source

if (-not $Python) {
    Write-Error "Python not found in PATH."
    exit 1
}

function Register-Task ($Name, $Description, $Trigger, $Arguments, $RunLevel = "LIMITED") {
    $Action = New-ScheduledTaskAction -Execute $Python -Argument $Arguments -WorkingDirectory $VaultRoot
    $Principal = New-ScheduledTaskPrincipal -UserId "INTERACTIVE" -LogonType Interactive -RunLevel $RunLevel
    $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

    try {
        $null = Register-ScheduledTask -TaskName $Name -Action $Action -Trigger $Trigger `
            -Principal $Principal -Settings $Settings -Description $Description -Force
        Write-Host "  [OK] $Name"
    }
    catch {
        Write-Warning "  [FAIL] $Name : $_"
    }
}

Write-Host "Registering wiki automation tasks..."
Write-Host "  Python: $Python"
Write-Host "  Vault:  $VaultRoot"
Write-Host ""

# 1. Daily lint at 06:00
$DailyTrigger = New-ScheduledTaskTrigger -Daily -At "06:00"
Register-Task -Name "wiki-lint" -Description "Wiki health check (daily)" `
    -Trigger $DailyTrigger -Arguments "scripts/lint-wiki.py --report"

# 2. Weekly compact on Sunday at 07:00
$WeeklyTrigger = New-ScheduledTaskTrigger -Weekly -WeeksInterval 1 -DaysOfWeek Sunday -At "07:00"
Register-Task -Name "wiki-compact" -Description "Memory compaction (weekly)" `
    -Trigger $WeeklyTrigger -Arguments "scripts/compact_memory.py --vault ."

# 3. Watcher at logon (background, no window)
$LogonTrigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
# wiki-watch runs hidden via pythonw to avoid console window
$PythonW = $Python -replace "python\.exe$", "pythonw.exe"
$WatchAction = New-ScheduledTaskAction -Execute $PythonW -Argument "scripts/wiki-watch.py watch --interval 60" `
    -WorkingDirectory $VaultRoot
$WatchPrincipal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel LIMITED
$WatchSettings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable `
    -Hidden
try {
    $null = Register-ScheduledTask -TaskName "wiki-watch" -Action $WatchAction -Trigger $LogonTrigger `
        -Principal $WatchPrincipal -Settings $WatchSettings -Description "Wiki watcher (background)" -Force
    Write-Host "  [OK] wiki-watch"
}
catch {
    Write-Warning "  [FAIL] wiki-watch : $_"
}

Write-Host ""
Write-Host "Done. Verify with: Get-ScheduledTask -TaskName wiki-*"
