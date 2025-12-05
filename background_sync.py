import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib
import json

class BackgroundSync:
    def __init__(self, app):
        self.app = app
        self.is_enabled = False
        self.timer_id = None
        self.last_unread_count = 0
        
        # JS to check for unread badges
        # We look for elements with 'aria-label' containing "unread message" or specific badge classes
        # WhatsApp Web classes change, but aria-labels are usually more stable.
        # A common badge selector is span[aria-label*="unread message"]
        self.check_script = """
        (function() {
            try {
                // Selector for unread badges in chat list
                // This targets the green badges
                var badges = document.querySelectorAll('span[aria-label*="unread message"]');
                var count = 0;
                var lastMessage = "";
                var sender = "";
                
                badges.forEach(function(badge) {
                    var val = parseInt(badge.innerText);
                    if (!isNaN(val)) {
                        count += val;
                        
                        // Try to get the chat row for this badge to find sender/message
                        // badge -> div -> div -> div -> row (roughly)
                        // This is fragile, so we'll just get the count for now to be safe
                        // and maybe the title of the chat if possible.
                        
                        var chatRow = badge.closest('[role="listitem"]');
                        if (chatRow) {
                            var titleEl = chatRow.querySelector('span[title]');
                            if (titleEl) sender = titleEl.getAttribute('title');
                            
                            // Last message preview
                            var previewEl = chatRow.querySelector('span[title] + span'); 
                            // This selector is a guess, usually it's separate.
                            // Let's rely on the count for the trigger first.
                        }
                    }
                });
                
                // Also check title for (N)
                var title = document.title;
                var titleMatch = title.match(/\((\d+)\)/);
                if (titleMatch) {
                    // If title has count, use it as fallback or primary
                    // count = parseInt(titleMatch[1]);
                }

                return JSON.stringify({
                    "count": count,
                    "sender": sender
                });
            } catch(e) {
                return JSON.stringify({"error": e.toString()});
            }
        })();
        """

    def enable(self):
        if self.is_enabled:
            return
        
        self.is_enabled = True
        # Poll every 3 seconds
        self.timer_id = GLib.timeout_add_seconds(3, self._poll_messages)
        print("Feature: Background Sync Enabled")

    def disable(self):
        if not self.is_enabled:
            return
            
        self.is_enabled = False
        if self.timer_id:
            GLib.source_remove(self.timer_id)
            self.timer_id = None
        print("Feature: Background Sync Disabled")

    def _poll_messages(self):
        if not self.is_enabled or not self.app.window or not self.app.window.webview:
            return True # Keep running if enabled but window not ready

        # Only poll if window is NOT focused/active (or if user wants always-on sync)
        # Requirement: "detect new messages... when minimized, hidden"
        # If window is active, the user sees it, but we can still notify.
        # Let's run always if enabled, but maybe suppress notification if focused?
        
        self.app.window.webview.run_javascript(self.check_script, None, self._on_js_result, None)
        return True

    def _on_js_result(self, webview, result, user_data):
        try:
            js_result = webview.run_javascript_finish(result)
            val = js_result.get_js_value()
            json_str = val.to_string()
            data = json.loads(json_str)
            
            if "error" in data:
                return

            count = data.get("count", 0)
            sender = data.get("sender", "WhatsApp")
            
            if count > self.last_unread_count:
                # New messages detected
                self.trigger_notification(count, sender)
            
            self.last_unread_count = count
            
        except Exception as e:
            # print(f"Sync Error: {e}")
            pass

    def trigger_notification(self, count, sender):
        # Notify if notifications are enabled
        if self.app.config.get("feature_notifications"):
            # We need to access the notification feature
            # Ideally app should expose it or we pass it
            # app.features["notifications"]
            
            notif_feature = self.app.features.get("notifications")
            if notif_feature and notif_feature.is_enabled:
                diff = count - self.last_unread_count
                msg = f"You have {diff} new message{'s' if diff > 1 else ''}"
                if sender:
                    msg = f"New message from {sender}"
                
                notif_feature.show_notification("WhatsApp Web Lite", msg)
