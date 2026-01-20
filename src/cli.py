"""
Simple CLI for OFChat
"""
import time
import sys
from typing import Optional
import pyperclip

from .config import Config
from .orchestrator import OFChatOrchestrator


class OFChatCLI:
    """Simple CLI for OFChat auto-reply system"""

    def __init__(self, config: Config):
        """
        Initialize CLI

        Args:
            config: Application configuration
        """
        self.config = config
        self.orchestrator = OFChatOrchestrator(config)

        # Set up callbacks
        self.orchestrator.on_message_received = self.on_message_received
        self.orchestrator.on_response_generated = self.on_response_generated
        self.orchestrator.on_error = self.on_error
        self.orchestrator.on_status_change = self.on_status_change

    def print_banner(self):
        """Print CLI banner"""
        print("\n" + "="*60)
        print("  OFChat - Auto Reply Assistant (CLI)")
        print("="*60)
        print("\nMonitoring clipboard for new messages...")
        print("Copy a fan message to clipboard to generate a response.")
        print("\nCommands:")
        print("  Ctrl+C - Stop monitoring and exit")
        print("  h - Toggle conversation history")
        print("="*60 + "\n")

    def on_message_received(self, message: str):
        """Callback when new message is received"""
        print(f"\n📨 Incoming Message:")
        print(f"   {message[:100]}..." if len(message) > 100 else f"   {message}")

    def on_response_generated(self, response: str):
        """Callback when response is generated"""
        print(f"\n✅ Generated Response:")
        print(f"   {response}")
        print(f"\n📋 Response copied to clipboard! Paste it to send.")
        print("\n" + "-"*60)

    def on_error(self, error: str):
        """Callback when error occurs"""
        print(f"\n❌ Error: {error}")

    def on_status_change(self, status: str):
        """Callback when status changes"""
        print(f"   Status: {status}")

    def test_connection(self) -> bool:
        """Test API connection"""
        print("🔌 Testing Groq API connection...")
        try:
            if self.orchestrator.test_connection():
                print("✅ API connection successful!\n")
                return True
            else:
                print("❌ Could not connect to Groq API.")
                print("   Please check your API key in .env file.\n")
                return False
        except Exception as e:
            print(f"❌ Error testing API: {e}\n")
            return False

    def run(self):
        """Start the CLI"""
        self.print_banner()

        # Test connection
        if not self.test_connection():
            return

        # Start monitoring
        print("🚀 Starting clipboard monitor...\n")
        self.orchestrator.start()

        try:
            # Keep running
            while True:
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n\n👋 Stopping OFChat...")
            self.orchestrator.stop()
            print("✅ Stopped. Goodbye!\n")


def create_cli(config: Config) -> OFChatCLI:
    """
    Create and return CLI instance

    Args:
        config: Application configuration

    Returns:
        CLI instance
    """
    return OFChatCLI(config)
