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
   - ✅ project setup with uv
   - ✅ directory structure organized
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

   - Step 3: Testing & Refinement (🚧 In Progress)
     * ✅ Unit tests for hotkey system
     * ✅ Integration tests
     * ⚠️ Coverage reports
     * ⚠️ Performance testing

### Current Focus

1. **Processing Pipeline Integration**:
   - Connecting audio transcription to AI processing
   - Implementing response playback
   - Adding conversation history

2. **Error Handling & Testing**:
   - Comprehensive test coverage
   - Improving error recovery
   - Adding better debug logging
   - Implementing graceful fallbacks

### Next Steps

1. **Polish Core Features**:
   - Add visual feedback for recording state
   - Implement proper error handling
   - Add configuration options

2. **Testing & Documentation**:
   - Add more integration tests
   - Improve documentation
   - Create user guide

## Project Structure

```
.
├── src/                    # Source code
│   ├── audio/             # Audio recording and playback
│   ├── hotkeys/           # Hotkey handling
│   └── processing/        # AI processing pipeline
├── tests/                 # Test suite
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
├── recordings/           # Recorded audio files
└── screenshots/          # Captured screenshots
```

## Technical Stack

- **Python 3.10.16**: Core runtime environment
- **uv**: Fast Python package installer and resolver
- **Anthropic Claude/GPT-4**: AI model backends
- **faster-whisper**: Efficient speech-to-text processing
- **PyObjC**: macOS system integration
- **Pillow**: Image processing for screenshots
- **sounddevice/soundfile**: Audio recording and file handling
- **pytest**: Testing framework

## Getting Started

### Prerequisites

- **macOS**: Currently macOS-only due to PyObjC dependency
- **API Keys**:
  - Anthropic API key (for Claude AI)
  - OpenAI API key (for text-to-speech)

That's it! The installation process will automatically handle:
- Installing Homebrew (if needed)
- Installing pyenv (if needed)
- Installing Python 3.10.16 (if needed)
- Installing UV package manager
- Setting up a virtual environment
- Installing all project dependencies

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/roll-your-own-assistant.git
cd roll-your-own-assistant
```

2. Run the installation:
```bash
# This will install everything needed, including Python 3.10.16
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

# Run unit tests
make test-unit

# Run all tests (unit + integration)
make test-all

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

2. Use the default hotkey (Command + Shift + A) to:
   - Start recording (press once)
   - Stop recording and process (press again)
   - The system will:
     * Capture a screenshot of your current context
     * Convert your speech to text
     * Process with AI
     * Provide an audio response

3. Use Command + Shift + Q to quit the application cleanly

### Configuration

- Default hotkeys: 
  * Command + Shift + A: Start/Stop recording
  * Command + Shift + Q: Quit application
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
   - Try restarting the application

3. For model loading issues:
   - Ensure you have sufficient disk space (~2GB for models)
   - Check your internet connection for initial model downloads

4. For installation issues:
   - Ensure you're using Python 3.10.16 exactly
   - Try running `make clean` followed by `make install`
   - Check that portaudio is installed (`brew install portaudio`)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Run tests to ensure everything works (`make test-all`)
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.