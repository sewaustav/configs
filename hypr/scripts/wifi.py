#!/usr/bin/env python3
import subprocess
import sys
import os

# === Настройки ===
ROFI_THEME_PATH = os.path.expanduser("~/.config/rofi/network.rasi")

# === Утилиты ===
def run_command(cmd, show_stderr=False):
    """Запускает команду в shell и возвращает stdout"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if show_stderr:
            print(f"Stderr: {e.stderr.strip()}")
        print(f"Ошибка: {e}")
        return None

def rofi_menu(options, prompt="Выберите:", message=None, theme=ROFI_THEME_PATH):
    """Выводит Rofi меню и возвращает выбор"""
    cmd = ["rofi", "-dmenu", "-p", prompt, "-theme", theme]
    if message:
        cmd += ["-mesg", message]
    try:
        result = subprocess.run(cmd, input="\n".join(options), text=True, capture_output=True)
        return result.stdout.strip() if result.stdout.strip() else None
    except FileNotFoundError:
        print("❌ Rofi не найден. Установи его: sudo apt install rofi")
        sys.exit(1)

def ensure_wifi_on():
    run_command("nmcli radio wifi on")
    run_command("nmcli device wifi list --rescan yes", show_stderr=True)

def scan_wifi():
    ensure_wifi_on()
    output = run_command("nmcli -t -f SSID,SIGNAL,SECURITY device wifi list | grep -v '^--'")
    if not output:
        run_command("notify-send 'Wi-Fi' 'Нет доступных сетей'")
        return None
    networks = []
    for line in output.splitlines():
        ssid, signal, sec = line.split(":")[:3]
        ssid = ssid or "<скрытая>"
        networks.append(f"{ssid}  ({signal}%)  {sec}")
    return networks

def get_uuid_for_ssid(ssid):
    cmd = f"nmcli -t -f NAME,UUID connection show | grep '^{ssid}:' | cut -d: -f2"
    uuid_output = run_command(cmd)
    return uuid_output.strip() if uuid_output else None

def connect_wifi():
    ensure_wifi_on()
    networks = scan_wifi()
    if not networks:
        return
    ssid_choice = rofi_menu(networks, prompt="Выберите сеть:")
    if not ssid_choice:
        return
    ssid = ssid_choice.split("  (")[0].strip()
    uuid = get_uuid_for_ssid(ssid)

    if uuid:
        run_command(f"nmcli connection up {uuid}", show_stderr=True)
        run_command(f"notify-send 'Wi-Fi' 'Подключено к {ssid}'")
        return

    password = subprocess.run(
        ["rofi", "-dmenu", "-p", f"Пароль для {ssid}", "-theme", ROFI_THEME_PATH],
        text=True,
        capture_output=True
    ).stdout.strip()

    if password:
        cmd = f'nmcli device wifi connect "{ssid}" password "{password}"'
    else:
        cmd = f'nmcli device wifi connect "{ssid}"'

    run_command(cmd, show_stderr=True)
    run_command(f"notify-send 'Wi-Fi' 'Подключено к {ssid}'")

def disconnect_wifi():
    iface = run_command("nmcli -t -f NAME,TYPE device | grep wifi: | cut -d: -f1")
    if iface:
        run_command(f"nmcli device disconnect {iface}", show_stderr=True)
        run_command("notify-send 'Wi-Fi' 'Отключено'")
    else:
        run_command("notify-send 'Wi-Fi' 'Не найден Wi-Fi интерфейс'")

def quick_connect_redmi():
    ensure_wifi_on()
    uuid = "3cf025e5-0054-4980-9033-bac5de5cc1b9"
    if run_command(f"nmcli connection show {uuid}"):
        run_command(f"nmcli connection up {uuid}", show_stderr=True)
        run_command("notify-send 'Wi-Fi' 'Подключено к Redmi 10(sewa)'")
    else:
        cmd = 'nmcli device wifi connect "Redmi 10(sewa)" password "1234567890"'
        run_command(cmd, show_stderr=True)
        run_command("notify-send 'Wi-Fi' 'Создано новое подключение к Redmi 10(sewa)'")

def main():
    while True:
        choice = rofi_menu(
            ["📶 Сканировать сети", "🔌 Подключиться", "❌ Отключиться", "⚡ Быстро к Redmi", "🚪 Выход"],
            prompt="Wi-Fi Менеджер:"
        )
        if choice == "📶 Сканировать сети":
            nets = scan_wifi()
            if nets:
                rofi_menu(nets, prompt="Сети:", message="Нажми Enter для выхода")
        elif choice == "🔌 Подключиться":
            connect_wifi()
        elif choice == "❌ Отключиться":
            disconnect_wifi()
        elif choice == "⚡ Быстро к Redmi":
            quick_connect_redmi()
        elif not choice or choice == "🚪 Выход":
            sys.exit(0)

if __name__ == "__main__":
    main()
