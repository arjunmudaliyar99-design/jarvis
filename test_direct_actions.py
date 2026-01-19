"""
Direct test of YouTube and WhatsApp opening
"""
import logging
logging.basicConfig(level=logging.INFO)

print("=" * 70)
print("DIRECT ACTION TEST")
print("=" * 70)

# Test System Controller
print("\n1. Testing System Controller (Cross-Platform)")
print("-" * 70)
try:
    from system_controller import get_system_controller
    controller = get_system_controller()
    
    print(f"OS: {controller.os}")
    
    # Test YouTube
    print("\nOpening YouTube...")
    success, msg = controller.open_youtube("test video")
    print(f"Result: {success} - {msg}")
    
    input("\nPress Enter to test WhatsApp...")
    
    # Test WhatsApp
    print("\nOpening WhatsApp...")
    success, msg = controller.open_application("whatsapp")
    print(f"Result: {success} - {msg}")
    
    input("\nPress Enter to test Chrome...")
    
    # Test Chrome
    print("\nOpening Chrome...")
    success, msg = controller.open_application("chrome")
    print(f"Result: {success} - {msg}")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

# Test Task Executor
print("\n\n2. Testing Task Executor")
print("-" * 70)
try:
    from jarvis_tasks import JarvisTasks
    tasks = JarvisTasks()
    
    input("\nPress Enter to test play_youtube...")
    
    print("\nCalling tasks.play_youtube('despacito')...")
    result = tasks.play_youtube("despacito", {})
    print(f"Result: {result}")
    
    input("\nPress Enter to test open_application (whatsapp)...")
    
    print("\nCalling tasks.open_application('open whatsapp')...")
    result = tasks.open_application("open whatsapp", {})
    print(f"Result: {result}")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("TEST COMPLETE - Check if apps opened!")
print("=" * 70)
