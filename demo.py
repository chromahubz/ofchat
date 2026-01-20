#!/usr/bin/env python3
"""
Demo script to test OFChat without clipboard/GUI
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import Config
from src.llm.groq_client import GroqClient


def main():
    """Run demo"""
    print("\n" + "="*60)
    print("  OFChat - Demo Mode")
    print("="*60)

    # Validate configuration
    try:
        Config.validate()
        print(f"\n✅ Configuration loaded successfully")
        print(f"   Model: {Config.LLM_MODEL}")
        print(f"   API Key: {Config.GROQ_API_KEY[:20]}...")
    except Exception as e:
        print(f"\n❌ Configuration error: {e}")
        return

    # Initialize LLM client
    print("\n🔌 Initializing Groq client...")
    client = GroqClient(
        api_key=Config.GROQ_API_KEY,
        model=Config.LLM_MODEL
    )

    # Test connection
    print("🧪 Testing API connection...")
    if not client.test_connection():
        print("❌ Could not connect to Groq API")
        return
    print("✅ API connection successful!\n")

    # Test with sample messages
    sample_messages = [
        "Hey beautiful! Just wanted to say you're amazing 😍",
        "I loved your latest post! Can't wait to see more",
        "When are you posting new content?",
        "You're so gorgeous! How's your day going?",
    ]

    print("="*60)
    print("  Testing Response Generation")
    print("="*60 + "\n")

    for i, message in enumerate(sample_messages, 1):
        print(f"\n📨 Test Message #{i}:")
        print(f"   \"{message}\"\n")

        print("   Generating response...")
        try:
            response = client.generate_response(
                user_message=message,
                message_type="master",
                use_history=False
            )

            print(f"\n✅ Generated Response:")
            print(f"   \"{response}\"\n")
            print("-"*60)

        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            print("-"*60)

    print("\n" + "="*60)
    print("  Demo Complete!")
    print("="*60)
    print("\n💡 In production, these responses would be:")
    print("   1. Triggered by clipboard monitoring")
    print("   2. Automatically copied to clipboard")
    print("   3. Ready to paste into fansmetric chat\n")


if __name__ == "__main__":
    main()
