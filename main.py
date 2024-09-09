import sys
from argparse import ArgumentParser, RawTextHelpFormatter

from PySide6.QtWidgets import *
from PySide6.QtCore import *


from src.PageWorker.PageWoker import PageWorker


class App(QWidget):

    def keyPressEvent(self, event):
        # если нажата клавиша F11
        if event.key() == Qt.Key.Key_F11:
            # если в полный экран 
            if self.isFullScreen():
                # вернуть прежнее состояние
                self.showNormal()
            else:
                # иначе во весь экран
                self.showFullScreen()
        elif event.key() == Qt.Key.Key_Escape:
            self.close()

    def __init__(self):
        super().__init__()
        self.title = 'EcoPrint'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.page_worker = PageWorker()
        
        layout_v_box_main = QVBoxLayout(self)
        layout_v_box_main.addWidget(self.page_worker)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())