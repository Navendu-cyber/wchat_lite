from gi.repository import Gtk, Gdk

# GTK CSS for the application UI
GTK_CSS = b"""
headerbar {
    min-height: 38px;
    padding: 0px;
    background: #202c33;
    color: #e9edef;
    border-bottom: 1px solid #111b21;
}

headerbar button {
    margin: 2px;
    padding: 4px;
    border-radius: 50%;
}

window {
    background-color: #ffffff;
}

label {
    color: #111b21;
}

/* Lock Screen Styling */
.lock-title {
    font-size: 24px;
    font-weight: bold;
    color: #41525d;
    margin-bottom: 8px;
}

.lock-subtitle {
    font-size: 14px;
    color: #8696a0;
    margin-bottom: 24px;
}

.lock-error {
    color: #ea0038;
    font-weight: bold;
    margin-top: 10px;
}

entry {
    background-color: #ffffff;
    color: #111b21;
    border: 1px solid #d1d7db;
    border-radius: 4px;
    padding: 8px;
    min-width: 250px;
}

entry:focus {
    border-color: #00a884;
}

button.suggested-action {
    background-color: #00a884;
    color: #ffffff;
    border-radius: 20px;
    padding: 8px 24px;
    font-weight: bold;
    border: none;
}

button.suggested-action:hover {
    background-color: #008f6f;
}
"""

# CSS to inject into the WebView for WhatsApp Web
# This targets specific WhatsApp Web elements to refine the look
WHATSAPP_CSS = """
/* Scrollbar customization */
::-webkit-scrollbar {
    width: 6px !important;
    height: 6px !important;
}
::-webkit-scrollbar-thumb {
    background-color: rgba(255, 255, 255, 0.2) !important;
}
::-webkit-scrollbar-track {
    background: transparent !important;
}

/* Hide "Get the app" banner if present */
div[data-testid="intro-md-beta-logo-dark"], 
div[data-testid="intro-md-beta-logo-light"] {
    display: none !important;
}
"""

def apply_gtk_theme():
    screen = Gdk.Screen.get_default()
    provider = Gtk.CssProvider()
    provider.load_from_data(GTK_CSS)
    Gtk.StyleContext.add_provider_for_screen(
        screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )
