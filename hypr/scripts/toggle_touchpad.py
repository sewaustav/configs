#!/usr/bin/env python
import os

status = 0
command = "hyprctl keyword 'device[synaptics-tm3336-001]:enabled' "

with open("/home/sewaustav/.config/hypr/scripts/status.txt", "r") as file:
    status = file.readline()

with open("/home/sewaustav/.config/hypr/scripts/status.txt", "w") as file:
    if status == "1":
        os.popen(command + "'false'")
        file.write("0")
    else:
        os.popen(command + "'true'")
        file.write("1")
