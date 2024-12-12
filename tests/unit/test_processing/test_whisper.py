from faster_whisper import WhisperModel
import os

def test_whisper():
    print("Testing faster-whisper installation...")
    
    # First check if the file exists
    if not os.path.exists("output.wav"):
        print("\nError: output.wav not found in the current directory")
        print(f"Current directory: {os.getcwd()}")
        print("Available files:", os.listdir())
        return None
    
    # Load the small model - better accuracy while still being relatively fast
    print("Loading Whisper model (small)...")
    try:
        model = WhisperModel("small")
        print("Whisper model loaded successfully!")
        print("Ready for speech-to-text conversion.")
        
        # Test with output.wav
        print("\nAttempting to transcribe output.wav...")
        segments, info = model.transcribe("output.wav", beam_size=5)
        
        print("\nTranscription results:")
        print(f"Detected language: {info.language} ({info.language_probability:.2f} probability)")
        
        segment_count = 0
        for segment in segments:
            segment_count += 1
            print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
        
        if segment_count == 0:
            print("No segments were transcribed. The audio might be silent or unclear.")
            
        return model
    except Exception as e:
        print(f"\nError during transcription: {str(e)}")
        print(f"Error type: {type(e)}")
        return None

if __name__ == "__main__":
    test_whisper() 