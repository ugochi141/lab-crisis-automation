#!/usr/bin/env node
/**
 * Enhanced Dashboard Builder
 * Creates unified dashboard for all lab systems
 */

const fs = require('fs');
const path = require('path');

class DashboardBuilder {
    constructor() {
        this.dashboardData = {
            timestamp: new Date().toISOString(),
            title: 'Lab Automation Dashboard',
            version: '2.0.0',
            sections: [],
            metrics: {},
            alerts: []
        };
    }

    loadReports() {
        console.log('📊 Loading analysis reports...');
        
        const reportsDir = path.join(process.cwd(), 'reports');
        
        // Load health report
        try {
            const healthReport = JSON.parse(
                fs.readFileSync(path.join(reportsDir, 'health_report.json'), 'utf8')
            );
            this.dashboardData.health = healthReport;
            console.log('✓ Health report loaded');
        } catch (e) {
            console.log('⚠️  Health report not found');
        }
        
        // Load repository analysis
        try {
            const repoAnalysis = JSON.parse(
                fs.readFileSync(path.join(reportsDir, 'repo_analysis.json'), 'utf8')
            );
            this.dashboardData.repositories = repoAnalysis;
            console.log('✓ Repository analysis loaded');
        } catch (e) {
            console.log('⚠️  Repository analysis not found');
        }
        
        // Load performance analysis
        try {
            const perfAnalysis = JSON.parse(
                fs.readFileSync(path.join(reportsDir, 'performance_analysis.json'), 'utf8')
            );
            this.dashboardData.performance = perfAnalysis;
            console.log('✓ Performance analysis loaded');
        } catch (e) {
            console.log('⚠️  Performance analysis not found');
        }
    }

    buildSections() {
        console.log('🔨 Building dashboard sections...');
        
        // System Health Section
        this.dashboardData.sections.push({
            id: 'system-health',
            title: 'System Health',
            type: 'status',
            data: {
                status: this.dashboardData.health?.status || 'unknown',
                checks: this.dashboardData.health?.checks || {},
                lastUpdate: this.dashboardData.health?.timestamp || new Date().toISOString()
            }
        });
        
        // Performance Metrics Section
        this.dashboardData.sections.push({
            id: 'performance-metrics',
            title: 'Performance Metrics',
            type: 'metrics',
            data: {
                tatCompliance: this.dashboardData.performance?.lab_operations?.tat_compliance?.current || 0,
                qcPassRate: this.dashboardData.performance?.lab_operations?.qc_performance?.pass_rate || 0,
                automationRate: this.dashboardData.performance?.workflow_efficiency?.automation_rate?.current || 0,
                systemUptime: this.dashboardData.performance?.system_performance?.availability?.uptime_percent || 0
            }
        });
        
        // Repository Status Section
        this.dashboardData.sections.push({
            id: 'repository-status',
            title: 'Repository Status',
            type: 'table',
            data: {
                repositories: this.dashboardData.repositories?.repositories || [],
                summary: this.dashboardData.repositories?.summary || {}
            }
        });
        
        // Alerts Section
        if (this.dashboardData.performance?.bottlenecks?.length > 0) {
            this.dashboardData.alerts = this.dashboardData.performance.bottlenecks.map(b => ({
                severity: b.severity,
                area: b.area,
                message: `${b.area}: ${b.current_value} (target: ${b.target_value})`,
                impact: b.impact
            }));
        }
        
        console.log(`✓ Built ${this.dashboardData.sections.length} sections`);
    }

