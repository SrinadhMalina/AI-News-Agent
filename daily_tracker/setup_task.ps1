# Get the current logged-in user
$currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name

# Action: Launch the interactive dashboard via the batch file
$action = New-ScheduledTaskAction -Execute "D:\Projects\autoReactor\daily_tracker\launch_tracker.bat"

# Trigger: Every day at 02:30 AM IST (11:00 PM CET)
$trigger = New-ScheduledTaskTrigger -Daily -At "02:30"

# Principal: Run as the current user.
# By NOT specifying a password and using the current user, Windows defaults to "Run only when user is logged on",
# which is the ONLY way to get a GUI window to appear on the desktop.
$principal = New-ScheduledTaskPrincipal -UserId $currentUser -RunLevel Highest

# Register the task
Register-ScheduledTask -Action $action -Trigger $trigger -Principal $principal -TaskName "DailyHustleChecklist" -Force

Write-Host "Successfully scheduled the Daily Hustle Checklist for 02:30 AM IST (11:00 PM CET)!" -ForegroundColor Green
Write-Host "The window will now pop up on your screen. 🚀" -ForegroundColor Cyan
