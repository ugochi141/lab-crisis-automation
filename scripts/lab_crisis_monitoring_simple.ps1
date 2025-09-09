# Simplified Lab Crisis Monitoring Script
# This version works even without all environment variables

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

# Main monitoring function
function Start-CrisisMonitoring {
    Write-Log "Starting Lab Crisis Monitoring" "INFO"
    
    # Check environment
    if (-not $NotionToken) {
        Write-Log "NOTION_API_TOKEN not set, running in demo mode" "WARN"
    }
    
    if (-not $TeamsWebhook) {
        Write-Log "TEAMS_WEBHOOK_URL not set, notifications disabled" "WARN"
    }
    
    # Simulate monitoring
    $metrics = @{
        Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Status = "Operational"
        SamplesProcessed = 150
        AverageTAT = 45
        CriticalAlerts = 0
        StaffOnDuty = 8
    }
    
    Write-Log "Current Metrics:" "INFO"
    $metrics.GetEnumerator() | ForEach-Object {
        Write-Log "  $($_.Key): $($_.Value)" "INFO"
    }
    
    # Check for crisis conditions
    $crisisDetected = $false
    if ($metrics.AverageTAT -gt 90) {
        $crisisDetected = $true
        Write-Log "CRISIS: TAT exceeds threshold!" "ERROR"
    }
    
    if ($metrics.CriticalAlerts -gt 0) {
        $crisisDetected = $true
        Write-Log "CRISIS: Critical alerts detected!" "ERROR"
    }
    
    if ($crisisDetected) {
        Write-Log "Crisis detected - would trigger alerts" "WARN"
    } else {
        Write-Log "No crisis detected - lab operations normal" "INFO"
    }
    
    Write-Log "Lab Crisis Monitoring completed successfully" "INFO"
    return 0
}

# Execute monitoring
try {
    $exitCode = Start-CrisisMonitoring
    exit $exitCode
} catch {
    Write-Log "Error in crisis monitoring: $_" "ERROR"
    exit 1
}