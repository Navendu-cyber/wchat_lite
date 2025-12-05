import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class FeatureTrayIcon:
    def __init__(self, app):
        self.app = app
        self.tray_icon = None
        self.is_enabled = False

    def enable(self):
        if self.is_enabled:
            return

        self.tray_icon = Gtk.StatusIcon()
        self.tray_icon.set_from_icon_name("user-available-symbolic") # Generic icon, ideally use app icon
        self.tray_icon.set_tooltip_text("WhatsApp Web Lite")
        self.tray_icon.connect("popup-menu", self._on_right_click)
        self.tray_icon.connect("activate", self._on_left_click)
        self.tray_icon.set_visible(True)
        
        self.is_enabled = True
        print("Feature: Tray Icon Enabled")

    def disable(self):
        if not self.is_enabled:
            return
        
        if self.tray_icon:
            self.tray_icon.set_visible(False)
            self.tray_icon = None
            
        self.is_enabled = False
        print("Feature: Tray Icon Disabled")

    def _on_left_click(self, icon):
        if self.app.window:
            if self.app.window.is_active():
                self.app.window.iconify()
            else:
                self.app.window.present()

    def _on_right_click(self, icon, button, time):
        menu = Gtk.Menu()

        show_item = Gtk.MenuItem(label="Show/Hide")
        show_item.connect("activate", self._on_left_click)
        menu.append(show_item)

        lock_item = Gtk.MenuItem(label="Lock")
        lock_item.connect("activate", lambda w: self.app.lock_app())
        menu.append(lock_item)

        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", lambda w: self.app.quit())
        menu.append(quit_item)

        menu.show_all()
        menu.popup(None, None, Gtk.StatusIcon.position_menu, icon, button, time)
