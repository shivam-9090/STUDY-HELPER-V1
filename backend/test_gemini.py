import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('AI_API_KEY', '')

if not api_key:
    print("❌ No API key found in .env file")
    exit(1)

print(f"✅ API Key found: {api_key[:20]}...")

# Configure Gemini
genai.configure(api_key=api_key)

print("\n📋 Listing available models...")
try:
    models = genai.list_models()
    
    print("\n✅ Available models that support generateContent:\n")
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"  • {model.name}")
            print(f"    Display name: {model.display_name}")
            print(f"    Description: {model.description}")
            print()
    
    print("\n🧪 Testing with a simple question...")
    
    # Try different model names
    model_names = [
        'gemini-pro',
        'models/gemini-pro',
        'gemini-1.5-pro',
        'gemini-1.5-flash',
        'gemini-1.0-pro',
    ]
    
    for model_name in model_names:
        try:
            print(f"\nTrying model: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say hello")
            print(f"✅ SUCCESS with {model_name}!")
            print(f"Response: {response.text}")
            break
        except Exception as e:
            print(f"❌ Failed: {str(e)[:100]}")
            
except Exception as e:
    print(f"\n❌ Error: {e}")
