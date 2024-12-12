class HotkeyManager:
    def __init__(self):
        self.hotkeys = {}
        self.callbacks = {}
        
    def register_hotkey(self, hotkey: str, action: str, callback=None):
        """Register a hotkey with an associated action and optional callback"""
        self.hotkeys[hotkey] = action
        if callback:
            self.callbacks[hotkey] = callback
        
    def unregister_hotkey(self, hotkey: str):
        """Remove a registered hotkey"""
        self.hotkeys.pop(hotkey, None)
        self.callbacks.pop(hotkey, None)
        
    def trigger_hotkey(self, hotkey: str):
        """Trigger the action associated with a hotkey"""
        if hotkey in self.callbacks:
            return self.callbacks[hotkey]()
        return None
        
    def is_registered(self, hotkey: str) -> bool:
        """Check if a hotkey is registered"""
        return hotkey in self.hotkeys
        
    def get_action(self, hotkey: str) -> str:
        """Get the action associated with a hotkey"""
        return self.hotkeys.get(hotkey) 