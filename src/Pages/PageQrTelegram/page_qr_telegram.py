from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import qrcode
from time import time



class PageQrTelegram(QWidget):

    def __init__(self):
        super().__init__()

        self.session_id = int(time())
        img = qrcode.make(f'https://t.me/ur_he1per_bot?start={self.session_id}')
        img.save("./icons/tg_qr.png")


        self.qr_tg = QPixmap()
        self.qr_tg.load("./icons/tg_qr.png")
        self.initUI()

    def initUI(self):

        self.qr_label = QLabel()
        self.qr_label.setPixmap(self.qr_tg)

        info_font = QFont()
        info_font.setPixelSize(26)

        self.info_label = QLabel()
        self.info_label.setText("Для продолжения, отсканируйте qr-код")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.info_label.setFont(info_font)
        self.info_label.setWordWrap(True)


        placeholder_v = QWidget()
        placeholder_v.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        placeholder_v_1 = QWidget()
        placeholder_v_1.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        
        placeholder_h = QWidget()
        placeholder_h.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        placeholder_h_1 = QWidget()
        placeholder_h_1.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)


        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(placeholder_h)
        self.h_layout.addWidget(self.qr_label)
        self.h_layout.addWidget(placeholder_h_1)


        self.v_layout = QVBoxLayout(self)
        self.v_layout.addWidget(placeholder_v)
        self.v_layout.addWidget(self.info_label)
        self.v_layout.addLayout(self.h_layout)
        self.v_layout.addWidget(placeholder_v_1)
        

        