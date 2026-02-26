import sys
import requests
import threading
import time
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFrame, QLineEdit, QGraphicsDropShadowEffect)


class WebhookSpammer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(450, 600)

        self.spamming = False  # Çalışma kontrolü

        # Ana Gövde (Liquid Glass)
        self.main_frame = QFrame(self)
        self.main_frame.setGeometry(10, 10, 430, 580)
        self.main_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(15, 15, 15, 230); 
                border: 1px solid rgba(255, 255, 255, 25); 
                border-radius: 35px;
            }
            QLabel { color: white; background: transparent; border: none; }
        """)

        layout = QVBoxLayout(self.main_frame)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        # Header
        header = QHBoxLayout()
        title = QLabel("WEBHOOK SPAMMER")
        title.setStyleSheet("font-size: 18px; font-weight: 900; letter-spacing: 2px; color: #FF3B30;")
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet(
            "background: rgba(255,59,48,20); color: #FF3B30; border-radius: 10px; font-weight: bold; border: none;")
        header.addWidget(title);
        header.addStretch();
        header.addWidget(close_btn)
        layout.addLayout(header)

        layout.addSpacing(10)

        # Giriş Alanları
        self.webhook_url = self.create_input("Webhook URL:", "https://discord.com/api/webhooks/...")
        layout.addWidget(self.webhook_url)

        self.message_content = self.create_input("Gönderilecek Mesaj:", "Liquid Hub on Top!")
        layout.addWidget(self.message_content)

        self.delay_input = self.create_input("Gecikme (Saniye):", "0.5")
        layout.addWidget(self.delay_input)

        # Durum Bilgisi
        self.status_lbl = QLabel("Durum: Bekleniyor...")
        self.status_lbl.setStyleSheet("color: rgba(255,255,255,150); font-size: 12px;")
        self.status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_lbl)

        layout.addStretch()

        # Kontrol Butonları
        self.start_btn = QPushButton("SPAM BAŞLAT")
        self.start_btn.setFixedHeight(50)
        self.start_btn.clicked.connect(self.toggle_spam)
        self.start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_btn.setStyleSheet("""
            QPushButton { 
                background: #34C759; color: white; border-radius: 15px; font-weight: 900; border: none;
            }
            QPushButton:hover { background: #28a745; }
        """)
        layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("DURDUR")
        self.stop_btn.setFixedHeight(50)
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_spam)
        self.stop_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.stop_btn.setStyleSheet("""
            QPushButton { background: rgba(255,255,255,10); color: white; border-radius: 15px; font-weight: 900; border: none; }
            QPushButton:disabled { color: rgba(255,255,255,30); }
        """)
        layout.addWidget(self.stop_btn)

    def create_input(self, label_text, placeholder):
        container = QWidget()
        l = QVBoxLayout(container)
        l.setContentsMargins(0, 0, 0, 0);
        l.setSpacing(5)
        lbl = QLabel(label_text)
        lbl.setStyleSheet("font-size: 11px; color: rgba(255,255,255,120); font-weight: bold; margin-left: 5px;")
        edit = QLineEdit()
        edit.setPlaceholderText(placeholder)
        edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        edit.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 8); border: 1px solid rgba(255, 255, 255, 12);
                border-radius: 12px; padding: 12px; color: white;
            }
            QLineEdit:focus { border: 1px solid #FF3B30; }
        """)
        l.addWidget(lbl);
        l.addWidget(edit)
        container.input_field = edit
        return container

    def toggle_spam(self):
        url = self.webhook_url.input_field.text()
        msg = self.message_content.input_field.text()

        if not url.startswith("https://"):
            self.status_lbl.setText("HATA: Geçersiz Webhook URL!")
            return

        self.spamming = True
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.start_btn.setText("SPAM AKTİF...")

        # Spam işlemini ayrı bir thread'de başlat ki arayüz donmasın
        threading.Thread(target=self.spam_logic, daemon=True).start()

    def stop_spam(self):
        self.spamming = False
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.start_btn.setText("SPAM BAŞLAT")
        self.status_lbl.setText("Durum: Durduruldu.")

    def spam_logic(self):
        url = self.webhook_url.input_field.text()
        msg = self.message_content.input_field.text()
        try:
            delay = float(self.delay_input.input_field.text())
        except:
            delay = 1.0

        count = 0
        while self.spamming:
            try:
                response = requests.post(url, json={"content": msg})
                if response.status_code == 204:
                    count += 1
                    self.status_lbl.setText(f"Başarıyla Gönderildi: {count}")
                elif response.status_code == 429:  # Rate Limit
                    self.status_lbl.setText("Rate Limit! Bekleniyor...")
                    time.sleep(2)
                else:
                    self.status_lbl.setText(f"Hata Kodu: {response.status_code}")
            except Exception as e:
                self.status_lbl.setText(f"Bağlantı Hatası!")
                break

            time.sleep(delay)

    # Sürükleme
    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebhookSpammer()
    window.show()
    sys.exit(app.exec())