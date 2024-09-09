from PySide6.QtWidgets import *
from PySide6.QtCore import *

class PageQrTelegram(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        self.label = QLabel("PageQrTelegram")

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.label)