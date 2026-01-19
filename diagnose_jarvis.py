"""
Quick diagnostic to identify why JARVIS isn't responding
Tests each component individually
"""
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

print("=" * 70)
print("JARVIS NOT RESPONDING - DIAGNOSTIC")
print("=" * 70)

# Test 1: Voice Output (Speaking)
print("\n[TEST 1] Voice Output (TTS)")
print("-" * 70)
try:
    from jarvis_voice_advanced import JarvisVoiceSystem
    voice = JarvisVoiceSystem()
    
    print("Speaking: 'Test successful'")
    voice.speak("Test successful", async_mode=False)
    print("SUCCESS: Voice output is working!")
    
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Voice Input (Recognition)
print("\n[TEST 2] Voice Input (Speech Recognition)")
print("-" * 70)
print("Say: 'open youtube' when prompted")
print("Listening in 3 seconds...")

import time
time.sleep(3)

try:
    from jarvis_voice_advanced import JarvisVoiceSystem
    voice = JarvisVoiceSystem()
    
    print("\n>>> SPEAK NOW: 'open youtube' <<<\n")
    text, lang = voice.listen(timeout=5)
    
    if text:
        print(f"SUCCESS: Recognized '{text}' in language '{lang}'")
    else:
        print("FAILED: No speech recognized")
        print("\nPOSSIBLE ISSUES:")
        print("1. Microphone not working or muted")
        print("2. Microphone permissions not granted")
        print("3. Speaking too quietly")
        print("4. No internet connection (Google Speech needs internet)")
        print("\nSOLUTION: Run 'python test_microphone.py' for detailed diagnosis")
    
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Task Execution
print("\n[TEST 3] Task Execution")
print("-" * 70)
try:
    from jarvis_tasks import JarvisTasks
    tasks = JarvisTasks()
    
    print("Executing: open_application('open chrome')")
    result = tasks.open_application("open chrome", {})
    
    if result is None:
        print("SUCCESS: Chrome should have opened (None = success)")
    else:
        print(f"Result: {result}")
    
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Full Flow
print("\n[TEST 4] Full Flow (Brain Processing)")
print("-" * 70)
try:
    from jarvis_memory import ConversationMemory
    from jarvis_brain import JarvisBrain
    
    memory = ConversationMemory()
    brain = JarvisBrain(memory)
    
    test_command = "open youtube"
    print(f"Processing: '{test_command}'")
    
    result = brain.process_input(test_command, 'en')
    
    print(f"\nIntent: {result.get('intent')}")
    print(f"Action: {result.get('action')}")
    print(f"Response: {result.get('response')}")
    
    if result.get('action'):
        print("\nSUCCESS: Brain correctly identified action")
        
        # Now execute the task
        from jarvis_tasks import JarvisTasks
        tasks = JarvisTasks()
        
        print("Executing task...")
        task_result = tasks.execute_task(result)
        print(f"Task result: {task_result}")
    else:
        print("FAILED: Brain did not identify action")
    
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("DIAGNOSIS COMPLETE")
print("=" * 70)
print("\nSUMMARY:")
print("- If Test 1 passed: Voice OUTPUT (speaking) works")
print("- If Test 2 failed: Voice INPUT (microphone) is the problem")
print("- If Test 3 passed: Task execution works")
print("- If Test 4 passed: Full system works")
print("\nIf Test 2 failed, run: python test_microphone.py")
print("=" * 70)
