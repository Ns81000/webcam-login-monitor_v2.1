"""
Advanced Login Monitor for Windows (v4 - Native Windows Location)

This script captures an image, gathers system intelligence, and sends a
detailed HTML report to a specified email address.
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

# --- Intelligence Gathering Functions ---

async def get_windows_location():
    """Asynchronously get location from Windows Location Service."""
    if not wdg: return None
    locator = wdg.Geolocator()
    pos = await locator.get_geoposition_async()
    return pos.coordinate

def get_geolocation():
    """
    Retrieves precise geolocation using the native Windows Location Service,
    with IP-based geolocation as a fallback.
    """
    # --- METHOD 1: High-Accuracy Native Windows Location ---
    try:
        coordinate = asyncio.run(get_windows_location())
        if coordinate:
            lat = coordinate.point.position.latitude
            lng = coordinate.point.position.longitude
            accuracy = coordinate.accuracy
            maps_link = f"https://www.google.com/maps?q={lat},{lng}"

            logging.info(f"High-accuracy location found via Windows Service. Accuracy: {accuracy:.0f} meters.")
            return {
                "IP Address": "N/A (Used Native Location)",
                "Location": f"Coordinates: {lat:.6f}, {lng:.6f}",
                "ISP": f"<a href='{maps_link}' target='_blank'>View on Google Maps</a>"
            }
        else:
            raise ValueError("Windows Location Service not available.")
    except Exception as e:
        logging.warning(f"Native Windows Location failed: {e}. Falling back to IP-based method.")
        
        # --- METHOD 2: IP-Based Geolocation (Fallback) ---
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
                res = requests.get(api['url'], timeout=5)
                res.raise_for_status()
                data = res.json()
                logging.info(f"Successfully fetched fallback location from {api['url']}")
                return api['parser'](data)
            except requests.RequestException:
                continue
    
    logging.error("All geolocation attempts failed.")
    return {"IP Address": "N/A", "Location": "N/A", "ISP": "N/A"}


def get_system_snapshot():
    """Gathers CPU/Memory usage, processes, and network connections with process names."""
    pids = {p.pid: p.info['name'] for p in psutil.process_iter(['name'])}
    
    connection_html = "<ul>"
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == 'ESTABLISHED' and conn.raddr and conn.pid in pids:
            process_name = pids[conn.pid]
            connection_html += f"<li><b>{process_name}:</b> connects to {conn.raddr.ip}:{conn.raddr.port}</li>"
    connection_html += "</ul>"

    snapshot = {
        "cpu_usage": f"{psutil.cpu_percent(interval=1)}%",
        "mem_usage": f"{psutil.virtual_memory().percent}%",
        "processes": "<ul>" + "".join([f"<li>{name}</li>" for name in pids.values()][:15]) + "</ul>",
        "connections": connection_html
    }
    return snapshot

def capture_image(filename):
    """Captures an image from the webcam."""
    cam = None
    for i in range(3):
        cam = cv2.VideoCapture(i)
        if cam.isOpened():
            logging.info(f"Webcam found at index {i}.")
            for _ in range(5): cam.read()
            ret, frame = cam.read()
            if ret:
                cv2.imwrite(filename, frame)
                cam.release()
                return True
            cam.release()
    logging.error("Failed to capture image from any webcam.")
    return False

# --- Email and Reporting Functions ---

def create_html_report(timestamp, geo_data, sys_snapshot):
    """Builds the HTML email body with all the gathered data."""
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
            part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(image_filename)}")
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

# --- Main Execution ---

def main():
    """Main function to run the monitoring and alerting process."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_filename = f"capture_{timestamp}.jpg"
    
    image_captured = capture_image(image_filename)
    logging.info("Gathering intelligence...")
    geo_data = get_geolocation()
    sys_snapshot = get_system_snapshot()

    logging.info("Creating report...")
    html_report = create_html_report(timestamp, geo_data, sys_snapshot)
    
    send_alert(html_report, image_filename if image_captured else None)

    if image_captured and os.path.exists(image_filename):
        os.remove(image_filename)
        logging.info("Cleaned up temporary image file.")

if __name__ == "__main__":
    logging.info("--- Login Monitor Script Started ---")
    main()
    logging.info("--- Login Monitor Script Finished ---")