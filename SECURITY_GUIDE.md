# 🔒 Security & HIPAA Compliance Guide
## Kaiser Permanente Lab Automation System

### ⚠️ CRITICAL SECURITY NOTICE

**Your credentials have been exposed in plain text. Take immediate action:**

1. **Rotate ALL credentials immediately**
2. **Secure your environment files**
3. **Review access logs**
4. **Implement the security measures below**

---

## 🚨 Immediate Security Actions Required

### 1. Rotate Exposed Credentials

#### Notion Integration Token
- Go to https://www.notion.so/my-integrations
- Revoke current token: `[YOUR_CURRENT_TOKEN]`
- Generate new integration token
- Update `.env` file with new token

#### Power BI API Keys
- Access Power BI Admin Portal
- Revoke current keys:
  - Performance: `E8RCLTiv4Zd17FW9sumuDuyR2hNLN2SPp%2F%2BOL4vfTo64RzKcjJWSPh%2Bjwivz7w0vwk8sGB%2B57EtsEQSFP8VzwQ%3D%3D`
  - Operations: `Yd7yXwwYIUbzaYpP5FNkYM8BtK1GjZVXLiNAIST7QMF8t%2FEbG6WBlaM8YCO6LO6mUbXffKTaIMeaux0vEweQLQ%3D%3D`
- Generate new API keys
- Update dataset configurations

#### Teams Webhook URL
- Go to Teams channel settings
- Delete current webhook
- Create new webhook URL
- Update `.env` file

### 2. Secure Environment Files

```bash
# Set restrictive permissions
chmod 600 .env
chmod 600 config/*.json

# Remove from version control if committed
git rm --cached .env
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Remove sensitive environment file"
```

### 3. Review Access Logs

```bash
# Check for unauthorized access
grep -i "unauthorized\|failed\|error" logs/audit_trail.log
grep -i "login\|access" logs/lab_automation.log

# Review recent API calls
tail -n 100 logs/audit_trail.log | grep "API_CALL"
```

---

## 🛡️ Comprehensive Security Implementation

### Environment Variable Security

#### 1. Use Environment Variable Encryption
```bash
# Generate encryption key
python -c "from config.config_manager import generate_encryption_key; print(generate_encryption_key())"

# Encrypt sensitive values
python -c "
from cryptography.fernet import Fernet
key = b'your-encryption-key-here'
f = Fernet(key)
encrypted = f.encrypt(b'your-sensitive-value')
print('enc:' + encrypted.decode())
"
```

#### 2. Implement Azure Key Vault (Recommended)
```python
# Install Azure Key Vault SDK
pip install azure-keyvault-secrets azure-identity

# Example implementation
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://your-vault.vault.azure.net/", credential=credential)

# Store secrets
client.set_secret("notion-api-token", "your-new-token")
client.set_secret("powerbi-api-key", "your-new-key")
```

### File System Security

#### 1. Set Proper File Permissions
```bash
# Linux/Mac permissions
chmod 700 /Users/ugochi141/Desktop/LabAutomation
chmod 600 .env config/*.json
chmod 700 logs/
chmod 600 logs/*.log

# Create secure directories
mkdir -p secure/{keys,certs}
chmod 700 secure/
```

#### 2. Implement File Encryption
```bash
# Encrypt sensitive configuration files
gpg --symmetric --cipher-algo AES256 config/production.json
rm config/production.json  # Remove unencrypted version
```

### Network Security

#### 1. API Endpoint Security
```python
# Implement request signing
import hmac
import hashlib
import time

def sign_request(secret_key: str, payload: str) -> str:
    timestamp = str(int(time.time()))
    message = f"{timestamp}.{payload}"
    signature = hmac.new(
        secret_key.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    return f"t={timestamp},v1={signature}"
```

#### 2. TLS/SSL Configuration
```python
# Enforce HTTPS for all API calls
import aiohttp
import ssl

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED

async with aiohttp.ClientSession(
    connector=aiohttp.TCPConnector(ssl=ssl_context)
) as session:
    # Your API calls here
    pass
```

### Authentication & Authorization

#### 1. Implement Service Account Authentication
```python
# Example service account setup
class ServiceAccount:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expiry = None
    
    async def get_access_token(self) -> str:
        if self.token_expiry and datetime.now() < self.token_expiry:
            return self.access_token
        
        # Refresh token logic
        # ...
        
        return self.access_token
```

#### 2. Role-Based Access Control
```python
# Define access roles
ROLES = {
    'admin': ['read', 'write', 'delete', 'configure'],
    'supervisor': ['read', 'write', 'alert'],
    'technician': ['read', 'update_performance'],
    'readonly': ['read']
}

def check_permission(user_role: str, action: str) -> bool:
    return action in ROLES.get(user_role, [])
```

