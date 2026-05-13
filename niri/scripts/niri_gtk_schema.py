#!/usr/bin/env python
import subprocess 

DARK_THEME = 'catppuccin-mocha-blue-standard+default'
LIGHT_THEME = 'catppuccin-latte-blue-standard+default'


def toggle_theme(theme):
    current_theme = theme.split()[1].strip("'")
    print(current_theme)
    if "prefer-dark" in theme:
        set_dark()
        
    else: 
        set_light()

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
