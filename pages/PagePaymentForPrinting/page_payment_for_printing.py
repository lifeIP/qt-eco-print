from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import qrcode
from time import time

class PagePaymentForPrinting(QWidget):
    def __init__(self):
        super().__init__()

        
        # img = qrcode.make(f'')
        # img.save("./icons/tg_qr.png")

        self.qr_tg = QPixmap()
        # self.qr_tg.load("./icons/payment_qr.png")

        self.exit_pixmap = QPixmap()
        self.exit_pixmap.load("./icons/exit.png")

        self.font_label = QFont()
        self.font_label.setPixelSize(45)

        self.price:float = 5.0
        self.count:int = 9999

        self.initUI()



    signal_back_clicked = Signal()
    Slot()
    def slot_back_clicked(self):
        self.signal_back_clicked.emit()


    Slot()
    def slot_generate_qr(self):
        # self.session_id = int(time())
        # img = qrcode.make(f'https://t.me/ur_he1per_bot?start={self.session_id}')
        # img.save("./icons/tg_qr.png")
        
        self.qr_tg.load("./icons/payment_qr.png")
        self.qr_label.setPixmap(self.qr_tg)


    signal_payment_done = Signal()
    Slot()
    def slot_payment_done(self):
        self.signal_payment_done.emit()
    

    Slot(int)
    def slot_change_count_of_pages(self, count:int):
        self.count:int = count
        self.label_sum.setText(f"Итого: {self.count * self.price}₽")
        self.label_math.setText(f"{int(self.count)} листов x {self.price}₽ = {self.count * self.price}₽")

    def initUI(self):

        self.label_header = QLabel("Оплата по QR")
        self.label_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_header.setFont(self.font_label)

        self.label_header_2 = QLabel("Печать начнется после оплаты")
        self.label_header_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_header_2.setFont(QFont("Arial", 16))

        self.qr_label = QLabel()


        self.label_sum = QLabel(f"Итого: {self.count * self.price}₽")
        self.label_sum.setFont(QFont("Arial", 30))
        self.label_sum.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_math = QLabel("45 листов x 5₽ = 225₽")
        self.label_math.setFont(QFont("Arial", 10))
        self.label_math.setAlignment(Qt.AlignmentFlag.AlignCenter)


        self.btn_payment_is_done = QPushButton("ОТЛАДОЧНАЯ КНОПКА. ЕЁ НЕ ДОЛЖНО БЫТЬ В ГОТОВОМ ПРОДУКТЕ")
        self.btn_payment_is_done.clicked.connect(self.slot_payment_done)

        self.btn_back = QPushButton("Назад")
        self.btn_back.setIcon(self.exit_pixmap)
        self.btn_back.setIconSize(QSize(60,60))
        self.btn_back.setFont(self.font_label)
        self.btn_back.clicked.connect(self.slot_back_clicked)


        placeholder_v = QWidget()
        placeholder_v.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        placeholder_v_1 = QWidget()
        placeholder_v_1.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        placeholder_v_2 = QWidget()
        placeholder_v_2.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)


        placeholder_h = QWidget()
        placeholder_h.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        placeholder_h_1 = QWidget()
        placeholder_h_1.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)

        
        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(placeholder_h)
        self.h_layout.addWidget(self.qr_label)
        self.h_layout.addWidget(placeholder_h_1)


        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addWidget(self.label_header)
        self.mainLayout.addWidget(self.label_header_2)
        self.mainLayout.addWidget(placeholder_v)
        self.mainLayout.addLayout(self.h_layout)
        self.mainLayout.addWidget(placeholder_v_1)
        self.mainLayout.addWidget(self.label_sum)
        self.mainLayout.addWidget(self.label_math)
        self.mainLayout.addWidget(placeholder_v_2)
        self.mainLayout.addWidget(self.btn_payment_is_done)
        self.mainLayout.addWidget(self.btn_back)
        