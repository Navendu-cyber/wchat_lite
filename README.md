# WhatsApp Web Lite

## Prerequisites
Before running the application, ensure you have the necessary system dependencies installed. This app relies on GTK3 and WebKit2GTK via GObject Introspection.

Run the following command in your terminal:

```bash
sudo apt update
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-webkit2-4.1
```

## How to Run
1. Navigate to the project directory:
   ```bash
   cd /home/optimus/Desktop/Whatsapp-lite
   ```

2. Run the application using Python 3:
   ```bash
   python3 main.py
   ```

## Troubleshooting
- **"ModuleNotFoundError: No module named 'gi'"**: Make sure you installed `python3-gi`.
- **"ValueError: Namespace WebKit2 not available"**: Make sure you installed `gir1.2-webkit2-4.1`.
