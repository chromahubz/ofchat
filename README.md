# OFChat - Auto-Reply Assistant

An intelligent auto-reply system for fansmetric chat that uses AI to generate professional, engaging responses to fan messages.

## Features

- **Clipboard Monitoring**: Automatically detects when you copy messages
- **Screenshot OCR**: Extract text from screenshots using vision AI
- **AI-Powered Responses**: Uses Groq's LLaMA models for natural, engaging replies
- **Smart Prompts**: Different prompt templates for various message types
- **Simple GUI**: Easy-to-use interface with real-time monitoring
- **Conversation History**: Optional context-aware responses
- **Auto-Copy**: Generated responses automatically copied to clipboard

## Tech Stack

- **Language**: Python 3.10+
- **LLM Provider**: Groq (LLaMA 3.1 70B for text, LLaMA 3.2 90B Vision for OCR)
- **GUI**: Tkinter (built-in)
- **Key Libraries**:
  - `groq` - Groq API client
  - `pillow` - Image processing
  - `pyautogui` - Screenshot capture
  - `pyperclip` - Clipboard operations
  - `pynput` - Input monitoring

## Installation

### Prerequisites

- Python 3.10 or higher
- Groq API key ([Get one here](https://console.groq.com/keys))

### Setup

1. **Clone the repository**
   ```bash
   cd ofchat
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   ```

5. **Add your Groq API key**

   Edit `.env` file and add your API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

## Usage

### Starting the Application

```bash
python main.py
```

### Using the GUI

1. **Start Monitoring**
   - Click "Start Monitoring" button
   - Application will watch your clipboard for new messages

2. **Copy a Message**
   - Copy any fan message to your clipboard
   - The app will automatically detect it and generate a response

3. **Get Response**
   - Generated response appears in the "Generated Response" section
   - If "Auto-copy" is enabled, response is automatically copied to clipboard
   - Paste the response back into your chat

4. **Screenshot Mode** (Alternative)
   - Click "Capture Screenshot" button
   - Screenshot will be captured and text extracted using vision AI
   - Response will be generated from extracted text

### Settings

- **Auto-copy response to clipboard**: Automatically copy generated responses
- **Use conversation history**: Enable context-aware responses based on chat history

## How It Works

```
User copies message → Clipboard Monitor detects change
                    ↓
              Extract message text
                    ↓
        Send to Groq LLM with prompt template
                    ↓
          Generate engaging response
                    ↓
      Copy to clipboard (ready to paste)
```

### Prompt System

The system uses specialized prompts for different scenarios:

- **Master Prompt**: General-purpose responses
- **First Message**: Welcoming new fans
- **Simple Response**: Quick, brief replies
- **Question Response**: Answering fan questions
- **Compliment Response**: Gracious acknowledgment

## Configuration

Edit `.env` to customize:

```bash
# API Configuration
GROQ_API_KEY=your_key_here
LLM_MODEL=llama-3.1-70b-versatile
VISION_MODEL=llama-3.2-90b-vision-preview

# Application Settings
CLIPBOARD_CHECK_INTERVAL=0.5
MIN_MESSAGE_LENGTH=5
MAX_RESPONSE_LENGTH=500

# UI Settings
WINDOW_WIDTH=600
WINDOW_HEIGHT=400
```

## Project Structure

```
ofchat/
├── src/
│   ├── config.py              # Configuration management
│   ├── orchestrator.py        # Main orchestration logic
│   ├── ui.py                  # GUI interface
│   ├── capture/
│   │   ├── clipboard.py       # Clipboard monitoring
│   │   ├── screenshot.py      # Screenshot capture
│   │   └── vision_ocr.py      # Vision OCR extraction
│   └── llm/
│       ├── groq_client.py     # Groq API integration
│       └── prompts.py         # Prompt templates
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
└── README.md                 # This file
```

## Main Entry Points

- **`main.py`**: Application entry point - launches the GUI
- **`src/ui.py`**: GUI implementation and user interaction
- **`src/orchestrator.py`**: Core logic coordinator
- **`src/llm/groq_client.py`**: LLM API integration

## Troubleshooting

### API Key Issues

If you see "GROQ_API_KEY not found" error:
1. Ensure `.env` file exists in project root
2. Verify your API key is correct
3. Get a new key from: https://console.groq.com/keys

### Clipboard Not Working

- On Linux, you may need to install `xclip` or `xsel`:
  ```bash
  sudo apt-get install xclip  # Ubuntu/Debian
  ```

### Screenshot Issues

- Ensure you have necessary permissions for screen capture
- On macOS, grant screen recording permissions in System Preferences

## Future Enhancements

- [ ] Custom prompt editor in GUI
- [ ] Response rating and feedback system
- [ ] Multiple profile support
- [ ] Keyboard shortcuts for all actions
- [ ] Response history log
- [ ] Statistics and analytics
- [ ] Browser extension integration

## License

This project is for personal use.

## Support

For issues or questions, please create an issue in the repository.

---

**Built with Groq AI** 🚀
