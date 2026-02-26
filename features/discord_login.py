import sys
import os
import time
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QLineEdit, QLabel, QFrame, QGraphicsDropShadowEffect, QHBoxLayout)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class DiscordTokenTool(QWidget):
    def __init__(self):
        super().__init__()

        # 1. Pencere Ayarları
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(450, 550)

        # 2. Ana Cam Gövde
        self.main_frame = QFrame(self)
        self.main_frame.setGeometry(10, 10, 430, 530)
        self.main_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(15, 15, 15, 190); 
                border: 1px solid rgba(255, 255, 255, 30); 
                border-radius: 40px;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(Qt.GlobalColor.black)
        self.main_frame.setGraphicsEffect(shadow)

        self.layout = QVBoxLayout(self.main_frame)
        self.layout.setContentsMargins(35, 25, 35, 35)
        self.layout.setSpacing(15)

        # --- KAPATMA BUTONU ---
        self.top_bar = QHBoxLayout()
        self.top_bar.addStretch()
        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 10);
                color: rgba(255, 255, 255, 150);
                border-radius: 15px;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover { background-color: rgba(255, 60, 60, 180); color: white; }
        """)
        self.close_btn.clicked.connect(self.close)
        self.top_bar.addWidget(self.close_btn)
        self.layout.addLayout(self.top_bar)

        # --- BAŞLIKLAR (Çizgisiz Temiz Yazı) ---
        self.title = QLabel("LIQUID LOGIN")
        self.title.setStyleSheet(
            "color: white; font-size: 26px; font-weight: 900; border: none; background: transparent;")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title)

        self.subtitle = QLabel("Safe connection via Token")
        self.subtitle.setStyleSheet(
            "color: rgba(255, 255, 255, 80); font-size: 12px; border: none; background: transparent;")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.subtitle)

        self.layout.addSpacing(25)

        # --- INPUT (Cam Efekti) ---
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("Paste token here...")
        self.token_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 7);
                border: 1px solid rgba(255, 255, 255, 15);
                border-radius: 15px;
                padding: 15px;
                color: white;
                font-size: 13px;
                selection-background-color: #007AFF;
            }
            QLineEdit:focus { border: 1px solid rgba(0, 122, 255, 60); }
        """)
        self.layout.addWidget(self.token_input)

        # --- LİQUİD GLASS BUTON ---
        self.login_btn = QPushButton("SİSTEME BAĞLAN")
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 10);
                color: #007AFF;
                border: 1px solid rgba(0, 122, 255, 50);
                border-radius: 20px;
                padding: 18px;
                font-size: 14px;
                font-weight: 800;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background-color: rgba(0, 122, 255, 25);
                border: 1px solid #007AFF;
                color: white;
            }
            QPushButton:pressed { background-color: rgba(0, 122, 255, 45); }
        """)
        self.login_btn.clicked.connect(self.automated_login)
        self.layout.addWidget(self.login_btn)

        self.layout.addStretch()

    def automated_login(self):
        token = self.token_input.text().strip().replace('"', '')
        if not token: return

        self.login_btn.setText("BAĞLANILIYOR...")

        try:
            chrome_options = Options()
            chrome_options.add_experimental_option("detach", True)
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--log-level=3")  # Gereksiz konsol yazılarını gizler

            driver = webdriver.Chrome(options=chrome_options)
            driver.get("https://discord.com/login")

            # Token Enjeksiyonu (3 saniye sonra otomatik login)
            script = """
            setTimeout(() => {
                function login(token) {
                    setInterval(() => {
                        document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
                    }, 50);
                    setTimeout(() => { location.reload(); }, 500);
                }
                login('%s');
            }, 2500);
            """ % token

            driver.execute_script(script)
            self.login_btn.setText("ERİŞİM SAĞLANDI")

        except Exception as e:
            self.login_btn.setText("HATA OLUŞTU!")
            print(f"Hata: {e}")

    # Sürükleme
    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiscordTokenTool()
    window.show()
    sys.exit(app.exec())