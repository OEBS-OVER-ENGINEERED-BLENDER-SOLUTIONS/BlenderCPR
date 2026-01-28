import pystray
from PIL import Image
import threading
import sys
import os
import argparse
import ctypes
import traceback
import datetime
from gui import BlenderCPRApp
from logic import kill_targets
from config import ConfigManager

ICON_PATH = "icon.png"

def create_tray_icon(app):
    """
    Creates and returns the pystray Icon.
    """
    # Load Icon
    if hasattr(sys, '_MEIPASS'):
        icon_path = os.path.join(sys._MEIPASS, ICON_PATH)
    else:
        icon_path = ICON_PATH
    
    try:
        image = Image.open(icon_path)
    except:
        image = Image.new('RGB', (64, 64), color=(255, 165, 0))

    def on_open_click(icon, item):
        app.after(0, app.show_window)

    def on_rescue_click(icon, item):
        # We can run kill_targets immediately
        # Ideally, we also log this to the GUI if it exists
        targets = ConfigManager().get_targets()
        killed = kill_targets(targets)
        if killed:
             icon.notify(f"Killed {len(killed)} processes.", "Blender CPR")
        else:
             icon.notify("No stuck processes found.", "Blender CPR")

    def on_exit_click(icon, item):
        icon.stop()
        app.quit()

    menu = pystray.Menu(
        pystray.MenuItem("Open Dashboard", on_open_click, default=True),
        pystray.MenuItem("🚑 Rescue Blender", on_rescue_click),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Exit", on_exit_click)
    )

    icon = pystray.Icon("BlenderCPR", image, "Blender CPR", menu)
    return icon

def run_tray(icon):
    icon.run()

def main():
    # Single Instance Check (Windows Mutex)
    mutex_name = "Global\\BlenderCPR_SingleInstance_Mutex"
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)
    last_error = ctypes.windll.kernel32.GetLastError()
    
    if last_error == 183: # ERROR_ALREADY_EXISTS
        # If we are starting with --tray, just exit silently.
        # Otherwise, we could try to find the existing window and show it, 
        # but for now, simple exit is safest.
        sys.exit(0)

    parser = argparse.ArgumentParser()
    parser.add_argument("--tray", action="store_true", help="Start minimized to tray")
    args = parser.parse_args()

    app = BlenderCPRApp()
    
    # Create tray icon
    icon = create_tray_icon(app)
    app.tray_icon = icon

    # Start tray in background thread
    tray_thread = threading.Thread(target=run_tray, args=(icon,), daemon=True)
    tray_thread.start()

    # Handle startup state
    if args.tray:
        # Start hidden
        app.withdraw()
    else:
        # Show window
        app.deiconify()

    app.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Create a crash log file
        log_path = "crash_report.log"
        with open(log_path, "w") as f:
            f.write(f"Blender CPR Crash Report - {datetime.datetime.now()}\n")
            f.write("="*50 + "\n")
            f.write(traceback.format_exc())
        
        # Also try to show a message box if possible via ctypes
        try:
            ctypes.windll.user32.MessageBoxW(0, f"Blender CPR has crashed.\nA log has been saved to: {os.path.abspath(log_path)}\n\nError: {str(e)}", "Critical Error", 0x10)
        except:
            pass
        sys.exit(1)
