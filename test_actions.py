"""
Quick test to verify YouTube and WhatsApp actions work
"""
import sys
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Test commands
test_commands = [
    "open youtube",
    "play youtube",
    "youtube chalao",
    "open whatsapp",
    "whatsapp kholo",
    "play despacito on youtube",
    "search google for python",
    "open chrome"
]

print("=" * 70)
print("TESTING JARVIS ACTION DETECTION")
print("=" * 70)

# Test 1: Intent Detection
print("\n1. TESTING INTENT DETECTOR")
print("-" * 70)
try:
    from intent_detector import IntentDetector
    detector = IntentDetector()
    
    for cmd in test_commands:
        intent, confidence, details = detector.classify_intent(cmd)
        print(f"\n  Command: '{cmd}'")
        print(f"  Intent: {intent} (confidence: {confidence:.2f})")
        if intent != 'ACTION':
            print(f"  ⚠️ WARNING: Should be ACTION, got {intent}")
except Exception as e:
    print(f"❌ Intent detector failed: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Brain Processing
print("\n\n2. TESTING BRAIN PROCESSING")
print("-" * 70)
try:
    from jarvis_memory import ConversationMemory
    from jarvis_brain import JarvisBrain
    
    memory = ConversationMemory()
    brain = JarvisBrain(memory)
    
    test_cmd = "open youtube"
    print(f"\n  Processing: '{test_cmd}'")
    result = brain.process_input(test_cmd, 'en')
    
    print(f"\n  Result:")
    print(f"    Intent: {result.get('intent')}")
    print(f"    Action: {result.get('action')}")
    print(f"    Response: {result.get('response')}")
    
    if result.get('action'):
        print(f"  ✅ Action detected correctly")
    else:
        print(f"  ❌ No action detected!")
        
except Exception as e:
    print(f"❌ Brain test failed: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Task Execution
print("\n\n3. TESTING TASK EXECUTOR")
print("-" * 70)
try:
    from jarvis_tasks import JarvisTasks
    
    tasks = JarvisTasks()
    
    # Test YouTube
    print("\n  Test 1: Opening YouTube directly")
    print("  Calling: tasks.play_youtube('test video')")
    result = tasks.play_youtube("test video", {})
    print(f"  Result: {result}")
    
    # Test WhatsApp
    print("\n  Test 2: Opening WhatsApp directly")
    print("  Calling: tasks.open_application('open whatsapp', {})")
    result = tasks.open_application("open whatsapp", {})
    print(f"  Result: {result}")
    
    # Test Chrome
    print("\n  Test 3: Opening Chrome directly")
    print("  Calling: tasks.open_application('open chrome', {})")
    result = tasks.open_application("open chrome", {})
    print(f"  Result: {result}")
    
except Exception as e:
    print(f"❌ Task executor test failed: {e}")
    import traceback
    traceback.print_exc()

# Test 4: System Controller
print("\n\n4. TESTING SYSTEM CONTROLLER")
print("-" * 70)
try:
    from system_controller import get_system_controller
    
    controller = get_system_controller()
    
    print(f"\n  System: {controller.os}")
    
    # Test YouTube
    print("\n  Test 1: open_youtube('despacito')")
    success, msg = controller.open_youtube('despacito')
    print(f"  Success: {success}, Message: {msg}")
    
    # Test application
    print("\n  Test 2: open_application('chrome')")
    success, msg = controller.open_application('chrome')
    print(f"  Success: {success}, Message: {msg}")
    
except Exception as e:
    print(f"❌ System controller test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
