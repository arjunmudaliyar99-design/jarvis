"""
Test if brain routing fix works
"""
from jarvis_memory import ConversationMemory
from jarvis_brain import JarvisBrain

print("=" * 70)
print("TESTING BRAIN ROUTING FIX")
print("=" * 70)

memory = ConversationMemory()
brain = JarvisBrain(memory)

test_cases = [
    ("open youtube", "play_youtube"),
    ("youtube chalao", "play_youtube"),
    ("play despacito on youtube", "play_youtube"),
    ("open whatsapp", "open_app"),
    ("open chrome", "open_app"),
    ("search google for python", "search"),
]

print("\nProcessing test cases...")
print("-" * 70)

for command, expected_action in test_cases:
    result = brain.process_input(command, 'en')
    actual_action = result.get('action')
    
    status = "PASS" if actual_action == expected_action else "FAIL"
    print(f"{status} | Command: '{command}'")
    print(f"      Expected: {expected_action}, Got: {actual_action}")
    print()

print("=" * 70)
print("TEST COMPLETE")
print("=" * 70)
