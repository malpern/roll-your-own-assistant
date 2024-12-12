import sounddevice as sd
import soundfile as sf
import numpy as np

def record_audio(duration=5, samplerate=16000):
    """Record audio for a specified duration."""
    print(f"Recording for {duration} seconds...")
    recording = sd.rec(int(samplerate * duration), 
                      samplerate=samplerate, 
                      channels=1, 
                      dtype='float32')
    sd.wait()  # Wait until recording is finished
    print("Recording finished!")
    return recording

def save_audio(recording, filename='output.wav', samplerate=16000):
    """Save the recording to a WAV file."""
    sf.write(filename, recording, samplerate)
    print(f"Audio saved to {filename}")

def test_audio_recording():
    try:
        # List available audio devices
        print("\nAvailable audio devices:")
        print(sd.query_devices())
        
        # Record audio
        recording = record_audio()
        
        # Save the recording
        save_audio(recording)
        
        print("\nAudio test completed successfully!")
        
    except Exception as e:
        print(f"Error during audio recording: {str(e)}")

if __name__ == "__main__":
    test_audio_recording() 