#!/bin/bash

# Получаем список окон на текущем workspace
windows=$(hyprctl clients | grep "workspace: $(hyprctl activeworkspace | awk '{print $2}')" | awk '{print $4}' )

# Выбираем окно через wofi
selected=$(echo "$windows" | wofi --dmenu --prompt "Switch window: ")

# Фокусируем выбранное окно
if [ -n "$selected" ]; then
    hyprctl dispatch focuswindow address:$selected
fi
