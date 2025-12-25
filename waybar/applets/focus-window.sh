#!/bin/sh

address=$1

# https://api.gtkd.org/gdk.c.types.GdkEventButton.button.html
button=$2

if [ $button -eq 1 ]; then
    hyprctl keyword cursor:no_warps true
    hyprctl dispatch focuswindow address:$address
    hyprctl keyword cursor:no_warps false
elif [ $button -eq 2 ]; then
    hyprctl dispatch closewindow address:$address
fi
