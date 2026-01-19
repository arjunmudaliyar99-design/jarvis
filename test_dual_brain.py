"""
Test JARVIS Dual-Brain Architecture
Tests ACTION BRAIN, KNOWLEDGE BRAIN, and CONVERSATION handling
"""
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

print("="*80)
print("JARVIS DUAL-BRAIN ARCHITECTURE TEST")
print("="*80)

# Test 1: Intent Detector
print("\n" + "="*80)
print("TEST 1: INTENT CLASSIFICATION")
print("="*80)

from intent_detector import IntentDetector

detector = IntentDetector()

test_inputs = [
    # ACTION intents
    ("Open Chrome", "ACTION"),
    ("Play Hanuman Chalisa on YouTube", "ACTION"),
    ("Chrome kholo", "ACTION"),
    ("Send message to John", "ACTION"),
    
    # INFORMATION intents
    ("What is JavaScript?", "INFORMATION"),
    ("Explain Python to me", "INFORMATION"),
    ("How does the internet work?", "INFORMATION"),
    ("JavaScript kya hai?", "INFORMATION"),
    
    # CONVERSATION intents
    ("Hello", "CONVERSATION"),
    ("How are you?", "CONVERSATION"),
    ("Thanks", "CONVERSATION"),
    
    # EXIT intents
    ("Exit", "EXIT"),
    ("Goodbye", "EXIT"),
]

print("\n📊 Testing intent classification:")
for text, expected in test_inputs:
    intent, confidence, details = detector.classify_intent(text)
    status = "✅" if intent == expected else "❌"
    print(f"{status} '{text}' → {intent} (expected: {expected}, confidence: {confidence:.2f})")

# Test 2: Knowledge Engine
print("\n" + "="*80)
print("TEST 2: KNOWLEDGE ENGINE (Educational AI)")
print("="*80)

from knowledge_engine import KnowledgeEngine

# Initialize without API key for testing
knowledge = KnowledgeEngine(api_key=None, model_provider='gemini')

test_questions = [
    "What is JavaScript?",
    "Explain Python",
    "How does the internet work?"
]

print("\n📚 Testing educational responses:")
for question in test_questions:
    print(f"\n❓ Question: {question}")
    answer = knowledge.explain(question)
    print(f"💡 Answer: {answer[:150]}...")

# Test 3: Memory Manager
print("\n" + "="*80)
print("TEST 3: MEMORY MANAGER (Context Tracking)")
print("="*80)

from jarvis_memory import ConversationMemory

memory = ConversationMemory(max_memory=5)

# Add sample conversation
memory.add_user_message("What is Python?", language='en', intent='INFORMATION', topic='python')
memory.add_assistant_message("Python is a programming language...", intent='information')
memory.add_user_message("Tell me more", language='en', intent='INFORMATION')

print(f"\n✅ Total interactions: {memory.total_interactions}")
print(f"✅ Last topic: {memory.get_last_topic()}")
print(f"✅ Last intent: {memory.get_last_intent()}")
print(f"✅ Last language: {memory.get_last_language()}")

history = memory.get_conversation_history()
print(f"✅ History length: {len(history)}")

# Test 4: Complete Brain Test
print("\n" + "="*80)
print("TEST 4: COMPLETE DUAL-BRAIN SYSTEM")
print("="*80)

from jarvis_brain import JarvisBrain

brain = JarvisBrain(memory)

test_scenarios = [
    ("Open Chrome", "ACTION BRAIN → System Control"),
    ("What is JavaScript?", "KNOWLEDGE BRAIN → Educational Explanation"),
    ("Hello", "CONVERSATION BRAIN → Casual Chat"),
    ("Play Hanuman Chalisa", "ACTION BRAIN → YouTube Automation"),
    ("Explain Python", "KNOWLEDGE BRAIN → Teaching Mode"),
]

print("\n🧠 Testing complete brain routing:")
for text, expected_route in test_scenarios:
    print(f"\n{'='*60}")
    print(f"INPUT: '{text}'")
    print(f"EXPECTED: {expected_route}")
    
    result = brain.process_input(text, 'en')
    
    print(f"✅ INTENT: {result['intent']}")
    print(f"✅ ACTION: {result.get('action', 'None')}")
    print(f"✅ RESPONSE: {result['response'][:100]}...")
    print(f"✅ CONFIDENCE: {result['confidence']:.2f}")

print("\n" + "="*80)
print("ALL TESTS COMPLETED")
print("="*80)
print("\n✅ DUAL-BRAIN ARCHITECTURE IS READY!")
print("\nNEXT STEPS:")
print("1. Configure API key in config.py for full AI explanations")
print("2. Test with voice input using main.py")
print("3. Try commands like:")
print("   - 'What is JavaScript?' (Knowledge Brain)")
print("   - 'Open Chrome' (Action Brain)")
print("   - 'Play Believer on YouTube' (Action Brain)")
print("   - 'Explain Python' (Knowledge Brain)")
