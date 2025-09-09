# 🚨 Lab Crisis Automation System

A comprehensive automation system for monitoring and managing lab performance crises using Notion, Microsoft Teams, and Power BI integration.

## 🎯 Features

- **Real-time Crisis Monitoring**: Tracks TAT compliance, wait times, staffing gaps, and performance metrics
- **Automated Teams Alerts**: Sends critical alerts to Microsoft Teams channels
- **Notion Integration**: Tracks staff performance and incidents in Notion databases
- **Power BI Integration**: Streams data to Power BI dashboards
- **GitHub Actions**: Automated monitoring every 5 minutes during business hours
- **Mobile Command Center**: Access dashboards and control lab operations from mobile devices

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/ugochi141/lab-crisis-automation.git
cd lab-crisis-automation
```

### 2. Set Up Environment Variables
```bash
# Copy the example environment file
cp env.example .env

# Edit .env with your actual credentials
nano .env
```

Required environment variables:
```bash
NOTION_API_TOKEN=your_notion_token_here
NOTION_PERFORMANCE_DB_ID=your_performance_db_id_here
NOTION_INCIDENT_DB_ID=your_incident_db_id_here
TEAMS_WEBHOOK_URL=your_teams_webhook_url_here
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Test the System
```bash
python scripts/secure_crisis_monitor.py
```

### 5. Set Up GitHub Secrets
Go to your repository settings → Secrets and variables → Actions, and add:
- `NOTION_API_TOKEN`
- `NOTION_PERFORMANCE_DB_ID`
- `NOTION_INCIDENT_DB_ID`
- `NOTION_LAB_MANAGEMENT_CENTER`
- `TEAMS_WEBHOOK_URL`
- `POWERBI_MONITOR_PUSH_URL` (optional)
- `POWERBI_METRICS_PUSH_URL` (optional)

## 📊 Crisis Metrics Monitored

- **TAT Compliance**: 35% → 90% target
- **Wait Times**: 25+ min → 15 min target
- **Staffing Gap**: 3.3 FTE shortage
- **Error Rate**: 12% → 5% target
- **Staff Utilization**: 67.6% → 80% target

## 🎯 What This System Solves

### Current Crisis Issues:
- ✅ **TAT Crisis**: Only 35% meeting targets (need 90%)
- ✅ **Staffing Shortage**: 3.3 FTE gap
- ✅ **Behavioral Issues**: Staff sneaking off, hiding mistakes
- ✅ **Idle Time**: 32.4% average (target: ≤20%)
- ✅ **No-shows**: 1,026 per month

### Automated Solutions:
- 🤖 **Real-time monitoring** every 5 minutes
- 🚨 **Instant alerts** sent to Teams when issues occur
- 📊 **Performance tracking** with AI-powered scoring
- 📱 **Mobile control** of entire lab operations
- 📈 **Data-driven decisions** with automated reporting

## 📱 Mobile Command Center

Access your dashboards:
- **Lab Management**: [Notion Dashboard](https://www.notion.so/Lab-Management-Command-Center-266d222751b3818996b4ce1cf18e0913)
- **Performance DB**: [Performance Tracking](https://www.notion.so/c1500b1816b14018beabe2b826ccafe9)
- **Incident DB**: [Incident Tracking](https://www.notion.so/cf2bb4448aff4324a602cb770cbae0a2)

## 🔧 Configuration

### Alert Thresholds
Edit `config/secure_config.py` to adjust thresholds:
```python
self.CRISIS_THRESHOLDS = {
    'tat_critical': 50,      # TAT < 50% = Critical
    'wait_critical': 30,     # Wait > 30 min = Critical
    'idle_max': 30,          # Idle > 30 min = Alert
    'break_max': 15,         # Break > 15 min = Violation
}
```

### Custom Alerts
Add custom monitoring logic in `scripts/secure_crisis_monitor.py`:
```python
if custom_condition:
    alert_data = {
        'title': 'Custom Alert',
        'type': 'Custom Type',
        'severity': 'Critical',
        'action': 'Custom action required'
    }
    send_teams_alert(config.TEAMS_WEBHOOK_URL, alert_data)
```

## 📈 Expected Results

### Week 1:
- ✅ Crisis monitoring active
- ✅ Alerts sent to Teams
- ✅ Data flowing to Notion
- ✅ Problem staff identified

### Month 1:
- 🎯 TAT compliance: 70% (from 35%)
- ⏰ Wait times: <20 min (from 25+)
- 👥 Staff utilization: 75% (from 67.6%)
- 📉 Error rate: 8% (from 12%)

### Month 3:
- 🎯 All targets achieved
- 🤖 Fully automated operations
- 📊 Sustained improvements
- 💰 Cost savings: $4,500/day

## 🛠️ Troubleshooting

### Common Issues:

1. **Environment Variables Not Set**
   ```bash
   export NOTION_API_TOKEN='your_token_here'
   export TEAMS_WEBHOOK_URL='your_webhook_here'
   ```

2. **Notion Connection Failed**
   - Check your API token
   - Verify database IDs are correct
   - Ensure integration has access to databases

3. **Teams Alerts Not Working**
   - Test webhook URL in browser
   - Check Teams channel permissions
   - Verify webhook is active

4. **GitHub Actions Failing**
   - Check repository secrets are set
   - Review Actions logs for errors
   - Verify workflow file syntax

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review logs in `logs/` directory
3. Check GitHub Actions for error details
4. Create an issue in this repository

## 🔒 Security

- All sensitive data stored in environment variables
- No hardcoded credentials in code
- GitHub Secrets used for CI/CD
- Secure configuration management

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Ready to transform your lab from crisis to high performance? 🚀**
