# WChat Lite

**WChat Lite** is a lightweight, privacy-focused Linux desktop wrapper for WhatsApp Web.  
Built with **Python**, **GTK3**, and **WebKit2GTK**, it adds security and usability features that WhatsApp Web does not provide — including **password lock**, **blurred privacy screen**, **auto-lock**, **background sync**, and **desktop integration**.

---

## 🚀 Features

### 🔐 **Secure App Lock**
- App is protected with a **password lock**.
- First launch asks you to create a password.
- Your password is **not stored directly** — only its **SHA-256 hash** is saved.

### 🧊 **Blurred Lock Screen**
- When the app locks, it captures the window and creates a **blurred background** behind the login dialog for privacy — similar to macOS.

### 🔄 **Background Sync & Tray Mode**
- **Background Sync**: The app polls for new messages even when minimized or hidden.
- **System Tray Icon**: Keeps the app running in the background.
- **Taskbar Alert**: When you close the window, a notification reminds you: *"WChat lives in the taskbar."*

### 🔔 **Desktop Notifications**
- Receive native Linux desktop notifications for new messages.
- Works even when the app is minimized or hidden in the tray.
- Can be toggled on/off in settings.

### ⏱️ **Auto-Lock on Inactivity**
- The app automatically locks after a set period of inactivity (default: 5 minutes).
- Timeout duration can be customized in settings.

### 🖥️ **Smooth & Polished UI**
- **Dark Mode**: Matches WhatsApp Web's dark theme perfectly.
- **Glassmorphism**: Modern, semi-transparent lock screen card.
- **Smooth Scrolling**: Enabled for a fluid experience.
- **Native Feel**: Circular header icons and clean settings dialog.

### 🛡️ **No Account Data Stored**
- WChat Lite does NOT store or access your WhatsApp messages.  
- Everything stays inside the official WhatsApp Web sandbox.

---

## 📦 Installation

### 1. Install System Dependencies
You need **GTK3**, **WebKit2GTK**, and **libnotify** (for notifications).

**Ubuntu / Debian / Linux Mint:**
```bash
sudo apt update
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-webkit2-4.1 libnotify-bin gir1.2-notify-0.7 gir1.2-appindicator3-0.1
```
*(Note: `gir1.2-appindicator3-0.1` is recommended for the tray icon, but the app will fallback to a standard status icon if missing.)*

### 2. Clone the Repository
```bash
git clone https://github.com/Navendu-cyber/wchat_lite.git
cd wchat_lite
```

### 3. Run the Application
```bash
python3 main.py
```

---

## ⚙️ Configuration

Your settings are stored securely in your home directory:
`~/.config/whatsapp-lite/config.json`

This file contains:
- **password_hash**: SHA-256 hash of your lock password.
- **auto_lock_timeout**: Seconds before auto-lock.
- **feature_***: Toggles for various features.

> **Note:** Never manually edit the password hash unless you know what you are doing. If you forget your password, you can delete this file to reset the app (this will NOT delete your WhatsApp data, only the app lock settings).

---

## 🛠️ Troubleshooting

**❌ ModuleNotFoundError: No module named 'gi'**
```bash
sudo apt install python3-gi
```

**❌ ValueError: Namespace WebKit2 not available**
```bash
sudo apt install gir1.2-webkit2-4.1
```

**❌ Notifications Disabled / Warning: libnotify not found**
```bash
sudo apt install libnotify-bin gir1.2-notify-0.7
```

---

## 📜 License
This project is licensed under the **MIT License**.

**Disclaimer:**
This project is not affiliated with, endorsed by, or associated with WhatsApp or Meta. It simply provides a secure desktop wrapper around the official [WhatsApp Web](https://web.whatsapp.com) interface.

---

## ❤️ Author
**Navendu**  
*Linux + Flutter + Cybersecurity enthusiast*