"""Test if all required packages are installed"""

import sys

required_packages = {
    'selenium': 'Web scraping',
    'bs4': 'HTML parsing (beautifulsoup4)',
    'webdriver_manager': 'ChromeDriver management',
    'google.generativeai': 'Gemini AI',
    'schedule': 'Task scheduling',
    'dotenv': 'Environment variables (python-dotenv)',
    'fpdf': 'PDF generation (fpdf2)'
}

optional_packages = {
    'PIL': 'Image processing (Pillow)',
    'pandas': 'Data analysis'
}

print("=" * 60)
print("🔍 CHECKING REQUIRED PACKAGES")
print("=" * 60)

all_installed = True

for package, description in required_packages.items():
    try:
        __import__(package)
        print(f"✅ {package.ljust(25)} - {description}")
    except ImportError:
        print(f"❌ {package.ljust(25)} - {description} [MISSING]")
        all_installed = False

print("\n" + "=" * 60)
print("🔍 CHECKING OPTIONAL PACKAGES")
print("=" * 60)

for package, description in optional_packages.items():
    try:
        __import__(package)
        print(f"✅ {package.ljust(25)} - {description}")
    except ImportError:
        print(f"⚠️  {package.ljust(25)} - {description} [OPTIONAL]")

print("\n" + "=" * 60)

if all_installed:
    print("🎉 ALL REQUIRED PACKAGES INSTALLED!")
    print("✅ You can run the project now!")
else:
    print("❌ SOME PACKAGES ARE MISSING")
    print("Run: pip install selenium beautifulsoup4 webdriver-manager google-generativeai schedule python-dotenv fpdf2")

if __name__ == "__main__":
    print("=" * 60)
    if all_installed:
        print("🎉 ALL REQUIRED PACKAGES INSTALLED!")
        print("✅ You can run the project now!")
    else:
        print("❌ SOME PACKAGES ARE MISSING")
        print("Run: pip install selenium beautifulsoup4 webdriver-manager google-generativeai schedule python-dotenv fpdf2")
    print("=" * 60)
