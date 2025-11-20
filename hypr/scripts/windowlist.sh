#!/bin/bash

# Функция поиска иконки через .desktop файл
find_icon_from_desktop() {
    local app_class="$1"
    local icon_name=""

    # Пути к .desktop файлам
    local desktop_dirs=(
        "$HOME/.local/share/applications"
        "/usr/share/applications"
        "/usr/local/share/applications"
        "/var/lib/flatpak/exports/share/applications"
        "$HOME/.local/share/flatpak/exports/share/applications"
    )

    # Варианты названий .desktop файлов
    local desktop_variants=(
        "${app_class}.desktop"
        "${app_class,,}.desktop"
        "$(echo $app_class | tr '[:upper:]' '[:lower:]').desktop"
    )

    # Ищем .desktop файл
    for dir in "${desktop_dirs[@]}"; do
        if [ -d "$dir" ]; then
            for variant in "${desktop_variants[@]}"; do
                if [ -f "$dir/$variant" ]; then
                    # Извлекаем Icon из .desktop файла
                    icon_name=$(grep -m 1 "^Icon=" "$dir/$variant" | cut -d'=' -f2)
                    if [ -n "$icon_name" ]; then
                        echo "$icon_name"
                        return 0
                    fi
                fi
            done
        fi
    done

    # Если не нашли точное совпадение, ищем по содержимому
    for dir in "${desktop_dirs[@]}"; do
        if [ -d "$dir" ]; then
            local found_file=$(grep -l "StartupWMClass=${app_class}" "$dir"/*.desktop 2>/dev/null | head -n1)
            if [ -n "$found_file" ]; then
                icon_name=$(grep -m 1 "^Icon=" "$found_file" | cut -d'=' -f2)
                if [ -n "$icon_name" ]; then
                    echo "$icon_name"
                    return 0
                fi
            fi
        fi
    done

    return 1
}

# Функция поиска полного пути к иконке в Papirus
find_icon_path() {
    local icon_name="$1"

    # Если это уже полный путь, возвращаем его
    if [ -f "$icon_name" ]; then
        echo "$icon_name"
        return 0
    fi

    # Приоритетные пути для Papirus
    local icon_dirs=(
        "/usr/share/icons/Papirus/48x48/apps"
        "/usr/share/icons/Papirus-Dark/48x48/apps"
        "/usr/share/icons/Papirus/32x32/apps"
        "/usr/share/icons/Papirus-Dark/32x32/apps"
        "$HOME/.local/share/icons/Papirus/48x48/apps"
        "$HOME/.icons/Papirus/48x48/apps"
    )

    # Ищем иконку
    for dir in "${icon_dirs[@]}"; do
        if [ -d "$dir" ]; then
            if [ -f "$dir/${icon_name}.svg" ]; then
                echo "$dir/${icon_name}.svg"
                return 0
            elif [ -f "$dir/${icon_name}.png" ]; then
                echo "$dir/${icon_name}.png"
                return 0
            fi
        fi
    done

    # Ищем в любых подпапках Papirus
    local found_icon=$(find /usr/share/icons/Papirus*/48x48/ -name "${icon_name}.*" 2>/dev/null | head -n1)
    if [ -n "$found_icon" ]; then
        echo "$found_icon"
        return 0
    fi

    return 1
}

# Получаем список окон из hyprctl
windows=$(hyprctl clients -j | jq -r '.[] | "\(.address)|\(.class)"')

# Формируем список для wofi с иконками
selection=$(echo "$windows" | while IFS='|' read -r address class; do
    # Сначала пробуем найти иконку через .desktop файл
    icon_name=$(find_icon_from_desktop "$class")

    # Если не нашли, используем class как имя иконки
    if [ -z "$icon_name" ]; then
        icon_name="$class"
    fi

    # Теперь ищем полный путь к иконке
    icon_path=$(find_icon_path "$icon_name")

    if [ -n "$icon_path" ]; then
        echo -e "img:$icon_path:text:$class"
    else
        echo "$class"
    fi
done | wofi --dmenu --conf ~/.config/wofi/window.conf --style ~/.config/wofi/style.css --prompt "Windows" --parse-search)

# Если что-то выбрано, переключаемся на это окно
if [ -n "$selection" ]; then
    # Убираем img: префикс если есть
    clean_selection=$(echo "$selection" | sed 's/img:.*:text://')

    # Получаем адрес выбранного окна
    address=$(echo "$windows" | grep -F "|${clean_selection}" | head -n1 | cut -d'|' -f1)

    if [ -n "$address" ]; then
        hyprctl dispatch focuswindow address:$address
    fi
fi
