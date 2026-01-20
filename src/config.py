"""
Configuration management for OFChat
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""

    # API Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-70b-versatile")
    VISION_MODEL = os.getenv("VISION_MODEL", "llama-3.2-90b-vision-preview")

    # Application Settings
    CLIPBOARD_CHECK_INTERVAL = float(os.getenv("CLIPBOARD_CHECK_INTERVAL", "0.5"))
    SCREENSHOT_HOTKEY = os.getenv("SCREENSHOT_HOTKEY", "ctrl+shift+s")
    MIN_MESSAGE_LENGTH = int(os.getenv("MIN_MESSAGE_LENGTH", "5"))
    MAX_RESPONSE_LENGTH = int(os.getenv("MAX_RESPONSE_LENGTH", "500"))

    # UI Settings
    WINDOW_WIDTH = int(os.getenv("WINDOW_WIDTH", "600"))
    WINDOW_HEIGHT = int(os.getenv("WINDOW_HEIGHT", "400"))

    # Directories
    BASE_DIR = Path(__file__).parent.parent
    SCREENSHOTS_DIR = BASE_DIR / "screenshots"
    LOGS_DIR = BASE_DIR / "logs"

    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        cls.SCREENSHOTS_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)

    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY not found. Please set it in .env file. "
                "Get your API key from: https://console.groq.com/keys"
            )
        return True
