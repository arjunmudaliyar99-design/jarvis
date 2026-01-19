"""
Microphone and Speech Recognition Diagnostic Tool
Tests if JARVIS can hear and recognize your voice
"""
import speech_recognition as sr
import sys

print("=" * 70)
print("JARVIS MICROPHONE DIAGNOSTIC")
print("=" * 70)

recognizer = sr.Recognizer()

# Step 1: List microphones
print("\n1. AVAILABLE MICROPHONES:")
print("-" * 70)
try:
    microphones = sr.Microphone.list_microphone_names()
    for i, name in enumerate(microphones):
        print(f"   [{i}] {name}")
    print(f"\n   Total: {len(microphones)} microphones found")
except Exception as e:
    print(f"ERROR listing microphones: {e}")
    sys.exit(1)

# Step 2: Test default microphone
print("\n2. TESTING DEFAULT MICROPHONE:")
print("-" * 70)
try:
    with sr.Microphone() as source:
        print("   Adjusting for ambient noise (please wait 2 seconds)...")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print(f"   Energy threshold set to: {recognizer.energy_threshold}")
        print(f"   Dynamic energy threshold: {recognizer.dynamic_energy_threshold}")
        
        print("\n   ✅ Microphone is working!")
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    print("\n   TROUBLESHOOTING:")
    print("   - Check if microphone is plugged in")
    print("   - Check Windows microphone permissions")
    print("   - Try running as administrator")
    sys.exit(1)

# Step 3: Test speech recognition
print("\n3. TESTING SPEECH RECOGNITION:")
print("-" * 70)
print("   I will listen for 5 seconds.")
print("   Please say: 'open youtube'")
print("\n   >>> SPEAK NOW! <<<\n")

try:
    with sr.Microphone() as source:
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        # Lower energy threshold for better sensitivity
        recognizer.energy_threshold = 300  # Lower = more sensitive
        recognizer.dynamic_energy_threshold = True
        
        print(f"   Energy threshold: {recognizer.energy_threshold}")
        print("   Listening...")
        
        # Listen with timeout
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        
        print("   Audio captured! Processing...")
        
        # Try recognizing with multiple language options
        recognized = False
        
        # Try English (India)
        try:
            text = recognizer.recognize_google(audio, language='en-IN')
            print(f"\n   ✅ RECOGNIZED (English-India): '{text}'")
            recognized = True
        except sr.UnknownValueError:
            print("   ❌ Could not understand (English-India)")
        except sr.RequestError as e:
            print(f"   ❌ API error (English-India): {e}")
        
        # Try Hindi
        if not recognized:
            try:
                text = recognizer.recognize_google(audio, language='hi-IN')
                print(f"\n   ✅ RECOGNIZED (Hindi): '{text}'")
                recognized = True
            except sr.UnknownValueError:
                print("   ❌ Could not understand (Hindi)")
            except sr.RequestError as e:
                print(f"   ❌ API error (Hindi): {e}")
        
        # Try English (US)
        if not recognized:
            try:
                text = recognizer.recognize_google(audio, language='en-US')
                print(f"\n   ✅ RECOGNIZED (English-US): '{text}'")
                recognized = True
            except sr.UnknownValueError:
                print("   ❌ Could not understand (English-US)")
            except sr.RequestError as e:
                print(f"   ❌ API error (English-US): {e}")
        
        if not recognized:
            print("\n   ❌ NO SPEECH RECOGNIZED")
            print("\n   POSSIBLE ISSUES:")
            print("   1. Microphone volume too low")
            print("   2. Too much background noise")
            print("   3. Speaking too quietly")
            print("   4. No internet connection (Google Speech needs internet)")
            print("\n   SOLUTIONS:")
            print("   - Increase microphone volume in Windows settings")
            print("   - Speak louder and clearer")
            print("   - Move to a quieter location")
            print("   - Check internet connection")
        else:
            print("\n   ✅ SPEECH RECOGNITION IS WORKING!")
            print("\n   Your JARVIS should work now. Try saying:")
            print("   - 'open youtube'")
            print("   - 'play despacito on youtube'")
            print("   - 'open whatsapp'")
            
except sr.WaitTimeoutError:
    print("\n   ❌ TIMEOUT: No speech detected in 5 seconds")
    print("\n   POSSIBLE ISSUES:")
    print("   - Microphone is not picking up sound")
    print("   - Microphone is muted")
    print("   - Microphone permissions denied")
    print("\n   SOLUTIONS:")
    print("   - Check Windows Sound settings")
    print("   - Unmute microphone")
    print("   - Grant microphone permissions to Python")
    
except Exception as e:
    print(f"\n   ❌ UNEXPECTED ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("DIAGNOSTIC COMPLETE")
print("=" * 70)
