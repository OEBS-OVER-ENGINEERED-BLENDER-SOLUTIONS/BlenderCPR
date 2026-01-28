import customtkinter as ctk
import tkinter as tk # For some constants if needed
from logic import kill_targets
from config import ConfigManager
import threading
import os
import sys

class BlenderCPRApp(ctk.CTk):
    def __init__(self, tray_icon=None):
        super().__init__()

        self.tray_icon = tray_icon
        self.config = ConfigManager()

        # Window Setup
        self.title("Blender CPR")
        self.geometry("600x450")
        self.resizable(False, False)
        
        # Determine Icon Path for Window Icon
        if hasattr(sys, '_MEIPASS'):
            icon_path = os.path.join(sys._MEIPASS, "icon.png")
        else:
            icon_path = "icon.png"
        self.iconbitmap(default=icon_path)

        # Theme
        ctk.set_appearance_mode(self.config.data.get("theme", "Dark"))
        ctk.set_default_color_theme("blue")

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.tab_dashboard = self.tab_view.add("Dashboard")
        self.tab_settings = self.tab_view.add("Settings")

        self.setup_dashboard()
        self.setup_settings()
        
        # Override Close Button to Minimize to Tray
        self.protocol("WM_DELETE_WINDOW", self.on_close_window)

    def setup_dashboard(self):
        self.tab_dashboard.grid_columnconfigure(0, weight=1)
        
        # Title Label
        self.lbl_title = ctk.CTkLabel(self.tab_dashboard, text="Blender CPR", font=("Roboto", 24, "bold"))
        self.lbl_title.grid(row=0, column=0, pady=(30, 10))
        
        self.lbl_subtitle = ctk.CTkLabel(self.tab_dashboard, text="System Ready", font=("Roboto", 14), text_color="gray")
        self.lbl_subtitle.grid(row=1, column=0, pady=(0, 40))

        # Big Rescue Button
        self.btn_rescue = ctk.CTkButton(
            self.tab_dashboard, 
            text="RESCUE BLENDER", 
            font=("Roboto", 20, "bold"),
            fg_color="#D32F2F", 
            hover_color="#B71C1C",
            height=100,
            width=300,
            command=self.run_rescue
        )
        self.btn_rescue.grid(row=2, column=0, pady=20)
        
        self.lbl_status = ctk.CTkTextbox(self.tab_dashboard, height=100, width=400)
        self.lbl_status.grid(row=3, column=0, pady=20)
        self.lbl_status.insert("0.0", "Ready to prevent crashes...")
        self.lbl_status.configure(state="disabled")

    def log(self, message):
        self.lbl_status.configure(state="normal")
        self.lbl_status.insert("end", f"\n{message}")
        self.lbl_status.see("end")
        self.lbl_status.configure(state="disabled")

    def run_rescue(self):
        targets = self.config.get_targets()
        self.log(f"Scanning for {len(targets)} targets...")
        
        killed = kill_targets(targets)
        
        if killed:
            self.log(f"SUCCESS: Killed {len(killed)} processes.")
            for k in killed:
                self.log(f" - {k}")
        else:
            self.log("No stuck processes found.")

    def setup_settings(self):
        self.tab_settings.grid_columnconfigure(0, weight=1)

        # Startup Toggle
        self.var_startup = ctk.BooleanVar(value=self.config.is_startup_enabled())
        self.sw_startup = ctk.CTkSwitch(
            self.tab_settings, 
            text="Start with Windows (Minimize to Tray)", 
            command=self.toggle_startup,
            variable=self.var_startup
        )
        self.sw_startup.grid(row=0, column=0, pady=20, padx=20, sticky="w")

        # Process List Label
        self.lbl_list = ctk.CTkLabel(self.tab_settings, text="Target Processes (Kill List):", anchor="w")
        self.lbl_list.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")

        # Scrollable Frame for items
        self.scroll_frame = ctk.CTkScrollableFrame(self.tab_settings, height=200)
        self.scroll_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.refresh_process_list()

        # Add New Item
        self.entry_new = ctk.CTkEntry(self.tab_settings, placeholder_text="godot.exe")
        self.entry_new.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="ew")
        
        self.btn_add = ctk.CTkButton(self.tab_settings, text="Add Process", command=self.add_process)
        self.btn_add.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

    def refresh_process_list(self):
        # Clear existing
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        targets = self.config.get_targets()
        for i, target in enumerate(targets):
            f = ctk.CTkFrame(self.scroll_frame)
            f.pack(fill="x", pady=2)
            
            lbl = ctk.CTkLabel(f, text=target)
            lbl.pack(side="left", padx=10)
            
            btn = ctk.CTkButton(f, text="X", width=30, fg_color="transparent", border_width=1, command=lambda t=target: self.remove_process(t))
            btn.pack(side="right", padx=5)

    def add_process(self):
        new_p = self.entry_new.get().strip()
        if new_p:
            targets = self.config.get_targets()
            if new_p not in targets:
                targets.append(new_p)
                self.config.set_targets(targets)
                self.refresh_process_list()
                self.entry_new.delete(0, 'end')

    def remove_process(self, target):
        targets = self.config.get_targets()
        if target in targets:
            targets.remove(target)
            self.config.set_targets(targets)
            self.refresh_process_list()

    def toggle_startup(self):
        self.config.set_startup(self.var_startup.get())

    def on_close_window(self):
        self.withdraw() # Hide window
        if self.tray_icon:
            self.tray_icon.notify("Blender CPR is running in the background.", "Minimized to Tray")

    def show_window(self):
        self.deiconify()
        self.lift()
