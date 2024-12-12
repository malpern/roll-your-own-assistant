print("\n🎧 Initializing AI Assistant...")
print("   Loading Whisper model (this may take a moment)...")

# Standard library imports
import os
import sys
import time
import signal
from datetime import datetime

# Third-party imports
from AppKit import (
    NSObject, 
    NSEvent,
    NSApplication,
    NSKeyDown,
    NSKeyUp,
    NSEventMaskKeyDown,
    NSEventMaskKeyUp,
    NSEventTypeKeyDown,
    NSEventTypeKeyUp,
    NSCommandKeyMask,
    NSShiftKeyMask,
    NSAlternateKeyMask,
    NSControlKeyMask
)
from PIL import ImageGrab
from objc import super

# Local imports
from audio_recorder import AudioRecorder
from audio_player import AudioPlayer
from processing import ProcessingPipeline

COMMAND_SHIFT_FLAGS = NSCommandKeyMask | NSShiftKeyMask

print("   Core components loaded...")

class HotkeyListener(NSObject):
    # Command key constants
    CMD_SHIFT_A_MASK = NSCommandKeyMask | NSShiftKeyMask
    CMD_SHIFT_Q_MASK = NSCommandKeyMask | NSShiftKeyMask
    
    def init(self):
        # Call super's init first
        self = super().init()
        if self is None:
            return None
            
        # Initialize all attributes
        self.recording_in_progress = False
        self.monitor = None
        self.local_monitor = None
        self.monitors = []
        self.app = None
        self.recorder = None
        self.player = None
        self.pipeline = None
            
        try:
            print("\n1. Loading audio components...")
            self.recorder = AudioRecorder()
            self.player = AudioPlayer()
            
            print("\n2. Loading AI pipeline...")
            self.pipeline = ProcessingPipeline()
            
        except Exception as e:
            print(f"\n⚠️  Error during initialization: {e}")
            self.cleanup()
            return None
            
        return self

    def start(self):
        """Start listening for events"""
        print("\nStarting event monitor...")
        
        try:
            self.app = NSApplication.sharedApplication()
            
            # Set up event monitors
            mask = NSEventMaskKeyDown | NSEventMaskKeyUp
            self.monitor = NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(
                mask, self.handle_event)
            self.local_monitor = NSEvent.addLocalMonitorForEventsMatchingMask_handler_(
                mask, self.handle_event)
                
            # Check if monitors were created successfully
            if not self.monitor or not self.local_monitor:
                print("\n⚠️  Error setting up event monitor: Failed to create monitors")
                self.cleanup()
                return False
                
            # Add successful monitors to list
            if self.monitor:
                self.monitors.append(self.monitor)
            if self.local_monitor:
                self.monitors.append(self.local_monitor)
                
            print("\n🎧 Setting up event monitor...")
            
        except Exception as e:
            print(f"\n⚠️  Error setting up event monitor: {e}")
            self.cleanup()
            return False
        
        return True

    def lazy_setup(self):
        """Lazy initialization of components when first needed"""
        if self.setup_complete:
            return True
            
        try:
            print("\n1. Loading audio components...")
            self.recorder = AudioRecorder()
            self.player = AudioPlayer()
            
            print("\n2. Loading AI pipeline...")
            self.pipeline = ProcessingPipeline()
            
            self.setup_complete = True
            return True
            
        except Exception as e:
            print(f"\n⚠️  Error during lazy setup: {e}")
            return False

    def handle_event(self, event):
        if event is None:
            return None
            
        try:
            event_type = event.type()
            key_code = event.keyCode()
            flags = event.modifierFlags()
            
            if __debug__:
                print(f"\nDEBUG: Event received:")
                print(f"  - Type: {event_type}")
                print(f"  - KeyCode: {key_code}")
                print(f"  - Flags: {flags}")
            
            # Handle Command+Shift+A (start/stop recording)
            if key_code == 0 and flags & self.CMD_SHIFT_A_MASK:
                if event_type == NSEventTypeKeyDown:
                    # Only start if not already recording
                    if not self.recording_in_progress:
                        self.start_recording()
                elif event_type == NSEventTypeKeyUp:
                    # Only stop if currently recording
                    if self.recording_in_progress:
                        self.stop_recording()
                    
            # Handle Command+Shift+Q (quit)
            elif key_code == 12 and flags & self.CMD_SHIFT_Q_MASK:
                if event_type == NSEventTypeKeyDown:  # Only trigger on key down
                    self.cleanup()
                
            return event
            
        except Exception as e:
            print(f"Error handling event: {e}")
            return event

    def start_recording(self):
        """Start recording audio"""
        if not self.recorder:
            return
        print("\n🎤 Starting recording...")
        self.recording_in_progress = True
        self.recorder.start()

    def stop_recording(self):
        """Stop recording and process audio"""
        print("⏹️  Stopping recording...")
        if not self.recording_in_progress:
            print("DEBUG: Not recording, nothing to stop")
            return False
        
        try:
            if not self.recorder:
                raise RuntimeError("Recorder not initialized")
            
            audio_data = self.recorder.stop()
            self.recording_in_progress = False
            
            if not audio_data:
                print("DEBUG: No audio data captured")
                return False
            
            if not self.pipeline:
                raise RuntimeError("Pipeline not initialized")
            
            return self.pipeline.process(audio_data)
            
        except Exception as e:
            print(f"Error stopping recording: {e}")
            self.recording_in_progress = False
            return False

    def cleanup(self):
        """Clean up resources and stop monitoring"""
        try:
            # First stop recording if in progress
            if self.recording_in_progress:
                try:
                    self.stop_recording()
                except:
                    pass
                self.recording_in_progress = False
                
            # Clean up monitors
            for monitor in list(self.monitors):
                try:
                    NSEvent.removeMonitor_(monitor)
                    self.monitors.remove(monitor)
                except Exception as e:
                    print(f"Error removing monitor: {e}")
                    
            # Clean up audio resources
            if self.recorder:
                try:
                    self.recorder.stop()
                except:
                    pass
                self.recorder = None
                
            if self.player:
                try:
                    self.player.cleanup()
                except:
                    pass
                self.player = None
                
            # Clean up pipeline
            if self.pipeline:
                try:
                    self.pipeline.cleanup()
                except:
                    pass
                self.pipeline = None
                
        except Exception as e:
            print(f"Error during cleanup: {e}")
        finally:
            self.monitors.clear()
            self.recording_in_progress = False

    def take_screenshot(self):
        """Capture and save screenshot"""
        try:
            screenshot = ImageGrab.grab()
            # Create screenshots directory if it doesn't exist
            os.makedirs('screenshots', exist_ok=True)
            # Save with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            path = f'screenshots/screen_{timestamp}.png'
            screenshot.save(path)
            print(f"Screenshot saved: {path}")
            return path
        except Exception as e:
            print(f"Screenshot error: {e}")
            return None

    def signal_handler(self, signum, frame):
        """Handle Ctrl+C"""
        print("\n\n⚠️  Interrupted by user")
        print("Cleaning up...")
        self.cleanup()
        if self.app:
            self.app.terminate_(None)
        sys.exit(0)

    def stop_recording_session(self):
        """Handle end of recording session"""
        # Get the recorded audio file
        audio_file = self.recorder.stop_recording()
        if not audio_file:
            print("No audio recorded")
            return
        
        # Process the interaction
        response_file = self.pipeline.process_interaction(
            audio_file, 
            self.screenshot_path
        )
        
        # Play the response
        if response_file:
            self.player.play_file(response_file)

if __name__ == "__main__":
    print("\n🎧 Initializing AI Assistant...")
    print("   This may take a few moments while models load\n")
    listener = HotkeyListener()
    listener.start() 