---

## 📋 HIPAA Compliance Implementation

### Audit Logging Requirements

#### 1. Comprehensive Audit Trail
```python
# Enhanced audit logging
class HIPAAAuditLogger:
    def log_phi_access(self, user_id: str, patient_id: str, action: str):
        """Log PHI access events"""
        self._log_audit_entry(
            event_type="PHI_ACCESS",
            action=action,
            details={
                "patient_id_hash": self._hash_patient_id(patient_id),
                "access_reason": "lab_operations",
                "data_elements": ["lab_results", "demographics"]
            },
            user_id=user_id
        )
    
    def _hash_patient_id(self, patient_id: str) -> str:
        """Hash patient ID for audit compliance"""
        return hashlib.sha256(patient_id.encode()).hexdigest()[:16]
```

#### 2. Data Retention Policy
```bash
# Implement automated log rotation
# /etc/logrotate.d/lab-automation
/Users/ugochi141/Desktop/LabAutomation/logs/*.log {
    daily
    rotate 2555  # 7 years retention
    compress
    delaycompress
    missingok
    create 0600 labautomation labautomation
}
```

### Data Protection

#### 1. Encryption at Rest
```python
# Encrypt sensitive data before storage
from cryptography.fernet import Fernet

class DataEncryption:
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)
    
    def encrypt_patient_data(self, data: dict) -> str:
        """Encrypt patient data for storage"""
        json_data = json.dumps(data)
        encrypted = self.cipher.encrypt(json_data.encode())
        return encrypted.decode()
    
    def decrypt_patient_data(self, encrypted_data: str) -> dict:
        """Decrypt patient data for processing"""
        decrypted = self.cipher.decrypt(encrypted_data.encode())
        return json.loads(decrypted.decode())
```

#### 2. Data Minimization
```python
# Only collect necessary data
def sanitize_performance_data(raw_data: dict) -> dict:
    """Remove unnecessary PHI from performance data"""
    allowed_fields = [
        'staff_member', 'date', 'shift', 'samples_processed',
        'error_count', 'performance_score', 'tat_target_met'
    ]
    return {k: v for k, v in raw_data.items() if k in allowed_fields}
```

### Access Controls

#### 1. Multi-Factor Authentication
```python
# Implement TOTP for admin access
import pyotp

class MFAAuth:
    def generate_secret(self) -> str:
        return pyotp.random_base32()
    
    def verify_totp(self, secret: str, token: str) -> bool:
        totp = pyotp.TOTP(secret)
        return totp.verify(token, valid_window=1)
```

#### 2. Session Management
```python
# Secure session handling
class SecureSession:
    def __init__(self, timeout_minutes: int = 30):
        self.timeout = timedelta(minutes=timeout_minutes)
        self.sessions = {}
    
    def create_session(self, user_id: str) -> str:
        session_id = secrets.token_urlsafe(32)
        self.sessions[session_id] = {
            'user_id': user_id,
            'created': datetime.now(),
            'last_activity': datetime.now()
        }
        return session_id
    
    def validate_session(self, session_id: str) -> bool:
        session = self.sessions.get(session_id)
        if not session:
            return False
        
        if datetime.now() - session['last_activity'] > self.timeout:
            del self.sessions[session_id]
            return False
        
        session['last_activity'] = datetime.now()
        return True
```

---

## 🔍 Security Monitoring

### 1. Intrusion Detection
```python
# Monitor for suspicious activities
class SecurityMonitor:
    def __init__(self):
        self.failed_attempts = {}
        self.rate_limits = {}
    
    def check_rate_limit(self, user_id: str, action: str) -> bool:
        """Check if user is within rate limits"""
        key = f"{user_id}:{action}"
        now = time.time()
        
        if key not in self.rate_limits:
            self.rate_limits[key] = []
        
        # Remove old attempts (older than 1 hour)
        self.rate_limits[key] = [
            t for t in self.rate_limits[key] 
            if now - t < 3600
        ]
        
        # Check if under limit (e.g., 100 requests per hour)
        if len(self.rate_limits[key]) >= 100:
            return False
        
        self.rate_limits[key].append(now)
        return True
```

### 2. Vulnerability Scanning
```bash
# Regular security scans
pip install safety bandit

# Check for known vulnerabilities
safety check --json

# Static code analysis
bandit -r automation/ integrations/ utils/ -f json
```

