import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

HAS_INDICATOR = False
try:
    gi.require_version('AppIndicator3', '0.1')
    from gi.repository import AppIndicator3
    HAS_INDICATOR = True
except ValueError:
    pass

class FeatureTrayIcon:
    def __init__(self, app):
        self.app = app
        self.indicator = None
        self.status_icon = None
        self.is_enabled = False

    def enable(self):
        if self.is_enabled:
            return

        if HAS_INDICATOR:
            self.indicator = AppIndicator3.Indicator.new(
                "com.whatsapp.lite",
                "user-available-symbolic",
                AppIndicator3.IndicatorCategory.APPLICATION_STATUS
            )
            self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
            self.indicator.set_menu(self._build_menu())
        else:
            self.status_icon = Gtk.StatusIcon()
            self.status_icon.set_from_icon_name("user-available-symbolic")
            self.status_icon.set_tooltip_text("WhatsApp Web Lite")
            self.status_icon.connect("popup-menu", self._on_right_click)
            self.status_icon.connect("activate", self._on_left_click)
            self.status_icon.set_visible(True)
        
        self.is_enabled = True
        print("Feature: Tray Icon Enabled")

    def disable(self):
        if not self.is_enabled:
            return
        
        if self.indicator:
            self.indicator.set_status(AppIndicator3.IndicatorStatus.PASSIVE)
            self.indicator = None
            
        if self.status_icon:
            self.status_icon.set_visible(False)
            self.status_icon = None
            
        self.is_enabled = False
        print("Feature: Tray Icon Disabled")

    def _build_menu(self):
        menu = Gtk.Menu()

        show_item = Gtk.MenuItem(label="Show WChat Lite")
        show_item.connect("activate", self._on_show)
        menu.append(show_item)

        lock_item = Gtk.MenuItem(label="Lock App")
        lock_item.connect("activate", lambda w: self.app.lock_app())
        menu.append(lock_item)
        
        menu.append(Gtk.SeparatorMenuItem())

        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", lambda w: self.app.quit())
        menu.append(quit_item)

        menu.show_all()
        return menu

    def _on_show(self, widget):
        if self.app.window:
            self.app.window.present()
            self.app.window.deiconify()

    def _on_left_click(self, icon):
        self._on_show(None)

    def _on_right_click(self, icon, button, time):
        menu = self._build_menu()
        menu.popup(None, None, Gtk.StatusIcon.position_menu, icon, button, time)
