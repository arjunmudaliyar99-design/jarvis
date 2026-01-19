"""
Quick voice system test
"""
import speech_recognition as sr
from gtts import gTTS
import pygame
import tempfile
import os

def test_microphone():
    """Test if microphone is working"""
    print("\n🎤 TESTING MICROPHONE...")
    print("=" * 50)
    
    recognizer = sr.Recognizer()
    
    # List all microphones
    print("\n📋 Available microphones:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"  [{index}] {name}")
    
    # Test recording
    print("\n🎙️ Recording 5 seconds... SPEAK NOW!")
    try:
        with sr.Microphone() as source:
            print("📊 Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            print("🔴 RECORDING... Speak clearly!")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("✅ Audio captured! Attempting recognition...")
            
            # Try multiple languages
            results = []
            
            # English (India)
            try:
                text = recognizer.recognize_google(audio, language='en-IN')
                results.append(('en-IN', text))
                print(f"✅ English (India): {text}")
            except Exception as e:
                print(f"❌ English (India): {e}")
            
            # Hindi
            try:
                text = recognizer.recognize_google(audio, language='hi-IN')
                results.append(('hi-IN', text))
                print(f"✅ Hindi: {text}")
            except Exception as e:
                print(f"❌ Hindi: {e}")
            
            # English (US)
            try:
                text = recognizer.recognize_google(audio, language='en-US')
                results.append(('en-US', text))
                print(f"✅ English (US): {text}")
            except Exception as e:
                print(f"❌ English (US): {e}")
            
            if results:
                print(f"\n🎯 BEST RESULT: {results[0][1]}")
                
                # Test speaking
                test_speak(results[0][1])
            else:
                print("\n❌ No speech recognized in any language!")
                print("\nTROUBLESHOOTING:")
                print("1. Check microphone is plugged in and working")
                print("2. Check microphone permissions in Windows Settings")
                print("3. Try speaking louder and clearer")
                print("4. Check internet connection (Google Speech needs internet)")
                
    except sr.WaitTimeoutError:
        print("❌ No speech detected (timeout)")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_speak(text):
    """Test text-to-speech"""
    print(f"\n🔊 TESTING SPEECH OUTPUT...")
    print(f"📝 Speaking: {text}")
    
    try:
        # Test Hindi TTS
        tts = gTTS(text=text, lang='hi', slow=False)
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_path = temp_file.name
        temp_file.close()
        
        tts.save(temp_path)
        
        pygame.mixer.init()
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        
        print("🔊 Playing audio... (listen for sound)")
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        pygame.mixer.music.unload()
        os.unlink(temp_path)
        
        print("✅ Speech test completed!")
        
    except Exception as e:
        print(f"❌ Speech error: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("JARVIS VOICE SYSTEM TEST")
    print("=" * 50)
    test_microphone()
