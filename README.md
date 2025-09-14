# 🚀 Advanced Login Monitor for Windows (v2.1 Enhanced)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-blue.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Security](https://img.shields.io/badge/security-monitoring-red.svg)](https://github.com)
[![Email](https://img.shields.io/badge/email-HTML%20reports-orange.svg)](mailto:)
[![Webcam](https://img.shields.io/badge/webcam-capture-purple.svg)](https://opencv.org)
[![Offline](https://img.shields.io/badge/offline-capable-green.svg)](https://github.com)
[![Geolocation](https://img.shields.io/badge/geolocation-native%20%2B%20IP-blue.svg)](https://github.com)

A comprehensive, enterprise-grade Python security monitoring system that transforms your Windows PC into an intelligent surveillance hub. This advanced script combines multiple data sources - webcam capture, native Windows location services, system intelligence, and network monitoring - to create detailed HTML security reports that are automatically sent via email. Features robust offline capabilities, multi-API geolocation fallbacks, and professional-grade logging. Perfect for personal security, IT monitoring, and device access tracking! 🕵️‍♂️✨

## ✨ Advanced Core Features

### 🔐 **Multi-Layered Security Intelligence**
* 🤫 **Stealth Operation**: Runs completely invisible using `pythonw.exe` - no windows, console, or system tray icons
* 📸 **Smart Webcam Capture**: Automatically detects and captures from available cameras with optimized initialization timing
* � **Hybrid Geolocation System**: 
  * **Primary**: Native Windows Location Service for GPS-level accuracy (±3-10 meters)
  * **Fallback**: Multi-API IP geolocation with 1-second timeout optimization
  * **APIs**: ipapi.co and ip-api.com with intelligent failover
  * **Google Maps Integration**: Direct clickable links to precise coordinates

### 📊 **Comprehensive System Intelligence**
* **Real-Time Process Monitoring**: Complete snapshot of all running processes at login moment
* **Network Connection Analysis**: Maps active network connections to specific processes (e.g., which app is connecting where)
* **Resource Utilization**: Live CPU and memory usage with optimized 0.1-second sampling
* **Connection Security**: Identifies established connections with IP addresses and ports

### 🌐 **Advanced Connectivity & Offline Features**
* **Internet Connectivity Detection**: Smart connection testing to Google DNS (8.8.8.8) with configurable timeout
* **Offline Report Caching**: Automatically saves reports as JSON when internet is unavailable
* **Automatic Retry System**: Sends cached reports when connection is restored
* **File Management**: Intelligent cleanup of sent reports and associated images

### 📧 **Professional Email Reporting**
* **Rich HTML Templates**: Beautiful, responsive email reports with professional styling
* **Structured Data Tables**: Organized presentation of system, location, and security data
* **Image Attachments**: Secure webcam captures with proper MIME encoding
* **SMTP Security**: Full TLS encryption with Gmail App Password support
* **Custom Subject Lines**: Configurable alert subjects with computer name identification

### 🛡️ **Enterprise-Grade Reliability**
* **Comprehensive Logging**: Detailed `monitor.log` with timestamps and error tracking
* **Configuration Management**: Secure INI file for credentials and settings
* **Error Recovery**: Graceful handling of camera failures, network issues, and API timeouts
* **Cross-Camera Support**: Automatic fallback across multiple camera indices
* **Memory Efficient**: Optimized resource usage with proper cleanup

### 🔧 **Advanced Technical Features**
* **Async Location Services**: Non-blocking Windows SDK integration for faster execution
* **Multi-API Architecture**: Redundant data sources prevent single points of failure
* **JSON Data Persistence**: Structured offline storage for complex report data
* **Path Management**: Intelligent file handling with automatic directory creation
* **Background Processing**: Task scheduler integration for seamless startup automation

-----

## 📋 Enhanced Requirements & Dependencies

### 💻 **System Requirements**
* **Operating System**: Windows 10 (1903+) or Windows 11
* **Python**: Version 3.8 or higher (3.9+ recommended for better async support)
* **Hardware**: 
  * Webcam (built-in or external USB camera)
  * Minimum 2GB RAM (4GB+ recommended)
  * Active internet connection (offline caching available)
* **Permissions**: 
  * **Location Services enabled** in Windows Settings (critical for GPS accuracy)
  * Administrator privileges for Task Scheduler automation
  * Windows SDK access for native location services

### 📦 **Python Dependencies**
* **`opencv-python`**: Advanced computer vision for webcam capture and image processing
* **`requests`**: HTTP client for multi-API geolocation services with timeout controls
* **`psutil`**: Cross-platform system and process monitoring utilities
* **`winsdk`**: Native Windows SDK integration for Location Services and system APIs
* **Built-in modules**: `smtplib`, `email`, `configparser`, `logging`, `asyncio`, `socket`, `json`

### 🌐 **Network & Service Dependencies**
* **SMTP Access**: Gmail SMTP servers (smtp.gmail.com:587) with TLS encryption
* **Geolocation APIs**: 
  * **Primary**: Windows Location Service (offline capable)
  * **Fallback 1**: ipapi.co (1-second timeout)
  * **Fallback 2**: ip-api.com (1-second timeout)
* **Connectivity Check**: Google DNS (8.8.8.8:53) for internet status verification

### 📁 **File Structure & Permissions**
* **Configuration**: `config.ini` (sensitive credentials storage)
* **Logging**: `monitor.log` (detailed execution history)
* **Offline Cache**: `offline_reports/` directory (auto-created)
* **Temporary Files**: Webcam captures (auto-deleted after sending)

-----

## 🚀 Step-by-Step Installation Guide

### 1️⃣ **Prepare Your System**

1. **Install Python**: If you don't have it, download Python from [python.org](https://www.python.org/downloads/windows/). **Important**: During installation, make sure to check the box that says "✅ Add Python to PATH".
2. **Enable Location Services**: This is crucial for precise location tracking.
   * Go to **Settings > Privacy & security > Location**.
   * Ensure **Location services** is turned **On**.

### 2️⃣ **Download the Project & Install Libraries**

1. **Download Files**: Place the `monitor.py`, `config.ini`, and `requirements.txt` files into a folder (e.g., `C:\LoginMonitor`).
2. **Install Libraries**: Open a Command Prompt, navigate to your folder, and run:

```bash
cd C:\LoginMonitor
pip install -r requirements.txt
```

### 3️⃣ **Configure Your Credentials & Security**

**Security Best Practices**:
1. **Generate a Gmail App Password** (More secure than regular passwords):
   * Enable 2-Step Verification for your Google Account
   * Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
   * Generate a new password for "Mail" on "Windows Computer"
   * Copy the 16-character password (this will be used only once)

2. **Secure Configuration Setup**:
   * Open `config.ini` with a secure text editor
   * Never share this file - it contains sensitive credentials
   * Consider encrypting the folder if on a shared computer

**Configuration Template**:
```ini
[Email]
SenderEmail = your_email@gmail.com
SenderPassword = your_16_char_app_password  # Never use regular password
ReceiverEmail = security_alerts@gmail.com   # Can be same or different
SmtpServer = smtp.gmail.com                 # Gmail SMTP (secure TLS)
SmtpPort = 587                              # Standard secure port

[Settings]
Subject = Security Alert: Login Detected on  # Customizable subject line
```

**Alternative Email Providers**:
```ini
# Microsoft Outlook/Hotmail
SmtpServer = smtp-mail.outlook.com
SmtpPort = 587

# Yahoo Mail
SmtpServer = smtp.mail.yahoo.com
SmtpPort = 587

# Custom SMTP (corporate/self-hosted)
SmtpServer = mail.yourdomain.com
SmtpPort = 587  # or 465 for SSL
```

### 4️⃣ **Automate with Task Scheduler**

Set the script to run automatically and silently at every login.

1. Press `Win + R`, type `taskschd.msc`, and hit Enter.
2. In the right panel, click **Create Basic Task...**.
3. **Name**: Give it a name like "Advanced Login Monitor".
4. **Trigger**: Choose **When I log on**.
5. **Action**: Select **Start a program**.
6. **Program/script**: Find `pythonw.exe`. (This runs the script without a black console window).
   * *Tip: In Command Prompt, type `where pythonw` to find the full path.*
7. **Add arguments**: Enter the full path to your script (e.g., `"C:\LoginMonitor\monitor.py"`).
8. **Start in**: Enter the path to your folder (e.g., `"C:\LoginMonitor"`). This is critical!
9. Click **Finish**.
10. **Final Polish**:
    * Find the task in the main library, right-click it, and select **Properties**.
    * Check ✅ **Run with highest privileges**.
    * Go to the **Conditions** tab and uncheck "Start the task only if the computer is on AC power".
    * Click **OK**.

-----

## 🛠️ Advanced Troubleshooting & Diagnostics

### 📊 **Log Analysis**
Check the comprehensive `monitor.log` file in your project folder for detailed diagnostic information:

```powershell
# View recent log entries
Get-Content "C:\LoginMonitor\monitor.log" -Tail 20

# Search for specific errors
Select-String -Path "C:\LoginMonitor\monitor.log" -Pattern "ERROR|WARNING"
```

### 🌍 **Geolocation Issues**

**Native Windows Location (Primary System)**:
* **"Windows Location Service failed"**: 
  * Verify Location Services are enabled: Settings > Privacy & security > Location
  * Ensure "Let apps access your location" is ON
  * Check that Python/Windows has location permissions
  * Requires Windows 10 1903+ or Windows 11

**IP-Based Geolocation (Fallback System)**:
* **"All geolocation attempts failed"**: 
  * Check internet connectivity (script tests 8.8.8.8:53)
  * Verify firewall isn't blocking Python network access
  * API services may be temporarily unavailable (automatic retry with multiple APIs)

### 📧 **Email Delivery Problems**

**Authentication Issues**:
* **"Failed to send email: Authentication failed"**: 
  * Ensure you're using Gmail **App Password**, not regular password
  * Verify 2-Step Verification is enabled on Google Account
  * Double-check `SenderEmail` and `ReceiverEmail` in `config.ini`

**SMTP Configuration**:
* **"Connection refused"**: Check firewall settings for port 587
* **"TLS handshake failed"**: Update Python/certificates, verify SMTP server settings
* **Custom SMTP servers**: Modify `SmtpServer` and `SmtpPort` in `config.ini`

### 📸 **Webcam Capture Issues**

**Camera Detection**:
* **"Webcam at index 0 not found"**: 
  * Try different camera indices (script auto-checks multiple)
  * Verify camera isn't in use by another application
  * Check Windows Camera privacy settings
  * Test with built-in Camera app first

**Image Quality**:
* **Blurry/dark images**: Script includes 0.1s initialization delay
* **Camera permissions**: Ensure Windows allows camera access for Python

### 🌐 **Offline & Connectivity Features**

**Offline Report Caching**:
* **Reports not sending when online**: 
  * Check `offline_reports/` directory for cached JSON files
  * Verify internet connectivity detection is working
  * Cached reports automatically retry when connection restored

**File Management**:
* **Disk space issues**: Script auto-deletes sent images and reports
* **Permission errors**: Ensure write access to script directory

### ⚡ **Performance Optimization**

**Slow Execution**:
* **Geolocation timeout**: API calls limited to 1-second timeout
* **CPU monitoring**: Optimized to 0.1-second interval
* **Memory usage**: Script includes proper resource cleanup

**Task Scheduler Issues**:
* **Script not running at login**: 
  * Verify Task Scheduler has "Run with highest privileges" checked
  * Ensure "Start in" directory is set correctly
  * Check Windows Event Viewer for task execution logs

### 🔧 **Advanced Configuration**

**Custom Settings** (modify `config.ini`):
```ini
[Email]
SmtpServer = smtp.gmail.com  # Custom SMTP server
SmtpPort = 587               # Custom SMTP port

[Settings] 
Subject = Custom Alert: Login on  # Custom email subject
```

**Environment Variables**:
* `COMPUTERNAME`: Automatically detected for reports
* `USERNAME`: Automatically included in system info
* Path variables: Ensure Python and scripts are accessible

### 🧪 **Testing & Validation**

**Manual Testing**:
```powershell
# Test script manually
cd "C:\LoginMonitor"
python monitor.py

# Test with Python debug mode
python -u monitor.py

# Background execution test
pythonw monitor.py
```

**Component Testing**:
* **Camera**: Use Windows Camera app
* **Location**: Check Windows Location settings
* **Email**: Test SMTP settings with simple email script
* **Internet**: Ping 8.8.8.8 to verify connectivity

### 🔍 **Common Error Patterns**

| Error Message | Cause | Solution |
|---------------|--------|----------|
| `ImportError: winsdk` | Missing Windows SDK | `pip install winsdk` |
| `cv2.error: camera not found` | Camera access issue | Check camera permissions & availability |
| `smtplib.SMTPAuthenticationError` | Wrong credentials | Use Gmail App Password |
| `requests.ConnectionError` | Network issue | Check internet & firewall settings |
| `PermissionError` | File access denied | Run as administrator or check permissions |
| `ConfigParser.NoSectionError` | Invalid config.ini | Verify config file format and sections |

-----

## 🔐 Data Security & Privacy Features

### 🛡️ **Privacy Protection**

**Local Data Processing**:
* All image processing happens locally on your device
* No cloud storage or third-party image services
* Webcam captures are temporary and automatically deleted after email sending
* System information is gathered locally without external data sharing

**Data Minimization**:
* Only essential system information is collected
* Images are captured only at login events
* No continuous monitoring or background recording
* Process lists limited to running applications (no personal file scanning)

**Secure Communications**:
* All email communications use TLS encryption (SMTP over port 587)
* No plain-text password storage (uses secure app passwords)
* Geolocation data is anonymized in reports
* No data retention on external servers

### 🔒 **Security Best Practices**

**Credential Management**:
* Uses Gmail App Passwords instead of main account passwords
* Configuration file should be readable only by administrator
* Supports custom SMTP servers for corporate environments
* No hardcoded credentials in source code

**Network Security**:
* Validates SSL certificates for all HTTPS connections
* Uses secure DNS (8.8.8.8) for connectivity testing
* 1-second timeout limits prevent hanging connections
* Graceful handling of network failures

**File System Security**:
* Automatic cleanup of temporary files
* Secure file permissions on created directories
* No sensitive data stored in plain text logs
* JSON caching uses structured, non-sensitive format

### 📊 **Data Collection Transparency**

**What is Collected**:
* ✅ **Computer name** (for device identification)
* ✅ **Username** (for login verification)
* ✅ **Timestamp** (for event correlation)
* ✅ **System resource usage** (CPU/Memory percentages)
* ✅ **Network connections** (active processes and IPs)
* ✅ **Running processes** (application names only)
* ✅ **Location data** (city/country level, not street addresses)
* ✅ **Webcam image** (single capture, not video)

**What is NOT Collected**:
* ❌ **Passwords or sensitive credentials**
* ❌ **File contents or personal documents**
* ❌ **Browsing history or web activity**
* ❌ **Keyboard inputs or mouse movements**
* ❌ **Audio recordings or microphone access**
* ❌ **Persistent tracking or user profiling**
* ❌ **Third-party data sharing or analytics**

### 🌍 **Geolocation Privacy**

**Windows Location Service** (Primary):
* Uses native Windows privacy controls
* Respects system-wide location permissions
* Provides GPS-level accuracy when available
* Falls back gracefully if disabled

**IP-Based Location** (Fallback):
* City/country level accuracy only
* No personal identification data
* Uses public IP geolocation services
* Cannot determine exact address or building

### 📧 **Email Content Security**

**Report Contents**:
* Professional HTML formatting (no executable content)
* Image attachments use standard MIME encoding
* No scripts or active content in emails
* Structured data tables for easy review

**Email Security**:
* Supports custom email providers
* Uses encrypted SMTP connections
* Configurable sender/receiver addresses
* No email content logging or storage

-----

## ⚠️ License & Legal Compliance

* This software is distributed under the **MIT License**. It is provided "AS IS" without any warranty, and the authors are not liable for any damages.
* **Responsible Use**: This tool is powerful and designed for legitimate security monitoring. Use it responsibly and only on computers you own or have explicit permission to monitor.
* **Privacy Compliance**: Be aware of and comply with all privacy laws and regulations in your region (GDPR, CCPA, etc.).
* **Corporate Use**: For enterprise deployment, ensure compliance with corporate security policies and data protection requirements.
* **Consent**: When monitoring shared computers, ensure all users are informed and have provided appropriate consent.

## � Advanced Configuration Options

### 📝 **Custom Configuration Parameters**

The `config.ini` file supports additional advanced options:

```ini
[Email]
SenderEmail = security@yourcompany.com
SenderPassword = your_app_password
ReceiverEmail = alerts@yourcompany.com
SmtpServer = smtp.gmail.com
SmtpPort = 587

[Settings]
Subject = SECURITY ALERT: Unauthorized Access on
# Future expansion options:
# LogLevel = INFO
# MaxOfflineReports = 100
# CameraIndex = 0
# LocationTimeout = 5
```

### 🌐 **Enterprise Deployment**

**Group Policy Integration**:
* Deploy via Group Policy for multiple machines
* Centralized configuration management
* Automated installation across domain

**Corporate SMTP Servers**:
```ini
[Email]
SmtpServer = mail.yourcompany.com
SmtpPort = 587  # or 25 for internal servers
# May require additional authentication methods
```

**Security Hardening**:
* Run script with least privilege principle
* Consider Windows Service deployment for enhanced security
* Implement log rotation for long-term deployments
* Use encrypted file systems for sensitive configuration

## 📞 Support & Development

### 🛠️ **Technical Support**
* **Issue Reporting**: Create detailed issues in the GitHub repository
* **Log Files**: Always include relevant `monitor.log` entries when reporting issues
* **System Info**: Provide Windows version, Python version, and hardware details
* **Configuration**: Share configuration (with sensitive data redacted) when relevant

### 🚀 **Future Enhancements**
* **Multi-camera support** with automatic failover
* **Enhanced location services** with indoor positioning
* **Real-time dashboard** for monitoring multiple devices
* **Machine learning** for anomaly detection
* **Mobile app notifications** for instant alerts
* **Encrypted local storage** for enhanced security

### 🤝 **Contributing**
* Fork the repository and create feature branches
* Follow PEP 8 style guidelines for Python code
* Include comprehensive testing for new features
* Update documentation for any new configuration options
* Ensure backward compatibility with existing installations

-----

**⭐ If you find this project useful, please consider giving it a star on GitHub!**
