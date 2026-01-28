import json
import os
import winreg
import sys

CONFIG_FILE = "config.json"
APP_NAME = "BlenderCPR"

DEFAULT_CONFIG = {
    "start_with_windows": False,
    "theme": "Dark",
    "targets": [
        "blender.exe",
        "blender-launcher.exe",
        "Wacom_Tablet.exe",
        "Wacom_TabletUser.exe",
        "WacomHost.exe",
        "HuionTablet.exe",
        "PenTablet.exe",
        "TabletDriver.exe",
        "Huion Tablet.exe",
        "PentabletService.exe",
        "PentabletHID.exe"
    ]
}

class ConfigManager:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), CONFIG_FILE)
        # If running as OneFile exe, sys.argv[0] is the exe path, which is what we want for config storage alongside it.
        # But if user puts exe in Program Files, we might need AppData. For now, local is fine for a portable tool.
        self.data = self.load()

    def load(self):
        if not os.path.exists(self.config_path):
            return DEFAULT_CONFIG.copy()
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except:
            return DEFAULT_CONFIG.copy()

    def save(self):
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get_targets(self):
        return self.data.get("targets", DEFAULT_CONFIG["targets"])

    def set_targets(self, targets):
        self.data["targets"] = targets
        self.save()

    def is_startup_enabled(self):
        return self.data.get("start_with_windows", False)

    def set_startup(self, enabled):
        self.data["start_with_windows"] = enabled
        self.save()
        self._apply_startup_registry(enabled)

    def _apply_startup_registry(self, enabled):
        """Adds or removes the app from Windows Startup Registry."""
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
            exe_path = os.path.abspath(sys.argv[0])
            
            if enabled:
                # Add registry key
                winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, f'"{exe_path}" --tray')
            else:
                # Remove registry key
                try:
                    winreg.DeleteValue(key, APP_NAME)
                except FileNotFoundError:
                    pass
            winreg.CloseKey(key)
        except Exception as e:
            print(f"Registry Error: {e}")

