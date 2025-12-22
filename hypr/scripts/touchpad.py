#!/usr/bin/env python
import os

import pyudev


def toggle_status(status: bool):
    with open("/home/sewaustav/.config/hypr/scripts/status.txt", "w") as file:
        file.write(str(int(status)))


output = os.popen("hyprctl devices").read().split("\n")

mice = []

command = "hyprctl keyword 'device[synaptics-tm3336-001]:enabled' "

for i in range(len(output)):
    if "Mouse at" in output[i]:
        mice.append(output[i + 1].strip("\t"))

if len(mice) > 1:
    res = os.popen(command + "'false'").read()
    toggle_status(False)
else:
    res = os.popen(command + "'true'").read()
    toggle_status(True)
active_devices = len(mice)

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem="input")

for device in iter(monitor.poll, None):
    res = device.action
    if device.properties.get("ID_INPUT_MOUSE") != "1":
        continue
    if res is not None:
        if res == "remove":
            os.popen(command + "'true'")
            toggle_status(True)
        elif res == "add":
            os.popen(command + "'false'")
            toggle_status(False)
        else:
            pass
