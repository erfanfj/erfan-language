import ctypes
import os
import shutil
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import winreg


APP_NAME = "Erfan"
EXE_NAME = "erfan.exe"
RUNTIME_NAME = "erfan_runtime.exe"

# ---------------- THEME ---------------- #
BG_DARK = "#151521"
BG_DARK_2 = "#1c1c2b"
BG_LIGHT = "#ffffff"
ACCENT = "#7c5cff"
ACCENT_HOVER = "#8f72ff"
TEXT_MAIN = "#111827"
TEXT_MUTED = "#6b7280"
TEXT_LIGHT = "#e5e7ff"
TEXT_LIGHT_MUTED = "#8b8bb3"
FONT_FAMILY = "Segoe UI"

STEPS = ["Welcome", "Location", "Install", "Finish"]


def get_app_dir():
    return os.path.join(os.environ.get("LOCALAPPDATA", os.getcwd()), APP_NAME)


def resource_path(relative_path):
    """
    Path to a bundled resource.
    - When frozen by PyInstaller (--onefile), files added with --add-binary
      are extracted to a temp folder pointed to by sys._MEIPASS at runtime.
    - When running as a plain .py script, fall back to the script's folder.
    """
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def copy_exe(progress_cb=None):
    app_dir = get_app_dir()
    os.makedirs(app_dir, exist_ok=True)

    source = resource_path(EXE_NAME)
    target = os.path.join(app_dir, EXE_NAME)

    if not os.path.exists(source):
        raise FileNotFoundError(f"{EXE_NAME} not found inside the installer")

    shutil.copy2(source, target)

    runtime_source = resource_path(RUNTIME_NAME)
    if os.path.exists(runtime_source):
        shutil.copy2(runtime_source, os.path.join(app_dir, RUNTIME_NAME))

    return app_dir


def add_to_path_registry(path):
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         "Environment",
                         0,
                         winreg.KEY_READ | winreg.KEY_WRITE) as key:

        try:
            current, _ = winreg.QueryValueEx(key, "Path")
        except FileNotFoundError:
            current = ""

        if path in current:
            return

        new_path = current + ";" + path if current else path
        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)

    # Tell Explorer and other running processes that the environment changed.
    # Without this, only brand-new processes launched AFTER a reboot/logoff
    # would ever see the updated PATH.
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x1A
    SMTO_ABORTIFHUNG = 0x0002
    result = ctypes.c_long()
    ctypes.windll.user32.SendMessageTimeoutW(
        HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment",
        SMTO_ABORTIFHUNG, 5000, ctypes.byref(result)
    )


# ---------------- WIDGETS ---------------- #

class RoundedButton(tk.Canvas):
    """A flat, modern accent/ghost button drawn on a canvas (no ugly system buttons)."""

    def __init__(self, parent, text, command=None, primary=True, width=140, height=42):
        super().__init__(parent, width=width, height=height,
                          bg=parent["bg"], highlightthickness=0, cursor="hand2")
        self.command = command
        self.primary = primary
        self.width = width
        self.height = height
        self.text = text
        self._draw(ACCENT if primary else BG_DARK_2)
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", lambda e: self._draw(ACCENT_HOVER if primary else "#2a2a40"))
        self.bind("<Leave>", lambda e: self._draw(ACCENT if primary else BG_DARK_2))

    def _draw(self, color):
        self.delete("all")
        r = 10
        w, h = self.width, self.height
        self.create_round_rect(1, 1, w - 1, h - 1, r, fill=color, outline="")
        fg = "#ffffff" if self.primary else TEXT_LIGHT
        self.create_text(w / 2, h / 2, text=self.text, fill=fg,
                          font=(FONT_FAMILY, 10, "bold"))

    def create_round_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
                  x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
                  x1, y2, x1, y2 - r, x1, y1 + r, x1, y1]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _on_click(self, event):
        if self.command:
            self.command()

    def set_enabled(self, enabled):
        self.command_backup = self.command if enabled else None


# ---------------- INSTALLER ---------------- #

