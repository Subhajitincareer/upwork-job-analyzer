"""
Email Sender
Production-ready email sending with retry logic
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from datetime import datetime
from typing import Optional
from config import Config
from utils.logger import logger

class EmailSender:
    """Email sender with error handling"""
    
    def __init__(self):
        self.config = Config
    
    def send_report(self, pdf_file: str, analysis_text: str, 
                   metadata: Optional[dict] = None) -> bool:
        """
        Send email with PDF report
        
        Args:
            pdf_file: Path to PDF file
            analysis_text: Analysis summary
            metadata: Additional metadata
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("📧 Preparing email...")
            
            # Create message
            msg = self._create_message(analysis_text, metadata)
            
            # Attach PDF
            if pdf_file and Path(pdf_file).exists():
                self._attach_pdf(msg, pdf_file)
            else:
                logger.warning("⚠️  PDF file not found, sending without attachment")
            
            # Send email
            self._send_email(msg)
            
            logger.info("✅ Email sent successfully")
            return True
        
        except Exception as e:
            logger.error(f"Email sending error: {e}")
            return False
    
    def _create_message(self, analysis_text: str, metadata: Optional[dict]) -> MIMEMultipart:
        """Create email message"""
        msg = MIMEMultipart()
        msg['From'] = self.config.GMAIL_USER
        msg['To'] = self.config.RECEIVER_EMAIL
        msg['Subject'] = f"🤖 Upwork Job Analysis - {datetime.now().strftime('%d %b %Y')}"
        
        # Email body
        body = self._create_body(analysis_text, metadata)
        msg.attach(MIMEText(body, 'plain'))
        
        return msg
    
    def _create_body(self, analysis_text: str, metadata: Optional[dict]) -> str:
        """Create email body"""
        body = f"""
Hi,

Your daily Upwork job market analysis is ready!

{'='*60}
SUMMARY
{'='*60}

Date: {datetime.now().strftime('%d %B %Y, %I:%M %p IST')}
Search Query: {self.config.SEARCH_QUERY}
"""
        
        if metadata:
            body += f"Total Jobs Found: {metadata.get('total_jobs', 'N/A')}\n"
            body += f"Pages Scraped: {metadata.get('pages', 'N/A')}\n"
        
        body += f"\n{'='*60}\n"
        body += "PREVIEW\n"
        body += f"{'='*60}\n\n"
        
        # Add preview of analysis (first 500 chars)
        preview = analysis_text[:500].strip()
        body += preview + "...\n\n"
        
        body += f"{'='*60}\n\n"
        body += "📎 Full detailed report is attached as PDF.\n\n"
        body += "Best regards,\n"
        body += "Your Upwork Job Analyzer Bot\n"
        body += f"\n{'='*60}\n"
        body += "This is an automated email. Do not reply.\n"
        
        return body
    
    def _attach_pdf(self, msg: MIMEMultipart, pdf_file: str):
        """Attach PDF to email"""
        try:
            with open(pdf_file, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            
            filename = Path(pdf_file).name
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}'
            )
            
            msg.attach(part)
            logger.info(f"✅ PDF attached: {filename}")
        
        except Exception as e:
            logger.error(f"Error attaching PDF: {e}")
    
    def _send_email(self, msg: MIMEMultipart):
        """Send email via SMTP"""
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            
            server.login(
                self.config.GMAIL_USER,
                self.config.GMAIL_APP_PASSWORD
            )
            
            server.send_message(msg)
            server.quit()
        
        except smtplib.SMTPAuthenticationError:
            logger.error("❌ SMTP Authentication failed. Check Gmail App Password")
            raise
        except smtplib.SMTPException as e:
            logger.error(f"❌ SMTP error: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Email sending error: {e}")
            raise

# Global sender instance
email_sender = EmailSender()

def send_email_report(pdf_file: str, analysis_text: str, 
                     metadata: Optional[dict] = None) -> bool:
    """Main email sending function"""
    return email_sender.send_report(pdf_file, analysis_text, metadata)
