Write-Host -BackgroundColor yellow -ForegroundColor Black "`n`n**Prepare new PSAP VDI**`n"
Write-Host "`n"

$targetVDI = Read-Host "Target VDI?"

Write-Host "$targetVDI selected"

if (Test-Connection -ComputerName $targetVDI -Count 2 -Quiet) {
    Write-Host "$targetVDI is online, adding $targetVDI user to local administrators group"

    $member = "EPTC911\$targetVDI"
    Invoke-Command -ComputerName $targetVDI -ScriptBlock {
        param($m)
        Add-LocalGroupMember -Group "Administrators" -Member $m
    } -ArgumentList $member

    # $processName = "DesktopUpdateScheduler"
    # Invoke-Command -ComputerName $targetVDI -ScriptBlock {
    #     param($p)
    #     $proc = Get-Process -Name $p -ErrorAction SilentlyContinue
    #     if ($proc) {
    #         Write-Host "Process $p is running, stopping it now..."
    #         Stop-Process -Name $p -Force
    #         Write-Host "Process $p stopped."
    #     } else {
    #         Write-Host "Process $p not found."
    #     }
    # } -ArgumentList $processName

    Write-Output "Copying local CPI & ProQA files to $targetVDI .."

    $sw = [System.Diagnostics.Stopwatch]::StartNew()

    #Copy-Item -Path ".\$targetVDI\**\**\*.dat" -Destination "\\$targetVDI\c$\**\**" -Recurse -Force
    Copy-Item -Path ".\$targetVDI\Priority Dispatch" -Destination "\\$targetVDI\c$\Program Files\" -Recurse -Force

    $sw.Stop()

    Write-Host "Files copied in $($sw.Elapsed.TotalMinutes) minutes"

    $destPath = "\\$targetVDI\c$\temp"

    if (-not (Test-Path $destPath)) {
        Write-Host "No temp folder found, creating one.."
        New-Item -ItemType Directory -Path $destPath | Out-Null
    }
    Write-Host "Copying Remote Access installer to $destPath .."
    Copy-Item -Path ".\Remote Access-windows64-offline.exe" -Destination $destPath -Force

    Write-Host "Installing SimpleHelp on $targetVDI .."
    Invoke-Command -ComputerName $targetVDI -ErrorAction Stop -ScriptBlock {
    $ErrorActionPreference = 'Stop'

    $installer = 'C:\Temp\Remote Access-windows64-offline.exe'
    if (-not (Test-Path $installer)) { throw "Not found: $installer" }

    $command = "& '$installer' /S /HOST=http://** /ForceVerification"

    $psArgs = @(
      '-NoProfile'
      '-ExecutionPolicy','Bypass'
      '-Command',$command
    )

    $proc = Start-Process -FilePath 'powershell.exe' -ArgumentList $psArgs -Wait -PassThru
    if ($null -eq $proc) { throw "Start-Process returned null" }

    $code = $proc.ExitCode
    Write-Output "Installer exit code: $code"
    if ($code -ne 0) { throw "Installer failed with exit code $code" }

    Write-Output "Install complete."
}
Write-Host "All steps completed."

}
    
else {
    Write-Host "$targetVDI is offline. Please check the machine and try again."
    exit
}

