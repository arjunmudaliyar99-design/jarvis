"""
Test script for JARVIS automation features
"""
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Test imports
try:
    from jarvis_automation import BrowserAutomation, ContentExtractor
    print("✅ Automation modules imported successfully")
except Exception as e:
    print(f"❌ Import failed: {e}")
    exit(1)

# Test ContentExtractor
print("\n" + "="*60)
print("TESTING CONTENT EXTRACTOR")
print("="*60)

extractor = ContentExtractor()

# Test video extraction
test_queries = [
    "YouTube mein Hanuman Chalisa play kijiye",
    "play hanuman chalisa",
    "chalao Shape of You",
    "bajao despacito song"
]

for query in test_queries:
    video_name = extractor.extract_video_content(query)
    print(f"\nQuery: '{query}'")
    print(f"Extracted: '{video_name}'")

# Test message extraction
print("\n" + "="*60)
print("TESTING MESSAGE EXTRACTOR")
print("="*60)

message_queries = [
    "Arjun ko message bhejo ki main late ho jaunga",
    "WhatsApp kholo aur Amma ko message bhejiye",
    "send message to John that I'm on my way"
]

for query in message_queries:
    contact, message = extractor.extract_contact_and_message(query)
    print(f"\nQuery: '{query}'")
    print(f"Contact: '{contact}'")
    print(f"Message: '{message}'")

# Test browser automation (if Selenium is available)
print("\n" + "="*60)
print("TESTING BROWSER AUTOMATION")
print("="*60)

automation = BrowserAutomation()

# Test if automation is ready
if automation:
    print("✅ Browser automation initialized")
    print("\nREADY TO TEST:")
    print("1. YouTube automation: automation.play_youtube_video('Hanuman Chalisa')")
    print("2. WhatsApp automation: automation.send_whatsapp_message('Contact', 'Message')")
    print("\nNote: Actual browser automation requires manual testing")
else:
    print("❌ Browser automation not available")

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)
