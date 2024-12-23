import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from time import time
from multiprocessing import Process
from manage_service_data import get_service_data_from_file, set_service_data_into_file
from tg_bot import bot_start

from page_woker import PageWorker



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
        
        p0 = Process(target=bot_start, args=(), daemon=True)
        p0.start()
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.page_worker = PageWorker() 
        
        layout_v_box_main = QVBoxLayout(self)
        layout_v_box_main.addWidget(self.page_worker)

        self.show()



if __name__ == '__main__':
    set_service_data_into_file("last_time_activity", f"{time()}")
    set_service_data_into_file("app_status", "busy")
    set_service_data_into_file("bot_request", "0")
    set_service_data_into_file("file_path", "0")
    
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())