import sys
import os
import subprocess
import requests
import random
from PyQt6.QtCore import Qt, QPoint, QTimer, QEasingCurve, QPropertyAnimation
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QGraphicsDropShadowEffect,
                             QFrame, QScrollArea, QStackedWidget, QGridLayout, QLineEdit)

# --- ⚙️ AYARLAR ---
VERSION = "v1.1"
# Kendi GitHub linklerini buraya yapıştır
RAW_BASE_URL = "https://raw.githubusercontent.com/iVennyy/LiquidHub-V1/main"
GITHUB_VERSION_URL = f"{RAW_BASE_URL}/version.txt"

# --- 🚀 SPLASH SCREEN & UPDATE SYSTEM ---
class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(450, 300)

        self.frame = QFrame(self)
        self.frame.setGeometry(10, 10, 430, 280)
        self.frame.setStyleSheet("""
            QFrame {
                background-color: rgba(15, 15, 15, 240); 
                border: 1px solid rgba(0, 122, 255, 50); 
                border-radius: 30px;
            }
        """)

        self.layout = QVBoxLayout(self.frame)
        self.label = QLabel("LIQUID HUB\nKontrol Ediliyor...")
        self.label.setStyleSheet("color: white; font-size: 20px; font-weight: 900; background: transparent;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)

        self.status = QLabel("Versiyon: " + VERSION)
        self.status.setStyleSheet("color: rgba(255,255,255,100); font-size: 12px; background: transparent;")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.status)

        QTimer.singleShot(2000, self.check_updates)

    def check_updates(self):
        try:
            import random
            cache_buster = f"?v={random.randint(1000, 9999)}"
            response = requests.get(GITHUB_VERSION_URL + cache_buster, timeout=5)

            # Dosyayı parçalara ayır (v1.1 ve Değişiklikler)
            data = response.text.strip().split('|')
            remote_version = data[0]  # v1.1 kısmı
            changes = data[1:]  # Geri kalan tüm maddeler

            if remote_version != VERSION:
                self.label.setText("GÜNCELLEME BULUNDU!")

                # --- DEĞİŞİKLİKLERİ GÖSTEREN ALAN ---
                change_text = "Yenilikler:\n" + "\n".join([f"• {c}" for c in changes])
                self.change_label = QLabel(change_text)
                self.change_label.setStyleSheet(
                    "color: #34C759; font-size: 11px; margin-top: 10px; background: transparent;")
                self.change_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.layout.addWidget(self.change_label)
                # ------------------------------------

                self.btn_up = QPushButton("GÜNCELLEMEYİ BAŞLAT")
                self.btn_up.setCursor(Qt.CursorShape.PointingHandCursor)
                self.btn_up.setStyleSheet("""
                    QPushButton {
                        background: #007AFF; color: white; border-radius: 12px; 
                        padding: 12px; font-weight: bold; border: none; margin-top: 10px;
                    }
                    QPushButton:hover { background: #0056b3; }
                """)
                self.btn_up.clicked.connect(self.start_full_update)
                self.layout.addWidget(self.btn_up)
            else:
                self.label.setText("SİSTEM GÜNCEL")
                QTimer.singleShot(1000, self.open_key_system)
        except Exception as e:
            print(f"Update Hatası: {e}")
            self.label.setText("ÇEVRİMDIŞI MOD")
            QTimer.singleShot(1500, self.open_key_system)

    def start_full_update(self):
        self.label.setText("DOSYALAR İNDİRİLİYOR...")
        try:
            # 1. Ana Dosyayı Güncelle (arayuz.py)
            main_url = f"{RAW_BASE_URL}/arayuz.py"
            main_code = requests.get(main_url, timeout=10).text
            
            # Kendi çalıştığı dosyayı (arayuz.py) günceller
            with open(__file__, "w", encoding="utf-8") as f:
                f.write(main_code)

            # 2. Features Klasörünü Güncelle
            if not os.path.exists("features"):
                os.makedirs("features")
            
            # Güncellenmesini istediğin tüm dosyaların listesi
            # Buraya yeni bir dosya eklersen (örn: spammer.py) adını buraya da ekle
            feature_files = [
                "discord_login.py", 
                "webhook.py", 
                "checker.py", 
                "rpc.py", 
                "joiner.py"
            ]
            
            for file_name in feature_files:
                self.label.setText(f"GÜNCELLENİYOR:\n{file_name}")
                file_url = f"{RAW_BASE_URL}/features/{file_name}"
                
                f_response = requests.get(file_url, timeout=10)
                if f_response.status_code == 200:
                    with open(f"features/{file_name}", "w", encoding="utf-8") as f:
                        f.write(f_response.text)
                else:
                    print(f"Uyarı: {file_name} dosyası GitHub'da bulunamadı.")

            self.label.setText("HER ŞEY GÜNCEL!\nYeniden Başlatılıyor...")
            
            # 3. Programı Kapat ve Yeni Sürümü Aç
            QTimer.singleShot(2000, lambda: subprocess.Popen([sys.executable, __file__]))
            QTimer.singleShot(2100, sys.exit)

        except Exception as e:
            self.label.setText(f"GÜNCELLEME HATASI!")
            print(f"Detaylı Hata: {e}")

    def open_key_system(self):
        self.key_win = KeySystem()
        self.key_win.show()
        self.close()

