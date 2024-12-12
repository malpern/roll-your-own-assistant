import sounddevice as sd
import soundfile as sf
import time
import numpy as np
from pathlib import Path
import sys
import threading

class AudioPlayer:
    def __init__(self):
        """Initialize the audio player"""
        self.current_stream = None
        self.terminal_width = self._get_terminal_width()
        self._portaudio_initialized = False
        
    def _get_terminal_width(self):
        """Get terminal width for visualization"""
        try:
            import shutil
            return shutil.get_terminal_size().columns
        except:
            return 80  # fallback width
            
    def _draw_waveform(self, data, num_bars=50):
        """Draw a simple waveform visualization"""
        # Calculate RMS values for chunks of audio
        chunk_size = len(data) // num_bars
        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        rms_values = [np.sqrt(np.mean(chunk**2)) for chunk in chunks if len(chunk) > 0]
        
        # Normalize RMS values to terminal height
        max_height = 8  # Maximum height in terminal lines
        if max(rms_values) > 0:  # Avoid division by zero
            normalized = [int((v / max(rms_values)) * max_height) for v in rms_values]
        else:
            normalized = [0] * len(rms_values)
        
        # Draw waveform
        waveform = ''
        blocks = '▁▂▃▄▅▆▇█'  # Unicode blocks for visualization
        for height in normalized:
            if height >= len(blocks):
                height = len(blocks) - 1
            waveform += blocks[height]
            
        print(f"\n📊 Waveform preview:")
        print(waveform)
        
    def play_file(self, file_path):
        """Play an audio file and wait for it to complete"""
        try:
            print(f"\n🔊 Playing response...")
            
            # Load the audio file
            data, samplerate = sf.read(file_path)
            
            # Show waveform preview
            self._draw_waveform(data)
            
            # Create an event to track when playback is finished
            finished = threading.Event()
            
            def callback(outdata, frames, time, status):
                if status:
                    print(f'\nStatus: {status}')
                    
                # Get the next chunk of data
                if len(data) > 0:
                    chunk = data[:frames]
                    outdata[:len(chunk)] = chunk
                    data = data[frames:]
                else:
                    print()  # New line after playback
                    finished.set()
                    raise sd.CallbackStop()
            
            # Start playback
            self.current_stream = sd.OutputStream(
                samplerate=samplerate,
                channels=len(data.shape) if len(data.shape) > 1 else 1,
                callback=callback
            )
            self._portaudio_initialized = True
            
            with self.current_stream:
                finished.wait()  # Wait for playback to finish
                
            print("✅ Playback complete")
            return True
            
        except Exception as e:
            print(f"❌ Error during playback: {e}")
            return False
            
    def cleanup(self):
        """Clean up all audio resources"""
        try:
            self.stop()
            # Only terminate if we actually had a stream
            if self.current_stream is not None and self._portaudio_initialized:
                try:
                    sd._terminate()
                except Exception as e:
                    print(f"Error terminating PortAudio: {e}")
                self._portaudio_initialized = False
        except Exception as e:
            print(f"Error during audio player cleanup: {e}")
            
    def stop(self):
        """Stop any current playback"""
        if self.current_stream:
            try:
                self.current_stream.stop()
                self.current_stream.close()
            except:
                pass
            finally:
                self.current_stream = None
                
    def __del__(self):
        """Ensure cleanup on deletion"""
        self.cleanup() 