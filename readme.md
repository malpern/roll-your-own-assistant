# AI Companion

An AI assistant that seamlessly integrates with your desktop workflow through voice and visual context.

## Goal

Create a seamless AI companion that can assist while you work by:
- Capturing screenshots of your current context
- Taking voice input through dictation
- Sending both visual and audio context to AI models
- Providing voice responses

The system should allow you to quickly trigger it with a hotkey, speak your question/request while sharing your screen context, and get an audio response - all while maintaining conversation history for context.

## Implementation Plan

### Phase 1: Core Components

1. Basic Setup (✅ Complete)
   - ✅ project setup, use uv
   - Key dependencies:
     * ✅ anthropic (AI API access) 
     * ✅ sounddevice (audio recording)
     * ✅ pillow (screenshot capture)
     * ✅ global hotkeys (using PyObjC for macOS)
     * ✅ faster-whisper (speech-to-text)
     * ✅ openai (text-to-speech)

2. Core Implementation (✅ Complete)
   - ✅ Screenshot capture module
   - ✅ Audio recording/stop module
   - ✅ Speech-to-text conversion
   - ✅ API integration (Claude/GPT-4)
   - ✅ Text-to-speech response
   - ✅ Global hotkey system

3. Integration Phase (⚠️ In Progress)
   - Step 1: Audio + Hotkeys Integration (✅ Complete)
     * ✅ Hotkey event detection working
     * ✅ Recording triggering on hotkey
     * ✅ Clean exit working
   
   - Step 2: Processing Pipeline (⚠️ In Progress)
     * ✅ Audio transcription
     * ✅ Screenshot capture
     * ⚠️ AI processing integration
     * ⚠️ Response generation

   - Step 3: Testing & Refinement (Not Started)

### Current Focus

1. **Processing Pipeline Integration**:
   - Connecting audio transcription to AI processing
   - Implementing response playback
   - Adding conversation history

2. **Error Handling**:
   - Improving error recovery
   - Adding better debug logging
   - Implementing graceful fallbacks

### Next Steps

1. **Polish Core Features**:
   - Add visual feedback for recording state
   - Implement proper error handling
   - Add configuration options

2. **Testing & Documentation**:
   - Add comprehensive tests
   - Improve documentation
   - Create user guide

## Technical Stack

- **Python 3.10+**: Core runtime environment
- **uv**: Fast Python package installer and resolver
- **Anthropic Claude/GPT-4**: AI model backends
- **faster-whisper**: Efficient speech-to-text processing
- **PyObjC**: macOS system integration
- **Pillow**: Image processing for screenshots
- **sounddevice/soundfile**: Audio recording and file handling

## Getting Started

### Prerequisites

- **Python**: Exactly version 3.10 (not 3.11 or 3.12)
  ```bash
  # Check your Python version
  python3 --version
  
  # If needed, install Python 3.10 using pyenv
  pyenv install 3.10
  pyenv global 3.10
  ```
- **macOS**: Currently macOS-only due to PyObjC dependency
- **API Keys**:
  - Anthropic API key (for Claude AI)
  - OpenAI API key (for text-to-speech)
- **uv**: Fast Python package installer
  ```bash
  # Install uv
  pip install uv
  ```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/roll-your-own-assistant.git
cd roll-your-own-assistant
```

2. Install dependencies using uv:
```bash
# This will verify Python 3.10 and install dependencies
make install
```

3. Create a `.env` file in the project root with your API keys:
```bash
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
```

### Development Commands

```bash
# Install dependencies
make install

# Run tests
make test

# Run the application
make run

# Clean temporary files
make clean

# Update dependencies
make update
```

### Usage

1. Start the application:
```bash
make run
```

2. Use the default hotkey (Command + Shift + Space) to:
   - Start recording (press once)
   - Stop recording and process (press again)
   - The system will:
     * Capture a screenshot of your current context
     * Convert your speech to text
     * Process with AI
     * Provide an audio response

### Configuration

- Default hotkey: Command + Shift + Space
- Audio recordings are stored in `recordings/`
- Screenshots are stored in `screenshots/`
- Logs are stored in the project root directory

### Troubleshooting

1. If you encounter permission issues with audio recording:
   - Ensure your terminal/IDE has microphone access
   - Grant permission in System Preferences > Security & Privacy > Microphone

2. If the hotkey doesn't work:
   - Ensure no other application is using the same hotkey
   - Check System Preferences > Security & Privacy > Accessibility

3. For model loading issues:
   - Ensure you have sufficient disk space (~2GB for models)
   - Check your internet connection for initial model downloads