# --- 🔑 PROFESYONEL KEY SİSTEMİ ---
class KeySystem(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(400, 350)

        self.frame = QFrame(self)
        self.frame.setGeometry(10, 10, 380, 330)
        self.frame.setStyleSheet("""
            QFrame {
                background-color: rgba(15, 15, 15, 225); 
                border: 1px solid rgba(255, 255, 255, 30); 
                border-radius: 30px;
            }
            QLabel, QLineEdit, QPushButton { border: none; background: transparent; }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(Qt.GlobalColor.black)
        self.frame.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self.frame)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title = QLabel("ERİŞİM SAĞLA")
        self.title.setStyleSheet("color: white; font-size: 22px; font-weight: 900; letter-spacing: 3px;")
        layout.addWidget(self.title)

        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Lisans anahtarını giriniz...")
        self.key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.key_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.key_input.setStyleSheet("background: rgba(255, 255, 255, 8); border: 1px solid rgba(255, 255, 255, 15); border-radius: 15px; padding: 15px; color: white;")
        layout.addWidget(self.key_input)

        self.login_btn = QPushButton("GİRİŞ YAP")
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.setFixedHeight(50)
        self.login_btn.setStyleSheet("background-color: rgba(0, 122, 255, 180); color: white; border-radius: 15px; font-weight: bold;")
        self.login_btn.clicked.connect(self.check_key)
        layout.addWidget(self.login_btn)

        self.status = QLabel("")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status)

    def check_key(self):
        if self.key_input.text().strip() == "bilader":
            self.status.setText("BAŞARIYLA GİRİŞ YAPILDI")
            self.status.setStyleSheet("color: #34C759;")
            self.anim = QPropertyAnimation(self, b"windowOpacity")
            self.anim.setDuration(800)
            self.anim.setStartValue(1.0)
            self.anim.setEndValue(0.0)
            self.anim.finished.connect(self.open_main_hub)
            self.anim.start()
        else:
            self.status.setText("ERİŞİM REDDEDİLDİ!")
            self.status.setStyleSheet("color: #FF3B30;")

    def open_main_hub(self):
        self.main_window = SafeLiquidGlass()
        self.main_window.show()
        self.close()

    def mousePressEvent(self, event): self.oldPos = event.globalPosition().toPoint()
    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()

# --- 🛡️ ANA HUB ---
class SafeLiquidGlass(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(1280, 720)
        self.setWindowOpacity(0.0)

        self.main_frame = QFrame(self)
        self.main_frame.setGeometry(10, 10, 1260, 700)
        self.main_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(12, 12, 12, 210); 
                border: 1px solid rgba(255, 255, 255, 30); 
                border-radius: 40px;
            }
        """)

        self.fade_in = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in.setDuration(600)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.start()

        self.main_layout = QHBoxLayout(self.main_frame)
        self.main_layout.setContentsMargins(25, 25, 25, 25)
        self.main_layout.setSpacing(20)

        # --- SIDEBAR (ORİJİNAL TASARIM) ---
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(260)
        self.sidebar.setStyleSheet("background: transparent; border: none;")
        self.sidebar_layout = QVBoxLayout(self.sidebar)

        self.brand = QLabel("LIQUID HUB")
        self.brand.setStyleSheet("color: white; font-size: 26px; font-weight: 900; background: transparent;")
        self.sidebar_layout.addWidget(self.brand, alignment=Qt.AlignmentFlag.AlignCenter)
        self.sidebar_layout.addSpacing(40)

        self.btn_discord = self.create_menu_btn("Discord")
        self.btn_discord.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        self.sidebar_layout.addWidget(self.btn_discord)

        for game in ["Minecraft", "CS 2", "Roblox"]:
            btn = self.create_menu_btn(game)
            btn.clicked.connect(lambda: self.pages.setCurrentIndex(0))
            self.sidebar_layout.addWidget(btn)

        self.sidebar_layout.addStretch()

        # --- SOL ALT KONTROLLER (ALTA ALMA BURADA) ---
        self.ctrl_layout = QHBoxLayout()
        self.ctrl_layout.setSpacing(10)

        self.min_btn = QPushButton("-")
        self.min_btn.setFixedSize(55, 55)
        self.min_btn.clicked.connect(self.showMinimized)
        self.min_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 10); color: white; border: 1px solid rgba(255, 255, 255, 20); 
                border-radius: 15px; font-size: 24px; font-weight: bold;
            }
            QPushButton:hover { background: rgba(255, 255, 255, 20); }
        """)

        self.exit_btn = QPushButton("✕")
        self.exit_btn.setFixedSize(55, 55)
        self.exit_btn.clicked.connect(self.close)
        self.exit_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 59, 48, 30); color: #FF3B30; border: 1px solid rgba(255, 59, 48, 60); 
                border-radius: 15px; font-size: 20px;
            }
            QPushButton:hover { background: rgba(255, 59, 48, 50); }
        """)

        self.ctrl_layout.addWidget(self.min_btn)
        self.ctrl_layout.addWidget(self.exit_btn)
        self.sidebar_layout.addLayout(self.ctrl_layout)

        # --- SAĞ PANEL ---
        self.pages = QStackedWidget()
        self.pages.setStyleSheet("background: transparent; border: none;")

        self.home_page = QFrame()
        h_layout = QVBoxLayout(self.home_page)
        welcome = QLabel(f"Hoş Geldin {os.getlogin().capitalize()}")
        welcome.setStyleSheet("color: white; font-size: 45px; font-weight: 200; background: transparent;")
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        h_layout.addWidget(welcome)

        self.discord_page = QFrame()
        d_layout = QVBoxLayout(self.discord_page)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background: transparent; border: none;")
        self.scroll_content = QFrame()
        self.grid = QGridLayout(self.scroll_content)
        self.grid.setSpacing(25)

        modules = [
            ("Discord Token Login", "Token ile hızlı tarayıcı girişi.", "features/discord_login.py"),
            ("Webhook Spammer", "Hızlı webhook mesaj gönderici.", "features/webhook.py"),
            ("Token Checker", "Token aktiflik kontrolcü.", "features/checker.py"),
            ("Discord RPC", "Güzel Görünümlü Discord RPC yapımı.", "features/rpc.py"),
            ("Server Joiner", "Otomatik sunucu katılımı.", "features/joiner.py"),
        ]

        for i, (title, desc, path) in enumerate(modules):
            card = self.create_square_card(title, desc, path)
            self.grid.addWidget(card, i // 2, i % 2)

        self.scroll.setWidget(self.scroll_content)
        d_layout.addWidget(self.scroll)

        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.discord_page)

        self.container = QFrame()
        self.container.setStyleSheet("background: rgba(255,255,255,8); border: 1px solid rgba(255,255,255,15); border-radius: 35px;")
        c_layout = QVBoxLayout(self.container)
        c_layout.addWidget(self.pages)

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.container)

    def create_menu_btn(self, text):
        btn = QPushButton(text)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        # BURASI KRİTİK: Senin orijinal tasarımını buraya birebir yapıştırdım
        btn.setStyleSheet("""
            QPushButton {
                color: white; background: rgba(255,255,255,10); border: none; 
                border-radius: 18px; padding: 15px; font-size: 15px; font-weight: 600;
            }
            QPushButton:hover { background: rgba(255,255,255,20); border-left: 4px solid #007AFF; }
        """)
        return btn

    def create_square_card(self, title, desc, path):
        card = QFrame()
        card.setFixedSize(420, 240)
        card.setStyleSheet("background: rgba(255,255,255,10); border: 1px solid rgba(255,255,255,15); border-radius: 25px;")
        l = QVBoxLayout(card)
        l.setContentsMargins(25, 25, 25, 25)
        t = QLabel(title); t.setStyleSheet("color: white; font-size: 20px; font-weight: 800; background: transparent; border: none;")
        d = QLabel(desc); d.setStyleSheet("color: rgba(255, 255, 255, 150); font-size: 13px; background: transparent; border: none;")
        b = QPushButton("YAZILIMI BAŞLAT")
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.setStyleSheet("background: rgba(0, 122, 255, 150); color: white; border-radius: 12px; font-weight: 900; height: 45px; border: none;")
        b.clicked.connect(lambda: self.run_script(path))
        l.addWidget(t); l.addWidget(d); l.addStretch(); l.addWidget(b)
        return card

    def run_script(self, path):
        if os.path.exists(path): subprocess.Popen([sys.executable, path])

    def mousePressEvent(self, event): self.oldPos = event.globalPosition().toPoint()
    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { outline: none; }")
    splash = SplashScreen()
    splash.show()

    sys.exit(app.exec())

