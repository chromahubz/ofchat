"""
Groq API client for LLM response generation
"""
from groq import Groq
from typing import Optional, List, Dict
from .prompts import PromptTemplates


class GroqClient:
    """Client for interacting with Groq LLM API"""

    def __init__(self, api_key: str, model: str = "llama-3.1-70b-versatile"):
        """
        Initialize Groq client

        Args:
            api_key: Groq API key
            model: Model to use for generation
        """
        self.client = Groq(api_key=api_key)
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []

    def generate_response(
        self,
        user_message: str,
        message_type: str = "master",
        temperature: float = 0.7,
        max_tokens: int = 500,
        use_history: bool = False
    ) -> str:
        """
        Generate response to user message

        Args:
            user_message: The fan's message
            message_type: Type of prompt template to use
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
            use_history: Whether to include conversation history

        Returns:
            Generated response text
        """
        # Format the prompt
        prompt = PromptTemplates.format_prompt(user_message, message_type)

        # Prepare messages
        messages = []

        # Add conversation history if requested
        if use_history and self.conversation_history:
            messages.extend(self.conversation_history)

        # Add current prompt
        messages.append({
            "role": "user",
            "content": prompt
        })

        try:
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=0.9,
                stream=False
            )

            # Extract response
            generated_text = response.choices[0].message.content.strip()

            # Update conversation history
            if use_history:
                self.conversation_history.append({
                    "role": "user",
                    "content": user_message
                })
                self.conversation_history.append({
                    "role": "assistant",
                    "content": generated_text
                })

                # Keep only last 10 exchanges (20 messages)
                if len(self.conversation_history) > 20:
                    self.conversation_history = self.conversation_history[-20:]

            return generated_text

        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history.clear()

    def test_connection(self) -> bool:
        """
        Test Groq API connection

        Returns:
            True if connection successful
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": "Say 'OK' if you can hear me."}
                ],
                max_tokens=10
            )
            return True
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
