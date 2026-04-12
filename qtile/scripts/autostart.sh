#!/bin/bash

export XCURSOR_THEME="breeze_cursors"
export XCURSOR_SIZE=25
export XDG_CURRENT_DESKTOP=sway
export SCREENSHOT_TOOL=flameshot
dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP=sway

systemctl --user stop xdg-desktop-portal xdg-desktop-portal-gnome xdg-desktop-portal-wlr xdg-desktop-portal-gtk

systemctl --user restart pipewire wireplumber

/usr/lib/xdg-desktop-portal-wlr & 
sleep 1
/usr/lib/xdg-desktop-portal &
wl-paste --type text --watch cliphist store &
wl-paste --type image --watch cliphist store &
nm-applet &
blueman-applet &
swaync &
hypridle &

awww-daemon &
awww img /home/sewaustav/Pictures/wallpapers/japan-background-digital-art.jpg