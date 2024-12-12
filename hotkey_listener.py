import objc
from AppKit import (NSObject, NSEvent, NSApplication, NSKeyDown, NSKeyUp,
                   NSEventMaskKeyDown, NSEventMaskKeyUp,
                   NSCommandKeyMask, NSShiftKeyMask, NSAlternateKeyMask, NSControlKeyMask)
from hotkey_manager import HotkeyManager

# Key code to name mapping
KEY_MAP = {
    0: 'a',
    1: 's',
    2: 'd',
    # ... add more keys as needed
}

# Modifier masks and their string representations
MODIFIER_MAP = {
    NSCommandKeyMask: 'cmd',
    NSShiftKeyMask: 'shift',
    NSAlternateKeyMask: 'alt',
    NSControlKeyMask: 'ctrl'
}

class HotkeyListener(NSObject):
    def __new__(cls):
        return cls.alloc().init()
        
    def __init__(self):
        objc.super(HotkeyListener, self).__init__()
        self.hotkey_manager = HotkeyManager()
        self.monitor = None
        
    def start(self):
        """Start listening for keyboard events"""
        # Set up application
        app = NSApplication.sharedApplication()
        
        # Create monitor for key events
        self.monitor = NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(
            NSEventMaskKeyDown | NSEventMaskKeyUp,
            self.handleEvent_
        )
        
        if not self.monitor:
            print("Failed to create event monitor")
            return False
            
        return True
        
    def stop(self):
        """Stop listening for keyboard events"""
        if self.monitor:
            NSEvent.removeMonitor_(self.monitor)
            self.monitor = None

    def get_hotkey_string(self, event):
        """Convert NSEvent to hotkey string (e.g., 'cmd+shift+a')"""
        modifiers = event.modifierFlags()
        keycode = event.keyCode()
        
        # Get key name
        key_name = KEY_MAP.get(keycode, f'key_{keycode}')
        
        # Get modifier names
        modifier_list = []
        for mask, name in MODIFIER_MAP.items():
            if modifiers & mask:
                modifier_list.append(name)
                
        # Combine modifiers and key
        if modifier_list:
            return '+'.join(modifier_list + [key_name])
        return key_name

    def handleEvent_(self, event):
        """Handle keyboard events"""
        if event.type() == NSKeyDown:
            hotkey = self.get_hotkey_string(event)
            
            if self.hotkey_manager.is_registered(hotkey):
                self.hotkey_manager.trigger_hotkey(hotkey) 