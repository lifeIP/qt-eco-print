from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import qrcode
from time import time



class PageQrTelegram(QWidget):

    def __init__(self):
        super().__init__()

        self.exit_pixmap = QPixmap()
        self.exit_pixmap.load("./icons/exit.png")
        
        self.qr_tg = QPixmap()

        self.font_label = QFont()
        self.font_label.setPixelSize(45)

        self.initUI()



    signal_back_clicked = Signal()
    Slot()
    def slot_back_clicked(self):
        self.signal_back_clicked.emit()
    

    signal_set_session_id = Signal(int)
    Slot()
    def slot_generate_qr(self):
        self.session_id = int(time())
        self.signal_set_session_id.emit(self.session_id)
        img = qrcode.make(f'https://t.me/ur_he1per_bot?start={self.session_id}')
        img.save("./icons/tg_qr.png")
        
        self.qr_tg.load("./icons/tg_qr.png")
        self.qr_label.setPixmap(self.qr_tg)


    def initUI(self):

        self.qr_label = QLabel()
        

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


        self.btn_back = QPushButton("Назад")
        self.btn_back.setIcon(QIcon(self.exit_pixmap))
        self.btn_back.setIconSize(QSize(60,60))
        self.btn_back.setFont(self.font_label)
        self.btn_back.clicked.connect(self.slot_back_clicked)

        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(placeholder_h)
        self.h_layout.addWidget(self.qr_label)
        self.h_layout.addWidget(placeholder_h_1)


        self.v_layout = QVBoxLayout(self)
        self.v_layout.addWidget(placeholder_v)
        self.v_layout.addWidget(self.info_label)
        self.v_layout.addLayout(self.h_layout)
        self.v_layout.addWidget(placeholder_v_1)
        self.v_layout.addWidget(self.btn_back)
        

        