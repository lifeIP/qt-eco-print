from PySide6.QtWidgets import *
from PySide6.QtCore import *




class PageWorkerThread(QThread):
    '''
    Выполняется в отдельном потоке бесконечно!\n
    Данный класс отвечает за работу:
    1. Поиск подключенных usb-носителей
    2. Автоматичекое переключение между страницами
    3. ... \n
    ***Находится в разработке!***
    '''
    def __init__(self, parent=None):
        super().__init__(self, parent)

    def initUI(self):
        pass