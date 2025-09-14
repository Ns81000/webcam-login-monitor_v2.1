"""
Advanced Login Monitor for Windows (v2.1 - Enhanced)

This script captures an image, gathers system intelligence, and sends a
detailed HTML report to a specified email address. Now with offline
caching and faster execution.
"""
import cv2
import smtplib
import os
import datetime
import logging
import configparser
import requests
import psutil
import time
import asyncio
import json
import socket
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

# Import the necessary Windows SDK components
try:
    from winsdk.windows.devices import geolocation as wdg
except ImportError:
    print("Error: PyWinSDK is not installed. Please run 'pip install winsdk'")
    wdg = None

# --- Setup Logging and Configuration ---
logging.basicConfig(filename='monitor.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

config = configparser.ConfigParser()
try:
    config.read('config.ini')
    EMAIL_CONFIG = config['Email']
    SETTINGS_CONFIG = config['Settings']
except KeyError:
    logging.error("Could not read config.ini. Make sure it exists and is formatted correctly.")
    exit()

# --- Utility Functions ---

def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
    """Check for an active internet connection."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        logging.warning("No internet connection detected.")
        return False

def save_report_offline(report_data):
    """Saves the report data to a JSON file for later sending."""
    offline_dir = Path("offline_reports")
    offline_dir.mkdir(exist_ok=True)
    file_path = offline_dir / f"report_{report_data['timestamp']}.json"
    with open(file_path, "w") as f:
        json.dump(report_data, f)
    logging.info(f"Saved report to {file_path}")

# --- Intelligence Gathering Functions ---

async def get_windows_location():
    """Asynchronously get location from Windows Location Service."""
    if not wdg: return None
    locator = wdg.Geolocator()
    pos = await locator.get_geoposition_async()
    return pos.coordinate

def get_ip_geolocation_fallback():
    """Fetches IP-based geolocation from multiple APIs with a 1-second timeout."""
    apis = [
        {'url': 'https://ipapi.co/json/', 'parser': lambda r: {
            "IP Address": r.get("ip", "N/A"),
            "Location": f"{r.get('city', 'N/A')}, {r.get('country_name', 'N/A')}",
            "ISP": r.get("org", "N/A")
        }},
        {'url': 'http://ip-api.com/json', 'parser': lambda r: {
            "IP Address": r.get("query", "N/A"),
            "Location": f"{r.get('city', 'N/A')}, {r.get('country', 'N/A')}",
            "ISP": r.get("isp", "N/A")
        }}
    ]
    for api in apis:
        try:
            # The timeout for the network request is now 1 second.
            res = requests.get(api['url'], timeout=1) 
            res.raise_for_status()
            data = res.json()
            logging.info(f"Successfully fetched fallback location from {api['url']}")
            return api['parser'](data)
        except requests.RequestException:
            continue
    return None

def get_geolocation():
    """
    Retrieves precise geolocation, optimized for speed.
    """
    try:
        coordinate = asyncio.run(get_windows_location())
        if coordinate:
            lat, lng, accuracy = coordinate.point.position.latitude, coordinate.point.position.longitude, coordinate.accuracy
            maps_link = f"http://www.google.com/maps/place/{lat},{lng}"
            logging.info(f"High-accuracy location found. Accuracy: {accuracy:.0f}m.")
            return {
                "IP Address": "N/A (Native Location)",
                "Location": f"Coordinates: {lat:.6f}, {lng:.6f}",
                "ISP": f"<a href='{maps_link}' target='_blank'>View on Google Maps</a>"
            }
    except Exception as e:
        logging.warning(f"Native Windows Location failed: {e}. Falling back.")
        geo_data = get_ip_geolocation_fallback()
        if geo_data:
            return geo_data

    logging.error("All geolocation attempts failed.")
    return {"IP Address": "N/A", "Location": "N/A", "ISP": "N/A"}

def get_system_snapshot():
    """Gathers system snapshot with a faster CPU interval."""
    pids = {p.pid: p.info['name'] for p in psutil.process_iter(['name'])}
    connection_html = "<ul>"
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == 'ESTABLISHED' and conn.raddr and conn.pid in pids:
            connection_html += f"<li><b>{pids[conn.pid]}:</b> connects to {conn.raddr.ip}:{conn.raddr.port}</li>"
    connection_html += "</ul>"
    return {
        "cpu_usage": f"{psutil.cpu_percent(interval=0.1)}%", # Faster interval
        "mem_usage": f"{psutil.virtual_memory().percent}%",
        "processes": "<ul>" + "".join([f"<li>{name}</li>" for name in pids.values()][:15]) + "</ul>",
        "connections": connection_html
    }

def capture_image(filename):
    """Captures an image from the webcam."""
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        logging.error("Webcam at index 0 not found.")
        return False
    time.sleep(0.1) # Allow camera to initialize
    ret, frame = cam.read()
    if ret:
        cv2.imwrite(filename, frame)
    cam.release()
    return ret

# --- Email and Reporting Functions ---

def create_html_report(timestamp, geo_data, sys_snapshot):
    """Builds the HTML email body."""
    computer_name = os.environ.get('COMPUTERNAME', 'Unknown')
    username = os.environ.get('USERNAME', 'Unknown')
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        .container {{ max-width: 650px; margin: auto; border: 1px solid #ddd; }}
        .header {{ background-color: #d9534f; color: white; padding: 15px; text-align: center; }}
        .content {{ padding: 20px; }}
        h2 {{ border-bottom: 2px solid #eee; padding-bottom: 5px; }}
        .info-table td {{ padding: 8px; border: 1px solid #ddd; }}
        .label {{ font-weight: bold; background-color: #f9f9f9; }}
    </style>
    </head>
    <body>
        <div class="container">
            <div class="header"><h1>🔒 Security Alert</h1></div>
            <div class="content">
                <h2>Login Details</h2>
                <table class="info-table" width="100%">
                    <tr><td class="label">Computer</td><td>{computer_name}</td></tr>
                    <tr><td class="label">User</td><td>{username}</td></tr>
                    <tr><td class="label">Time</td><td>{timestamp}</td></tr>
                </table>
                <h2>Geolocation</h2>
                <table class="info-table" width="100%">
                    <tr><td class="label">Method</td><td>{geo_data.get('IP Address', 'N/A')}</td></tr>
                    <tr><td class="label">Est. Location</td><td>{geo_data.get('Location', 'N/A')}</td></tr>
                    <tr><td class="label">Details</td><td>{geo_data.get('ISP', 'N/A')}</td></tr>
                </table>
                <h2>System Snapshot</h2>
                <table class="info-table" width="100%">
                    <tr><td class="label">CPU Usage</td><td>{sys_snapshot.get('cpu_usage')}</td></tr>
                    <tr><td class="label">Memory Usage</td><td>{sys_snapshot.get('mem_usage')}</td></tr>
                    <tr><td class="label">Running Processes</td><td>{sys_snapshot.get('processes')}</td></tr>
                    <tr><td class="label">Network Connections</td><td>{sys_snapshot.get('connections')}</td></tr>
                </table>
            </div>
        </div>
    </body>
    </html>
    """

def send_alert(html_report, image_filename):
    """Sends the email alert with the image attached."""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['SenderEmail']
        msg['To'] = EMAIL_CONFIG['ReceiverEmail']
        msg['Subject'] = f"{SETTINGS_CONFIG['Subject']} {os.environ.get('COMPUTERNAME', 'Unknown')}"
        msg.attach(MIMEText(html_report, 'html'))

        if image_filename and os.path.exists(image_filename):
            with open(image_filename, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(image_filename)}")
            msg.attach(part)

        server = smtplib.SMTP(EMAIL_CONFIG['SmtpServer'], int(EMAIL_CONFIG['SmtpPort']))
        server.starttls()
        server.login(EMAIL_CONFIG['SenderEmail'], EMAIL_CONFIG['SenderPassword'])
        server.sendmail(EMAIL_CONFIG['SenderEmail'], EMAIL_CONFIG['ReceiverEmail'], msg.as_string())
        server.quit()
        logging.info("Alert email sent successfully.")
        return True
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        return False

def send_offline_reports():
    """Checks for and sends any saved offline reports."""
    offline_dir = Path("offline_reports")
    if not offline_dir.exists():
        return

    if check_internet_connection():
        for report_file in sorted(offline_dir.glob("*.json")):
            logging.info(f"Attempting to send offline report: {report_file.name}")
            with open(report_file, "r") as f:
                report_data = json.load(f)

            html_report = create_html_report(
                report_data['timestamp'], report_data['geo_data'], report_data['sys_snapshot']
            )
            image_file = report_data.get('image_filename')
            if send_alert(html_report, image_file):
                report_file.unlink()
                if image_file and Path(image_file).exists():
                    Path(image_file).unlink()
                logging.info(f"Successfully sent and deleted offline report: {report_file.name}")
            else:
                break # Stop if sending fails to avoid multiple failures

# --- Main Execution ---
def main():
    """Main function to run the monitoring and alerting process."""
    send_offline_reports()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_filename = f"capture_{timestamp}.jpg"

    image_captured = capture_image(image_filename)
    geo_data = get_geolocation()
    sys_snapshot = get_system_snapshot()
    html_report = create_html_report(timestamp, geo_data, sys_snapshot)

    if not check_internet_connection():
        save_report_offline({
            "timestamp": timestamp,
            "geo_data": geo_data,
            "sys_snapshot": sys_snapshot,
            "image_filename": image_filename if image_captured else None
        })
    else:
        if send_alert(html_report, image_filename if image_captured else None):
            if image_captured and os.path.exists(image_filename):
                os.remove(image_filename)

if __name__ == "__main__":
    logging.info("--- Login Monitor Script Started ---")
    main()
    logging.info("--- Login Monitor Script Finished ---")
