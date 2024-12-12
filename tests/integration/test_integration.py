import unittest
from src.hotkeys.listener import CustomHotkeyListener
import time

class TestHotkeyIntegration(unittest.TestCase):
    def setUp(self):
        self.listener = CustomHotkeyListener()
        
    def test_basic_listener_setup(self):
        success = self.listener.start()
        self.assertTrue(success)
        
        # Register multiple test hotkeys
        self.triggered_keys = set()
        
        def make_callback(key):
            def callback():
                self.triggered_keys.add(key)
            return callback
            
        test_hotkeys = ['a', 'cmd+a', 'cmd+shift+a']
        for hotkey in test_hotkeys:
            self.listener.hotkey_manager.register_hotkey(
                hotkey, 
                f'test_action_{hotkey}', 
                make_callback(hotkey)
            )
        
        print("\nTest the following within 10 seconds:")
        print("1. Press 'A' key")
        print("2. Press Cmd+A")
        print("3. Press Cmd+Shift+A")
        time.sleep(10)
        
        self.listener.stop()
        print(f"\nTriggered hotkeys: {self.triggered_keys}")
        
    def tearDown(self):
        self.listener.stop()

if __name__ == '__main__':
    unittest.main() 