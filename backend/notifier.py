import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from pathlib import Path

class EmailNotifier:
    def __init__(self):
        # Load email configuration
        config_path = Path(__file__).parent / "config" / "config.json"
        with open(config_path) as f:
            config = json.load(f)
        self.email_config = config["email_config"]

    def send_alert(self, message):
        msg = MIMEMultipart()
        msg['From'] = self.email_config['sender_email']
        msg['To'] = self.email_config['receiver_email']
        msg['Subject'] = "FIM Alert - File Change Detected!"

        body = f"""
        File Integrity Monitor Alert!
        
        {message}
        
        This is an automated alert from your FIM system.
        """
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_config['sender_email'], 
                        self.email_config['sender_password'])
            server.send_message(msg)
            server.quit()
            print(f"Alert email sent: {message}")
        except Exception as e:
            print(f"Failed to send email: {e}")
