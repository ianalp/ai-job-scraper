"""
AI Job Scraper - Email Notification System
Send email alerts for new job postings
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailNotifier:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.receiver_email = os.getenv('RECEIVER_EMAIL')
        
        if not all([self.sender_email, self.sender_password, self.receiver_email]):
            logger.warning("Email credentials not configured. Check .env file.")
    
    def create_email_html(self, jobs: List[Dict]) -> str:
        """Create HTML email content"""
        html = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .header { background-color: #4CAF50; color: white; padding: 20px; text-align: center; }
                .job-card { 
                    background-color: #f9f9f9; 
                    border-left: 4px solid #4CAF50; 
                    padding: 15px; 
                    margin: 15px 0; 
                    border-radius: 5px;
                }
                .job-title { color: #2c3e50; font-size: 18px; font-weight: bold; margin-bottom: 10px; }
                .job-company { color: #34495e; font-size: 16px; margin-bottom: 5px; }
                .job-details { color: #7f8c8d; font-size: 14px; }
                .job-link { 
                    display: inline-block; 
                    background-color: #4CAF50; 
                    color: white; 
                    padding: 10px 20px; 
                    text-decoration: none; 
                    border-radius: 5px; 
                    margin-top: 10px;
                }
                .footer { text-align: center; color: #7f8c8d; padding: 20px; font-size: 12px; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎯 New Job Alerts</h1>
                <p>We found {} new jobs matching your criteria!</p>
            </div>
            <div style="padding: 20px;">
        """.format(len(jobs))
        
        for job in jobs:
            html += f"""
                <div class="job-card">
                    <div class="job-title">{job.get('title', 'N/A')}</div>
                    <div class="job-company">🏢 {job.get('company', 'N/A')}</div>
                    <div class="job-details">
                        📍 {job.get('location', 'N/A')} | 
                        💼 {job.get('experience', 'N/A')} | 
                        🎓 {job.get('education', 'N/A')}<br>
                        🔖 Source: {job.get('source', 'N/A')}
                    </div>
                    <a href="{job.get('url', '#')}" class="job-link">View Job</a>
                </div>
            """
        
        html += """
            </div>
            <div class="footer">
                <p>This is an automated email from AI Job Scraper</p>
                <p>To stop receiving these emails, update your notification settings</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def send_email(self, jobs: List[Dict], subject: str = None) -> bool:
        """Send email notification with job listings"""
        
        if not all([self.sender_email, self.sender_password, self.receiver_email]):
            logger.error("Email credentials not configured")
            return False
        
        if not jobs:
            logger.info("No jobs to send")
            return False
        
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject or f"🎯 {len(jobs)} New Job Postings Found!"
            message['From'] = self.sender_email
            message['To'] = self.receiver_email
            
            # Create HTML content
            html_content = self.create_email_html(jobs)
            html_part = MIMEText(html_content, 'html')
            message.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            logger.info(f"Email sent successfully to {self.receiver_email}")
            return True
        
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    def send_daily_summary(self, total_jobs: int, new_jobs: int, top_companies: List[str]):
        """Send daily summary email"""
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="background-color: #4CAF50; color: white; padding: 20px; text-align: center;">
                <h1>📊 Daily Job Scraping Summary</h1>
            </div>
            <div style="padding: 20px;">
                <h2>Today's Statistics:</h2>
                <ul style="font-size: 16px; line-height: 2;">
                    <li>📋 Total Jobs in Database: <strong>{total_jobs}</strong></li>
                    <li>✨ New Jobs Today: <strong>{new_jobs}</strong></li>
                    <li>🏢 Top Companies: {', '.join(top_companies[:5])}</li>
                </ul>
                <p style="margin-top: 30px;">
                    <a href="#" style="background-color: #4CAF50; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px;">
                        View Dashboard
                    </a>
                </p>
            </div>
        </body>
        </html>
        """
        
        try:
            message = MIMEMultipart('alternative')
            message['Subject'] = f"📊 Daily Summary: {new_jobs} New Jobs"
            message['From'] = self.sender_email
            message['To'] = self.receiver_email
            
            message.attach(MIMEText(html, 'html'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            logger.info("Daily summary email sent successfully")
            return True
        
        except Exception as e:
            logger.error(f"Error sending daily summary: {e}")
            return False


if __name__ == "__main__":
    # Test email notification
    notifier = EmailNotifier()
    
    test_jobs = [
        {
            'title': 'Python Backend Developer',
            'company': 'Tech Corp',
            'location': 'Seoul',
            'experience': '3-5 years',
            'education': 'Bachelor',
            'url': 'https://example.com/job1',
            'source': 'Saramin'
        },
        {
            'title': 'Data Engineer',
            'company': 'Data Inc',
            'location': 'Busan',
            'experience': '2-4 years',
            'education': 'Bachelor',
            'url': 'https://example.com/job2',
            'source': 'JobKorea'
        }
    ]
    
    notifier.send_email(test_jobs)
