import unittest
from unittest.mock import patch, MagicMock, create_autospec
from AppKit import (
    NSEvent,
    NSEventTypeKeyDown,
    NSEventTypeKeyUp,
    NSCommandKeyMask,
    NSShiftKeyMask
)
from hotkeys import HotkeyListener
from audio_recorder import AudioRecorder


class TestHotkeyListenerCore(unittest.TestCase):
    def setUp(self):
        # Create mocks
        self.mock_recorder = create_autospec(AudioRecorder)
        self.mock_recorder.start = MagicMock(return_value=True)
        self.mock_recorder.stop = MagicMock(return_value=True)
        
        self.mock_pipeline = MagicMock()
        self.mock_pipeline.process = MagicMock(return_value=True)
        
        # Create patches
        self.recorder_patcher = patch('hotkeys.AudioRecorder', return_value=self.mock_recorder)
        self.pipeline_patcher = patch('hotkeys.ProcessingPipeline', return_value=self.mock_pipeline)
        
        # Start patches
        self.mock_recorder_cls = self.recorder_patcher.start()
        self.mock_pipeline_cls = self.pipeline_patcher.start()
        
        # Initialize listener
        self.listener = HotkeyListener.alloc().init()
        if not self.listener:
            self.skipTest("Listener initialization failed")
            
    def tearDown(self):
        # Stop patches
        self.recorder_patcher.stop()
        self.pipeline_patcher.stop()
        
        if hasattr(self, 'listener') and self.listener:
            self.listener.cleanup()
            
    def test_state_transitions(self):
        """Test recording state transitions"""
        # Initial state
        self.assertFalse(self.listener.recording_in_progress)
        
        # Start recording
        event = self.create_mock_event(
            NSEventTypeKeyDown, 0, NSCommandKeyMask | NSShiftKeyMask
        )
        self.listener.handle_event(event)
        self.assertTrue(self.listener.recording_in_progress)
        self.mock_recorder.start.assert_called_once()
        
        # Stop recording
        event = self.create_mock_event(
            NSEventTypeKeyUp, 0, NSCommandKeyMask | NSShiftKeyMask
        )
        self.listener.handle_event(event)
        self.assertFalse(self.listener.recording_in_progress)
        self.mock_recorder.stop.assert_called_once()
        
    def test_concurrent_events(self):
        """Test handling of concurrent events"""
        # Start recording
        self.listener.handle_event(
            self.create_mock_event(
                NSEventTypeKeyDown, 0, NSCommandKeyMask | NSShiftKeyMask
            )
        )
        
        # Try to start recording again while already recording
        self.listener.handle_event(
            self.create_mock_event(
                NSEventTypeKeyDown, 0, NSCommandKeyMask | NSShiftKeyMask
            )
        )
        
        # Verify still in recording state
        self.assertTrue(self.listener.recording_in_progress)
        # Verify start was only called once
        self.assertEqual(self.mock_recorder.start.call_count, 1)
        
        # Stop recording
        self.listener.handle_event(
            self.create_mock_event(
                NSEventTypeKeyUp, 0, NSCommandKeyMask | NSShiftKeyMask
            )
        )
        
    def test_quit_handling(self):
        """Test quit event handling"""
        with patch.object(self.listener, 'cleanup') as mock_cleanup:
            event = self.create_mock_event(
                NSEventTypeKeyDown, 12, NSCommandKeyMask | NSShiftKeyMask
            )
            self.listener.handle_event(event)
            mock_cleanup.assert_called_once()
            
    def test_invalid_events(self):
        """Test handling of invalid events"""
        # Test None event
        result = self.listener.handle_event(None)
        self.assertIsNone(result)
        
        # Test event with invalid type
        event = self.create_mock_event(999, 0, 0)
        result = self.listener.handle_event(event)
        self.assertEqual(result, event)
        
    @staticmethod
    def create_mock_event(event_type, key_code, flags):
        """Create a mock NSEvent for testing."""
        event = MagicMock(spec=NSEvent)
        event.type.return_value = event_type
        event.keyCode.return_value = key_code
        event.modifierFlags.return_value = flags
        return event
        