import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class FeatureDragDrop:
    def __init__(self, app):
        self.app = app
        self.is_enabled = False
        self.handler_id = None

    def enable(self):
        if self.is_enabled:
            return

        if self.app.window:
            # Enable drag drop on the window
            self.app.window.drag_dest_set(
                Gtk.DestDefaults.ALL,
                [], 
                Gdk.DragAction.COPY
            )
            self.app.window.drag_dest_add_uri_targets()
            
            self.handler_id = self.app.window.connect("drag-data-received", self._on_drag_data_received)
        
        self.is_enabled = True
        print("Feature: Drag & Drop Enabled")

    def disable(self):
        if not self.is_enabled:
            return
            
        if self.app.window and self.handler_id:
            self.app.window.disconnect(self.handler_id)
            self.app.window.drag_dest_unset()
            self.handler_id = None
            
        self.is_enabled = False
        print("Feature: Drag & Drop Disabled")

    def _on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
        if not self.is_enabled:
            return

        uris = data.get_uris()
        if not uris:
            return

        # We only handle the first file for simplicity
        file_uri = uris[0]
        filename = file_uri.split('/')[-1]
        
        # Ask user
        dialog = Gtk.MessageDialog(
            transient_for=self.app.window,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text=f"Send file '{filename}'?"
        )
        dialog.format_secondary_text("This will drop the file into WhatsApp.")
        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.YES:
            # To "pass" the drop to the webview, we actually need to NOT finish the drag here
            # or manually forward it. 
            # However, since we intercepted it on the Window, the WebView might not get it 
            # if we don't propagate it.
            # Gtk.drag_finish(drag_context, True, False, time)
            # But we want the WebView to handle the upload.
            
            # If we return without calling drag_finish, it might not work.
            # Strategy: We let the event propagate to the WebView?
            # The WebView is a child. If the Window handles it, does it stop?
            # We connected to "drag-data-received".
            
            # Actually, the best way is to let the WebView handle the drop, 
            # but we want to intercept it first.
            # This is tricky in GTK.
            
            # Alternative: We just finish successfully, and rely on the user dragging DIRECTLY to the webview?
            # But we set dest on the WINDOW.
            
            # Let's try: If YES, we allow the drop.
            # But we are in the "received" handler, the drop has happened.
            # We can't "replay" it easily.
            
            # Revised approach:
            # We don't set dest on the window. We connect to the WebView's signal?
            # WebView handles its own D&D.
            # If we want to intercept, we should connect to the WebView.
            pass
            
        else:
            # Cancel the drop
            Gtk.drag_finish(drag_context, False, False, time)
            return

        Gtk.drag_finish(drag_context, True, False, time)

# Re-writing class to target WebView specifically for better integration
class FeatureDragDrop:
    def __init__(self, app):
        self.app = app
        self.is_enabled = False
        self.handler_id = None

    def enable(self):
        if self.is_enabled:
            return

        if self.app.window and self.app.window.webview:
            # Connect to the WebView's drag-drop signal
            # Note: WebKitWebView has 'drag-drop' signal? No, it's a GtkWidget.
            # We want to intercept 'drag-drop' (the event).
            self.handler_id = self.app.window.webview.connect("drag-drop", self._on_drag_drop)
        
        self.is_enabled = True
        print("Feature: Drag & Drop Enabled")

    def disable(self):
        if not self.is_enabled:
            return
            
        if self.app.window and self.app.window.webview and self.handler_id:
            self.app.window.webview.disconnect(self.handler_id)
            self.handler_id = None
            
        self.is_enabled = False
        print("Feature: Drag & Drop Disabled")

    def _on_drag_drop(self, widget, context, x, y, time):
        # This is called when a drop happens.
        # We can show a dialog here.
        
        # Problem: We don't know the filename yet. We need 'drag-data-received'.
        # But 'drag-data-received' requires us to request data.
        
        # Let's try a simpler UX:
        # Just ask "Allow file drop?" without filename if necessary, 
        # or request data.
        
        # To get filename, we need to request target.
        # widget.drag_get_data(context, target, time)
        # This is async.
        
        # For this task, let's just ask generic confirmation to be safe and simple.
        
        dialog = Gtk.MessageDialog(
            transient_for=self.app.window,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Send dropped file?"
        )
        response = dialog.run()
        dialog.destroy()

        if response == Gtk.ResponseType.YES:
            # Return False to propagate the event to WebKit's internal handler
            return False 
        else:
            # Return True to stop the event (cancel drop)
            return True
