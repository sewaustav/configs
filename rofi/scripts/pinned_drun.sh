#!/usr/bin/env bash

# --- pinned apps ---
pinned=(
    "Firefox:firefox"
    "Tilix:tilix"
    "Nemo:nemo"
)

for app in "${pinned[@]}"; do
    name="${app%%:*}"
    cmd="${app##*:}"
    echo -e "$name\x00icon\x1f${cmd}\x1finfo\x1f${cmd}"
done


# --- rest of drun ---
rofi -show drun -dump
