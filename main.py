"""
Upwork Job Analyzer - Main Script
Automated daily job analysis
"""

import schedule
import time
from datetime import datetime
from python-dotenv import load_dotenv
import os
import logging
import sys

# Setup logging
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Also log to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

# Load environment variables
load_dotenv()

# Import modules
try:
    from scraper.upwork_scraper import scrape_upwork_jobs
    from analyzer.gemini_analyzer import analyze_jobs_with_gemini
    from reporter.pdf_generator import generate_pdf_report
    from reporter.email_sender import send_email_report
    from utils.database import save_jobs_data
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure all required files are created and packages are installed.")
    sys.exit(1)

def daily_job_analysis():
    """Main analysis function"""
    try:
        print("\n" + "=" * 60)
        print(f"🤖 Starting Upwork Job Analysis")
        print(f"📅 {datetime.now().strftime('%d %b %Y, %I:%M %p IST')}")
        print("=" * 60)
        
        # 1. Scrape jobs
        search_query = os.getenv('SEARCH_QUERY', 'AI and ML engineer')
        pages = int(os.getenv('PAGES_TO_SCRAPE', '3'))
        
        print(f"\n📡 Scraping Upwork for: '{search_query}'")
        print(f"📄 Pages to scrape: {pages}")
        
        jobs = scrape_upwork_jobs(search_query, pages)
        
        print(f"✅ Found {len(jobs)} jobs")
        logging.info(f"Scraped {len(jobs)} jobs")
        
        if len(jobs) == 0:
            print("⚠️  No jobs found. Stopping analysis.")
            logging.warning("No jobs found")
            return
        
        # 2. Save raw data
        print("\n💾 Saving jobs data...")
        save_jobs_data(jobs)
        
        # 3. Analyze with Gemini AI
        print("\n🧠 Analyzing with Gemini AI...")
        analysis = analyze_jobs_with_gemini(jobs)
        print("✅ Analysis complete")
        logging.info("Analysis completed")
        
        # Print preview
        print("\n" + "-" * 60)
        print("📊 ANALYSIS PREVIEW:")
        print("-" * 60)
        print(analysis[:500] + "..." if len(analysis) > 500 else analysis)
        print("-" * 60)
        
        # 4. Generate PDF report
        print("\n📄 Generating PDF report...")
        pdf_file = generate_pdf_report(analysis, len(jobs))
        print(f"✅ Report saved: {pdf_file}")
        logging.info(f"PDF generated: {pdf_file}")
        
        # 5. Send email
        print("\n📧 Sending email report...")
        send_email_report(pdf_file, analysis)
        print("✅ Email sent successfully")
        logging.info("Email sent")
        
        print("\n" + "=" * 60)
        print("🎉 Daily analysis completed successfully!")
        print("=" * 60 + "\n")
        
    except Exception as e:
        error_msg = f"Error in daily analysis: {str(e)}"
        print(f"\n❌ {error_msg}")
        logging.error(error_msg, exc_info=True)
        raise

def test_run():
    """Run analysis once for testing"""
    print("\n🧪 TEST MODE: Running single analysis\n")
    daily_job_analysis()

def schedule_daily():
    """Schedule daily automated runs"""
    schedule_time = os.getenv('SCHEDULE_TIME', '08:00')
    
    print(f"\n⏰ Bot scheduled for daily {schedule_time} IST")
    print("🔄 Bot is running... Press Ctrl+C to stop\n")
    
    schedule.every().day.at(schedule_time).do(daily_job_analysis)
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\n\n👋 Bot stopped by user")
            break
        except Exception as e:
            logging.error(f"Scheduler error: {e}")
            time.sleep(60)

def main():
    """Main entry point"""
    print("\n" + "=" * 60)
    print("🤖 UPWORK JOB ANALYZER BOT")
    print("=" * 60)
    
    # Check environment variables
    if not os.getenv('GEMINI_API_KEY'):
        print("\n❌ ERROR: GEMINI_API_KEY not found in .env file")
        print("Please add your API key to .env file")
        sys.exit(1)
    
    print("\nSelect mode:")
    print("1. Run analysis now (Test mode)")
    print("2. Schedule daily automatic runs")
    print("3. Exit")
    
    try:
        choice = input("\nEnter choice (1/2/3): ").strip()
        
        if choice == "1":
            test_run()
        elif choice == "2":
            schedule_daily()
        elif choice == "3":
            print("\n👋 Goodbye!")
        else:
            print("\n❌ Invalid choice")
    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        logging.error(f"Main error: {e}", exc_info=True)

if __name__ == "__main__":
    main()