### 3. Log Analysis
```python
# Automated log analysis
import re
from collections import defaultdict

class LogAnalyzer:
    def analyze_security_events(self, log_file: str) -> dict:
        """Analyze logs for security events"""
        events = defaultdict(int)
        suspicious_ips = set()
        
        with open(log_file, 'r') as f:
            for line in f:
                # Check for failed authentication
                if 'AUTHENTICATION_FAILURE' in line:
                    events['failed_auth'] += 1
                
                # Check for unusual access patterns
                if 'API_CALL' in line and 'ERROR' in line:
                    events['api_errors'] += 1
                
                # Extract IP addresses from suspicious events
                ip_match = re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', line)
                if ip_match and 'FAILURE' in line:
                    suspicious_ips.add(ip_match.group())
        
        return {
            'events': dict(events),
            'suspicious_ips': list(suspicious_ips)
        }
```

---

## 🚀 Deployment Security

### 1. Container Security
```dockerfile
# Secure Dockerfile
FROM python:3.9-slim

# Create non-root user
RUN groupadd -r labuser && useradd -r -g labuser labuser

# Set secure permissions
RUN mkdir /app && chown labuser:labuser /app
WORKDIR /app

# Install dependencies as root, then switch to user
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application and set ownership
COPY --chown=labuser:labuser . .

# Switch to non-root user
USER labuser

# Remove shell access
RUN rm -rf /bin/bash /bin/sh || true

# Set security options
LABEL security.scan="enabled"
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

CMD ["python", "-m", "automation.lab_automation_core"]
```

### 2. Kubernetes Security
```yaml
# secure-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: lab-automation
  labels:
    app: lab-automation
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
  containers:
  - name: lab-automation
    image: lab-automation:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
    resources:
      limits:
        memory: "1Gi"
        cpu: "500m"
      requests:
        memory: "512Mi"
        cpu: "250m"
    volumeMounts:
    - name: config
      mountPath: /app/.env
      subPath: .env
      readOnly: true
  volumes:
  - name: config
    secret:
      secretName: lab-automation-config
```

---

## 📊 Security Checklist

### Immediate Actions (Do Now)
- [ ] Rotate all exposed credentials
- [ ] Set proper file permissions (600 for .env, 700 for directories)
- [ ] Remove credentials from any version control
- [ ] Generate and configure encryption keys
- [ ] Enable audit logging
- [ ] Configure secure backup procedures

### Short Term (This Week)
- [ ] Implement Azure Key Vault for credential management
- [ ] Set up TLS/SSL for all communications
- [ ] Configure rate limiting and intrusion detection
- [ ] Implement multi-factor authentication for admin access
- [ ] Set up automated vulnerability scanning
- [ ] Create incident response procedures

### Long Term (This Month)
- [ ] Complete HIPAA compliance audit
- [ ] Implement data encryption at rest
- [ ] Set up centralized logging and SIEM
- [ ] Conduct penetration testing
- [ ] Create disaster recovery procedures
- [ ] Implement zero-trust architecture
- [ ] Regular security training for staff

### Ongoing Monitoring
- [ ] Daily: Review security logs and alerts
- [ ] Weekly: Vulnerability scans and updates
- [ ] Monthly: Access review and credential rotation
- [ ] Quarterly: Security assessment and penetration testing
- [ ] Annually: Full HIPAA compliance audit

---

## 🆘 Incident Response Plan

### 1. Security Incident Detection
```python
# Automated incident detection
class IncidentDetector:
    def check_for_incidents(self):
        incidents = []
        
        # Check for multiple failed logins
        if self.count_failed_logins() > 10:
            incidents.append("Multiple failed login attempts")
        
        # Check for unusual data access
        if self.check_unusual_access_patterns():
            incidents.append("Unusual data access pattern detected")
        
        # Check for system anomalies
        if self.check_system_anomalies():
            incidents.append("System performance anomaly")
        
        return incidents
```

### 2. Incident Response Procedures
1. **Immediate Response** (0-15 minutes)
   - Isolate affected systems
   - Preserve evidence
   - Notify security team

2. **Assessment** (15-60 minutes)
   - Determine scope and impact
   - Identify root cause
   - Document findings

3. **Containment** (1-4 hours)
   - Stop the incident from spreading
   - Implement temporary fixes
   - Monitor for additional activity

4. **Recovery** (4-24 hours)
   - Restore systems from clean backups
   - Apply security patches
   - Update security controls

5. **Post-Incident** (1-7 days)
   - Complete incident report
   - Update security procedures
   - Conduct lessons learned session

---

**🔒 Remember: Security is an ongoing process, not a one-time setup. Regularly review and update your security measures to protect patient data and maintain HIPAA compliance.**
