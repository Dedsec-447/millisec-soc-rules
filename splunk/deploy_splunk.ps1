# MilliSec - Splunk rule deployer via REST API
# Usage: .\deploy_splunk.ps1 -SplunkHost "https://SPLUNK_IP:8089" -ConfFile ".\savedsearches.conf"
param(
    [Parameter(Mandatory=$true)][string]$SplunkHost,
    [Parameter(Mandatory=$true)][string]$ConfFile = ".\savedsearches.conf"
)
$cred = Get-Credential -Message "Splunk admin credentials"
$raw = Get-Content $ConfFile
$rules = @{}; $current = $null
foreach ($line in $raw) {
    $t = $line.Trim()
    if ($t -match '^\[(.+)\]$') { $current = $Matches[1]; $rules[$current] = @{}; continue }
    if ($current -and $t -match '^([A-Za-z0-9_.]+)\s*=\s*(.*)$') { $rules[$current][$Matches[1]] = $Matches[2] }
}
Write-Host "Parsed $($rules.Count) rules from $ConfFile" -ForegroundColor Cyan
$ok = 0; $fail = 0
foreach ($name in $rules.Keys) {
    $body = @{ name = $name }
    foreach ($k in $rules[$name].Keys) { $body[$k] = $rules[$name][$k] }
    try {
        Invoke-RestMethod -Method Post -Uri "$SplunkHost/servicesNS/nobody/search/saved/searches" `
            -Credential $cred -Body $body -TimeoutSec 30 | Out-Null
        Write-Host "[OK] $name" -ForegroundColor Green; $ok++
    } catch {
        Write-Host "[FAIL] $name : $($_.Exception.Message)" -ForegroundColor Red; $fail++
    }
}
Write-Host "`nDone: $ok deployed, $fail failed" -ForegroundColor Yellow
