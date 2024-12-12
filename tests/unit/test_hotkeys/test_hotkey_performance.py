import unittest
import time
import cProfile
import pstats
import io
from AppKit import (
    NSApplication,
    NSEvent,
    NSEventTypeKeyDown,
    NSEventTypeKeyUp,
    NSCommandKeyMask,
    NSShiftKeyMask
)
from src.hotkeys import HotkeyListener
from unittest.mock import MagicMock

class TestHotkeyListenerPerformance(unittest.TestCase):
    def setUp(self):
        self.app = NSApplication.sharedApplication()
        self.profiler = cProfile.Profile()
        self.init_times = []
        self.recording_start_times = []
        self.processing_times = []

    def test_initialization_performance(self):
        """Measure initialization performance"""
        print("\n=== Testing Initialization Performance ===")
        
        for i in range(5):
            print(f"\nIteration {i+1}/5")
            start_time = time.perf_counter()
            
            # Profile initialization
            self.profiler.enable()
            listener = HotkeyListener.alloc().init()
            self.profiler.disable()
            
            if listener:
                end_time = time.perf_counter()
                self.init_times.append(end_time - start_time)
                listener.cleanup()
            
        # Print statistics
        if self.init_times:
            avg_time = sum(self.init_times) / len(self.init_times)
            print(f"\nAverage initialization time: {avg_time:.2f} seconds")
            
            # Print profiler statistics
            s = io.StringIO()
            ps = pstats.Stats(self.profiler, stream=s).sort_stats('cumulative')
            ps.print_stats(20)
            print("\nDetailed Profile:")
            print(s.getvalue())

    def test_event_handling_performance(self):
        """Test event handling performance"""
        print("\n=== Testing Event Handling Performance ===")
        
        listener = HotkeyListener.alloc().init()
        if not listener:
            self.skipTest("Listener initialization failed")
            return
        
        try:
            # Create test event
            event = MagicMock(spec=NSEvent)
            event.type.return_value = NSEventTypeKeyDown
            event.keyCode.return_value = 0
            event.modifierFlags.return_value = NSCommandKeyMask | NSShiftKeyMask
            
            # Profile event handling
            self.profiler.enable()
            for _ in range(100):  # Test 100 events
                listener.handle_event(event)
            self.profiler.disable()
            
            # Print profiler statistics
            s = io.StringIO()
            ps = pstats.Stats(self.profiler, stream=s).sort_stats('cumulative')
            ps.print_stats(20)
            print(s.getvalue())
            
        finally:
            if listener:
                listener.cleanup()