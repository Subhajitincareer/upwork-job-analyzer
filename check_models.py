"""Check what models are actually available"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')

try:
    genai.configure(api_key=api_key)
    
    print("📋 Listing ALL available models:\n")
    print("=" * 80)
    
    models = list(genai.list_models())
    
    if not models:
        print("❌ No models found! This might mean:")
        print("   1. Invalid API key")
        print("   2. API key doesn't have access")
        print("   3. Need to generate new key")
        print("\n💡 Get new key: https://aistudio.google.com/app/apikey")
    else:
        print(f"Found {len(models)} models:\n")
        
        for model in models:
            print(f"Model: {model.name}")
            print(f"  Display Name: {model.display_name}")
            print(f"  Supported Methods: {model.supported_generation_methods}")
            print("-" * 80)

except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 Solutions:")
    print("1. Generate NEW API key: https://aistudio.google.com/app/apikey")
    print("2. Make sure you're using Gemini API, not MakerSuite API")
    print("3. Check if API is enabled in your Google Cloud project")
