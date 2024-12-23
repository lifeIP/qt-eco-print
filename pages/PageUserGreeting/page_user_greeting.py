from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class PageUserGreeting(QWidget):

    def resizeEvent(self, event):
        self.btn_usb.setIconSize(QSize(self.btn_usb.size().height() / 1.25, self.btn_usb.size().height() / 1.25))
        self.btn_tg.setIconSize(QSize(self.btn_tg.size().height() / 1.75, self.btn_tg.size().height() / 1.75))
        QWidget.resizeEvent(self, event)
    

    signal_btn_usb_clicked = Signal()
    signal_btn_tg_clicked = Signal()


    Slot()
    def slot_btn_usb_clicked(self):
        if self.flag == 0:
            self.msgBox.exec()
            
        else: 
            self.signal_btn_usb_clicked.emit()

    Slot()
    def slot_btn_tg_clicked(self):
        self.signal_btn_tg_clicked.emit()
        
    
    Slot(int)
    def slot_set_flag(self, flag):
        self.flag = flag

    def __init__(self):
        super().__init__()
        self.flag = 0
        self.font_label = QFont()
        self.font_label.setPixelSize(45)
        self.initUI()
    
    def initUI(self):

        self.upper_label = QLabel("Выберите источник")
        self.upper_label.setFont(self.font_label)
        self.upper_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.msgBox = QMessageBox()
        self.msgBox.setText("Вставьте usb-накопитель")
        
        self.btn_usb = QPushButton()
        self.btn_usb.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.btn_usb.setIcon(QIcon('./icons/usb-drive.png'))
        self.btn_usb.setIconSize(QSize(int(self.btn_usb.size().height() / 1.25), int(self.btn_usb.size().height() / 1.25)))
        self.btn_usb.clicked.connect(self.slot_btn_usb_clicked)

        self.btn_tg = QPushButton()
        self.btn_tg.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.btn_tg.setIcon(QIcon('./icons/telegram.png'))
        self.btn_tg.setIconSize(QSize(int(self.btn_tg.size().height() / 1.75), int(self.btn_tg.size().height() / 1.75)))
        self.btn_tg.clicked.connect(self.slot_btn_tg_clicked)

        
        c_layout = QVBoxLayout()
        c_layout.addWidget(QWidget(), 2)
        c_layout.addWidget(self.btn_usb, 8)
        c_layout.addWidget(self.btn_tg, 8)
        c_layout.addWidget(QWidget(), 2)

        c2_layout = QHBoxLayout()
        c2_layout.addWidget(QWidget(), 1)
        c2_layout.addLayout(c_layout, 4)
        c2_layout.addWidget(QWidget(), 1)



        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.upper_label, 1)
        main_layout.addLayout(c2_layout, 30)
