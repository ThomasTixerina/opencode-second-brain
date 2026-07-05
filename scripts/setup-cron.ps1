#Requires -Version 5.1
# setup-cron.ps1 — Register daily memory compaction in Windows Task Scheduler
# Runs compact_memory.py at 00:00 every day.

$TaskName = "SecondBrain-MemoryCompaction"
$VaultDir = Resolve-Path "$PSScriptRoot\.."
$ScriptPath = "$VaultDir\scripts\compact_memory.py"
$PythonExe = (Get-Command python).Source

if (-not $PythonExe) {
    Write-Error "Python not found. Install Python first."
    exit 1
}

$Action = New-ScheduledTaskAction -Execute $PythonExe -Argument "`"$ScriptPath`"" -WorkingDirectory $VaultDir
$Trigger = New-ScheduledTaskTrigger -Daily -At 00:00
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -RunLevel Limited
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopIfGoingOnBatteries

try {
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger `
        -Principal $Principal -Settings $Settings -Force
    Write-Host "[OK] Scheduled task '$TaskName' registered." -ForegroundColor Green
    Write-Host "    Runs daily at 00:00 as $env:USERNAME"
    Write-Host "    Script: $ScriptPath"
} catch {
    Write-Error "Failed to register task: $_"
    exit 1
}
