"""Email Sender"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime

def send_email_report(pdf_file, analysis_text):
    """
    Send email with PDF report
    
    Args:
        pdf_file: PDF file path
        analysis_text: Analysis summary
    """
    sender = os.getenv('GMAIL_USER')
    password = os.getenv('GMAIL_APP_PASSWORD')
    receiver = os.getenv('RECEIVER_EMAIL')
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = f"🤖 Upwork Job Analysis - {datetime.now().strftime('%d %b %Y')}"
    
    # Email body
    body = f"""
Hi,

Your daily Upwork job analysis is ready!

{analysis_text[:500]}...

Full detailed report is attached as PDF.

Best regards,
Your Upwork Job Analyzer Bot
"""
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach PDF
    with open(pdf_file, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(pdf_file)}')
        msg.attach(part)
    
    # Send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Email error: {e}")

