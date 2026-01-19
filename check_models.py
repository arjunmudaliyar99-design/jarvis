"""Check available Gemini models"""
import google.generativeai as genai

# Configure with your API key
genai.configure(api_key='AIzaSyAqtPVSuadyLWg2PNTTtOmdbJgFRgYAt6I')

print("Available Gemini models:\n")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✅ {model.name}")
        print(f"   Display name: {model.display_name}")
        print(f"   Description: {model.description}")
        print()
