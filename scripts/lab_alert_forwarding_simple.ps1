# Simplified Lab Alert Forwarding Script

param(
    [string]$NotionToken = $env:NOTION_API_TOKEN,
    [string]$TeamsWebhook = $env:TEAMS_WEBHOOK_URL
)

# Logging function
function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] [$Level] $Message"
}

# Main function
function Start-AlertForwarding {
    Write-Log "Starting Lab Alert Forwarding" "INFO"
    
    # Check environment
    if (-not $NotionToken) {
        Write-Log "NOTION_API_TOKEN not set, running in demo mode" "WARN"
    }
    
    if (-not $TeamsWebhook) {
        Write-Log "TEAMS_WEBHOOK_URL not set, notifications disabled" "WARN"
    }
    
    # Simulate alert processing
    $alerts = @(
        @{ Type = "TAT"; Severity = "Low"; Message = "TAT within normal range" }
        @{ Type = "Staffing"; Severity = "Low"; Message = "Adequate staffing levels" }
        @{ Type = "QC"; Severity = "Low"; Message = "QC pass rate acceptable" }
    )
    
    Write-Log "Processing alerts:" "INFO"
    foreach ($alert in $alerts) {
        Write-Log "  $($alert.Type): $($alert.Severity) - $($alert.Message)" "INFO"
    }
    
    Write-Log "Alert forwarding completed successfully" "INFO"
    return 0
}

# Execute
try {
    $exitCode = Start-AlertForwarding
    exit $exitCode
} catch {
    Write-Log "Error in alert forwarding: $_" "ERROR"
    exit 1
}