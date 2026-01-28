import customtkinter as ctk
import tkinter as tk # For some constants if needed
from logic import kill_targets
from config import ConfigManager
import threading
import os
import sys
from PIL import Image
import webbrowser

class BlenderCPRApp(ctk.CTk):
    def __init__(self, tray_icon=None):
        super().__init__()

        self.tray_icon = tray_icon
        self.config = ConfigManager()

        # Window Setup
        self.title("Blender CPR")
        self.geometry("600x550") # Slightly taller for better spacing
        self.resizable(False, False)
        
        # Determine Icon Path
        if hasattr(sys, '_MEIPASS'):
            self.base_path = sys._MEIPASS
        else:
            self.base_path = os.path.dirname(os.path.abspath(__file__))

        icon_path = os.path.join(self.base_path, "icon.png")
        self.iconbitmap(default=icon_path)

        # Load UI Icons
        self.add_img = ctk.CTkImage(Image.open(os.path.join(self.base_path, "add.png")), size=(20, 20))
        self.browse_img = ctk.CTkImage(Image.open(os.path.join(self.base_path, "browse.png")), size=(20, 20))

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
        self.tab_about = self.tab_view.add("About")

        self.setup_dashboard()
        self.setup_settings()
        self.setup_about()
        
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
        self.sw_startup.grid(row=0, column=0, pady=(10, 20), padx=20, sticky="w")

        # --- NEW Management Section ---
        self.mgmt_frame = ctk.CTkFrame(self.tab_settings, fg_color="transparent")
        self.mgmt_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.mgmt_frame.grid_columnconfigure(0, weight=1)

        self.lbl_mgmt = ctk.CTkLabel(self.mgmt_frame, text="Add New Process:", font=("Roboto", 14, "bold"))
        self.lbl_mgmt.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 5))

        self.entry_new = ctk.CTkEntry(self.mgmt_frame, placeholder_text="e.g. godot.exe", height=35)
        self.entry_new.grid(row=1, column=0, padx=(0, 5), sticky="ew")
        
        self.btn_browse = ctk.CTkButton(
            self.mgmt_frame, 
            text="", 
            image=self.browse_img, 
            width=40, 
            height=35, 
            fg_color="#434343", 
            hover_color="#555555",
            command=self.browse_file
        )
        self.btn_browse.grid(row=1, column=1, padx=5)
        
        self.btn_add = ctk.CTkButton(
            self.mgmt_frame, 
            text="Add to List", 
            image=self.add_img, 
            compound="left",
            width=120, 
            height=35,
            command=self.add_process
        )
        self.btn_add.grid(row=1, column=2, padx=(5, 0))

        # --- List Section ---
        self.lbl_list = ctk.CTkLabel(self.tab_settings, text="Current Kill List:", anchor="w")
        self.lbl_list.grid(row=2, column=0, padx=20, pady=(20, 0), sticky="w")

        self.scroll_frame = ctk.CTkScrollableFrame(self.tab_settings, height=220)
        self.scroll_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        self.refresh_process_list()

    def browse_file(self):
        file_path = tk.filedialog.askopenfilename(
            title="Select Application",
            filetypes=[("Executable Files", "*.exe"), ("All Files", "*.*")]
        )
        if file_path:
            filename = os.path.basename(file_path)
            self.entry_new.delete(0, 'end')
            self.entry_new.insert(0, filename)

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
            
            btn = ctk.CTkButton(f, text="X", width=30, fg_color="transparent", border_width=1, text_color="red", command=lambda t=target: self.remove_process(t))
            btn.pack(side="right", padx=5)

    def add_process(self):
        new_p = self.entry_new.get().strip()
        if new_p:
            if not new_p.lower().endswith(".exe"):
                new_p += ".exe"
            
            targets = self.config.get_targets()
            if new_p not in targets:
                targets.append(new_p)
                self.config.set_targets(targets)
                self.refresh_process_list()
                self.entry_new.delete(0, 'end')

    def setup_about(self):
        self.tab_about.grid_columnconfigure(0, weight=1)

        # Developer Title
        self.lbl_dev_title = ctk.CTkLabel(self.tab_about, text="About the Developer", font=("Roboto", 20, "bold"))
        self.lbl_dev_title.grid(row=0, column=0, pady=(30, 10))

        # Description
        desc_text = (
            "Over Engineered Blender Solutions (OEBS)\n\n"
            "Providing robust, specialized tools and automations\n"
            "tailored for the Blender ecosystem and creative workflows."
        )
        self.lbl_desc = ctk.CTkLabel(self.tab_about, text=desc_text, font=("Roboto", 13), justify="center")
        self.lbl_desc.grid(row=1, column=0, pady=20, padx=40)

        # Links Frame
        self.links_frame = ctk.CTkFrame(self.tab_about, fg_color="transparent")
        self.links_frame.grid(row=2, column=0, pady=20)

        self.btn_github_p = ctk.CTkButton(
            self.links_frame, 
            text="Personal GitHub", 
            command=lambda: webbrowser.open("https://github.com/Erisol254"),
            width=150
        )
        self.btn_github_p.grid(row=0, column=0, padx=10)

        self.btn_github_o = ctk.CTkButton(
            self.links_frame, 
            text="OEBS GitHub", 
            command=lambda: webbrowser.open("https://github.com/OEBS-OVER-ENGINEERED-BLENDER-SOLUTIONS"),
            width=150
        )
        self.btn_github_o.grid(row=0, column=1, padx=10)

        # Version
        self.lbl_version = ctk.CTkLabel(self.tab_about, text="v2.1.0", font=("Roboto", 10), text_color="gray")
        self.lbl_version.grid(row=3, column=0, pady=(40, 0))

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
