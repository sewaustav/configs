#!/bin/bash

app=$(hyprctl activewindow -j | jq -r '.class')

hyprctl dispatch togglefloating

if [[ "$app" == "kitty" ]]; then
    hyprctl dispatch resizeactive exact 800 520
else
    hyprctl dispatch resizeactive exact 800 600
fi

hyprctl dispatch centerwindow