class Installer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Erfan Setup")
        self.geometry("760x460")
        self.resizable(False, False)
        self.configure(bg=BG_LIGHT)

        try:
            self.iconbitmap(default="")
        except Exception:
            pass

        self.step = 0

        # ---- layout: sidebar + content + nav ----
        self.sidebar = tk.Frame(self, bg=BG_DARK, width=230)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content_wrap = tk.Frame(self, bg=BG_LIGHT)
        self.content_wrap.pack(side="right", fill="both", expand=True)

        self.content = tk.Frame(self.content_wrap, bg=BG_LIGHT)
        self.content.pack(fill="both", expand=True, padx=40, pady=30)

        self.nav = tk.Frame(self.content_wrap, bg=BG_LIGHT, height=60)
        self.nav.pack(fill="x", side="bottom", pady=(0, 20), padx=40)

        self.build_sidebar()
        self.frames = []
        self.create_steps()
        self.show_step(0)

    # ---------- sidebar ---------- #
    def build_sidebar(self):
        tk.Label(self.sidebar, text="Erfan", bg=BG_DARK, fg="#ffffff",
                 font=(FONT_FAMILY, 22, "bold")).pack(pady=(40, 4), padx=30, anchor="w")
        tk.Label(self.sidebar, text="Programming Language", bg=BG_DARK, fg=TEXT_LIGHT_MUTED,
                 font=(FONT_FAMILY, 10)).pack(padx=30, anchor="w")

        self.step_labels = []
        steps_frame = tk.Frame(self.sidebar, bg=BG_DARK)
        steps_frame.pack(pady=50, padx=30, anchor="w", fill="x")

        for i, name in enumerate(STEPS):
            row = tk.Frame(steps_frame, bg=BG_DARK)
            row.pack(fill="x", pady=12)

            dot = tk.Canvas(row, width=22, height=22, bg=BG_DARK, highlightthickness=0)
            dot.pack(side="left")
            circle = dot.create_oval(3, 3, 19, 19, outline=TEXT_LIGHT_MUTED, width=2)
            check = dot.create_text(11, 11, text="", fill="#ffffff",
                                     font=(FONT_FAMILY, 10, "bold"))

            lbl = tk.Label(row, text=name, bg=BG_DARK, fg=TEXT_LIGHT_MUTED,
                           font=(FONT_FAMILY, 11), anchor="w")
            lbl.pack(side="left", padx=10)

            self.step_labels.append((dot, circle, check, lbl))

        tk.Label(self.sidebar, text="Version 1.0.0", bg=BG_DARK, fg=TEXT_LIGHT_MUTED,
                 font=(FONT_FAMILY, 9)).pack(side="bottom", pady=20, padx=30, anchor="w")

    def update_sidebar(self, active_index):
        for i, (dot, circle, check, lbl) in enumerate(self.step_labels):
            if i < active_index:
                dot.itemconfig(circle, outline=ACCENT, fill=ACCENT)
                dot.itemconfig(check, text="✓", fill="#ffffff")
                lbl.config(fg=TEXT_LIGHT)
            elif i == active_index:
                dot.itemconfig(circle, outline=ACCENT, fill="")
                dot.itemconfig(check, text=str(i + 1), fill=ACCENT)
                lbl.config(fg="#ffffff", font=(FONT_FAMILY, 11, "bold"))
            else:
                dot.itemconfig(circle, outline=TEXT_LIGHT_MUTED, fill="")
                dot.itemconfig(check, text=str(i + 1), fill=TEXT_LIGHT_MUTED)
                lbl.config(fg=TEXT_LIGHT_MUTED, font=(FONT_FAMILY, 11, "normal"))

    # ---------- steps ---------- #
    def create_steps(self):
        # STEP 1 - Welcome
        f1 = tk.Frame(self.content, bg=BG_LIGHT)
        tk.Label(f1, text="Welcome to the Erfan Setup Wizard", font=(FONT_FAMILY, 20, "bold"),
                 bg=BG_LIGHT, fg=TEXT_MAIN, justify="left").pack(anchor="w", pady=(20, 10))
        tk.Label(f1,
                 text="This wizard will install the Erfan programming language\n"
                      "on your system and automatically add it to your PATH,\n"
                      "so you can run the erfan command from any terminal.",
                 font=(FONT_FAMILY, 11), bg=BG_LIGHT, fg=TEXT_MUTED,
                 justify="left").pack(anchor="w")
        self.frames.append(f1)

        # STEP 2 - Location
        f2 = tk.Frame(self.content, bg=BG_LIGHT)
        tk.Label(f2, text="Installation Location", font=(FONT_FAMILY, 20, "bold"),
                 bg=BG_LIGHT, fg=TEXT_MAIN).pack(anchor="w", pady=(20, 10))
        tk.Label(f2, text="Erfan will be installed to the following folder:",
                 font=(FONT_FAMILY, 11), bg=BG_LIGHT, fg=TEXT_MUTED).pack(anchor="w", pady=(0, 15))

        path_box = tk.Frame(f2, bg="#f3f4f6", highlightbackground="#e5e7eb",
                             highlightthickness=1)
        path_box.pack(fill="x", pady=5)
        self.path_label = tk.Label(path_box, text=get_app_dir(), bg="#f3f4f6", fg=TEXT_MAIN,
                                    font=(FONT_FAMILY, 10), anchor="w", padx=14, pady=12)
        self.path_label.pack(fill="x")

        tk.Label(f2, text="This folder will automatically be added to your PATH environment variable.",
                 font=(FONT_FAMILY, 9), bg=BG_LIGHT, fg=TEXT_MUTED).pack(anchor="w", pady=(10, 0))
        self.frames.append(f2)

        # STEP 3 - Install
        f3 = tk.Frame(self.content, bg=BG_LIGHT)
        tk.Label(f3, text="Ready to Install", font=(FONT_FAMILY, 20, "bold"),
                 bg=BG_LIGHT, fg=TEXT_MAIN).pack(anchor="w", pady=(20, 10))
        self.install_status = tk.Label(f3, text="Click Install to begin",
                                        font=(FONT_FAMILY, 11), bg=BG_LIGHT, fg=TEXT_MUTED)
        self.install_status.pack(anchor="w", pady=(0, 20))

        self.progress = ttk.Progressbar(f3, mode="determinate", length=400)
        self.progress.pack(pady=10, fill="x")
        self.frames.append(f3)

        # STEP 4 - Finish
        f4 = tk.Frame(self.content, bg=BG_LIGHT)
        tk.Label(f4, text="✓", font=(FONT_FAMILY, 40, "bold"),
                 bg=BG_LIGHT, fg=ACCENT).pack(pady=(30, 10))
        tk.Label(f4, text="Installation Complete", font=(FONT_FAMILY, 18, "bold"),
                 bg=BG_LIGHT, fg=TEXT_MAIN).pack()
        tk.Label(f4, text="Erfan has been installed on your system.\n"
                           "Close all open terminal/PowerShell windows and open a new one,\n"
                           "then run the erfan command.",
                 font=(FONT_FAMILY, 11), bg=BG_LIGHT, fg=TEXT_MUTED, justify="center").pack(pady=10)
        self.frames.append(f4)

        # style progress bar
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("TProgressbar", troughcolor="#e5e7eb", background=ACCENT,
                         thickness=8, bordercolor="#e5e7eb", lightcolor=ACCENT, darkcolor=ACCENT)

    def show_step(self, index):
        for f in self.frames:
            f.pack_forget()

        self.frames[index].pack(fill="both", expand=True)
        self.step = index
        self.update_sidebar(index)
        self.build_nav()

    def build_nav(self):
        for w in self.nav.winfo_children():
            w.destroy()

        index = self.step
        last = len(self.frames) - 1

        if 0 < index < last:
            RoundedButton(self.nav, "Back", command=self.back, primary=False).pack(side="left")

        if index < last - 1:
            RoundedButton(self.nav, "Next", command=self.next, primary=True).pack(side="right")

        if index == last - 1:
            RoundedButton(self.nav, "Install", command=self.install, primary=True, width=160).pack(side="right")

        if index == last:
            RoundedButton(self.nav, "Finish", command=self.destroy, primary=True, width=160).pack(side="right")

    def next(self):
        self.show_step(self.step + 1)

    def back(self):
        self.show_step(self.step - 1)

    # ---------- install flow with a smooth animated progress ---------- #
    def install(self):
        self.build_nav()  # remove buttons momentarily by disabling interaction
        for w in self.nav.winfo_children():
            w.destroy()
        self.install_status.config(text="Installing...")
        self.progress["value"] = 0
        self._animate_progress(0)

    def _animate_progress(self, value):
        if value < 70:
            self.progress["value"] = value
            self.after(15, self._animate_progress, value + 2)
        else:
            self._do_real_install()

    def _do_real_install(self):
        try:
            path = copy_exe()
            self.progress["value"] = 85
            add_to_path_registry(path)
            self._finish_progress(0)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.install_status.config(text="Installation failed")
            self.build_nav()

    def _finish_progress(self, value):
        target = 100
        cur = self.progress["value"]
        if cur < target:
            self.progress["value"] = cur + 3
            self.after(10, self._finish_progress, 0)
        else:
            self.install_status.config(text="Installation complete")
            self.after(300, lambda: self.show_step(3))


if __name__ == "__main__":
    if sys.platform != "win32":
        print("This installer is designed for Windows, but the UI can still run here.")
    app = Installer()
    app.mainloop()