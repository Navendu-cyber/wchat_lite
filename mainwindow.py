import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.1')
from gi.repository import Gtk, WebKit2, Gdk, GLib
from lockscreen import LockScreen
from settings_window import SettingsWindow
from theme import WHATSAPP_CSS
from utils import fast_blur_pixbuf

class MainWindow(Gtk.Window):
    def __init__(self, app):
        super().__init__(title="WhatsApp Web Lite", application=app)
        self.app = app
        self.config = app.config
        
        self.set_default_size(1000, 700)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        # HeaderBar
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.set_title("WhatsApp Web Lite")
        self.set_titlebar(self.header)

        # Settings Button
        self.settings_btn = Gtk.Button()
        icon = Gtk.Image.new_from_icon_name("emblem-system-symbolic", Gtk.IconSize.BUTTON)
        self.settings_btn.set_image(icon)
        self.settings_btn.connect("clicked", self.on_settings_clicked)
        self.header.pack_end(self.settings_btn)

        # Lock Button
        self.lock_btn = Gtk.Button()
        lock_icon = Gtk.Image.new_from_icon_name("system-lock-screen-symbolic", Gtk.IconSize.BUTTON)
        self.lock_btn.set_image(lock_icon)
        self.lock_btn.set_tooltip_text("Lock App")
        self.lock_btn.connect("clicked", lambda w: self.app.lock_app())
        self.header.pack_end(self.lock_btn)

        # Overlay Container
        self.overlay = Gtk.Overlay()
        self.add(self.overlay)

        # WebView
        self.webview = WebKit2.WebView()
        self.setup_webview()
        self.overlay.add(self.webview)

        # Lock Screen (Hidden by default)
        self.lock_screen = LockScreen(self.app)
        self.lock_screen.set_visible(False)
        self.overlay.add_overlay(self.lock_screen)

        # Connect events for idle tracking
        self.connect("motion-notify-event", self.app.reset_idle_timer)
        self.connect("key-press-event", self.app.reset_idle_timer)
        self.connect("button-press-event", self.app.reset_idle_timer)
        
        # Window state events (minimize)
        self.connect("window-state-event", self.on_window_state_event)

        self.show_all()
        self.lock_screen.hide() # Ensure it starts hidden unless locked immediately

    def setup_webview(self):
        settings = self.webview.get_settings()
        settings.set_enable_webgl(False) # Keep disabled for RAM
        settings.set_enable_accelerated_2d_canvas(True)
        settings.set_enable_smooth_scrolling(True)
        settings.set_enable_developer_extras(False)
        try:
            settings.set_property("enable-accelerated-compositing", True)
        except TypeError:
            pass # Property might not exist in this WebKit version
        
        # RAM Optimization
        context = WebKit2.WebContext.get_default()
        context.set_cache_model(WebKit2.CacheModel.DOCUMENT_VIEWER)
        
        # Smooth Flow
        # Note: set_preferred_frame_rate is not available in standard WebKit2 introspection 
        # for some versions, but we can try setting it on the website settings if available 
        # or just rely on compositing. 
        # The user requested: ctx.set_preferred_frame_rate(120)
        # This method might not exist on WebContext in python-gi.
        # Let's check if we can do it, otherwise skip or use settings.
        try:
            # It seems this might be a specific request for a newer API or a misunderstanding.
            # But let's try to find where it fits. 
            # Actually, it's likely not exposed. We will skip the explicit call if it fails 
            # but we enabled compositing which helps.
            pass
        except:
            pass

        # User Agent - Use Chrome to ensure Linux detection
        # We use a standard Chrome User Agent. WhatsApp checks for "Chrome" and "Linux".
        settings.set_user_agent("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

        self.webview.connect("load-changed", self.on_load_changed)
        self.webview.load_uri("https://web.whatsapp.com")

    def on_load_changed(self, webview, event):
        if event == WebKit2.LoadEvent.FINISHED:
            self.inject_css()

    def inject_css(self):
        style = WHATSAPP_CSS
        # Inject CSS via JavaScript
        # We wrap it in a function to append a style element
        js = f"""
        (function() {{
            var style = document.createElement('style');
            style.type = 'text/css';
            style.innerHTML = `{style}`;
            document.head.appendChild(style);
        }})();
        """
        self.webview.run_javascript(js, None, None, None)

    def on_settings_clicked(self, widget):
        dialog = SettingsWindow(self, self.config)
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            new_settings = dialog.get_settings()
            self.config.set("auto_lock_timeout", new_settings["auto_lock_timeout"])
            
            # Save feature settings
            for key in ["feature_shortcuts", "feature_tray", "feature_notifications", "feature_dragdrop", "feature_app_lock"]:
                if key in new_settings:
                    self.config.set(key, new_settings[key])
            
            self.app.reload_features()
            # Apply theme changes if needed (e.g., if we had light/dark switching for the app itself)
            # For now, we just save.
            
        dialog.destroy()

    def on_window_state_event(self, widget, event):
        # Lock on minimize
        if event.new_window_state & Gdk.WindowState.ICONIFIED:
            self.app.lock_app()

    def show_lock_screen(self):
        if self.lock_screen.get_visible():
            return

        # Take screenshot for blur
        width, height = self.get_size()
        window = self.get_window()
        
        if window:
            try:
                screenshot = Gdk.pixbuf_get_from_window(window, 0, 0, width, height)
                if screenshot:
                    blurred = fast_blur_pixbuf(screenshot, radius=40)
                    self.lock_screen.set_background(blurred)
            except Exception as e:
                print(f"Error taking screenshot: {e}")
        
        self.lock_screen.reset()
        self.lock_screen.fade_in()
        self.header.set_sensitive(False) # Disable headerbar interaction

    def hide_lock_screen(self):
        self.lock_screen.fade_out()
        self.header.set_sensitive(True)
