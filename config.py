import os
import json
import logging

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "whatsapp-lite")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "auto_lock_timeout": 300,  # Seconds
    "password_hash": None,     # SHA-256 hash
    "feature_shortcuts": False,
    "feature_tray": False,
    "feature_notifications": False,
    "feature_dragdrop": False,
    "feature_app_lock": True
}

class ConfigManager:
    def __init__(self):
        self._ensure_config_dir()
        self.config = self._load_config()

    def _ensure_config_dir(self):
        if not os.path.exists(CONFIG_DIR):
            try:
                os.makedirs(CONFIG_DIR)
            except OSError as e:
                logging.error(f"Could not create config directory: {e}")

    def _load_config(self):
        if not os.path.exists(CONFIG_FILE):
            return DEFAULT_CONFIG.copy()
        
        try:
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
                # Merge with defaults to ensure all keys exist
                config = DEFAULT_CONFIG.copy()
                config.update(data)
                return config
        except (json.JSONDecodeError, OSError) as e:
            logging.error(f"Error loading config: {e}")
            return DEFAULT_CONFIG.copy()

    def save(self):
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
        except OSError as e:
            logging.error(f"Error saving config: {e}")

    def get(self, key):
        return self.config.get(key, DEFAULT_CONFIG.get(key))

    def set(self, key, value):
        self.config[key] = value
        self.save()
