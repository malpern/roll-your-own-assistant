from dotenv import load_dotenv
import os
import time


class ProcessingPipeline:
    def __init__(self):
        """Initialize the processing pipeline with necessary models and clients"""
        print("   Loading environment configuration...")
        load_dotenv()
        
        print("   Loading AI models and clients...")
        print("      • Loading Whisper (this may take 15-20 seconds)...")
        print("        Please wait", end="", flush=True)
        
        # Show loading indicator while model loads
        loading_thread = None
        try:
            import threading
            
            def loading_indicator():
                while loading_thread and loading_thread.is_alive():
                    print(".", end="", flush=True)
                    time.sleep(0.5)
            
            loading_thread = threading.Thread(target=loading_indicator)
            loading_thread.start()
            
            from faster_whisper import WhisperModel
            self.model = WhisperModel(
                "base",
                device="cpu",
                compute_type="float32",
                download_root="./models"
            )
            
            # Stop loading indicator
            loading_thread = None
            print("\n        ✓ Model loaded")
            
        except Exception as e:
            loading_thread = None
            print(f"\n        ❌ Error loading model: {str(e)}")
            raise
        
        print("      • Loading Anthropic client...")
        from anthropic import Anthropic
        self.anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        
        print("      • Loading OpenAI TTS client...")
        from openai import OpenAI
        self.tts_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        print("\n✅ Processing pipeline ready!")
        
    def transcribe_audio(self, audio_path):
        """Transcribe audio file using Whisper"""
        print("\n🎤 Transcribing your message...")
        segments, info = self.whisper_model.transcribe(audio_path, beam_size=5)
        
        # Combine all segments into one text
        transcript = " ".join(segment.text for segment in segments)
        print(f"📝 Transcription: \"{transcript}\"")
        return transcript
    
    def get_ai_response(self, transcript, screenshot_path):
        """Get AI response from Claude using transcript and screenshot context"""
        print("\n🤖 Getting AI response...")
        print("   - Reading screenshot...")
        
        # Read screenshot as base64 for Claude
        with open(screenshot_path, "rb") as img_file:
            import base64
            image_base64 = base64.b64encode(img_file.read()).decode()
        
        print("   - Sending request to Claude...")
        # Create message with both text and image
        response = self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Here is my question/request: {transcript}\nPlease help me with this, taking into account the screenshot of my current work context."
                    },
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": image_base64
                        }
                    }
                ]
            }]
        )
        
        ai_response = response.content[0].text
        print(f"\n💭 AI response: \"{ai_response}\"")
        return ai_response
    
    def text_to_speech(self, text):
        """Convert text to speech using OpenAI TTS"""
        print("\n🔊 Converting response to speech...")
        
        response = self.tts_client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text
        )
        
        # Save to file with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"responses/response_{timestamp}.mp3"
        
        # Create responses directory if it doesn't exist
        os.makedirs('responses', exist_ok=True)
        
        print("   - Saving audio response...")
        response.stream_to_file(output_file)
        print(f"✅ Response saved to: {output_file}")
        return output_file
    
    def process(self, audio_data):
        """Process recorded audio"""
        if not audio_data or len(audio_data) == 0:
            print("DEBUG: No audio data to process")
            return False
            
        try:
            if not all([self.whisper, self.anthropic, self.tts]):
                raise RuntimeError("Pipeline components not properly initialized")
                
            text = self.transcribe(audio_data)
            if not text:
                print("DEBUG: No text transcribed from audio")
                return False
                
            response = self.get_ai_response(text)
            if not response:
                print("DEBUG: No response from AI")
                return False
                
            return self.synthesize_speech(response)
            
        except Exception as e:
            print(f"Error in processing pipeline: {e}")
            return False
    
    def cleanup(self):
        """Clean up resources and stop monitoring"""
        try:
            # Stop recording if active
            if hasattr(self, 'recording_in_progress') and self.recording_in_progress:
                self.stop_recording()
            
            # Remove monitors safely
            if hasattr(self, 'monitors'):
                for monitor in list(self.monitors):
                    try:
                        NSEvent.removeMonitor_(monitor)
                    except Exception as e:
                        print(f"Error removing monitor: {e}")
                self.monitors.clear()
            
            # Clean up recorder
            if hasattr(self, 'recorder') and self.recorder:
                try:
                    if hasattr(self.recorder, 'stop'):
                        self.recorder.stop()
                except Exception as e:
                    print(f"Error cleaning up recorder: {e}")
                
        except Exception as e:
            print(f"Error during cleanup: {e}")
    
    def handle_event(self, event):
        """Handle keyboard events"""
        if not event:
            return None
        
        try:
            event_type = event.type()
            key_code = event.keyCode()
            flags = event.modifierFlags()
            
            print(f"\nDEBUG: Event received:")
            print(f"  - Type: {event_type}")
            print(f"  - KeyCode: {key_code}")
            print(f"  - Flags: {flags}")
            
            if self.is_record_command(event_type, key_code, flags):
                if event_type == NSEventTypeKeyDown and not self.recording_in_progress:
                    return self.start_recording()
                elif event_type == NSEventTypeKeyUp and self.recording_in_progress:
                    return self.stop_recording()
                
            return event
            
        except Exception as e:
            print(f"Error handling event: {e}")
            return event