import sys
import time
import os
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFrame, QLineEdit, QStackedWidget)
from pypresence import Presence


class DiscordRPCManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(500, 720)

        self.RPC = None

        # --- ANA DIŞ ÇERÇEVE (Sadece bu kalsın) ---
        self.main_frame = QFrame(self)
        self.main_frame.setGeometry(10, 10, 480, 700)
        self.main_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(15, 15, 15, 235); 
                border: 1px solid rgba(255, 255, 255, 25); 
                border-radius: 40px;
            }
            QLabel { color: white; background: transparent; border: none; }
        """)

        # Sayfa Yapısı (İç çerçeveleri tamamen kaldırdık)
        self.pages = QStackedWidget(self.main_frame)
        self.pages.setGeometry(20, 20, 440, 660)
        self.pages.setStyleSheet("background: transparent; border: none;")

        self.setup_rpc_page()
        self.setup_guide_page()
        self.pages.setCurrentIndex(0)

    def setup_rpc_page(self):
        # QFrame yerine QWidget kullanarak iç kenarlığı yok ettik
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(8)

        # Header
        header = QHBoxLayout()
        title = QLabel("DISCORD RPC ENGINE")
        title.setStyleSheet("font-size: 20px; font-weight: 900; color: #007AFF;")

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("background: rgba(255,59,48,20); color: #FF3B30; border-radius: 10px; border: none;")

        header.addWidget(title);
        header.addStretch();
        header.addWidget(close_btn)
        layout.addLayout(header)

        # Inputlar
        self.client_id_input = self.create_styled_input("Application ID (Zorunlu)", "ID'yi buraya yapıştırın...")
        layout.addWidget(self.client_id_input)

        self.state_input = self.create_styled_input("Durum (State)", "Oyun Oynuyor...")
        self.details_input = self.create_styled_input("Detaylar", "Liquid Hub v2")
        layout.addWidget(self.state_input);
        layout.addWidget(self.details_input)

        img_row = QHBoxLayout()
        self.large_img = self.create_styled_input("Büyük Resim", "logo", half=True)
        self.small_img = self.create_styled_input("Küçük Resim", "verified", half=True)
        img_row.addWidget(self.large_img);
        img_row.addWidget(self.small_img)
        layout.addLayout(img_row)

        self.btn_text = self.create_styled_input("Buton Yazısı", "Discord'a Katıl")
        self.btn_url = self.create_styled_input("Buton Linki", "https://")
        layout.addWidget(self.btn_text);
        layout.addWidget(self.btn_url)

        layout.addStretch()

        # Butonlar
        self.start_btn = QPushButton("SİSTEMİ BAĞLA")
        self.start_btn.setFixedHeight(50)
        self.start_btn.clicked.connect(self.connect_rpc)
        self.start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_btn.setStyleSheet(
            "background: #007AFF; color: white; border-radius: 15px; font-weight: 900; border: none;")
        layout.addWidget(self.start_btn)

        self.update_btn = QPushButton("AYARLARI SENKRONİZE ET")
        self.update_btn.setFixedHeight(50)
        self.update_btn.setEnabled(False)
        self.update_btn.clicked.connect(self.update_rpc)
        self.update_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_btn.setStyleSheet("""
            QPushButton { background: rgba(255,255,255,10); color: white; border-radius: 15px; font-weight: 900; border: none; }
            QPushButton:disabled { color: rgba(255,255,255,30); }
        """)
        layout.addWidget(self.update_btn)

        guide_btn = QPushButton("❓ Nasıl Yapılır?")
        guide_btn.setStyleSheet(
            "color: #00C6FF; font-size: 13px; font-weight: bold; background: transparent; border: none;")
        guide_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        guide_btn.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        layout.addWidget(guide_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.pages.addWidget(page)

    def setup_guide_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        title = QLabel("YARDIM & REHBER")
        title.setStyleSheet("font-size: 22px; font-weight: 900; color: #34C759;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        guide_text = QLabel(
            "1. ADIM: Discord Developer Portal'a git ve bir Application oluştur.\n\n"
            "2. ADIM: 'General Information' sekmesindeki APPLICATION ID'yi kopyala.\n\n"
            "3. ADIM: ID'yi ana ekrandaki en üst kutuya yapıştır.\n\n"
            "4. ADIM: Art Assets kısmına resim yükle ve ismini 'Büyük Resim' kutusuna yaz.\n\n"
            "5. ADIM: 'Sistemi Bağla' de. Discord açıksa AKTİF uyarısı verir.\n\n"
            "6. ADIM: Güncelleme yaptıkça 'Senkronize Et' butonuna bas."
        )
        guide_text.setWordWrap(True)
        guide_text.setStyleSheet("font-size: 14px; line-height: 22px; color: rgba(255,255,255,180);")
        layout.addWidget(guide_text)

        layout.addStretch()

        back_btn = QPushButton("⬅ GERİ DÖN")
        back_btn.setFixedHeight(50)
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        back_btn.setStyleSheet(
            "background: rgba(255,255,255,15); color: white; border-radius: 15px; font-weight: 900; border: none;")
        layout.addWidget(back_btn)

        self.pages.addWidget(page)

    def create_styled_input(self, label_text, placeholder, half=False):
        container = QWidget()
        l = QVBoxLayout(container)
        l.setContentsMargins(0, 0, 0, 0);
        l.setSpacing(4)

        lbl = QLabel(label_text)
        lbl.setStyleSheet("color: rgba(255,255,255,100); font-size: 11px; margin-left: 5px;")

        edit = QLineEdit()
        edit.setPlaceholderText(placeholder)
        edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        edit.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 8); 
                border: 1px solid rgba(255, 255, 255, 12);
                border-radius: 12px; padding: 10px; color: white;
            }
            QLineEdit:focus { border: 1px solid #007AFF; }
        """)
        l.addWidget(lbl);
        l.addWidget(edit)
        if half: container.setFixedWidth(210)
        container.input_field = edit
        return container

    def connect_rpc(self):
        c_id = self.client_id_input.input_field.text().strip()
        if not c_id:
            self.start_btn.setText("ID GİRMEDİNİZ!")
            return

        try:
            self.RPC = Presence(c_id)
            self.RPC.connect()
            self.start_btn.setText("BAĞLANTI AKTİF ✅")
            self.start_btn.setEnabled(False)
            self.client_id_input.input_field.setEnabled(False)
            self.update_btn.setEnabled(True)
        except Exception as e:
            self.start_btn.setText("DİSCORD AÇIK MI?")

    def update_rpc(self):
        if self.RPC:
            try:
                btns = []
                txt, url = self.btn_text.input_field.text(), self.btn_url.input_field.text()
                if txt and url.startswith("http"): btns.append({"label": txt, "url": url})

                self.RPC.update(
                    state=self.state_input.input_field.text() or "Liquid Hub",
                    details=self.details_input.input_field.text() or "Processing...",
                    large_image=self.large_img.input_field.text() or "logo",
                    small_image=self.small_img.input_field.text() or "verified",
                    buttons=btns if btns else None,
                    start=time.time()
                )
            except Exception as e:
                print(f"Hata: {e}")

    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiscordRPCManager()
    window.show()
    sys.exit(app.exec())