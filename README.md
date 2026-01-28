# 🚑 Blender CPR (Crash Process Rescuer)

A modern, lightweight Windows utility to force-kill stuck Blender processes and tablet drivers that prevent Blender from restarting. No more logging out or rebooting just because Blender crashed!

![Blender CPR Icon](icon.png)

## ✨ Features

- **Modern UI**: Clean dark-mode dashboard built with `customtkinter`.
- **One-Click Rescue**: Instantly terminates "zombie" Blender processes and common tablet drivers.
- **Smart Tablet Reset**: Automatically resets Wacom, Huion, and XP-Pen drivers.
- **File Browser Integration**: Browse for `.exe` files instead of typing process names manually.
- **Start with Windows**: Customizable option to have the tool always ready in your system tray.
- **Custom Kill List**: Add any process name to the list to customize what gets "rescued".
- **Modern Icons**: Intuitive "+" and browse icons for easier navigation.

## 🛡️ Security & False Positives

Because Blender CPR is an **unsigned executable** that performs system-level actions (killing processes and modifying Registry for startup), some antivirus scanners (like Windows Defender or VirusTotal) may flag it as suspicious.

**This is a false positive.**

Since the project is open-source, you can:
1. Review the Python source code yourself.
2. Build the executable from source using the provided `build.bat`.
3. Check the file properties for official metadata (Developer: OEBS).

## 🚀 Installation & Usage

### Portable Version
1. Download `BlenderCPR.exe` from the [releases](releases/BlenderCPR.exe) folder (or the GitHub Releases page).
2. Move it to a permanent folder (e.g., `Documents/Tools`).
3. Run `BlenderCPR.exe`.

### First Time Setup
1. Switch to the **Settings** tab.
2. Toggle **"Start with Windows"** to ON.
3. The app will now automatically start minimized in your tray every time you boot your PC.

### Rescuing Blender
- **Option A**: Right-click the medical cross icon in your System Tray and select **"🚑 Rescue Blender"**.
- **Option B**: Open the dashboard and click the big red **"RESCUE BLENDER"** button.

## 🛠️ Built With

- **Python 3.x**
- **CustomTkinter**: Modern GUI framework.
- **Pystray**: System tray integration.
- **Psutil**: Robust process management.
- **PyInstaller**: Standalone executable packaging.

## 📝 Configuration

The app creates a `config.json` file in the same directory as the executable. This stores your target process list and startup preferences.

## 🤝 Contributing

Feel free to fork this repo and add more drivers or features!

---
**Author**: Erisol3d
**License**: MIT
