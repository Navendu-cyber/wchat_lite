# WChat Lite

**WChat Lite** is a lightweight, privacy-focused Linux desktop wrapper for WhatsApp Web.  
Built with **Python**, **GTK3**, and **WebKit2GTK**, it adds security and usability features that WhatsApp Web does not provide — including **password lock**, **blurred privacy screen**, **auto-lock**, **smooth UI**, and **optional desktop integration features**.

---

## 🚀 Features

### 🔐 **Secure App Lock**
- App is protected with a **password lock**.
- First launch asks you to create a password.
- Your password is **not stored directly** — only its **SHA-256 hash** is saved.

### 🔏 **What Does Password Hashing Mean?**
- The app stores a *one-way hash* such as:
a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e

markdown
Copy code
- This is **NOT** your password — it cannot be reversed.
- Even if someone opens your config file, they **cannot see your password**.

### 🧊 **Blurred Lock Screen**
When the app locks, it captures the window and creates a **blurred background** behind the login dialog for privacy — similar to macOS.

### ⏱️ **Auto-Lock on Inactivity**
- The app automatically locks after X seconds of no activity.
- Time can be changed in settings.

### 🖥️ **Smooth & Polished UI**
- Smooth scrolling enabled for WebKit.
- Custom CSS for clarity and better readability.
- Header icons styled to be properly circular.
- Settings window fully redesigned for visibility.

### 🔔 **Desktop Notifications (Optional)**
- Receive message notifications on your Linux desktop.
- Can be turned on/off in settings.
- Automatically disabled if `libnotify` is missing.

### 🛡️ **No Account Data Stored**
WChat Lite does NOT store or access WhatsApp messages.  
Everything stays inside the official WhatsApp Web sandbox.

---

## 📦 Installation

### ✅ System Dependencies (Ubuntu/Debian)
You must install GTK3 + WebKit2GTK:

```bash
sudo apt update
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-webkit2-4.1
Optional (for desktop notifications)
bash
Copy code
sudo apt install libnotify-bin libnotify4 gir1.2-notify-0.7
📁 Clone & Run
bash
Copy code
git clone https://github.com/Navendu-cyber/wchat_lite.git
cd wchat_lite
python3 main.py
🛠️ Troubleshooting
❌ ModuleNotFoundError: No module named 'gi'
You forgot to install python3-gi:

bash
Copy code
sudo apt install python3-gi
❌ ValueError: Namespace WebKit2 not available
Install WebKit2 introspection:

bash
Copy code
sudo apt install gir1.2-webkit2-4.1
❌ Notifications Disabled
If you see:

pgsql
Copy code
Warning: libnotify not found. Notifications will be disabled.
Install:

bash
Copy code
sudo apt install libnotify-bin libnotify4 gir1.2-notify-0.7
🔧 Configuration File
Your settings are stored at:

arduino
Copy code
~/.config/wchat_lite/config.json
This file contains:

auto-lock setting

password hash

feature toggles

Never manually edit the password hash.

📸 Screenshots (Coming Soon)
pgsql
Copy code
[ Add Lock Screen Image Here ]
[ Add Main Window Screenshot Here ]
[ Add Settings Window Screenshot Here ]
📜 License
This project is licensed under the MIT License.

Disclaimer:
This project is not affiliated with, endorsed by, or associated with WhatsApp or Meta.
It simply provides a secure desktop wrapper around the official https://web.whatsapp.com interface.

🌟 Contributing
Pull requests are welcome!
The app uses a clean modular structure — each new feature (shortcuts, AI helper, notifications, etc.) lives in its own module.

❤️ Author
Navendu
Linux + Flutter + Cybersecurity enthusiast