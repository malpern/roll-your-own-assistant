import time
from datetime import datetime
import signal
import sys

print("\n🎧 Initializing AI Assistant...")
print("   This may take a few moments while models load")
print("   Press Ctrl+C at any time to quit\n")

import os
from dotenv import load_dotenv
from hotkeys import HotkeyListener

def signal_handler(sig, frame):
    print("\n\n⚠️  Initialization interrupted by user")
    print("Cleaning up...")
    sys.exit(0)

def test_environment():
    """Test environment setup and dependencies"""
    signal.signal(signal.SIGINT, signal_handler)
    
    print("1. Testing environment setup...")
    
    # Check Python version
    import sys
    print(f"   • Python version: {sys.version.split()[0]}")
    
    # Check required directories exist
    print("   • Checking directories...")
    required_dirs = ['recordings', 'screenshots']
    for directory in required_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"     Created {directory}/ directory")
    
    # Test basic imports
    print("   • Testing imports...")
    try:
        import sounddevice as sd
        print(f"     - sounddevice version: {sd.__version__}")
    except ImportError as e:
        print(f"❌ Error: Failed to import sounddevice: {e}")
        return False
        
    try:
        from faster_whisper import WhisperModel
        print("     - faster_whisper imported successfully")
    except ImportError as e:
        print(f"❌ Error: Failed to import faster_whisper: {e}")
        return False
    
    return True

def main():
    try:
        # Test environment first
        if not test_environment():
            print("\n❌ Environment setup failed. Please check your environment variables.")
            return
            
        # Initialize hotkey listener
        print("\n2. Initializing hotkey listener and components...")
        listener = HotkeyListener()
        
        print("\nStarting event monitor...")
        listener.start()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Initialization interrupted by user")
        print("Cleaning up...")
        sys.exit(0)

if __name__ == "__main__":
    main() 