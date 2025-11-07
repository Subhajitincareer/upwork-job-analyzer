"""Test available Gemini models"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key: {api_key[:20]}...\n")

try:
    genai.configure(api_key=api_key)
    
    print("📋 Available Models:")
    print("=" * 60)
    
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
    
    print("\n" + "=" * 60)
    print("\n🧪 Testing models:")
    
    # Test different models
    test_models = [
        'gemini-1.5-flash',
        'gemini-1.5-pro',
        'gemini-pro'
    ]
    
    for model_name in test_models:
        try:
            print(f"\nTrying: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say 'Hello'")
            print(f"✅ {model_name} works!")
            print(f"   Response: {response.text}")
            break
        except Exception as e:
            print(f"❌ {model_name} failed: {str(e)[:100]}")

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n💡 Check your API key at: https://aistudio.google.com/app/apikey")
