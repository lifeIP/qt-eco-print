from PySide6.QtWidgets import *
from PySide6.QtCore import *

import time

class PageWorkerThread(QThread):
    '''
    ***Находится в разработке!***
    '''
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            time.sleep(1)
            print("run")