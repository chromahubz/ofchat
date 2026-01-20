"""
Clipboard monitoring for text capture
"""
import pyperclip
import threading
import time
from typing import Optional, Callable


class ClipboardMonitor:
    """Monitor clipboard for new text content"""

    def __init__(self, callback: Callable[[str], None], check_interval: float = 0.5):
        """
        Initialize clipboard monitor

        Args:
            callback: Function to call when new text is detected
            check_interval: Time between clipboard checks in seconds
        """
        self.callback = callback
        self.check_interval = check_interval
        self.last_content = ""
        self.running = False
        self.thread: Optional[threading.Thread] = None

    def start(self):
        """Start monitoring clipboard"""
        if self.running:
            return

        self.running = True
        self.last_content = pyperclip.paste()
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop monitoring clipboard"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)

    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.running:
            try:
                current_content = pyperclip.paste()

                # Check if content has changed and is not empty
                if (current_content and
                    current_content != self.last_content and
                    current_content.strip()):

                    self.last_content = current_content
                    self.callback(current_content)

            except Exception as e:
                print(f"Clipboard monitoring error: {e}")

            time.sleep(self.check_interval)

    def is_running(self) -> bool:
        """Check if monitor is running"""
        return self.running
