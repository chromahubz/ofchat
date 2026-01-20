"""
Vision OCR using Groq's vision models
"""
import base64
from io import BytesIO
from PIL import Image
from groq import Groq
from typing import Optional


class VisionOCR:
    """Extract text from images using Groq vision models"""

    def __init__(self, api_key: str, model: str = "llama-3.2-90b-vision-preview"):
        """
        Initialize Vision OCR

        Args:
            api_key: Groq API key
            model: Vision model to use
        """
        self.client = Groq(api_key=api_key)
        self.model = model

    def image_to_base64(self, image: Image.Image) -> str:
        """
        Convert PIL Image to base64 string

        Args:
            image: PIL Image

        Returns:
            Base64 encoded image string
        """
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()
        return base64.b64encode(img_bytes).decode('utf-8')

    def extract_text(self, image: Image.Image, prompt: Optional[str] = None) -> str:
        """
        Extract text from image using vision model

        Args:
            image: PIL Image to process
            prompt: Optional custom prompt for extraction

        Returns:
            Extracted text
        """
        if prompt is None:
            prompt = (
                "Extract all text from this image. "
                "Focus on chat messages or conversation text. "
                "Return only the text content, without any formatting or explanations."
            )

        # Convert image to base64
        image_base64 = self.image_to_base64(image)

        try:
            # Call Groq vision API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                temperature=0.1,
                max_tokens=1000
            )

            extracted_text = response.choices[0].message.content
            return extracted_text.strip()

        except Exception as e:
            raise Exception(f"Vision OCR failed: {str(e)}")

    def extract_from_path(self, image_path: str, prompt: Optional[str] = None) -> str:
        """
        Extract text from image file path

        Args:
            image_path: Path to image file
            prompt: Optional custom prompt

        Returns:
            Extracted text
        """
        image = Image.open(image_path)
        return self.extract_text(image, prompt)
