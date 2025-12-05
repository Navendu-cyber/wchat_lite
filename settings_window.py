import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from config import ConfigManager
from utils import hash_password, verify_password

class PasswordChangeDialog(Gtk.Dialog):
    def __init__(self, parent, config_manager):
        super().__init__(title="Change Password", transient_for=parent, flags=0)
        self.config_manager = config_manager
        self.set_default_size(300, 250)
        self.set_modal(True)
        self.set_border_width(20)
        
        box = self.get_content_area()
        box.set_spacing(16)

        # Current Password
        self.current_entry = Gtk.Entry()
        self.current_entry.set_visibility(False)
        self.current_entry.set_placeholder_text("Current Password")
        box.add(self.current_entry)

        # New Password
        self.new_entry = Gtk.Entry()
        self.new_entry.set_visibility(False)
        self.new_entry.set_placeholder_text("New Password")
        box.add(self.new_entry)

        # Confirm New Password
        self.confirm_entry = Gtk.Entry()
        self.confirm_entry.set_visibility(False)
        self.confirm_entry.set_placeholder_text("Confirm New Password")
        box.add(self.confirm_entry)

        # Error Label
        self.error_label = Gtk.Label()
        self.error_label.get_style_context().add_class("lock-error") # Reuse error style
        box.add(self.error_label)

        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("Change", Gtk.ResponseType.OK)
        
        self.show_all()

    def do_change(self):
        current = self.current_entry.get_text()
        new_pass = self.new_entry.get_text()
        confirm = self.confirm_entry.get_text()

        stored_hash = self.config_manager.get("password_hash")
        
        if not verify_password(current, stored_hash):
            self.error_label.set_text("Incorrect current password")
            return False
        
        if not new_pass:
            self.error_label.set_text("New password cannot be empty")
            return False

        if new_pass != confirm:
            self.error_label.set_text("New passwords do not match")
            return False
            
        # Save new hash
        self.config_manager.set("password_hash", hash_password(new_pass))
        return True

class SettingsWindow(Gtk.Dialog):
    def __init__(self, parent, config_manager):
        super().__init__(title="Settings", transient_for=parent, flags=0)
        self.config_manager = config_manager
        self.set_default_size(400, 350)
        self.set_modal(True)
        self.set_border_width(20)

        content_area = self.get_content_area()
        
        # Main Container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        content_area.add(main_box)

        # --- General Section ---
        general_label = Gtk.Label()
        general_label.set_markup("<b>General</b>")
        general_label.set_halign(Gtk.Align.START)
        main_box.pack_start(general_label, False, False, 0)

        # Auto-Lock Timeout
        timeout_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        timeout_label = Gtk.Label(label="Auto-lock timeout (seconds)")
        self.timeout_spin = Gtk.SpinButton.new_with_range(30, 3600, 30)
        self.timeout_spin.set_value(self.config_manager.get("auto_lock_timeout"))
        
        timeout_box.pack_start(timeout_label, False, False, 0)
        timeout_box.pack_end(self.timeout_spin, False, False, 0)
        main_box.pack_start(timeout_box, False, False, 0)

        # Change Password Button
        change_pass_btn = Gtk.Button(label="Change Password...")
        change_pass_btn.connect("clicked", self.on_change_password_clicked)
        change_pass_btn.set_halign(Gtk.Align.END)
        main_box.pack_start(change_pass_btn, False, False, 0)

        # --- Features Section ---
        features_label = Gtk.Label()
        features_label.set_markup("<b>Features</b>")
        features_label.set_halign(Gtk.Align.START)
        main_box.pack_start(features_label, False, False, 0)

        # Feature Toggles
        self.feature_switches = {}
        features = [
            ("feature_app_lock", "Enable App Lock"),
            ("feature_notifications", "Desktop Notifications"),
            ("feature_shortcuts", "Quick Lock (Ctrl+L)"),
            ("feature_tray", "Tray Icon"),
            ("feature_dragdrop", "Drag & Drop Sending")
        ]
        
        for key, label_text in features:
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            label = Gtk.Label(label=label_text)
            switch = Gtk.Switch()
            switch.set_active(self.config_manager.get(key) or False)
            
            hbox.pack_start(label, False, False, 0)
            hbox.pack_end(switch, False, False, 0)
            main_box.pack_start(hbox, False, False, 0)
            self.feature_switches[key] = switch

        # Buttons Area
        # Standard Dialog action area is usually at the bottom, but we can use our own if we want.
        # But Gtk.Dialog handles it. Let's just add buttons.
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("Save", Gtk.ResponseType.OK)
        
        self.show_all()

    def on_change_password_clicked(self, widget):
        dialog = PasswordChangeDialog(self, self.config_manager)
        while True:
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                if dialog.do_change():
                    dialog.destroy()
                    break
            else:
                dialog.destroy()
                break

    def get_settings(self):
        """Returns the new settings from the UI."""
        settings = {
            "auto_lock_timeout": int(self.timeout_spin.get_value())
        }
        
        for key, switch in self.feature_switches.items():
            settings[key] = switch.get_active()
            
        return settings
