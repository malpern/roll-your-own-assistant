import unittest
from unittest.mock import patch, MagicMock
from hotkeys import HotkeyListener


class TestHotkeyListenerErrors(unittest.TestCase):
    def test_init_audio_failure(self):
        """Test handling of audio initialization failure"""
        with patch('hotkeys.AudioRecorder') as mock_recorder_cls:
            # Make the constructor raise an exception
            mock_recorder_cls.side_effect = Exception("Audio init failed")
            
            # Initialize listener
            listener = HotkeyListener.alloc().init()
            self.assertIsNone(
                listener,
                "Listener should be None when audio init fails"
            )

    def test_init_pipeline_failure(self):
        """Test handling of pipeline initialization failure"""
        with patch('hotkeys.ProcessingPipeline') as mock_pipeline_cls:
            # Make the constructor raise an exception
            mock_pipeline_cls.side_effect = Exception("Pipeline init failed")
            
            # Initialize listener
            listener = HotkeyListener.alloc().init()
            self.assertIsNone(
                listener,
                "Listener should be None when pipeline init fails"
            )

    def test_monitor_setup_failure(self):
        """Test handling of monitor setup failure"""
        # Create a listener with mocked components
        with patch('hotkeys.AudioRecorder') as mock_recorder_cls, \
             patch('hotkeys.ProcessingPipeline') as mock_pipeline_cls:
            
            # Create mock instances
            mock_recorder = MagicMock()
            mock_pipeline = MagicMock()
            mock_recorder_cls.return_value = mock_recorder
            mock_pipeline_cls.return_value = mock_pipeline
            
            # Initialize listener
            listener = HotkeyListener.alloc().init()
            if not listener:
                self.skipTest("Listener initialization failed")
                return
            
            try:
                # Create a mock NSEvent class
                mock_event = MagicMock()
                mock_event.addGlobalMonitorForEventsMatchingMask_handler_ = \
                    MagicMock(return_value=None)
                mock_event.addLocalMonitorForEventsMatchingMask_handler_ = \
                    MagicMock(return_value=None)
                
                # Patch NSEvent with our mock
                with patch('hotkeys.NSEvent', mock_event):
                    # Try to start the listener
                    success = listener.start()
                    
                    # Verify failure handling
                    self.assertFalse(success)
                    self.assertEqual(len(listener.monitors), 0)
                
            finally:
                # Clean up
                if listener:
                    listener.cleanup()


if __name__ == '__main__':
    unittest.main() 