import pyaudio
import logging
import atexit

logger = logging.getLogger(__name__)

# Global PyAudio instance
_pa_instance = None

def _cleanup_at_exit():
    """Cleanup function registered with atexit"""
    global _pa_instance
    if _pa_instance:
        try:
            # Stop any active streams first
            for stream in _pa_instance._streams:
                try:
                    stream.stop_stream()
                    stream.close()
                except:
                    pass
            # Then terminate PyAudio
            _pa_instance.terminate()
        except:
            pass
        _pa_instance = None

def cleanup_pa():
    """Clean up PyAudio resources. This function is meant to be called during shutdown."""
    _cleanup_at_exit()

# Register cleanup function
atexit.register(_cleanup_at_exit)

def get_pa_instance():
    global _pa_instance
    if _pa_instance is None:
        _pa_instance = pyaudio.PyAudio()
    return _pa_instance

class AudioRecorder:
    def __init__(self):
        self.stream = None
        self.frames = []
        self.has_data = False
        
    def cleanup(self):
        """Clean up all resources"""
        if not self.stream:
            return
            
        if self.stream:
            try:
                self.stream.stop_stream()
                self.stream.close()
            except:
                pass
        self.stream = None
        self.frames = []
        self.has_data = False

    def start(self):
        try:
            pa = get_pa_instance()
            self.stream = pa.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024,
                stream_callback=self._audio_callback
            )
            self.stream.start_stream()
            logger.debug("Audio recording started successfully")
            self.has_data = False
            self.frames = []
        except Exception as e:
            logger.error(f"Failed to start audio recording: {e}")
            self.cleanup()
            raise

    def stop(self):
        """Stop recording and return audio data"""
        if not self.stream:
            return None
            
        try:
            # Get audio data before closing anything
            audio_data = b''.join(self.frames) if self.frames else None
            self.has_data = bool(audio_data)
            
            # Clean up resources
            self.cleanup()
            
            return audio_data
            
        except Exception as e:
            logger.error(f"Error stopping audio stream: {e}")
            self.cleanup()
            return None

    def _audio_callback(self, in_data, frame_count, time_info, status):
        if status:
            logger.warning(f"Audio callback status: {status}")
        try:
            self.frames.append(in_data)
            return (None, pyaudio.paContinue)
        except Exception as e:
            logger.error(f"Audio callback error: {e}")
            return (None, pyaudio.paAbort)

# Test the recorder
if __name__ == "__main__":
    import time
    
    recorder = AudioRecorder()
    print("Starting recording in 3 seconds...")
    time.sleep(3)
    
    recorder.start()
    print("Recording for 5 seconds...")
    time.sleep(5)
    
    audio_data = recorder.stop()
    print(f"Recording saved to: {audio_data}") 