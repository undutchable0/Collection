Write-Host -BackgroundColor yellow -ForegroundColor Black "`n`n**Prepare old PSAP VDI**`n"
Write-Host "`n"

Write-Host "Select target input method:"
Write-Host "1. Load targets from .\targets.text text file"
Write-Host "2. Enter a single target manually"

$choice = Read-Host "`nEnter choice (1 or 2)"

switch ($choice) {
    1 {
        $filePath = ".\targets.txt"
        if (Test-Path $filePath) {
            $targets = Get-Content $filePath | Where-Object { $_.Trim() -ne "" }
        } else {
            Write-Host "File not found. Exiting."
            exit
        }
    }
    2 {
        $singleTarget = Read-Host "Target VDI?"
        $targets = @($singleTarget)
    }
    Default {
        Write-Host "Invalid choice. Exiting."
        exit
    }
}

foreach ($targetVDI in $targets) {
    Write-Host "$targetVDI selected"

    if (Test-Connection -ComputerName $targetVDI -Count 2 -Quiet) {
        Write-Host "$targetVDI is online, copying CPI & ProQA files.."

        $sw = [System.Diagnostics.Stopwatch]::StartNew()

        # Copy CPI and Priority Dispatch folders from the remote VDI to local machine
        #$dest = ".\$targetVDI\CPI\Desktop"
        #New-Item -ItemType Directory -Path $dest -Force | Out-Null
        #Copy-Item -Path "\\$targetVDI\c$\CPI\Desktop\*.dat" -Destination ".\$targetVDI\CPI\Desktop" -Recurse -Force
        Copy-Item -Path "\\$targetVDI\c$\Program Files\***" -Destination ".\$targetVDI\**" -Recurse -Force

        $sw.Stop()
        Write-Host "Files copied in $($sw.Elapsed.TotalMinutes) minutes"
    }
    else {
        Write-Output "$targetVDI is offline. Please check the machine and try again."
    }
}

