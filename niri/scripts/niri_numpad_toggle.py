#!/usr/bin/env python
import asyncio
from evdev import InputDevice, list_devices, ecodes
from pathlib import Path
import kdl

CONFIG_PATH = Path("~/.config/niri/keybinds.kdl").expanduser()
NUM_PAD_ON = f"""binds {{
}}"""

NUM_PAD_OFF = f"""binds {{
    KP_Right {{ focus-column-right; }}
    KP_Left {{ focus-column-left; }}
    KP_Up {{ focus-workspace-up; }}
    KP_Down {{ focus-workspace-down; }}
}}"""

def toggle(is_on: bool):
    config = ""
    if is_on:
        config = NUM_PAD_ON
    else:
        config = NUM_PAD_OFF
    with open(CONFIG_PATH, "w", encoding="utf-8") as file:
        file.write(config)
        
    
def find_keyboard():
    for path in list_devices():
        try:
            device = InputDevice(path)
            if ecodes.EV_LED in device.capabilities():
                if ecodes.LED_NUML in device.capabilities()[ecodes.EV_LED]:
                    return device
        except Exception:
            continue
    return None

async def watch_numlock(device):
    last_status = ecodes.LED_NUML in device.leds()
    
    async for event in device.async_read_loop():
        if event.type == ecodes.EV_LED and event.code == ecodes.LED_NUML:
            current_status = bool(event.value)
            if current_status != last_status:
                toggle(current_status)
                last_status = current_status

async def main():
    device = find_keyboard()
    if device:
        await watch_numlock(device)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass