#!/bin/bash
touchpad="synaptics-tm3336-001"

while true; do
    if hyprctl devices | grep -q "instant-gxt-101-gaming-mouse"; then
        hyprctl keyword "device:$touchpad:enabled" false
    else
        hyprctl keyword "device:$touchpad:enabled" true
    fi
    sleep 5
done
