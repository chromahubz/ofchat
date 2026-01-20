#!/usr/bin/env python3
"""
OFChat - Auto-reply system for fansmetric chat
Main entry point
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import Config


def main():
    """Main entry point"""
    try:
        # Validate configuration
        Config.validate()

        # Ensure directories exist
        Config.ensure_directories()

        # Try to use GUI, fallback to CLI
        try:
            from src.ui import create_gui
            gui = create_gui(Config)
            gui.run()
        except (ImportError, Exception) as e:
            # Fallback to CLI if GUI not available
            from src.cli import create_cli
            cli = create_cli(Config)
            cli.run()

    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\n📝 Setup Instructions:")
        print("1. Copy .env.example to .env")
        print("2. Add your Groq API key to .env")
        print("3. Get your API key from: https://console.groq.com/keys\n")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
