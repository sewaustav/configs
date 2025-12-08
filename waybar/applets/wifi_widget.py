#!/usr/bin/env python3
"""
Wi-Fi Manager с CSS стилизацией (QSS)
Установка: pip install PyQt6
или: sudo pacman -S python-pyqt6
"""

import sys
import subprocess
import threading
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QScrollArea,
    QFrame, QInputDialog
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject, QTimer
from PyQt6.QtGui import QFont


# Сигналы для обновления UI из другого потока
class Signals(QObject):
    networks_scanned = pyqtSignal(list)
    notification = pyqtSignal(str, str)


class WiFiManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.signals = Signals()
        self.signals.networks_scanned.connect(self.update_networks)
        self.signals.notification.connect(self.show_notification)

        self.setWindowTitle("Wi-Fi Manager")
        self.setFixedSize(550, 650)

        # Загружаем CSS из файла style.qss
        self.load_stylesheet()

        # Основной виджет
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = QWidget()
        header.setObjectName("header")
        header.setFixedHeight(70)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(25, 0, 25, 0)

        title = QLabel("📶 Wi-Fi Networks")
        title.setObjectName("title")
        title.setFont(QFont("SF Pro Display", 20, QFont.Weight.Bold))
        header_layout.addWidget(title)

        header_layout.addStretch()

        self.status_dot = QLabel("●")
        self.status_dot.setObjectName("statusDot")
        self.status_dot.setFont(QFont("SF Pro Display", 18))
        header_layout.addWidget(self.status_dot)

        main_layout.addWidget(header)

        # Controls
        controls = QWidget()
        controls.setObjectName("controls")
        controls_layout = QHBoxLayout(controls)
        controls_layout.setContentsMargins(20, 15, 20, 15)
        controls_layout.setSpacing(10)

        self.scan_btn = QPushButton("🔄 Scan")
        self.scan_btn.setObjectName("btnPrimary")
        self.scan_btn.clicked.connect(self.scan_networks)
        controls_layout.addWidget(self.scan_btn)

        disconnect_btn = QPushButton("❌ Disconnect")
        disconnect_btn.setObjectName("btnDanger")
        disconnect_btn.clicked.connect(self.disconnect_wifi)
        controls_layout.addWidget(disconnect_btn)

        redmi_btn = QPushButton("⚡ Redmi")
        redmi_btn.setObjectName("btnPurple")
        redmi_btn.clicked.connect(self.quick_connect_redmi)
        controls_layout.addWidget(redmi_btn)

        main_layout.addWidget(controls)

        # Scroll Area для сетей
        scroll = QScrollArea()
        scroll.setObjectName("scrollArea")
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.networks_container = QWidget()
        self.networks_container.setObjectName("networksContainer")
        self.networks_layout = QVBoxLayout(self.networks_container)
        self.networks_layout.setContentsMargins(20, 10, 20, 10)
        self.networks_layout.setSpacing(12)
        self.networks_layout.addStretch()

        scroll.setWidget(self.networks_container)
        main_layout.addWidget(scroll)

        # Notification
        self.notif_label = QLabel()
        self.notif_label.setObjectName("notification")
        self.notif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.notif_label.hide()
        main_layout.addWidget(self.notif_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.ensure_wifi_on()
        self.scan_networks()

    def load_stylesheet(self):
        """Загружаем CSS стили (QSS)"""
        qss = """
/* Main Window */
QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #1e1e2e, stop:1 #2a2a3e);
}

/* Header */
#header {
    background: rgba(40, 40, 50, 200);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

#title {
    color: #ffffff;
}

#statusDot {
    color: #4ade80;
}

/* Controls */
#controls {
    background: transparent;
}

QPushButton {
    padding: 12px 20px;
    border: none;
    border-radius: 12px;
    font-size: 14px;
    font-weight: bold;
    color: white;
    min-width: 100px;
    background-color: #000000;
}

QPushButton:hover {
    margin-top: -2px;
    margin-bottom: 2px;
}

QPushButton:pressed {
    margin-top: 0px;
    margin-bottom: 0px;
}

#btnPrimary {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #3b82f6, stop:1 #2563eb);
}

#btnPrimary:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #2563eb, stop:1 #1d4ed8);
}

#btnDanger {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #ef4444, stop:1 #dc2626);
}

#btnDanger:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #dc2626, stop:1 #b91c1c);
}

#btnPurple {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #8b5cf6, stop:1 #7c3aed);
}

#btnPurple:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #7c3aed, stop:1 #6d28d9);
}

#btnSuccess {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #10b981, stop:1 #059669);
    min-width: 90px;
}

#btnSuccess:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #059669, stop:1 #047857);
}

/* Scroll Area */
#scrollArea {
    background: transparent;
    border: none;
}

#networksContainer {
    background: transparent;
}

/* Network Card */
#networkCard {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 20px;
}

#networkCard:hover {
    background: rgba(255, 255, 255, 0.08);
}

#networkSsid {
    color: #ffffff;
    font-size: 16px;
    font-weight: bold;
}

#networkDetails {
    color: #94a3b8;
    font-size: 13px;
}

/* Notification */
#notification {
    background: rgba(59, 130, 246, 230);
    color: white;
    padding: 15px 30px;
    border-radius: 12px;
    font-weight: bold;
    margin: 15px;
}

#notification[type="success"] {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #10b981, stop:1 #059669);
}

#notification[type="error"] {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #ef4444, stop:1 #dc2626);
}

#notification[type="info"] {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #3b82f6, stop:1 #2563eb);
}

QScrollBar:vertical {
    background: transparent;
    width: 8px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(255, 255, 255, 0.3);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
"""
        self.setStyleSheet(qss)

    def run_command(self, cmd, show_stderr=False):
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            if show_stderr:
                print(f"Stderr: {e.stderr.strip()}")
            return None

    def ensure_wifi_on(self):
        self.run_command("nmcli radio wifi on")

    def scan_networks(self):
        self.scan_btn.setEnabled(False)
        self.scan_btn.setText("Scanning...")
        threading.Thread(target=self._scan_thread, daemon=True).start()

    def _scan_thread(self):
        self.ensure_wifi_on()
        self.run_command("nmcli device wifi list --rescan yes")
        output = self.run_command(
            "nmcli -t -f SSID,SIGNAL,SECURITY device wifi list | grep -v '^--'"
        )

        networks = []
        if output:
            for line in output.splitlines():
                parts = line.split(":")
                if len(parts) >= 3:
                    ssid = parts[0] or "<hidden>"
                    signal = parts[1]
                    security = parts[2]
                    networks.append({
                        'ssid': ssid,
                        'signal': signal,
                        'security': security
                    })

        self.signals.networks_scanned.emit(networks)

    def update_networks(self, networks):
        # Очищаем старые сети
        while self.networks_layout.count() > 1:
            item = self.networks_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not networks:
            no_net = QLabel("No networks found")
            no_net.setStyleSheet("color: #64748b; font-size: 14px;")
            no_net.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.networks_layout.insertWidget(0, no_net)
        else:
            for net in networks:
                self.create_network_card(net)

        self.scan_btn.setEnabled(True)
        self.scan_btn.setText("🔄 Scan")

    def create_network_card(self, network):
        card = QFrame()
        card.setObjectName("networkCard")
        card.setFixedHeight(80)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(18, 14, 18, 14)

        # Левая часть - инфо
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)

        ssid_label = QLabel(network['ssid'])
        ssid_label.setObjectName("networkSsid")
        info_layout.addWidget(ssid_label)

        detail_text = f"Signal: {network['signal']}%  •  {network['security'] or 'Open'}"
        detail_label = QLabel(detail_text)
        detail_label.setObjectName("networkDetails")
        info_layout.addWidget(detail_label)

        layout.addLayout(info_layout)
        layout.addStretch()

        # Кнопка подключения
        connect_btn = QPushButton("Connect")
        connect_btn.setObjectName("btnSuccess")
        connect_btn.clicked.connect(lambda: self.connect_to_network(network))
        layout.addWidget(connect_btn)

        self.networks_layout.insertWidget(self.networks_layout.count() - 1, card)

    def connect_to_network(self, network):
        ssid = network['ssid']
        uuid = self.get_uuid_for_ssid(ssid)

        if uuid:
            threading.Thread(
                target=self._connect_saved,
                args=(uuid, ssid),
                daemon=True
            ).start()
        else:
            password, ok = QInputDialog.getText(
                self, "Wi-Fi Password",
                f"Enter password for:\n{ssid}",
                echo=QInputDialog.EchoMode.Password
            )

            if ok:
                threading.Thread(
                    target=self._connect_new,
                    args=(ssid, password),
                    daemon=True
                ).start()

    def _connect_saved(self, uuid, ssid):
        result = self.run_command(f"nmcli connection up {uuid}", show_stderr=True)
        msg = f"Connected to {ssid}" if result else f"Failed to connect to {ssid}"
        msg_type = "success" if result else "error"
        self.signals.notification.emit(msg, msg_type)

    def _connect_new(self, ssid, password):
        if password:
            cmd = f'nmcli device wifi connect "{ssid}" password "{password}"'
        else:
            cmd = f'nmcli device wifi connect "{ssid}"'

        result = self.run_command(cmd, show_stderr=True)
        msg = f"Connected to {ssid}" if result else f"Failed to connect to {ssid}"
        msg_type = "success" if result else "error"
        self.signals.notification.emit(msg, msg_type)

    def get_uuid_for_ssid(self, ssid):
        cmd = f"nmcli -t -f NAME,UUID connection show | grep '^{ssid}:' | cut -d: -f2"
        uuid_output = self.run_command(cmd)
        return uuid_output.strip() if uuid_output else None

    def disconnect_wifi(self):
        threading.Thread(target=self._disconnect_thread, daemon=True).start()

    def _disconnect_thread(self):
        iface = self.run_command("nmcli -t -f NAME,TYPE device | grep wifi: | cut -d: -f1")
        if iface:
            self.run_command(f"nmcli device disconnect {iface}", show_stderr=True)
            self.signals.notification.emit("Disconnected", "info")
        else:
            self.signals.notification.emit("No Wi-Fi interface found", "error")

    def quick_connect_redmi(self):
        threading.Thread(target=self._redmi_connect_thread, daemon=True).start()

    def _redmi_connect_thread(self):
        self.ensure_wifi_on()
        uuid = "3cf025e5-0054-4980-9033-bac5de5cc1b9"
        if self.run_command(f"nmcli connection show {uuid}"):
            self.run_command(f"nmcli connection up {uuid}", show_stderr=True)
            self.signals.notification.emit("Connected to Redmi 10(sewa)", "success")
        else:
            cmd = 'nmcli device wifi connect "Redmi 10(sewa)" password "1234567890"'
            self.run_command(cmd, show_stderr=True)
            self.signals.notification.emit("Connected to Redmi 10(sewa)", "success")

    def show_notification(self, message, msg_type):
        self.notif_label.setText(message)
        self.notif_label.setProperty("type", msg_type)
        self.notif_label.setStyle(self.notif_label.style())  # Refresh style
        self.notif_label.show()

        QTimer.singleShot(3000, self.notif_label.hide)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WiFiManager()
    window.show()
    sys.exit(app.exec())