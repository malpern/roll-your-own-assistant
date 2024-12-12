from AppKit import (NSApplication, NSEvent, NSKeyDown, NSKeyUp,
                   NSEventMaskKeyDown, NSEventMaskKeyUp,
                   NSEventModifierFlagCommand, NSEventModifierFlagShift,
                   NSEventModifierFlagControl)
import signal
import sys

def test_real_hotkeys():
    print("\n🎧 Listening for real keypresses...")
    print("\nPlease try:")
    print("1. Press and hold Command+Shift+A")
    print("2. Release Command+Shift+A")
    print("3. Press Command+Shift+Q")
    print("4. Press Ctrl+C to exit")
    print("\nWaiting for input...\n")
    
    app = NSApplication.sharedApplication()
    monitors = []  # Keep track of monitors for cleanup
    
    def signal_handler(sig, frame):
        print("\n\nStopping event monitors...")
        for monitor in monitors:
            NSEvent.removeMonitor_(monitor)
        print("Test completed.")
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    
    def handle_event(event):
        """Print information about received events"""
        flags = event.modifierFlags()
        keycode = event.keyCode()
        event_type = "KeyDown" if event.type() == NSKeyDown else "KeyUp"
        
        print(f"\nEvent detected:")
        print(f"  Type: {event_type}")
        print(f"  KeyCode: {keycode}")
        print(f"  Modifier flags: {flags}")
        
        # Check for our specific combinations
        cmd_shift = (flags & (NSEventModifierFlagCommand | NSEventModifierFlagShift))
        has_modifiers = cmd_shift == (NSEventModifierFlagCommand | NSEventModifierFlagShift)
        
        if has_modifiers and keycode == 0:  # Command+Shift+A
            print("  👉 Command+Shift+A detected!")
        elif has_modifiers and keycode == 12:  # Command+Shift+Q
            print("  👉 Command+Shift+Q detected!")
            
        return event
    
    # Monitor for both key down and up events
    mask = NSEventMaskKeyDown | NSEventMaskKeyUp
    
    # Set up local monitor (works when app is active)
    local_monitor = NSEvent.addLocalMonitorForEventsMatchingMask_handler_(
        mask, handle_event
    )
    monitors.append(local_monitor)
    
    # Set up global monitor (works when app is in background)
    global_monitor = NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(
        mask, handle_event
    )
    monitors.append(global_monitor)
    
    try:
        # Run the application
        app.run()
    except KeyboardInterrupt:
        print("\n\nStopping event monitors...")
        for monitor in monitors:
            NSEvent.removeMonitor_(monitor)
        print("Test completed.")

if __name__ == "__main__":
    test_real_hotkeys() 