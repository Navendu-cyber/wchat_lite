import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class FeatureShortcuts:
    def __init__(self, app):
        self.app = app
        self.accel_group = Gtk.AccelGroup()
        self.is_enabled = False

    def enable(self):
        if self.is_enabled:
            return
        
        # Register Ctrl+L to Lock
        key, mod = Gtk.accelerator_parse("<Control>l")
        self.accel_group.connect(key, mod, Gtk.AccelFlags.VISIBLE, self._on_lock_shortcut)
        
        if self.app.window:
            self.app.window.add_accel_group(self.accel_group)
        
        self.is_enabled = True
        print("Feature: Shortcuts Enabled")

    def disable(self):
        if not self.is_enabled:
            return
            
        if self.app.window:
            self.app.window.remove_accel_group(self.accel_group)
        
        self.is_enabled = False
        print("Feature: Shortcuts Disabled")

    def _on_lock_shortcut(self, accel_group, acceleratable, keyval, modifier):
        self.app.lock_app()
        return True