    generateHTML() {
        console.log('📝 Generating HTML dashboard...');
        
        const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${this.dashboardData.title}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        h1 {
            color: white;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
        }
        .card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        .card:hover {
            transform: translateY(-5px);
        }
        .card h2 {
            color: #333;
            margin-bottom: 20px;
            font-size: 1.4em;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        .metric {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 15px 0;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        .metric-value {
            font-size: 1.8em;
            font-weight: bold;
            color: #667eea;
        }
        .status-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.85em;
        }
        .status-healthy { background: #d4edda; color: #155724; }
        .status-warning { background: #fff3cd; color: #856404; }
        .status-critical { background: #f8d7da; color: #721c24; }
        .alert {
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            border-left: 4px solid;
        }
        .alert-high { background: #f8d7da; border-color: #dc3545; }
        .alert-medium { background: #fff3cd; border-color: #ffc107; }
        .alert-low { background: #d1ecf1; border-color: #17a2b8; }
        .timestamp {
            text-align: center;
            color: white;
            margin-top: 30px;
            opacity: 0.8;
        }
        .progress-bar {
            width: 100%;
            height: 25px;
            background: #e9ecef;
            border-radius: 12px;
            overflow: hidden;
            margin: 10px 0;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transition: width 0.5s;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 ${this.dashboardData.title}</h1>
        
        <div class="dashboard-grid">
            <!-- System Health Card -->
            <div class="card">
                <h2>System Health</h2>
                <div class="status-badge status-${this.dashboardData.health?.status || 'unknown'}">
                    ${this.dashboardData.health?.status || 'Unknown'}
                </div>
                ${this.generateHealthMetrics()}
            </div>
            
            <!-- Performance Score Card -->
            <div class="card">
                <h2>Performance Score</h2>
                ${this.generatePerformanceMetrics()}
            </div>
            
            <!-- Repository Status Card -->
            <div class="card">
                <h2>Repository Status</h2>
                ${this.generateRepoStatus()}
            </div>
            
            <!-- Alerts Card -->
            <div class="card">
                <h2>Active Alerts</h2>
                ${this.generateAlerts()}
            </div>
            
            <!-- Lab Metrics Card -->
            <div class="card">
                <h2>Lab Operations</h2>
                ${this.generateLabMetrics()}
            </div>
            
            <!-- Workflow Status Card -->
            <div class="card">
                <h2>Workflow Status</h2>
                ${this.generateWorkflowStatus()}
            </div>
        </div>
        
        <div class="timestamp">
            Last Updated: ${new Date().toLocaleString()}
        </div>
    </div>
    
    <script>
        // Auto-refresh every 60 seconds
        setTimeout(() => location.reload(), 60000);
    </script>
</body>
</html>`;
        
        // Save HTML file
        const dashboardPath = path.join(process.cwd(), 'dashboard.html');
        fs.writeFileSync(dashboardPath, html);
        console.log(`✓ Dashboard saved to ${dashboardPath}`);
        
        return dashboardPath;
    }

    generateHealthMetrics() {
        const health = this.dashboardData.health;
        if (!health) return '<p>No health data available</p>';
        
        const metrics = health.metrics || {};
        return Object.entries(metrics).slice(0, 3).map(([key, value]) => `
            <div class="metric">
                <span>${key.replace(/_/g, ' ')}</span>
                <span class="metric-value">${typeof value === 'number' ? value.toFixed(1) : value}</span>
            </div>
        `).join('');
    }

    generatePerformanceMetrics() {
        const perf = this.dashboardData.performance?.performance_score;
        if (!perf) return '<p>No performance data available</p>';
        
        return `
            <div class="metric">
                <span>Overall Score</span>
                <span class="metric-value">${perf.overall || 0}%</span>
            </div>
            <div class="metric">
                <span>Grade</span>
                <span class="metric-value">${perf.grade || 'N/A'}</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${perf.overall || 0}%">
                    ${perf.overall || 0}%
                </div>
            </div>
        `;
    }

    generateRepoStatus() {
        const repos = this.dashboardData.repositories?.summary;
        if (!repos) return '<p>No repository data available</p>';
        
        return `
            <div class="metric">
                <span>Total Repositories</span>
                <span class="metric-value">${repos.total_repositories || 0}</span>
            </div>
            <div class="metric">
                <span>Healthy</span>
                <span class="metric-value">${repos.healthy || 0}</span>
            </div>
            <div class="metric">
                <span>With Tests</span>
                <span class="metric-value">${repos.with_tests || 0}</span>
            </div>
        `;
    }

    generateAlerts() {
        if (!this.dashboardData.alerts || this.dashboardData.alerts.length === 0) {
            return '<p style="color: green;">✓ No active alerts</p>';
        }
        
        return this.dashboardData.alerts.slice(0, 3).map(alert => `
            <div class="alert alert-${alert.severity}">
                <strong>${alert.area}</strong><br>
                ${alert.message}
            </div>
        `).join('');
    }

    generateLabMetrics() {
        const lab = this.dashboardData.performance?.lab_operations;
        if (!lab) return '<p>No lab data available</p>';
        
        return `
            <div class="metric">
                <span>TAT Compliance</span>
                <span class="metric-value">${lab.tat_compliance?.current || 0}%</span>
            </div>
            <div class="metric">
                <span>QC Pass Rate</span>
                <span class="metric-value">${lab.qc_performance?.pass_rate || 0}%</span>
            </div>
            <div class="metric">
                <span>Samples Today</span>
                <span class="metric-value">${lab.sample_volume?.daily_average || 0}</span>
            </div>
        `;
    }

    generateWorkflowStatus() {
        const workflow = this.dashboardData.performance?.workflow_efficiency;
        if (!workflow) return '<p>No workflow data available</p>';
        
        return `
            <div class="metric">
                <span>Automation Rate</span>
                <span class="metric-value">${workflow.automation_rate?.current || 0}%</span>
            </div>
            <div class="metric">
                <span>Pipeline Success</span>
                <span class="metric-value">${workflow.pipeline_performance?.github_actions_success_rate || 0}%</span>
            </div>
            <div class="metric">
                <span>Data Quality</span>
                <span class="metric-value">${workflow.data_quality?.validation_pass_rate || 0}%</span>
            </div>
        `;
    }

    build() {
        console.log('\n🚀 Building Enhanced Dashboard...\n');
        
        this.loadReports();
        this.buildSections();
        const dashboardPath = this.generateHTML();
        
        console.log('\n✅ Dashboard built successfully!');
        console.log(`📊 Open ${dashboardPath} in your browser to view\n`);
        
        return 0;
    }
}

// Main execution
const builder = new DashboardBuilder();
process.exit(builder.build());