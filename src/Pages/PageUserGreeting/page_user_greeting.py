from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class PageUserGreeting(QWidget):

    def resizeEvent(self, event):
        self.btn_usb.setIconSize(QSize(self.btn_usb.size().height() / 1.25, self.btn_usb.size().height() / 1.25))
        self.btn_tg.setIconSize(QSize(self.btn_tg.size().height() / 1.25, self.btn_tg.size().height() / 1.25))
        QWidget.resizeEvent(self, event)
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):

        self.btn_usb = QPushButton()
        self.btn_usb.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.btn_usb.setIcon(QIcon('./icons/usb-drive.png'))
        self.btn_usb.setIconSize(QSize(self.btn_usb.size().height() / 1.25, self.btn_usb.size().height() / 1.25))

        self.btn_tg = QPushButton()
        self.btn_tg.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.btn_tg.setIcon(QIcon('./icons/telegram.png'))
        self.btn_tg.setIconSize(QSize(self.btn_tg.size().height() / 1.25, self.btn_tg.size().height() / 1.25))
        

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.btn_usb, 1)
        main_layout.addWidget(self.btn_tg, 1)
