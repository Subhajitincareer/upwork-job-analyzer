"""Quick test to check if project components work"""

import os
import sys

print("=" * 60)
print("🧪 QUICK PROJECT TEST")
print("=" * 60)

# Test 1: Check folder structure
print("\n1️⃣ Checking Project Structure...")
folders = ['scraper', 'analyzer', 'reporter', 'utils', 'data', 'logs']
files = ['main.py', '.env', 'requirements.txt']

for folder in folders:
    status = "✅" if os.path.exists(folder) else "❌"
    print(f"   {status} {folder}/")

for file in files:
    status = "✅" if os.path.exists(file) else "❌"
    print(f"   {status} {file}")

# Test 2: Check packages
print("\n2️⃣ Checking Installed Packages...")
packages = [
    'selenium',
    'bs4',
    'webdriver_manager',
    'google.generativeai',
    'schedule',
    'dotenv',
    'fpdf'
]

for package in packages:
    try:
        __import__(package)
        print(f"   ✅ {package}")
    except ImportError:
        print(f"   ❌ {package} - NOT INSTALLED")

# Test 3: Check credentials
print("\n3️⃣ Checking Credentials...")
from dotenv import load_dotenv
load_dotenv()

gemini_key = os.getenv('GEMINI_API_KEY')
gmail_user = os.getenv('GMAIL_USER')
gmail_pass = os.getenv('GMAIL_APP_PASSWORD')

if gemini_key and gemini_key != 'your_api_key_here':
    print(f"   ✅ Gemini API Key: {gemini_key[:10]}...")
else:
    print("   ❌ Gemini API Key not set")

if gmail_user and gmail_user != 'your_email@gmail.com':
    print(f"   ✅ Gmail User: {gmail_user}")
else:
    print("   ❌ Gmail User not set")

if gmail_pass and gmail_pass != 'your_app_password':
    print(f"   ✅ Gmail Password: {gmail_pass[:4]}...")
else:
    print("   ❌ Gmail Password not set")

# Test 4: Test import modules
print("\n4️⃣ Testing Project Modules...")
try:
    from scraper.upwork_scraper import scrape_upwork_jobs
    print("   ✅ scraper.upwork_scraper")
except Exception as e:
    print(f"   ❌ scraper.upwork_scraper - {e}")

try:
    from analyzer.gemini_analyzer import analyze_jobs_with_gemini
    print("   ✅ analyzer.gemini_analyzer")
except Exception as e:
    print(f"   ❌ analyzer.gemini_analyzer - {e}")

try:
    from reporter.pdf_generator import generate_pdf_report
    print("   ✅ reporter.pdf_generator")
except Exception as e:
    print(f"   ❌ reporter.pdf_generator - {e}")

try:
    from reporter.email_sender import send_email_report
    print("   ✅ reporter.email_sender")
except Exception as e:
    print(f"   ❌ reporter.email_sender - {e}")

try:
    from utils.database import save_jobs_data
    print("   ✅ utils.database")
except Exception as e:
    print(f"   ❌ utils.database - {e}")

print("\n" + "=" * 60)
print("✅ QUICK TEST COMPLETE!")
print("=" * 60)
