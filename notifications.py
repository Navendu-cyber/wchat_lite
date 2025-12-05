import gi
gi.require_version('Gtk', '3.0')

HAS_NOTIFY = False
try:
    gi.require_version('Notify', '0.7')
    from gi.repository import Notify
    HAS_NOTIFY = True
except ValueError:
    print("Warning: libnotify not found. Notifications will be disabled.")

from gi.repository import Gtk, WebKit2
import json

class FeatureNotifications:
    def __init__(self, app):
        self.app = app
        self.is_enabled = False
        self.script_handler_name = "notificationHandler"

    def enable(self):
        if self.is_enabled:
            return

        if not HAS_NOTIFY:
            print("Feature: Notifications cannot be enabled (missing libnotify)")
            return

        try:
            if not Notify.is_initted():
                Notify.init("WhatsApp Web Lite")
        except Exception as e:
            print(f"Failed to init notifications: {e}")
            return

        if self.app.window and self.app.window.webview:
            ucm = self.app.window.webview.get_user_content_manager()
            # Check if already registered to avoid error
            try:
                ucm.register_script_message_handler(self.script_handler_name)
                ucm.connect(f"script-message-received::{self.script_handler_name}", self._on_notification_received)
            except Exception:
                pass # Already registered

            # Inject JS: Pass JSON string
            js = """
            window.Notification = function(title, options) {
                var payload = JSON.stringify({
                    title: title,
                    body: options ? options.body : ""
                });
                window.webkit.messageHandlers.notificationHandler.postMessage(payload);
                return { close: function() {} };
            };
            window.Notification.permission = "granted";
            window.Notification.requestPermission = function(cb) {
                if(cb) cb("granted");
                return Promise.resolve("granted");
            };
            """
            self.app.window.webview.run_javascript(js, None, None, None)

        self.is_enabled = True
        print("Feature: Notifications Enabled")

    def disable(self):
        # Hard to fully disable JS injection without reloading, but we can stop showing notifications
        self.is_enabled = False
        print("Feature: Notifications Disabled")

    def _on_notification_received(self, ucm, js_result):
        if not self.is_enabled or not HAS_NOTIFY:
            return
            
        try:
            # Get the value from the JS result
            val = js_result.get_js_value()
            json_str = val.to_string()
            
            data = json.loads(json_str)
            
            title = data.get("title", "WhatsApp")
            body = data.get("body", "New Message")
            
            self.show_notification(title, body)
            
        except Exception as e:
            print(f"Error handling notification: {e}")

    def show_notification(self, title, body, force=False):
        if (not self.is_enabled and not force) or not HAS_NOTIFY:
            return
            
        try:
            notification = Notify.Notification.new(title, body, "dialog-information")
            notification.show()
        except Exception as e:
            print(f"Error showing notification: {e}")
