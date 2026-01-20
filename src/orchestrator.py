"""
Main orchestration logic for OFChat
"""
import pyperclip
from typing import Optional, Callable
from pathlib import Path
from PIL import Image

from .config import Config
from .capture.clipboard import ClipboardMonitor
from .capture.screenshot import ScreenshotCapture
from .capture.vision_ocr import VisionOCR
from .llm.groq_client import GroqClient


class OFChatOrchestrator:
    """Main orchestrator for auto-reply system"""

    def __init__(self, config: Config):
        """
        Initialize orchestrator

        Args:
            config: Application configuration
        """
        self.config = config

        # Initialize components
        self.llm_client = GroqClient(
            api_key=config.GROQ_API_KEY,
            model=config.LLM_MODEL
        )
        self.vision_ocr = VisionOCR(
            api_key=config.GROQ_API_KEY,
            model=config.VISION_MODEL
        )
        self.screenshot_capture = ScreenshotCapture(
            save_dir=config.SCREENSHOTS_DIR
        )

        # Clipboard monitor (will be initialized when started)
        self.clipboard_monitor: Optional[ClipboardMonitor] = None

        # Callbacks for UI updates
        self.on_message_received: Optional[Callable[[str], None]] = None
        self.on_response_generated: Optional[Callable[[str], None]] = None
        self.on_error: Optional[Callable[[str], None]] = None
        self.on_status_change: Optional[Callable[[str], None]] = None

        # State
        self.is_running = False
        self.auto_copy_enabled = True
        self.use_conversation_history = False

    def start(self):
        """Start the orchestrator"""
        if self.is_running:
            return

        # Initialize clipboard monitor
        self.clipboard_monitor = ClipboardMonitor(
            callback=self._on_clipboard_change,
            check_interval=self.config.CLIPBOARD_CHECK_INTERVAL
        )

        self.clipboard_monitor.start()
        self.is_running = True

        if self.on_status_change:
            self.on_status_change("Running - Monitoring clipboard")

    def stop(self):
        """Stop the orchestrator"""
        if not self.is_running:
            return

        if self.clipboard_monitor:
            self.clipboard_monitor.stop()

        self.is_running = False

        if self.on_status_change:
            self.on_status_change("Stopped")

    def _on_clipboard_change(self, text: str):
        """
        Handle clipboard content change

        Args:
            text: New clipboard content
        """
        # Validate message length
        if len(text.strip()) < self.config.MIN_MESSAGE_LENGTH:
            return

        # Notify UI
        if self.on_message_received:
            self.on_message_received(text)

        # Generate response
        self.process_message(text)

    def process_message(self, message: str, message_type: str = "master"):
        """
        Process incoming message and generate response

        Args:
            message: Fan message
            message_type: Type of message for prompt selection
        """
        try:
            if self.on_status_change:
                self.on_status_change("Generating response...")

            # Generate response using LLM
            response = self.llm_client.generate_response(
                user_message=message,
                message_type=message_type,
                use_history=self.use_conversation_history
            )

            # Notify UI
            if self.on_response_generated:
                self.on_response_generated(response)

            # Auto-copy to clipboard if enabled
            if self.auto_copy_enabled:
                pyperclip.copy(response)

            if self.on_status_change:
                self.on_status_change("Response generated and copied!")

        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            if self.on_error:
                self.on_error(error_msg)
            if self.on_status_change:
                self.on_status_change("Error occurred")

    def process_screenshot(self, image: Image.Image):
        """
        Process screenshot to extract text and generate response

        Args:
            image: Screenshot image
        """
        try:
            if self.on_status_change:
                self.on_status_change("Extracting text from screenshot...")

            # Extract text using vision OCR
            extracted_text = self.vision_ocr.extract_text(image)

            if not extracted_text or len(extracted_text.strip()) < self.config.MIN_MESSAGE_LENGTH:
                if self.on_error:
                    self.on_error("No valid text extracted from screenshot")
                return

            # Notify UI
            if self.on_message_received:
                self.on_message_received(extracted_text)

            # Process the extracted message
            self.process_message(extracted_text)

        except Exception as e:
            error_msg = f"Error processing screenshot: {str(e)}"
            if self.on_error:
                self.on_error(error_msg)

    def capture_and_process_screenshot(self):
        """Capture screenshot and process it"""
        try:
            if self.on_status_change:
                self.on_status_change("Capturing screenshot...")

            # Capture fullscreen (in production, you might want region selection)
            screenshot = self.screenshot_capture.capture_fullscreen()

            # Process the screenshot
            self.process_screenshot(screenshot)

        except Exception as e:
            error_msg = f"Error capturing screenshot: {str(e)}"
            if self.on_error:
                self.on_error(error_msg)

    def test_connection(self) -> bool:
        """Test Groq API connection"""
        try:
            return self.llm_client.test_connection()
        except Exception:
            return False

    def clear_history(self):
        """Clear conversation history"""
        self.llm_client.clear_history()
        if self.on_status_change:
            self.on_status_change("Conversation history cleared")
