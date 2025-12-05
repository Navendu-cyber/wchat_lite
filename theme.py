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

headerbar label.title {
    color: #e9edef;
    font-weight: bold;
}

headerbar button {
    min-width: 32px;
    min-height: 32px;
    border-radius: 50%;
    padding: 0px; /* Remove padding to ensure icon fills 32x32 area properly or center it */
    margin: 2px;
    background: transparent;
    border: none;
    box-shadow: none;
    color: #e9edef; /* Ensure icons are light */
}

headerbar button:hover {
    background: rgba(255, 255, 255, 0.1);
}

/* Window Controls (Close, Maximize, Minimize) */
headerbar button.titlebutton {
    color: #ffffff;
    min-width: 24px;
    min-height: 24px;
    padding: 0;
    margin: 0 2px;
    border-radius: 50%;
    background: transparent;
    border: none;
    box-shadow: none;
}

headerbar button.titlebutton image {
    color: #ffffff;
}

headerbar button.titlebutton:hover {
    background: rgba(255, 255, 255, 0.1);
    color: #ffffff;
}

headerbar button.titlebutton:backdrop {
    color: #cccccc;
}

window {
    background-color: #ffffff;
}

/* Global Label Color (default to dark for main window) */
label {
    color: #111b21;
}

/* Lock Screen Styling */
.lock-title {
    font-size: 24px;
    font-weight: bold;
    color: #e9edef;
    margin-bottom: 8px;
}

.lock-subtitle {
    font-size: 14px;
    color: #e9edef;
    margin-bottom: 24px;
}

.lock-error {
    color: #ea0038;
    font-weight: bold;
    margin-top: 10px;
}

/* Entry Styling - Dark background for better contrast in dark settings/lock */
entry {
    background-color: #2a3942;
    color: #e9edef;
    border: 1px solid #8696a0;
    border-radius: 4px;
    padding: 8px;
    min-width: 250px;
}

entry:focus {
    border-color: #00a884;
    background-color: #2a3942;
    color: #e9edef;
}

entry selection {
    background-color: #00a884;
    color: #ffffff;
}

/* Custom Green Button (Unlock, Save, Cancel) */
.unlock-button {
   background: #25D366;
   color: white;
   border-radius: 6px;
   padding: 8px 16px;
   font-weight: bold;
   border: none;
}

.unlock-button:hover {
   background: #1DA851;
}

/* Settings Window Styling - Dark Theme */
.settings-window {
   background: #111b21;
   color: #e9edef;
   padding: 20px;
}

.settings-window label {
    color: #e9edef;
}

.settings-window separator {
    background: #2a3942;
}

/* Glassmorphism Lock Card */
.lock-card {
    background-color: rgba(32, 44, 51, 0.85); /* Semi-transparent dark */
    border: 1px solid rgba(134, 150, 160, 0.3);
    border-radius: 16px;
    padding: 40px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
}

/* Tray Menu Styling */
menu {
    background-color: #202c33;
    color: #e9edef;
    border: 1px solid #111b21;
    padding: 5px;
}

menuitem {
    padding: 4px 8px;
}

menuitem:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

menuitem label {
    color: #e9edef;
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

_theme_loaded = False

def apply_gtk_theme():
    global _theme_loaded
    if _theme_loaded:
        return

    screen = Gdk.Screen.get_default()
    provider = Gtk.CssProvider()
    provider.load_from_data(GTK_CSS)
    Gtk.StyleContext.add_provider_for_screen(
        screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )
    _theme_loaded = True
