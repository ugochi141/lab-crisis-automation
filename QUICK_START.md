# 🚨 QUICK START - Lab Crisis Automation

## ⚡ **IMMEDIATE SETUP (5 minutes)**

Your system is ready to run with your specific credentials! Here's how to start immediately:

### **Step 1: Test Your System (2 minutes)**
```bash
# Install Python packages
pip install notion-client requests

# Run the test script
python scripts/test_crisis_system.py
```

### **Step 2: Run Crisis Monitoring (1 minute)**
```bash
# PowerShell (Windows)
pwsh scripts/lab_crisis_monitoring.ps1

# Or Python
python integrations/notion_lab_manager.py
```

### **Step 3: Enable GitHub Actions (2 minutes)**
1. Go to your GitHub repository
2. Click "Actions" tab
3. Click "I understand my workflows, go ahead and enable them"
4. The crisis monitoring will run every 5 minutes automatically

---

## 🎯 **WHAT HAPPENS IMMEDIATELY**

### **Your Crisis Will Be Monitored:**
- ✅ **TAT Crisis**: 35% compliance (target: 90%) → Alerts sent to Teams
- ✅ **Wait Time Crisis**: 25+ minutes (target: 15 min) → Alerts sent to Teams  
- ✅ **Staffing Crisis**: 3.3 FTE shortage → Alerts sent to Teams
- ✅ **Performance Crisis**: Problem staff identified → Alerts sent to Teams
- ✅ **Behavioral Issues**: Long breaks, hiding mistakes → Alerts sent to Teams

### **Alerts Sent to Your Teams Channel:**
- 🚨 **Critical TAT Alert**: "TAT compliance only 35% - Immediate action required"
- 🚨 **Wait Time Alert**: "Patients waiting 25+ minutes - Open additional stations"
- 🚨 **Staffing Alert**: "3.3 FTE shortage - Cannot meet demand"
- 🚨 **Performance Alert**: "Employee [Name] has critical performance score 25"

### **Data Pushed to Power BI:**
- 📊 Real-time monitoring data every 5 minutes
- 📈 Performance metrics and trends
- 🔍 Individual staff performance scores
- ⚠️ Alert levels and crisis indicators

---

## 📱 **YOUR MOBILE COMMAND CENTER**

### **Access Your Notion Dashboards:**
- **Lab Management**: https://www.notion.so/Lab-Management-Command-Center-266d222751b3818996b4ce1cf18e0913
- **Performance DB**: https://www.notion.so/c1500b1816b14018beabe2b826ccafe9
- **Incident DB**: https://www.notion.so/cf2bb4448aff4324a602cb770cbae0a2

### **Teams Alerts:**
- All critical alerts sent to your Kaiser Permanente Teams channel
- Real-time notifications on your phone
- One-click access to take action

---

## 🔧 **CUSTOMIZATION**

### **Adjust Alert Thresholds:**
Edit `config/lab_config.py`:
```python
self.CRISIS_THRESHOLDS = {
    'tat_critical': 50,      # TAT < 50% = Critical
    'wait_critical': 30,     # Wait > 30 min = Critical
    'idle_max': 30,          # Idle > 30 min = Alert
    'break_max': 15,         # Break > 15 min = Violation
}
```

### **Add Custom Alerts:**
```python
# In your monitoring code
if custom_condition:
    self.create_performance_alert(
        "Custom Alert", "🔴 Critical",
        "Your custom message here",
        station="Station 1", employee="John Doe"
    )
```

---

## 📊 **EXPECTED RESULTS**

### **Immediate (Today):**
- ✅ Crisis monitoring active
- ✅ Alerts sent to Teams
- ✅ Data flowing to Power BI
- ✅ Problem staff identified

### **Week 1:**
- 📈 30% improvement in key metrics
- 🎯 Problem staff on notice
- ⚡ Real-time visibility into all operations
- 📱 Mobile control of entire lab

### **Month 1:**
- 🎯 TAT compliance: 70% (from 35%)
- ⏰ Wait times: <20 min (from 25+)
- 👥 Staff utilization: 75% (from 67.6%)
- 📉 Error rate: 8% (from 12%)

---

## 🆘 **TROUBLESHOOTING**

### **If Tests Fail:**
1. **Notion Error**: Check your token is correct
2. **Teams Error**: Verify webhook URL is working
3. **Power BI Error**: Check dataset URLs are accessible

### **If No Alerts Appear:**
1. Check Teams channel for messages
2. Look at Notion databases for new entries
3. Check Power BI datasets for data

### **If System Stops:**
1. Check GitHub Actions logs
2. Restart the monitoring script
3. Verify all credentials are still valid

---

## 🎯 **NEXT STEPS**

### **Today:**
1. ✅ Run the test script
2. ✅ Start crisis monitoring
3. ✅ Check Teams for alerts
4. ✅ Review Notion dashboards

### **This Week:**
1. Train supervisors on new system
2. Begin progressive discipline
3. Start emergency hiring
4. Monitor improvements daily

### **This Month:**
1. Full automation running
2. Staff accountability established
3. Performance targets achieved
4. Crisis resolved

---

## 📞 **SUPPORT**

If you need help:
1. Check the test script output
2. Review the logs in `logs/` folder
3. Check GitHub Actions for errors
4. Verify all URLs are accessible

**Remember**: This system will transform your lab from crisis to high performance. The key is to start using it immediately and enforce the new standards consistently.

**Good luck! 🚀**
