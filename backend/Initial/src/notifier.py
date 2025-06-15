import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from pathlib import Path
import os

class EmailNotifier:
    def __init__(self):
        # Get the absolute path to the project root
        project_root = Path(__file__).parent.parent
        config_path = project_root / "config" / "config.json"
        
        with open(config_path) as f:
            config = json.load(f)
        self.email_config = config["email_config"]

    def send_alert(self, changes):
        """Send email alert for detected changes."""
        msg = MIMEMultipart()
        msg["From"] = self.email_config["sender_email"]
        msg["To"] = self.email_config["recipient_email"]
        msg["Subject"] = "File Integrity Monitor - Changes Detected!"

        body = "The following changes were detected:\n\n"
        for file_path, details in changes.items():
            body += f"File: {file_path}\n"
            body += f"Old Hash: {details['old_hash']}\n"
            body += f"New Hash: {details['new_hash']}\n"
            body += f"Timestamp: {details['timestamp']}\n\n"

        msg.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP(self.email_config["smtp_server"], self.email_config["smtp_port"])
            server.starttls()
            server.login(self.email_config["sender_email"], self.email_config["sender_password"])
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False
