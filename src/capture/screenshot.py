"""
Screenshot capture functionality
"""
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

from PIL import Image
from pathlib import Path
from datetime import datetime
from typing import Optional


class ScreenshotCapture:
    """Handle screenshot capture operations"""

    def __init__(self, save_dir: Path):
        """
        Initialize screenshot capture

        Args:
            save_dir: Directory to save screenshots
        """
        self.save_dir = save_dir
        self.save_dir.mkdir(exist_ok=True)

    def capture_fullscreen(self) -> Image.Image:
        """
        Capture full screen

        Returns:
            PIL Image of the screen
        """
        if not PYAUTOGUI_AVAILABLE:
            raise ImportError("pyautogui is not installed. Install with: pip install pyautogui")
        screenshot = pyautogui.screenshot()
        return screenshot

    def capture_region(self, x: int, y: int, width: int, height: int) -> Image.Image:
        """
        Capture specific screen region

        Args:
            x: X coordinate of top-left corner
            y: Y coordinate of top-left corner
            width: Width of region
            height: Height of region

        Returns:
            PIL Image of the region
        """
        if not PYAUTOGUI_AVAILABLE:
            raise ImportError("pyautogui is not installed. Install with: pip install pyautogui")
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        return screenshot

    def save_screenshot(self, image: Image.Image, prefix: str = "screenshot") -> Path:
        """
        Save screenshot to disk

        Args:
            image: PIL Image to save
            prefix: Filename prefix

        Returns:
            Path to saved file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.png"
        filepath = self.save_dir / filename

        image.save(filepath)
        return filepath

    def capture_and_save(self, region: Optional[tuple] = None) -> Path:
        """
        Capture screenshot and save to disk

        Args:
            region: Optional (x, y, width, height) tuple for region capture

        Returns:
            Path to saved screenshot
        """
        if region:
            image = self.capture_region(*region)
        else:
            image = self.capture_fullscreen()

        return self.save_screenshot(image)
