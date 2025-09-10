# 🚀 Advanced Login Monitor for Windows

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-blue.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Security](https://img.shields.io/badge/security-monitoring-red.svg)](https://github.com)
[![Email](https://img.shields.io/badge/email-HTML%20reports-orange.svg)](mailto:)
[![Webcam](https://img.shields.io/badge/webcam-capture-purple.svg)](https://opencv.org)

An enhanced, multi-faceted Python script that transforms your Windows PC into a high-alert security system. When a login event occurs, it silently captures a webcam image, gathers detailed system and location intelligence, and sends an instant, beautifully formatted HTML report directly to your email. Perfect for monitoring access and ensuring the security of your device! 🕵️‍♂️

## ✨ Core Features

* 🤫 **Silent Operation**: Runs completely hidden in the background using `pythonw.exe`. No windows, no icons.
* 📸 **Webcam Capture**: Instantly captures an image of the user at login.
* 🌎 **High-Accuracy Geolocation**: Uses the native **Windows Location Service** to get precise latitude and longitude, falling back to IP-based location if necessary.
* 📊 **System Intelligence Snapshot**: Gathers critical data at the moment of login, including:
  * Active network connections and the processes that own them (e.g., `chrome.exe`).
  * A list of all running processes.
  * Current CPU and Memory usage.
* 📧 **HTML Email Reports**: Sends a professional, easy-to-read HTML report with all gathered intelligence.
* ⚙️ **Robust & Resilient**:
  * Includes a `config.ini` file to securely manage your credentials.
  * Maintains a detailed `monitor.log` for easy troubleshooting.
  * Gracefully handles errors like missing webcams or internet outages.
* 🧹 **Automatic Cleanup**: Ensures the captured image is always deleted after being sent.

-----

## 📋 Requirements

* 💻 **OS**: Windows 10 or 11
* 🐍 **Python**: Version 3.8 or higher
* 📹 **Hardware**: A webcam (built-in or external)
* 🌐 **Permissions**: An active internet connection and **Location Services enabled** in Windows Settings.

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

### 3️⃣ **Configure Your Credentials**

1. **Generate a Google App Password**:
   * Enable 2-Step Verification for your Google Account.
   * Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).
   * Generate a new password for "Mail" on "Windows Computer".
   * Copy the 16-character password.

2. **Edit the `config.ini` file**:
   * Open `config.ini` with a text editor.
   * Fill in your `SenderEmail`, `SenderPassword` (the app password you just generated), and `ReceiverEmail`.

```ini
[Email]
SenderEmail = your_email@gmail.com
SenderPassword = your_google_app_password
ReceiverEmail = recipient_email@gmail.com
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

## 🛠️ Troubleshooting

If you aren't receiving emails, check the `monitor.log` file in your project folder. It will contain detailed error messages.

* **"High-accuracy Wi-Fi geolocation failed"**: This means the script fell back to IP-based location. The most common cause is that **Location Services are turned off** in Windows Settings.
* **"Failed to send email"**:
  * Verify your internet connection.
  * Double-check that the `SenderPassword` in `config.ini` is the correct 16-character **App Password**, not your regular Gmail password.
* **"Failed to capture image from any webcam"**: Ensure your webcam is connected and working. The script checks the first three camera indices (0, 1, 2).

-----

## ⚠️ License & Security

* This software is distributed under the **MIT License**. It is provided "AS IS" without any warranty, and the authors are not liable for any damages.
* This tool is powerful. Use it responsibly and only on computers you own. Be aware of and comply with all privacy laws in your region.

## 📞 Support

For issues, questions, or contributions, please create an issue in the repository or contact the maintainer.

-----

**⭐ If you find this project useful, please consider giving it a star on GitHub!**