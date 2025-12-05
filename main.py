#!/usr/bin/env python3
import sys
import signal
import gi

# Ensure we have the correct versions before importing Gtk/WebKit
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.1')

from app import WhatsAppLiteApp

def main():
    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    try:
        print("Initializing App...")
        app = WhatsAppLiteApp()
        print("Running App...")
        exit_status = app.run(sys.argv)
        print(f"App finished with status: {exit_status}")
        sys.exit(exit_status)
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
