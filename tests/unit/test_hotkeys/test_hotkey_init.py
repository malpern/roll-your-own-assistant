import unittest
from AppKit import NSObject, NSApplication
from src.hotkeys import HotkeyListener
import time
from unittest.mock import patch, MagicMock, create_autospec
from src.audio import AudioRecorder
import pyaudio  # This will use our mock

class TestHotkeyListenerInit(unittest.TestCase):
    def setUp(self):
        self.app = NSApplication.sharedApplication()
        
        # Create mocks
        self.mock_recorder = create_autospec(AudioRecorder)
        self.mock_recorder.stream = MagicMock()
        self.mock_recorder.start = MagicMock(return_value=True)
        self.mock_recorder.stop = MagicMock(return_value=True)
        
        self.mock_pipeline = MagicMock()
        self.mock_pipeline.process = MagicMock(return_value=True)
        
        # Create patches
        self.recorder_patcher = patch('src.hotkeys.listener.AudioRecorder', return_value=self.mock_recorder)
        self.pipeline_patcher = patch('src.hotkeys.listener.ProcessingPipeline', return_value=self.mock_pipeline)
        
        # Start patches
        self.mock_recorder_cls = self.recorder_patcher.start()
        self.mock_pipeline_cls = self.pipeline_patcher.start()

    def tearDown(self):
        # Stop patches
        self.recorder_patcher.stop()
        self.pipeline_patcher.stop()

    def test_basic_initialization(self):
        """Test basic initialization"""
        listener = HotkeyListener.alloc().init()
        self.assertIsNotNone(listener)
        self.assertFalse(listener.recording_in_progress)

    def test_attributes_initialized(self):
        """Test that all attributes are properly initialized"""
        listener = HotkeyListener.alloc().init()
        
        # Check all attributes exist and have correct initial values
        self.assertFalse(listener.recording_in_progress)
        self.assertIsNone(listener.monitor)
        self.assertIsNone(listener.local_monitor)
        self.assertEqual(listener.monitors, [])
        self.assertIsNone(listener.app)
        self.assertIsNotNone(listener.recorder)  # Should be initialized
        self.assertIsNotNone(listener.player)    # Should be initialized
        self.assertIsNotNone(listener.pipeline)  # Should be initialized

    def test_start_monitor_setup(self):
        """Test that monitors are properly set up"""
        listener = HotkeyListener.alloc().init()
        success = listener.start()
        
        self.assertTrue(success)
        self.assertIsNotNone(listener.monitor)
        self.assertIsNotNone(listener.local_monitor)
        self.assertEqual(len(listener.monitors), 2)
        
        # Cleanup
        listener.cleanup()

    def test_cleanup(self):
        """Test that cleanup works properly"""
        listener = HotkeyListener.alloc().init()
        if not listener:
            self.skipTest("Listener initialization failed")
            return
        
        try:
            listener.start()
            
            # Force cleanup
            listener.cleanup()
            
            # Add small delay to allow cleanup
            time.sleep(0.2)
            
            # Verify cleanup
            self.assertEqual(len(listener.monitors), 0)
            self.assertIsNone(listener.recorder)  # Recorder should be None after cleanup
            
            # Verify mock was called
            self.mock_recorder.stop.assert_called()
            
        except Exception as e:
            self.fail(f"Cleanup test failed: {e}")
        finally:
            # Ensure cleanup runs even if test fails
            if listener:
                listener.cleanup()

if __name__ == '__main__':
    unittest.main() 