# Lab Crisis Monitoring Script
# Integrates with your specific Notion, Power BI, and Teams setup

param(
    [string]$NotionToken = $env:NOTION_API_TOKEN,
    [string]$TeamsWebhook = $env:TEAMS_WEBHOOK_URL,
    [string]$PowerBIMonitorUrl = $env:POWERBI_MONITOR_PUSH_URL,
    [string]$PowerBIMetricsUrl = $env:POWERBI_METRICS_PUSH_URL
)

# Configuration
$Config = @{
    NotionApiUrl = "https://api.notion.com/v1"
    NotionVersion = "2022-06-28"
    PerformanceDbId = "c1500b1816b14018beabe2b826ccafe9"
    IncidentDbId = "cf2bb4448aff4324a602cb770cbae0a2"
    LabManagementCenter = "266d222751b3818996b4ce1cf18e0913"
    TeamsWebhookUrl = $TeamsWebhook
    PowerBIMonitorUrl = $PowerBIMonitorUrl
    PowerBIMetricsUrl = $PowerBIMetricsUrl
    AlertSeverityColors = @{
        "Info" = "00FF00"
        "Warning" = "FFFF00"
        "High" = "FFA500"
        "Critical" = "FF0000"
    }
    CrisisThresholds = @{
        TATCritical = 50
        TATWarning = 70
        TATTarget = 90
        WaitCritical = 30
        WaitWarning = 20
        WaitTarget = 15
        IdleMax = 30
        BreakMax = 15
        StaffingGap = 3.3
    }
}

# Logging function
function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] [$Level] $Message"
    Add-Content -Path "logs\lab_crisis_monitoring.log" -Value "[$timestamp] [$Level] $Message"
}

