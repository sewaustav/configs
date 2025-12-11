#!/bin/bash
while true; do
    if hyprctl devices | grep -q "Mouse.*USB"; then
        echo "мышь подключена"
    else
        echo "мышь не подключена"
    fi
    sleep 5
done
