from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

import time

class PageFarewellToTheUser(QWidget):

    signal_back_to_greeting_page = Signal()


    Slot()
    def slot_end_countdown(self):
        self.signal_back_to_greeting_page.emit()
        self.timer.stop()
    
    Slot()
    def slot_start_countdown(self):
        self.timer.start(3000)
        


    def __init__(self):
        super().__init__()
        
        self.timer = QTimer(self)

        self.font_label = QFont()
        self.font_label.setPixelSize(45)
        
        self.initUI()

    def initUI(self):
        main_vertical_layout = QVBoxLayout()
    
        main_horizontal_layout = QHBoxLayout(self)
        main_horizontal_layout.addLayout(main_vertical_layout)
        

        label = QLabel("Спасибо, что пользуетесь EcoPrint")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFont(self.font_label)
        label.setWordWrap(True)
        main_vertical_layout.addWidget(label)


        self.timer.timeout.connect(self.slot_end_countdown)