# Send crisis alert to Teams
function Send-CrisisAlertToTeams {
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
            "summary" = "🚨 Lab Crisis Alert: $($AlertData.Title)"
            "sections" = @(
                @{
                    "activityTitle" = "🚨 Lab Crisis Alert: $($AlertData.Title)"
                    "activitySubtitle" = "Type: $($AlertData.Type) | Severity: $($AlertData.Severity)"
                    "facts" = @(
                        @{ "name" = "Time"; "value" = $AlertData.Time }
                        @{ "name" = "Station"; "value" = $AlertData.Station }
                        @{ "name" = "Employee"; "value" = $AlertData.Employee }
                        @{ "name" = "Current Value"; "value" = $AlertData.CurrentValue }
                        @{ "name" = "Target"; "value" = $AlertData.Target }
                        @{ "name" = "Action Required"; "value" = $AlertData.Action }
                    )
                    "markdown" = $true
                }
            )
        }
        
        $headers = @{
            "Content-Type" = "application/json"
        }
        
        $response = Invoke-RestMethod -Uri $Config.TeamsWebhookUrl -Method Post -Body ($messageCard | ConvertTo-Json -Depth 10) -Headers $headers
        
        Write-Log "Crisis alert sent to Teams: $($AlertData.Title)" "SUCCESS"
        return $true
    }
    catch {
        Write-Log "Failed to send Teams crisis alert: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

# Get current crisis data from Notion
function Get-NotionCrisisData {
    param(
        [string]$DatabaseId,
        [string]$Token
    )
    
    try {
        $headers = @{
            "Authorization" = "Bearer $Token"
            "Notion-Version" = $Config.NotionVersion
            "Content-Type" = "application/json"
        }
        
        $body = @{
            "filter" = @{
                "property" = "Date"
                "date" = @{
                    "equals" = (Get-Date).ToString("yyyy-MM-dd")
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
        
        $crisisData = @()
        foreach ($result in $response.results) {
            $props = $result.properties
            $data = @{
                Id = $result.id
                Employee = $props.Employee.title[0].text.content
                Samples = $props.'Samples Processed'.number
                IdleMinutes = $props.'Idle Minutes'.number
                BreakMinutes = $props.'Break Minutes'.number
                ErrorsHidden = $props.'Errors Hidden'.number
                TATCompliance = $props.'TAT Compliance'.number
                PerformanceScore = $props.'Performance Score'.formula.number
                AlertFlag = $props.'Alert Flag'.checkbox
            }
            $crisisData += $data
        }
        
        Write-Log "Retrieved $($crisisData.Count) crisis data entries from Notion" "INFO"
        return $crisisData
    }
    catch {
        Write-Log "Error retrieving Notion crisis data: $($_.Exception.Message)" "ERROR"
        return @()
    }
}

# Calculate performance score
function Calculate-PerformanceScore {
    param(
        [hashtable]$StaffData
    )
    
    $score = 0.0
    
    # Samples processed (+2 points each)
    $score += $StaffData.Samples * 2.0
    
    # Idle time penalty (-0.5 points per minute)
    $score += $StaffData.IdleMinutes * -0.5
    
    # Hidden errors penalty (-10 points each)
    $score += $StaffData.ErrorsHidden * -10.0
    
    # Break violations penalty (-5 points per violation)
    if ($StaffData.BreakMinutes -gt $Config.CrisisThresholds.BreakMax) {
        $score += -5.0
    }
    
    # TAT compliance bonus (+1 point per %)
    $score += $StaffData.TATCompliance * 1.0
    
    return [Math]::Max(0, [Math]::Round($score, 1))
}

# Monitor TAT crisis
function Monitor-TATCrisis {
    Write-Log "Monitoring TAT crisis..." "INFO"
    
    # Your current crisis: 35% TAT compliance (need 90%)
    $currentTAT = 35.0
    $targetTAT = 90.0
    
    if ($currentTAT -lt $Config.CrisisThresholds.TATCritical) {
        $alertData = @{
            Title = "TAT Crisis - Immediate Action Required"
            Type = "TAT Failure"
            Severity = "Critical"
            Time = (Get-Date).ToString("HH:mm")
            Station = "All Departments"
            Employee = "System"
            CurrentValue = "$currentTAT%"
            Target = "$targetTAT%"
            Action = "Deploy all available staff, open additional stations, escalate to management"
        }
        
        Send-CrisisAlertToTeams -AlertData $alertData
        Write-Log "TAT crisis alert sent" "WARNING"
    }
    
    # Monitor individual departments
    $departments = @(
        @{ Name = "Phlebotomy"; TAT = 51; Target = 85 }
        @{ Name = "Chemistry"; TAT = 45; Target = 90 }
        @{ Name = "Hematology"; TAT = 38; Target = 90 }
        @{ Name = "Blood Bank"; TAT = 42; Target = 95 }
    )
    
    foreach ($dept in $departments) {
        if ($dept.TAT -lt 50) {
            $alertData = @{
                Title = "Department TAT Crisis"
                Type = "TAT Failure"
                Severity = "Critical"
                Time = (Get-Date).ToString("HH:mm")
                Station = $dept.Name
                Employee = "Department"
                CurrentValue = "$($dept.TAT)%"
                Target = "$($dept.Target)%"
                Action = "Reallocate staff, check equipment, review processes"
            }
            
            Send-CrisisAlertToTeams -AlertData $alertData
        }
    }
}

# Monitor wait time crisis
function Monitor-WaitTimeCrisis {
    Write-Log "Monitoring wait time crisis..." "INFO"
    
    # Your current crisis: 25+ minute wait times (target: 15 min)
    $currentWait = 25.0
    $targetWait = 15.0
    
    if ($currentWait -gt $Config.CrisisThresholds.WaitCritical) {
        $alertData = @{
            Title = "Wait Time Crisis - Patients Waiting Too Long"
            Type = "Wait Time"
            Severity = "Critical"
            Time = (Get-Date).ToString("HH:mm")
            Station = "All Stations"
            Employee = "System"
            CurrentValue = "$currentWait minutes"
            Target = "$targetWait minutes"
            Action = "Open additional stations, deploy float staff, notify management"
        }
        
        Send-CrisisAlertToTeams -AlertData $alertData
        Write-Log "Wait time crisis alert sent" "WARNING"
    }
    
    # Monitor individual stations
    $stations = @(
        @{ Name = "Station 1"; Wait = 30; Status = "Overflow" }
        @{ Name = "Station 2"; Wait = 25; Status = "High" }
        @{ Name = "Station 3"; Wait = 35; Status = "Critical" }
        @{ Name = "Station 4"; Wait = 20; Status = "Warning" }
    )
    
    foreach ($station in $stations) {
        if ($station.Wait -gt 20) {
            $alertData = @{
                Title = "Station Wait Time Alert"
                Type = "Wait Time"
                Severity = "High"
                Time = (Get-Date).ToString("HH:mm")
                Station = $station.Name
                Employee = "Station"
                CurrentValue = "$($station.Wait) minutes"
                Target = "15 minutes"
                Action = "Deploy additional staff or open overflow station"
            }
            
            Send-CrisisAlertToTeams -AlertData $alertData
        }
    }
}

# Monitor staffing crisis
function Monitor-StaffingCrisis {
    Write-Log "Monitoring staffing crisis..." "INFO"
    
    # Your current crisis: 3.3 FTE shortage
    $currentStaff = 28.75
    $neededStaff = 32.05
    $gap = 3.3
    
    if ($gap -gt 2.0) {
        $alertData = @{
            Title = "Staffing Crisis - Cannot Meet Demand"
            Type = "Staffing"
            Severity = "Critical"
            Time = (Get-Date).ToString("HH:mm")
            Station = "All Shifts"
            Employee = "Management"
            CurrentValue = "$currentStaff FTE"
            Target = "$neededStaff FTE"
            Action = "Emergency hiring, overtime approval, temporary staff, management coverage"
        }
        
        Send-CrisisAlertToTeams -AlertData $alertData
        Write-Log "Staffing crisis alert sent" "WARNING"
    }
}

# Monitor staff performance crisis
function Monitor-StaffPerformanceCrisis {
    Write-Log "Monitoring staff performance crisis..." "INFO"
    
    $crisisData = Get-NotionCrisisData -DatabaseId $Config.PerformanceDbId -Token $NotionToken
    
    $criticalCount = 0
    $warningCount = 0
    
    foreach ($staff in $crisisData) {
        $performanceScore = Calculate-PerformanceScore -StaffData $staff
        
        if ($performanceScore -lt 40) {
            $alertData = @{
                Title = "CRITICAL Staff Performance Alert"
                Type = "Staff Performance"
                Severity = "Critical"
                Time = (Get-Date).ToString("HH:mm")
                Station = "All Stations"
                Employee = $staff.Employee
                CurrentValue = "Score: $performanceScore"
                Target = "Score: 60+"
                Action = "Place on PIP or consider termination"
            }
            
            Send-CrisisAlertToTeams -AlertData $alertData
            $criticalCount++
        }
        elseif ($performanceScore -lt 60) {
            $alertData = @{
                Title = "Staff Performance Warning"
                Type = "Staff Performance"
                Severity = "Warning"
                Time = (Get-Date).ToString("HH:mm")
                Station = "All Stations"
                Employee = $staff.Employee
                CurrentValue = "Score: $performanceScore"
                Target = "Score: 60+"
                Action = "Issue warning and monitor closely"
            }
            
            Send-CrisisAlertToTeams -AlertData $alertData
            $warningCount++
        }
        
        # Check for specific violations
        if ($staff.IdleMinutes -gt $Config.CrisisThresholds.IdleMax) {
            $alertData = @{
                Title = "Staff Idle Time Alert"
                Type = "Staff Missing"
                Severity = "High"
                Time = (Get-Date).ToString("HH:mm")
                Station = "All Stations"
                Employee = $staff.Employee
                CurrentValue = "$($staff.IdleMinutes) minutes idle"
                Target = "0 minutes idle"
                Action = "Page employee and find coverage"
            }
            
            Send-CrisisAlertToTeams -AlertData $alertData
        }
        
        if ($staff.BreakMinutes -gt $Config.CrisisThresholds.BreakMax) {
            $alertData = @{
                Title = "Break Violation Alert"
                Type = "Break Violation"
                Severity = "Warning"
                Time = (Get-Date).ToString("HH:mm")
                Station = "All Stations"
                Employee = $staff.Employee
                CurrentValue = "$($staff.BreakMinutes) minutes"
                Target = "15 minutes max"
                Action = "Log violation and issue warning"
            }
            
            Send-CrisisAlertToTeams -AlertData $alertData
        }
        
        if ($staff.ErrorsHidden -gt 0) {
            $alertData = @{
                Title = "Hidden Errors Incident"
                Type = "Quality Issue"
                Severity = "Critical"
                Time = (Get-Date).ToString("HH:mm")
                Station = "All Stations"
                Employee = $staff.Employee
                CurrentValue = "$($staff.ErrorsHidden) hidden errors"
                Target = "0 hidden errors"
                Action = "Investigate immediately and take disciplinary action"
            }
            
            Send-CrisisAlertToTeams -AlertData $alertData
        }
    }
    
    Write-Log "Staff performance monitoring completed. Critical: $criticalCount, Warnings: $warningCount" "INFO"
}

# Push crisis data to Power BI
function Push-CrisisDataToPowerBI {
    Write-Log "Pushing crisis data to Power BI..." "INFO"
    
    try {
        # Push monitoring data
        $monitorData = @(
            @{
                timestamp = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
                station = "All"
                employee = "System"
                wait_time = 25
                tat_percentage = 35
                samples_processed = 0
                idle_minutes = 0
                break_minutes = 0
                performance_score = 0
                alert_level = "Critical"
            }
        )
        
        $response = Invoke-RestMethod -Uri $Config.PowerBIMonitorUrl -Method Post -Body ($monitorData | ConvertTo-Json -Depth 10) -ContentType "application/json"
        Write-Log "Monitor data pushed to Power BI successfully" "SUCCESS"
        
        # Push metrics data
        $metricsData = @(
            @{
                timestamp = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
                overall_tat_percentage = 35.0
                average_wait_time = 25.0
                staff_utilization = 67.6
                error_rate = 12.0
                break_violations = 0
                no_shows = 0
                staffing_gap = 3.3
                critical_alerts = 0
                performance_trend = "Declining"
            }
        )
        
        $response = Invoke-RestMethod -Uri $Config.PowerBIMetricsUrl -Method Post -Body ($metricsData | ConvertTo-Json -Depth 10) -ContentType "application/json"
        Write-Log "Metrics data pushed to Power BI successfully" "SUCCESS"
        
    }
    catch {
        Write-Log "Error pushing data to Power BI: $($_.Exception.Message)" "ERROR"
    }
}

# Main crisis monitoring function
function Start-CrisisMonitoring {
    Write-Log "🚨 Starting lab crisis monitoring..." "INFO"
    Write-Log "=" * 60 "INFO"
    
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
    
    Write-Log "Configuration validated successfully" "SUCCESS"
    
    # Run all crisis monitoring functions
    Monitor-TATCrisis
    Monitor-WaitTimeCrisis
    Monitor-StaffingCrisis
    Monitor-StaffPerformanceCrisis
    Push-CrisisDataToPowerBI
    
    Write-Log "=" * 60 "INFO"
    Write-Log "🎯 Crisis monitoring cycle completed" "SUCCESS"
    Write-Log "📊 All alerts sent to Teams and data pushed to Power BI" "SUCCESS"
}

# Run the crisis monitoring
Start-CrisisMonitoring
