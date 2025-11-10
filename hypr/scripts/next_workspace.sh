#!/usr/bin/env bash
LOGFILE="/tmp/hypr_nextws.log"
TOTAL_WS=10
EXCLUDE_CLASSES=("chromium" "code-oss" "firefox")

log() { printf '%s %s\n' "$(date '+%F %T')" "$*" >>"$LOGFILE"; }

SOCKET="${XDG_RUNTIME_DIR}/hypr/${HYPRLAND_INSTANCE_SIGNATURE}/.socket2.sock"
log "=== start next_workspace.sh ==="
log "socket path: $SOCKET"

if [[ ! -S "$SOCKET" ]]; then
    log "ERROR: Socket not found: $SOCKET"
    exit 1
fi

# Слушаем сокет Hyprland (события в текстовом формате)
socat - UNIX-CONNECT:"$SOCKET" | while read -r line; do
    log "RAW: $line"

    # Ивент открытия окна
    if [[ "$line" =~ openwindow ]]; then
        addr=$(echo "$line" | grep -oE '0x[0-9a-fA-F]+')
        log "Detected openwindow -> address: $addr"
        [[ -z "$addr" ]] && continue

        # Определяем текущий workspace
        current_ws=$(hyprctl activeworkspace -j | jq '.id')
        next_ws=$((current_ws + 1))
        (( next_ws > TOTAL_WS )) && next_ws=1
        log "Current WS=$current_ws | Next WS=$next_ws"

        # Ждём, пока клиент появится в списке
        sleep 0.1
        win_class=$(hyprctl clients -j | jq -r ".[] | select(.address==\"$addr\") | .class")
        log "Window class: '$win_class'"

        if [[ -z "$win_class" || "$win_class" == "null" ]]; then
            log "Class not found, skipping"
            continue
        fi

        # Проверяем исключения
        for c in "${EXCLUDE_CLASSES[@]}"; do
            if [[ "${win_class,,}" == "${c,,}" ]]; then
                log "Class '$win_class' in exclude list, skip"
                continue 2
            fi
        done

        # Перемещаем
        log "Dispatch: movetoworkspace $next_ws,address:$addr"
        hyprctl dispatch movetoworkspace "$next_ws,address:$addr" 2>>"$LOGFILE" \
            && log "Moved successfully" \
            || log "Dispatch failed"
    fi
done
