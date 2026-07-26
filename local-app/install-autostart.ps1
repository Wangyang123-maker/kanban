$ErrorActionPreference = 'Stop'
$TaskName = 'RetailDashboardLocalService'
$Launcher = Join-Path $PSScriptRoot 'start-local-dashboard.bat'
$Action = New-ScheduledTaskAction -Execute $Launcher
$Trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Description 'Start the local retail dashboard at Windows logon' -Force | Out-Null
Write-Host "Autostart installed: $TaskName" -ForegroundColor Green

