# 🏥 Blender CPR v2.0.0 Release Notes

## [2.0.0] - 2026-01-28

### 🚀 Added
- **Modern GUI (CustomTkinter)**: A complete overhaul from the batch script/tray-only version. Features a sleek dark-mode dashboard.
- **System Tray Integration**: The app now minimizes to the system tray (medical cross icon) to stay out of the way while remaining accessible.
- **Big Red Rescue Button**: One-click solution to force-quit all hung Blender processes.
- **Customizable Kill List**: Users can now add or remove specific process names (e.g., `photoshop.exe`, `substance.exe`) via the Settings tab.
- **Start with Windows**: Native registry integration to automatically launch the tool on system boot (minimized to tray).
- **Driver Support**: Expanded targeting for Wacom, Huion, and XP-Pen drivers to resolve the "cannot restart without reboot" issue commonly caused by driver locks.
- **Real-time Logging**: Dashboard status log shows exactly which processes were found and terminated.

### 🛠️ Fixed
- Resolved issue where `blender.exe` would remain as a "zombie" process invisible to Task Manager's main view but blocking new instances.
- Fixed driver-level locks by forcefully resetting the tablet driver's connection to the crashed app.

### 📦 Installation
1. Download `BlenderCPR.exe` from the Assets below.
2. No installer required—it's portable! Move it to your preferred tools folder.
3. **Important**: Run as Administrator at least once to enable the "Start with Windows" feature.

---
*Created by Erisol3d*
