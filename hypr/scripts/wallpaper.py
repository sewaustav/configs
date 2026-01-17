#!/usr/bin/env python
import os
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import subprocess

WALL_DIR = "/home/sewaustav/Pictures/wallpapers"
CONF_PATH = "/home/sewaustav/.config/hypr/hyprpaper.conf"

THUMB_WIDTH = 220
THUMB_HEIGHT = 130
CORNER_RADIUS = 20

class WallpaperPicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Hyprland Wallpaper Selector")
        self.root.geometry("950x700")
        self.root.configure(bg="#1e1e2e")

        self.canvas = tk.Canvas(root, bg="#1e1e2e", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)

        self.frame = tk.Frame(self.canvas, bg="#1e1e2e")
        self.canvas_window = self.canvas.create_window(0, 0, window=self.frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.root.bind_all("<Button-4>", self._on_mousewheel)
        self.root.bind_all("<Button-5>", self._on_mousewheel)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self.items = []
        self.load_wallpapers()

    def add_corners(self, im, rad):
        im = im.convert("RGBA")
        mask = Image.new('L', im.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0) + im.size, radius=rad, fill=255)
        im.putalpha(mask)
        return im

    def _on_mousewheel(self, event):
        if event.num == 4: self.canvas.yview_scroll(-1, "units")
        elif event.num == 5: self.canvas.yview_scroll(1, "units")

    def _on_canvas_configure(self, event):
        self.reorganize_grid()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def load_wallpapers(self):
        files = []
        try:
            with os.scandir(WALL_DIR) as entries:
                for entry in entries:
                    if entry.is_file() and entry.name.split(".")[-1].lower() in ["png", "jpg", "jpeg", "webp"]:
                        files.append(entry.name)
        except Exception as e:
            print(f"Ошибка папки: {e}")
            return

        for file in files:
            full_path = os.path.join(WALL_DIR, file)
            try:
                img = Image.open(full_path)
                img.thumbnail((THUMB_WIDTH * 2, THUMB_HEIGHT * 2), Image.Resampling.LANCZOS)

                w, h = img.size
                img = img.crop(((w - THUMB_WIDTH)//2, (h - THUMB_HEIGHT)//2,
                                (w + THUMB_WIDTH)//2, (h + THUMB_HEIGHT)//2))

                img = self.add_corners(img, CORNER_RADIUS)
                photo = ImageTk.PhotoImage(img)

                container = tk.Frame(self.frame, bg="#1e1e2e")
                btn = tk.Button(container, image=photo,
                                command=lambda p=full_path: self.set_wallpaper(p),
                                relief="flat", bg="#1e1e2e", activebackground="#313244",
                                bd=0, highlightthickness=0)
                btn.image = photo
                btn.pack(padx=5, pady=5)

                lbl = tk.Label(container, text=file[:18], fg="#cdd6f4", bg="#1e1e2e", font=("Arial", 9))
                lbl.pack(pady=(0, 10))

                self.items.append(container)
            except Exception as e:
                print(f"Файл {file} не загружен: {e}")

    def reorganize_grid(self):
        window_width = self.canvas.winfo_width()
        if window_width < 100: window_width = 900

        col_width = THUMB_WIDTH + 30
        cols = max(1, window_width // col_width)

        for i, item in enumerate(self.items):
            item.grid_forget()
            item.grid(row=i // cols, column=i % cols, padx=10, pady=5, sticky="n")

        for c in range(cols):
            self.frame.grid_columnconfigure(c, weight=1)

    def set_wallpaper(self, path):
        config_text = f"preload = {path}\n\nwallpaper {{\n    monitor = eDP-1\n    path = {path}\n}}\n\nsplash = false"
        with open(CONF_PATH, "w") as f:
            f.write(config_text)

        subprocess.run(["pkill", "hyprpaper"])
        subprocess.Popen(["hyprpaper"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = WallpaperPicker(root)
    root.after(100, lambda: app.canvas.configure(scrollregion=app.canvas.bbox("all")))
    root.mainloop()
