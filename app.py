import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from config import ConfigManager
from mainwindow import MainWindow
from theme import apply_gtk_theme
from shortcuts import FeatureShortcuts
from tray_icon import FeatureTrayIcon
from notifications import FeatureNotifications
from dragdrop import FeatureDragDrop
from background_sync import BackgroundSync
import time

class WhatsAppLiteApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.whatsapp.lite", flags=0)
        self.config = ConfigManager()
        self.window = None
        self.last_activity_time = time.time()
        self.is_locked = False
        self.idle_timer_id = None
        
        self.features = {
            "shortcuts": FeatureShortcuts(self),
            "tray": FeatureTrayIcon(self),
            "notifications": FeatureNotifications(self),
            "dragdrop": FeatureDragDrop(self),
            "sync": BackgroundSync(self),
        }

    def do_activate(self):
        print("App Activated")
        if not self.window:
            apply_gtk_theme()
            self.window = MainWindow(self)
            self.window.connect("destroy", self.quit)
            self.window.show_all()
            
            # Load Features
            self.load_features()
            
            # Start Idle Timer
            self.idle_timer_id = GLib.timeout_add_seconds(1, self.check_idle)
            
            # Check if we need to lock on startup (optional, but good security)
            # If password exists, lock.
            if self.config.get("password_hash"):
                self.lock_app()
            else:
                # If no password, we might want to prompt setup, 
                # but LockScreen handles setup mode when shown.
                # Let's show lock screen to force setup.
                self.lock_app()

        self.window.present()

    def reset_idle_timer(self, *args):
        self.last_activity_time = time.time()

    def check_idle(self):
        if self.is_locked:
            return True # Keep running timer

        timeout = self.config.get("auto_lock_timeout")
        if time.time() - self.last_activity_time > timeout:
            self.lock_app()
        
        return True # Continue calling

    def lock_app(self):
        if self.is_locked:
            return
            
        if not self.config.get("feature_app_lock"):
            return
        
        self.is_locked = True
        if self.window:
            self.window.show_lock_screen()

    def unlock_app(self):
        self.is_locked = False
        self.last_activity_time = time.time()
        if self.window:
            self.window.hide_lock_screen()

    def load_features(self):
        for key, feature in self.features.items():
            if self.config.get(f"feature_{key}"):
                feature.enable()
            else:
                feature.disable()

    def reload_features(self):
        self.load_features()

    def quit(self, *args):
        super().quit()
