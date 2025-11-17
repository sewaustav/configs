#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys
import time
import tkinter as tk
from tkinter import ttk


def get_panel_data():
    return {
        "text": " [CP]",  # Unicode-иконка (шестерёнка) + текст. Если шрифт не тянет — " [CP]" или "🔧".
        "tooltip": "Control Panel: Click to open",
        "class": "control-panel",
    }


def open_gui():
    root = tk.Tk()
    root.title("Control Panel")
    root.geometry("200x150")
    root.resizable(False, False)

    frame = ttk.Frame(root, padding="10")
    # frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Button(frame, text="WiFi", command=lambda: print("WiFi toggled")).grid(
        row=0, column=0, pady=5, sticky=tk.W
    )
    ttk.Button(frame, text="Bluetooth", command=lambda: print("BT toggled")).grid(
        row=1, column=0, pady=5, sticky=tk.W
    )
    ttk.Button(frame, text="Volume", command=lambda: print("Volume adjusted")).grid(
        row=2, column=0, pady=5, sticky=tk.W
    )
    ttk.Button(frame, text="Close", command=root.destroy).grid(
        row=3, column=0, pady=10, sticky=tk.W
    )

    root.mainloop()


def handle_click(event_data):
    button = event_data.get("button", 0)
    if button == 1:
        open_gui()


if __name__ == "__main__":
    for line in sys.stdin:
        try:
            event = json.loads(line.strip())
            handle_click(event)
        except json.JSONDecodeError:
            pass

    while True:
        print(json.dumps(get_panel_data(), ensure_ascii=False))
        sys.stdout.flush()
        time.sleep(60)
