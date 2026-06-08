#Powershell code to turn on specific port for listening, for testing purposes

Write-Host -ForegroundColor Cyan "**Port Listener 3000**`n` "

$userInput = Read-Host -Prompt "Enter port to listen on (integer value)"
$ipendpoint = new-object System.Net.IPEndPoint([ipaddress]::any, $userInput)
$listener = new-object System.Net.Sockets.TcpListener $ipendpoint
try {
    $listener.start()
    Write-Host "Currently listening on port $userInput..."
    Read-Host -Prompt "Press 'Enter' to stop listening"
}
catch {
    Write-Host -ForegroundColor Red "Unable to start listener on port $($userInput). Please check if there is already a listener present using the netstat -a command.`n`Error: $($_.Exception.Message)"
    Read-Host -Prompt "Press 'Enter' to exit this script"
} 
finally {
    $listener.stop()
}


#Powershell code to test port against target (from another device)
#Test-NetConnection <computername> -Port <port#>