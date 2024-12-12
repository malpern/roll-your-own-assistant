import unittest
from unittest.mock import patch, MagicMock
from AppKit import (
    NSEvent, 
    NSEventTypeKeyDown, 
    NSEventTypeKeyUp,
    NSCommandKeyMask,
    NSShiftKeyMask
)
from src.hotkeys import HotkeyListener
import time

class TestHotkeyListenerEvents(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method"""
        # Create the mock first
        self.mock_process = unittest.mock.Mock()
        
        # Initialize the listener with the mock
        self.listener = HotkeyListener()
        self.listener.pipeline.process = self.mock_process  # Replace the real process method with our mock
        
    def tearDown(self):
        """Clean up test fixtures after each test method"""
        if hasattr(self, 'listener'):
            self.listener.cleanup()
            # Add small delay to allow resources to be released
            time.sleep(0.1)
        super().tearDown()

    def create_mock_event(self, event_type, key_code, flags):
        """Helper to create mock events"""
        mock_event = MagicMock()
        mock_event.type.return_value = event_type
        mock_event.keyCode.return_value = key_code
        mock_event.modifierFlags.return_value = flags
        return mock_event

    def test_cmd_shift_a_down(self):
        """Test Command+Shift+A keydown event"""
        # Create mock event for Cmd+Shift+A down
        event = self.create_mock_event(
            NSEventTypeKeyDown,
            0,  # 'A' key code
            NSCommandKeyMask | NSShiftKeyMask
        )
        
        # Verify not recording initially
        self.assertFalse(self.listener.recording_in_progress)
        
        # Handle event
        self.listener.handle_event(event)
        
        # Verify recording started
        self.assertTrue(self.listener.recording_in_progress)

    def test_cmd_shift_a_up(self):
        """Test Command+Shift+A keyup event"""
        # First simulate key down to start recording
        down_event = self.create_mock_event(
            NSEventTypeKeyDown,
            0,  # 'A' key
            NSCommandKeyMask | NSShiftKeyMask
        )
        
        self.listener.handle_event(down_event)
        
        # Verify recording started
        self.assertTrue(self.listener.recording_in_progress)
        
        # Mock some audio data
        self.listener.recorder.has_data = True
        # Mock the recorder's stop method to return audio data
        self.listener.recorder.stop = MagicMock(return_value=b'some audio data')
        # Add this line to ensure the recorder returns some data
        self.listener.recorder.get_audio_data = MagicMock(return_value=b'some audio data')
        
        # Now simulate key up
        up_event = self.create_mock_event(
            NSEventTypeKeyUp,
            0,  # 'A' key
            NSCommandKeyMask | NSShiftKeyMask
        )
        
        self.listener.handle_event(up_event)
        
        # Verify that process was called once
        self.mock_process.assert_called_once()

    def test_cmd_shift_q(self):
        """Test Command+Shift+Q quit event"""
        # Create mock event for Cmd+Shift+Q
        event = self.create_mock_event(
            NSEventTypeKeyDown,
            12,  # 'Q' key code
            NSCommandKeyMask | NSShiftKeyMask
        )
        
        # Mock app.terminate_
        self.listener.app = MagicMock()
        
        # Handle event 