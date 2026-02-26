import sys
import requests
import time
from PyQt6.QtCore import Qt, QPoint, QTimer, QThread, pyqtSignal
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFrame, QLineEdit, QTextEdit)


class JoinWorker(QThread):
    status_signal = pyqtSignal(str)

    def __init__(self, token, invite_list):
        super().__init__()
        self.token = token
        self.invite_list = invite_list

    def run(self):
        # Header kısmına 'User-Agent' ekledik ki Discord bizi bot sanıp hemen engellemesin
        headers = {
            "Authorization": self.token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        for invite in self.invite_list:
            # Akıllı Ayıklama: Linkten sadece kodu alır (Örn: discord.gg/craftrise -> craftrise)
            clean_code = invite.strip().split('/')[-1]
            if not clean_code: continue

            self.status_signal.emit(f"⏳ {clean_code} sunucusuna giriliyor...")

            try:
                # Discord Join API
                res = requests.post(
                    f"https://discord.com/api/v9/invites/{clean_code}",
                    headers=headers,
                    json={}  # Boş JSON gövdesi şart
                )

                if res.status_code == 200:
                    self.status_signal.emit(f"✅ Başarılı: {clean_code}")
                elif res.status_code == 403:
                    self.status_signal.emit(f"❌ Hata: Captcha/Doğrulama Gerekli")
                elif res.status_code == 401:
                    self.status_signal.emit(f"❌ Hata: Geçersiz Token")
                else:
                    self.status_signal.emit(f"❌ Hata ({res.status_code}): {clean_code}")
            except Exception as e:
                self.status_signal.emit(f"☢️ Bağlantı Hatası!")

            time.sleep(3)  # Ban riskine karşı süreyi biraz artırdım


class ServerJoiner(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(500, 650)

        # ANA PANEL - DIŞ ÇİZGİLER SIFIRLANDI
        self.main_frame = QFrame(self)
        self.main_frame.setGeometry(10, 10, 480, 630)
        self.main_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(15, 15, 15, 235); 
                border: none; 
                border-radius: 35px;
            }
        """)

        layout = QVBoxLayout(self.main_frame)
        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(15)

        self.title = QLabel("SERVER JOINER")
        self.title.setStyleSheet("color: white; font-size: 24px; font-weight: 900; letter-spacing: 2px; border: none;")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)

        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("Hesap Tokenini Giriniz...")
        self.token_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 8); 
                border: none; 
                border-radius: 15px; 
                padding: 15px; 
                color: white;
            }
        """)
        layout.addWidget(self.token_input)

        self.label_desc = QLabel("Sunucu Linklerini Alt Alta Yazın:")
        self.label_desc.setStyleSheet("color: rgba(255,255,255,120); font-size: 11px; border: none;")
        layout.addWidget(self.label_desc)

        self.invite_input = QTextEdit()
        self.invite_input.setPlaceholderText("discord.gg/craftrise\ndiscord.gg/liquid")
        self.invite_input.setStyleSheet("""
            QTextEdit {
                background: rgba(255, 255, 255, 5); 
                border: none; 
                border-radius: 15px; 
                padding: 12px; 
                color: #34C759; 
                font-family: Consolas;
            }
        """)
        layout.addWidget(self.invite_input)

        self.join_btn = QPushButton("KATILIMI BAŞLAT")
        self.join_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.join_btn.setFixedHeight(55)
        self.join_btn.setStyleSheet("""
            QPushButton {
                background: rgba(0, 122, 255, 180); 
                color: white; 
                border-radius: 15px; 
                font-weight: bold; 
                border: none;
            }
            QPushButton:hover { background: rgba(0, 122, 255, 240); }
        """)
        self.join_btn.clicked.connect(self.start_joining)
        layout.addWidget(self.join_btn)

        self.log_area = QLabel("Sistem Hazır.")
        self.log_area.setStyleSheet("color: rgba(255,255,255,100); font-size: 12px; border: none;")
        self.log_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.log_area)

        self.close_btn = QPushButton("GERİ DÖN")
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setStyleSheet(
            "color: #FF3B30; background: transparent; border: none; font-weight: bold; margin-top: 5px;")
        layout.addWidget(self.close_btn)

    def start_joining(self):
        token = self.token_input.text().strip()
        invites = self.invite_input.toPlainText().split('\n')
        invites = [i.strip() for i in invites if i.strip()]

        if not token or not invites:
            self.log_area.setText("⚠️ Token veya linkler eksik!")
            return

        self.join_btn.setEnabled(False)
        self.worker = JoinWorker(token, invites)
        self.worker.status_signal.connect(self.log_area.setText)
        self.worker.finished.connect(lambda: self.join_btn.setEnabled(True))
        self.worker.start()

    def mousePressEvent(self, event): self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ServerJoiner()
    win.show()
    sys.exit(app.exec())