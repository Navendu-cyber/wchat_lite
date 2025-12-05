import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GLib
from utils import hash_password, verify_password

class LockScreen(Gtk.EventBox):
    def __init__(self, app_controller):
        super().__init__()
        self.app = app_controller
        self.config = app_controller.config
        
        # Container for the background and the login box
        self.overlay = Gtk.Overlay()
        self.add(self.overlay)

        # Background Image (Blurred)
        self.bg_image = Gtk.Image()
        self.overlay.add(self.bg_image)

        # Center Box for Login UI
        self.center_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.center_box.set_valign(Gtk.Align.CENTER)
        self.center_box.set_halign(Gtk.Align.CENTER)
        
        # Login Card (The visible box)
        self.card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.card.get_style_context().add_class("card")
        self.card.get_style_context().add_class("lock-card")
        # Add some padding/margin to the card via CSS or widget props if needed
        # For now, we rely on the theme.py styling for internal widgets
        
        # Title
        self.title_label = Gtk.Label(label="WhatsApp Web Lite")
        self.title_label.get_style_context().add_class("lock-title")
        self.card.pack_start(self.title_label, False, False, 0)

        # Subtitle
        self.subtitle_label = Gtk.Label(label="Locked")
        self.subtitle_label.get_style_context().add_class("lock-subtitle")
        self.card.pack_start(self.subtitle_label, False, False, 0)

        # Password Entry
        self.password_entry = Gtk.Entry()
        self.password_entry.set_visibility(False)
        self.password_entry.set_placeholder_text("Enter Password")
        self.password_entry.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, "view-reveal-symbolic")
        self.password_entry.set_icon_tooltip_text(Gtk.EntryIconPosition.SECONDARY, "Show/Hide Password")
        self.password_entry.connect("icon-press", self.on_password_icon_press)
        self.password_entry.connect("activate", self.on_unlock_clicked)
        self.card.pack_start(self.password_entry, False, False, 0)

        # Confirm Password Entry (Only for setup)
        self.confirm_entry = Gtk.Entry()
        self.confirm_entry.set_visibility(False)
        self.confirm_entry.set_placeholder_text("Confirm Password")
        self.confirm_entry.connect("activate", self.on_unlock_clicked)
        
        # Unlock/Set Button
        self.action_button = Gtk.Button(label="Unlock")
        self.action_button.get_style_context().add_class("unlock-button")
        self.action_button.connect("clicked", self.on_unlock_clicked)
        self.card.pack_start(self.action_button, False, False, 0)

        # Error Label
        self.error_label = Gtk.Label()
        self.error_label.get_style_context().add_class("lock-error")
        self.card.pack_start(self.error_label, False, False, 0)

        self.center_box.pack_start(self.card, True, True, 20)
        self.overlay.add_overlay(self.center_box)

        self.setup_mode = False
        self.check_setup_mode()

    def set_background(self, pixbuf):
        if pixbuf:
            self.bg_image.set_from_pixbuf(pixbuf)
        else:
            self.bg_image.clear()

    def check_setup_mode(self):
        stored_hash = self.config.get("password_hash")
        if not stored_hash:
            self.setup_mode = True
            self.subtitle_label.set_text("Create a Password")
            self.action_button.set_label("Set Password")
            self.card.pack_start(self.confirm_entry, False, False, 0)
            self.card.reorder_child(self.confirm_entry, 3) # Place after password_entry
            self.confirm_entry.show()
        else:
            self.setup_mode = False
            self.subtitle_label.set_text("Locked")
            self.action_button.set_label("Unlock")
            self.confirm_entry.hide()

    def on_password_icon_press(self, entry, icon_pos, event):
        if icon_pos == Gtk.EntryIconPosition.SECONDARY:
            current_vis = entry.get_visibility()
            entry.set_visibility(not current_vis)
            
            # Update icon
            icon_name = "view-reveal-symbolic" if not current_vis else "view-remove-symbolic" # Logic inverted because we just flipped it? No, wait.
            # If it WAS visible (True), we set it to False (hidden). Icon should be 'reveal' (eye).
            # If it WAS hidden (False), we set it to True (visible). Icon should be 'remove' (crossed eye) or just stay 'reveal' but usually it changes.
            # Let's stick to simple toggle.
            # Actually standard is:
            # Visible -> Icon: view-remove (hide)
            # Hidden -> Icon: view-reveal (show)
            
            new_icon = "view-remove-symbolic" if not current_vis else "view-reveal-symbolic"
            entry.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, new_icon)

    def on_unlock_clicked(self, widget):
        password = self.password_entry.get_text()
        self.error_label.set_text("")

        if self.setup_mode:
            confirm = self.confirm_entry.get_text()
            if not password:
                self.error_label.set_text("Password cannot be empty")
                return
            if password != confirm:
                self.error_label.set_text("Passwords do not match")
                return
            
            # Save new password
            new_hash = hash_password(password)
            self.config.set("password_hash", new_hash)
            self.check_setup_mode() # Switch to normal mode (or just unlock)
            self.app.unlock_app()
            
        else:
            stored_hash = self.config.get("password_hash")
            if verify_password(password, stored_hash):
                self.password_entry.set_text("")
                self.app.unlock_app()
            else:
                self.error_label.set_text("Incorrect Password")
                self.password_entry.set_text("")

    def reset(self):
        """Resets the UI state when re-locking."""
        self.password_entry.set_text("")
        self.error_label.set_text("")
        self.check_setup_mode()

    def fade_in(self):
        self.set_opacity(0.0)
        self.show()
        # Smoother animation: 5ms interval, 0.05 step
        GLib.timeout_add(5, self._animate_fade, 0.05)

    def fade_out(self):
        GLib.timeout_add(5, self._animate_fade, -0.05)

    def _animate_fade(self, step):
        current = self.get_opacity()
        new_opacity = current + step
        
        if new_opacity >= 1.0:
            self.set_opacity(1.0)
            return False # Stop animation
        elif new_opacity <= 0.0:
            self.set_opacity(0.0)
            self.hide()
            return False # Stop animation
        
        self.set_opacity(new_opacity)
        return True # Continue animation
