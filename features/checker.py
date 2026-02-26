import sys
import requests
from PyQt6.QtCore import Qt, QPoint, QTimer, QPropertyAnimation
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFrame, QLineEdit, QGraphicsDropShadowEffect)


class TokenChecker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(500, 600)

        # Ana Arkaplan Paneli
        self.main_frame = QFrame(self)
        self.main_frame.setGeometry(10, 10, 480, 580)
        self.main_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(15, 15, 15, 230); 
                border: 1px solid rgba(0, 122, 255, 60); 
                border-radius: 35px;
            }
        """)

        self.layout = QVBoxLayout(self.main_frame)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(15)

        # Başlık
        self.title = QLabel("TOKEN CHECKER")
        self.title.setStyleSheet("color: white; font-size: 24px; font-weight: 900; letter-spacing: 2px;")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title)

        # Token Giriş Alanı
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("Discord Tokenini Yapıştır...")
        self.token_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 10); border: 1px solid rgba(255, 255, 255, 20);
                border-radius: 15px; padding: 15px; color: white; font-size: 13px;
            }
        """)
        self.layout.addWidget(self.token_input)

        # Sorgula Butonu
        self.check_btn = QPushButton("SORGULA")
        self.check_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.check_btn.setFixedHeight(50)
        self.check_btn.setStyleSheet("""
            QPushButton {
                background: rgba(0, 122, 255, 180); color: white; border-radius: 15px; font-weight: bold;
            }
            QPushButton:hover { background: rgba(0, 122, 255, 230); }
        """)
        self.check_btn.clicked.connect(self.start_checking)
        self.layout.addWidget(self.check_btn)

        # Bilgi Ekranı (Sonuçların çıkacağı yer)
        self.result_box = QFrame()
        self.result_box.setStyleSheet(
            "background: rgba(255, 255, 255, 5); border-radius: 20px; border: 1px solid rgba(255, 255, 255, 10);")
        self.result_layout = QVBoxLayout(self.result_box)

        self.info_label = QLabel("Bekleniyor...")
        self.info_label.setStyleSheet("color: rgba(255, 255, 255, 150); font-size: 13px;")
        self.info_label.setWordWrap(True)
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.result_layout.addWidget(self.info_label)

        self.layout.addWidget(self.result_box)

        # Kapatma Butonu
        self.close_btn = QPushButton("KAPAT")
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setStyleSheet(
            "color: rgba(255, 59, 48, 200); background: transparent; font-weight: bold; border: none;")
        self.layout.addWidget(self.close_btn)

    def start_checking(self):
        token = self.token_input.text().strip()
        if not token:
            self.info_label.setText("⚠️ Lütfen bir token girin!")
            return

        self.info_label.setText("⏳ Kullanıcı bilgileri toplanıyor...")
        self.check_btn.setEnabled(False)

        # Gerçekçilik için 1.5 saniye gecikme (Senin istediğin o "toplanıyor" hissi)
        QTimer.singleShot(1500, lambda: self.fetch_discord_data(token))

    def fetch_discord_data(self, token):
        try:
            headers = {"Authorization": token, "Content-Type": "application/json"}
            res = requests.get("https://discord.com/api/v9/users/@me", headers=headers)

            if res.status_code == 200:
                data = res.json()

                # Bilgileri Hazırla
                username = f"{data['username']}#{data['discriminator']}"
                user_id = data['id']
                email = data.get('email', 'Yok')
                phone = data.get('phone', 'Yok')
                mfa = "Aktif" if data['mfa_enabled'] else "Devre Dışı"
                nitro = "Var" if "premium_type" in data and data['premium_type'] > 0 else "Yok"

                # Şık Bir Liste Hazırla
                summary = (
                    f"✅ **DURUM:** AKTİF\n\n"
                    f"👤 **Kullanıcı:** {username}\n"
                    f"🆔 **ID:** {user_id}\n"
                    f"📧 **E-Posta:** {email}\n"
                    f"📱 **Telefon:** {phone}\n"
                    f"🔐 **2FA:** {mfa}\n"
                    f"💎 **Nitro:** {nitro}"
                )
                self.info_label.setText(summary)
                self.info_label.setStyleSheet("color: #34C759; font-size: 14px; line-height: 150%;")
            else:
                self.info_label.setText("❌ GEÇERSİZ TOKEN!\nLütfen doğru girdiğinizden emin olun.")
                self.info_label.setStyleSheet("color: #FF3B30; font-size: 14px;")

        except Exception as e:
            self.info_label.setText(f"☢️ Hata: {str(e)}")

        self.check_btn.setEnabled(True)

    # Pencereyi sürükleme özelliği
    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TokenChecker()
    window.show()
    sys.exit(app.exec())