"""Test if credentials are working"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("🔐 TESTING CREDENTIALS")
print("=" * 60)

# Test 1: Check .env file exists
print("\n1️⃣ Checking .env file...")
if os.path.exists('.env'):
    print("✅ .env file found")
else:
    print("❌ .env file NOT found")
    print("💡 Create .env file in project root")
    exit()

# Test 2: Check Gemini API Key
print("\n2️⃣ Checking Gemini API Key...")
gemini_key = os.getenv('GEMINI_API_KEY')
if gemini_key and gemini_key != 'your_api_key_here':
    print(f"✅ Gemini API Key found: {gemini_key[:10]}...")
    
    # Try to use it
    try:
        import google.generativeai as genai
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Say hello in one word")
        print(f"✅ Gemini API WORKING! Response: {response.text}")
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        print("💡 Check if API key is correct")
else:
    print("❌ Gemini API Key not set")
    print("💡 Get it from: https://aistudio.google.com/app/apikey")

# Test 3: Check Gmail Credentials
print("\n3️⃣ Checking Gmail Credentials...")
gmail_user = os.getenv('GMAIL_USER')
gmail_pass = os.getenv('GMAIL_APP_PASSWORD')

if gmail_user and gmail_user != 'your_email@gmail.com':
    print(f"✅ Gmail User: {gmail_user}")
else:
    print("❌ Gmail User not set")

if gmail_pass and gmail_pass != 'your_app_password':
    print(f"✅ Gmail App Password found: {gmail_pass[:4]}...")
    
    # Try to connect
    try:
        import smtplib
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_pass)
        server.quit()
        print("✅ Gmail SMTP CONNECTION SUCCESSFUL!")
    except Exception as e:
        print(f"❌ Gmail SMTP Error: {e}")
        print("💡 Make sure you're using App Password, not regular password")
        print("💡 Get it from: https://myaccount.google.com/apppasswords")
else:
    print("❌ Gmail App Password not set")

# Test 4: Other Settings
print("\n4️⃣ Checking Other Settings...")
search_query = os.getenv('SEARCH_QUERY', 'NOT SET')
pages = os.getenv('PAGES_TO_SCRAPE', 'NOT SET')
schedule_time = os.getenv('SCHEDULE_TIME', 'NOT SET')
receiver = os.getenv('RECEIVER_EMAIL', 'NOT SET')

print(f"   Search Query: {search_query}")
print(f"   Pages to Scrape: {pages}")
print(f"   Schedule Time: {schedule_time}")
print(f"   Receiver Email: {receiver}")

# Summary
print("\n" + "=" * 60)
print("📊 SUMMARY")
print("=" * 60)

all_good = True

if not gemini_key or gemini_key == 'your_api_key_here':
    print("❌ Missing: GEMINI_API_KEY")
    all_good = False

if not gmail_user or gmail_user == 'your_email@gmail.com':
    print("❌ Missing: GMAIL_USER")
    all_good = False

if not gmail_pass or gmail_pass == 'your_app_password':
    print("❌ Missing: GMAIL_APP_PASSWORD")
    all_good = False

if all_good:
    print("✅ ALL CREDENTIALS ARE SET!")
    print("🚀 You can now run: python main.py")
else:
    print("\n📝 TO DO:")
    print("1. Edit .env file")
    print("2. Add missing credentials")
    print("3. Run this test again")

print("=" * 60)
