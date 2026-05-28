#!/usr/bin/env python
from pathlib import Path
import subprocess 
import kdl

DARK_THEME = 'catppuccin-mocha-blue-standard+default'
LIGHT_THEME = 'catppuccin-latte-blue-standard+default'
CONFIG_PATH = Path("~/.config/niri/theme.kdl").expanduser()

def set_niri(color:str):
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        config = kdl.parse(file.read())
        overview_node = config["overview"]
        backdrop_node = overview_node.get("backdrop-color")
        
        if backdrop_node:
            backdrop_node.args[0] = color

    with open(CONFIG_PATH, "w", encoding="utf-8") as file:
        file.write(str(config))
    

def toggle_theme(theme):
    current_theme = theme.split()[1].strip("'")
    print(current_theme)
    if "prefer-dark" in theme:
        set_dark()
        set_niri("#000000")
        
    else: 
        set_light()
        set_niri("#f5f5f5")

def set_dark():
    subprocess.run(['gsettings', 'set', 'org.gnome.desktop.interface', 'gtk-theme', DARK_THEME])

def set_light():
    subprocess.run(['gsettings', 'set', 'org.gnome.desktop.interface', 'gtk-theme', LIGHT_THEME])

process = subprocess.Popen(
    ['gsettings', 'monitor', 'org.gnome.desktop.interface', 'color-scheme'],
    stdout=subprocess.PIPE,
    text=True
)

while True:
    line = process.stdout.readline()
    if not line:
        break
    toggle_theme(line)
