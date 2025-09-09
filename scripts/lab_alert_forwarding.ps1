# Lab Alert Forwarding Script
# Pulls alerts from Notion and Power BI, forwards to Microsoft Teams

param(
    [string]$NotionToken = $env:NOTION_TOKEN,
    [string]$TeamsWebhook = $env:TEAMS_WEBHOOK,
    [string]$PowerBIEndpoint = $env:POWERBI_ENDPOINT,
    [string]$NotionDatabaseId = $env:NOTION_ALERTS_DB_ID
)

# Configuration
$Config = @{
    NotionApiUrl = "https://api.notion.com/v1"
    TeamsWebhookUrl = $TeamsWebhook
    PowerBIEndpoint = $PowerBIEndpoint
    AlertSeverityColors = @{
        "Info" = "00FF00"
        "Warning" = "FFFF00"
        "High" = "FFA500"
        "Critical" = "FF0000"
    }
    RetryAttempts = 3
    RetryDelay = 5
}

# Logging function
function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] [$Level] $Message"
    Add-Content -Path "logs\lab_alerts.log" -Value "[$timestamp] [$Level] $Message"
}

# Send alert to Microsoft Teams
function Send-LabAlertToTeams {
    param(
        [hashtable]$AlertData
    )
    
    try {
        $severity = $AlertData.Severity
        $color = $Config.AlertSeverityColors[$severity]
        
        $messageCard = @{
            "@type" = "MessageCard"
            "@context" = "http://schema.org/extensions"
            "themeColor" = $color
            "summary" = "Lab Alert: $($AlertData.Title)"
            "sections" = @(
                @{
                    "activityTitle" = "🚨 Lab Alert: $($AlertData.Title)"
                    "activitySubtitle" = "Type: $($AlertData.Type)"
                    "facts" = @(
                        @{ "name" = "Time"; "value" = $AlertData.Time }
                        @{ "name" = "Station"; "value" = $AlertData.Station }
                        @{ "name" = "Employee"; "value" = $AlertData.Employee }
                        @{ "name" = "Severity"; "value" = $AlertData.Severity }
                    )
                    "markdown" = $true
                }
            )
        }
        
        $headers = @{
            "Content-Type" = "application/json"
        }
        
        $response = Invoke-RestMethod -Uri $Config.TeamsWebhookUrl -Method Post -Body ($messageCard | ConvertTo-Json -Depth 10) -Headers $headers
        
        Write-Log "Alert sent to Teams: $($AlertData.Title)" "SUCCESS"
        return $true
    }
    catch {
        Write-Log "Failed to send Teams alert: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

# Pull alerts from Notion
function Get-NotionAlerts {
    param(
        [string]$DatabaseId,
        [string]$Token
    )
    
    try {
        $headers = @{
            "Authorization" = "Bearer $Token"
            "Notion-Version" = "2022-06-28"
            "Content-Type" = "application/json"
        }
        
        $body = @{
            "filter" = @{
                "property" = "Resolved"
                "checkbox" = @{
                    "equals" = $false
                }
            }
            "sorts" = @(
                @{
                    "property" = "Time"
                    "direction" = "descending"
                }
            )
        } | ConvertTo-Json -Depth 10
        
        $response = Invoke-RestMethod -Uri "$($Config.NotionApiUrl)/databases/$DatabaseId/query" -Method Post -Body $body -Headers $headers
        
        $alerts = @()
        foreach ($result in $response.results) {
            $props = $result.properties
            $alert = @{
                Id = $result.id
                Title = $props.Alert.title[0].text.content
                Time = $props.Time.date.start
                Type = $props.Type.select.name
                Severity = $props.Severity.select.name
                Station = $props.Station.rich_text[0].text.content
                Employee = $props.Employee.rich_text[0].text.content
                Resolved = $props.Resolved.checkbox
            }
            $alerts += $alert
        }
        
        Write-Log "Retrieved $($alerts.Count) alerts from Notion" "INFO"
        return $alerts
    }
    catch {
        Write-Log "Error retrieving Notion alerts: $($_.Exception.Message)" "ERROR"
        return @()
    }
}

# Pull alerts from Power BI
function Get-PowerBIAlerts {
    param(
        [string]$Endpoint
    )
    
    try {
        if (-not $Endpoint) {
            Write-Log "Power BI endpoint not configured" "WARNING"
            return @()
        }
        
        $response = Invoke-RestMethod -Uri $Endpoint -Method Get
        
        $alerts = @()
        foreach ($alert in $response.alerts) {
            $alertData = @{
                Id = $alert.id
                Title = $alert.title
                Time = $alert.timestamp
                Type = $alert.type
                Severity = $alert.severity
                Station = $alert.station
                Employee = $alert.employee
                Resolved = $false
            }
            $alerts += $alertData
        }
        
        Write-Log "Retrieved $($alerts.Count) alerts from Power BI" "INFO"
        return $alerts
    }
    catch {
        Write-Log "Error retrieving Power BI alerts: $($_.Exception.Message)" "ERROR"
        return @()
    }
}

# Mark alert as resolved in Notion
function Set-NotionAlertResolved {
    param(
        [string]$AlertId,
        [string]$Token
    )
    
    try {
        $headers = @{
            "Authorization" = "Bearer $Token"
            "Notion-Version" = "2022-06-28"
            "Content-Type" = "application/json"
        }
        
        $body = @{
            "properties" = @{
                "Resolved" = @{
                    "checkbox" = $true
                }
                "Resolution Time" = @{
                    "date" = @{
                        "start" = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
                    }
                }
            }
        } | ConvertTo-Json -Depth 10
        
        $response = Invoke-RestMethod -Uri "$($Config.NotionApiUrl)/pages/$AlertId" -Method Patch -Body $body -Headers $headers
        
        Write-Log "Marked alert $AlertId as resolved in Notion" "SUCCESS"
        return $true
    }
    catch {
        Write-Log "Error marking alert as resolved: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

# Main execution function
function Start-LabAlertForwarding {
    Write-Log "Starting lab alert forwarding process..." "INFO"
    
    # Ensure logs directory exists
    if (-not (Test-Path "logs")) {
        New-Item -ItemType Directory -Path "logs" -Force | Out-Null
    }
    
    # Validate configuration
    if (-not $NotionToken) {
        Write-Log "Notion token not provided" "ERROR"
        return
    }
    
    if (-not $TeamsWebhook) {
        Write-Log "Teams webhook not provided" "ERROR"
        return
    }
    
    # Get alerts from both sources
    $notionAlerts = Get-NotionAlerts -DatabaseId $NotionDatabaseId -Token $NotionToken
    $powerBIAlerts = Get-PowerBIAlerts -Endpoint $PowerBIEndpoint
    
    # Combine and deduplicate alerts
    $allAlerts = $notionAlerts + $powerBIAlerts
    $uniqueAlerts = $allAlerts | Sort-Object -Property Id -Unique
    
    Write-Log "Processing $($uniqueAlerts.Count) unique alerts" "INFO"
    
    # Process each alert
    $successCount = 0
    $failureCount = 0
    
    foreach ($alert in $uniqueAlerts) {
        try {
            # Format alert data for Teams
            $alertData = @{
                Title = $alert.Title
                Type = $alert.Type
                Severity = $alert.Severity
                Time = (Get-Date $alert.Time -Format "HH:mm")
                Station = $alert.Station
                Employee = $alert.Employee
            }
            
            # Send to Teams
            $success = Send-LabAlertToTeams -AlertData $alertData
            
            if ($success) {
                $successCount++
                
                # Mark as resolved in Notion if it came from there
                if ($alert.Id -and $alert.Id -like "*-*-*-*-*") {
                    Set-NotionAlertResolved -AlertId $alert.Id -Token $NotionToken
                }
            }
            else {
                $failureCount++
            }
            
            # Add delay to avoid rate limiting
            Start-Sleep -Milliseconds 500
        }
        catch {
            Write-Log "Error processing alert $($alert.Id): $($_.Exception.Message)" "ERROR"
            $failureCount++
        }
    }
    
    Write-Log "Alert forwarding completed. Success: $successCount, Failures: $failureCount" "INFO"
}

# Run the main function
Start-LabAlertForwarding
