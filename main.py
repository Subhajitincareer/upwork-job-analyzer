"""
Upwork Job Analyzer - Main Application
Production-ready automation with error handling
"""

import schedule
import time
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from utils.logger import logger
from utils.database import db
from scraper.upwork_scraper import scrape_upwork_jobs
from analyzer.gemini_analyzer import analyze_jobs_with_gemini
from reporter.pdf_generator import generate_pdf_report
from reporter.email_sender import send_email_report

class UpworkJobAnalyzer:
    """Main application class"""
    
    def __init__(self):
        self.config = Config
        logger.info("=" * 60)
        logger.info("🤖 Upwork Job Analyzer Initialized")
        logger.info("=" * 60)
    
    def run_analysis(self) -> bool:
        """
        Run complete analysis workflow
        
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"\n{'='*60}")
            logger.info(f"🚀 Starting Analysis - {datetime.now().strftime('%d %b %Y, %I:%M %p IST')}")
            logger.info(f"{'='*60}\n")
            
            # Step 1: Scrape jobs
            logger.info("📡 Step 1/5: Scraping Upwork...")
            jobs = scrape_upwork_jobs(
                self.config.SEARCH_QUERY,
                self.config.PAGES_TO_SCRAPE
            )
            
            if not jobs or len(jobs) == 0:
                logger.warning("⚠️  No jobs found. Stopping analysis.")
                return False
            
            logger.info(f"✅ Found {len(jobs)} valid jobs\n")
            
            # Step 2: Save data
            logger.info("💾 Step 2/5: Saving data...")
            saved_file = db.save_jobs(jobs, 'raw')
            if not saved_file:
                logger.warning("⚠️  Failed to save data, continuing anyway...")
            
            # Step 3: Analyze with AI
            logger.info("🧠 Step 3/5: Analyzing with Gemini AI...")
            
            # Get historical data for comparison
            historical_data = db.get_historical_stats(days=7)
            
            analysis = analyze_jobs_with_gemini(jobs, historical_data)
            
            if not analysis:
                logger.error("❌ Analysis failed")
                return False
            
            logger.info("✅ Analysis complete\n")
            
            # Preview
            logger.info("📊 Analysis Preview:")
            logger.info("-" * 60)
            preview = analysis[:500].replace('\n', ' ')
            logger.info(preview + "...")
            logger.info("-" * 60 + "\n")
            
            # Step 4: Generate PDF
            logger.info("📄 Step 4/5: Generating PDF report...")
            
            metadata = {
                'total_jobs': len(jobs),
                'pages': self.config.PAGES_TO_SCRAPE,
                'valid_jobs': len(jobs),
                'search_query': self.config.SEARCH_QUERY
            }
            
            pdf_file = generate_pdf_report(analysis, len(jobs), metadata)
            
            if not pdf_file:
                logger.warning("⚠️  PDF generation failed")
            else:
                logger.info(f"✅ PDF saved: {pdf_file}\n")
            
            # Step 5: Send email
            logger.info("📧 Step 5/5: Sending email report...")
            
            email_sent = send_email_report(pdf_file, analysis, metadata)
            
            if email_sent:
                logger.info("✅ Email sent successfully\n")
            else:
                logger.warning("⚠️  Email sending failed\n")
            
            # Success summary
            logger.info("=" * 60)
            logger.info("🎉 ANALYSIS COMPLETED SUCCESSFULLY!")
            logger.info("=" * 60)
            logger.info(f"📊 Jobs analyzed: {len(jobs)}")
            logger.info(f"📄 Report: {pdf_file if pdf_file else 'N/A'}")
            logger.info(f"📧 Email: {'Sent' if email_sent else 'Failed'}")
            logger.info(f"⏰ Time: {datetime.now().strftime('%I:%M:%S %p')}")
            logger.info("=" * 60 + "\n")
            
            return True
        
        except KeyboardInterrupt:
            logger.warning("\n⚠️  Analysis interrupted by user")
            return False
        
        except Exception as e:
            logger.error(f"❌ Analysis failed: {e}", exc_info=True)
            return False
    
    def schedule_daily(self):
        """Schedule daily automatic runs"""
        schedule_time = self.config.SCHEDULE_TIME
        
        logger.info(f"\n⏰ Scheduling daily runs at {schedule_time} {self.config.TIMEZONE}")
        logger.info("🔄 Bot is now running...")
        logger.info("Press Ctrl+C to stop\n")
        
        schedule.every().day.at(schedule_time).do(self.run_analysis)
        
        # Show next run time
        next_run = schedule.next_run()
        logger.info(f"📅 Next run scheduled: {next_run}\n")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        except KeyboardInterrupt:
            logger.info("\n👋 Scheduler stopped by user")
        
        except Exception as e:
            logger.error(f"❌ Scheduler error: {e}")
    
    def run_interactive(self):
        """Run interactive menu"""
        while True:
            print("\n" + "=" * 60)
            print("🤖 UPWORK JOB ANALYZER")
            print("=" * 60)
            print("\nOptions:")
            print("1. Run analysis now (Test mode)")
            print("2. Schedule daily automatic runs")
            print("3. View configuration")
            print("4. Test credentials")
            print("5. Exit")
            print("\n" + "=" * 60)
            
            try:
                choice = input("\nEnter choice (1-5): ").strip()
                
                if choice == "1":
                    logger.info("\n🧪 Running test analysis...")
                    success = self.run_analysis()
                    if success:
                        input("\n✅ Test complete! Press Enter to continue...")
                    else:
                        input("\n❌ Test failed! Check logs. Press Enter to continue...")
                
                elif choice == "2":
                    self.schedule_daily()
                
                elif choice == "3":
                    self._show_config()
                
                elif choice == "4":
                    self._test_credentials()
                
                elif choice == "5":
                    logger.info("\n👋 Goodbye!")
                    break
                
                else:
                    print("\n❌ Invalid choice. Please try again.")
            
            except KeyboardInterrupt:
                logger.info("\n\n👋 Goodbye!")
                break
            
            except Exception as e:
                logger.error(f"\n❌ Error: {e}")
                input("\nPress Enter to continue...")
    
    def _show_config(self):
        """Display current configuration"""
        print("\n" + "=" * 60)
        print("⚙️  CURRENT CONFIGURATION")
        print("=" * 60)
        print(f"\n📧 Email: {self.config.GMAIL_USER}")
        print(f"🔍 Search Query: {self.config.SEARCH_QUERY}")
        print(f"📄 Pages to Scrape: {self.config.PAGES_TO_SCRAPE}")
        print(f"⏰ Schedule Time: {self.config.SCHEDULE_TIME} {self.config.TIMEZONE}")
        print(f"🔄 Max Retries: {self.config.MAX_RETRIES}")
        print(f"⏱️  Timeout: {self.config.TIMEOUT_SECONDS}s")
        print(f"📊 Log Level: {self.config.LOG_LEVEL}")
        print("\n" + "=" * 60)
        input("\nPress Enter to continue...")
    
    def _test_credentials(self):
        """Test API credentials"""
        print("\n" + "=" * 60)
        print("🔐 TESTING CREDENTIALS")
        print("=" * 60 + "\n")
        
        # Test Gemini
        print("1️⃣ Testing Gemini API...")
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.config.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("Say hello in one word")
            print(f"✅ Gemini API working! Response: {response.text}")
        except Exception as e:
            print(f"❌ Gemini API failed: {e}")
        
        # Test Gmail
        print("\n2️⃣ Testing Gmail SMTP...")
        try:
            import smtplib
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.config.GMAIL_USER, self.config.GMAIL_APP_PASSWORD)
            server.quit()
            print(f"✅ Gmail SMTP working! ({self.config.GMAIL_USER})")
        except Exception as e:
            print(f"❌ Gmail SMTP failed: {e}")
        
        print("\n" + "=" * 60)
        input("\nPress Enter to continue...")

def main():
    """Main entry point"""
    try:
        # Validate configuration
        Config.validate()
        
        # Create analyzer instance
        analyzer = UpworkJobAnalyzer()
        
        # Run interactive menu
        analyzer.run_interactive()
    
    except ValueError as e:
        logger.error(f"❌ Configuration error: {e}")
        logger.info("\n💡 Please check your .env file and ensure all required values are set.")
        sys.exit(1)
    
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
