from PySide6.QtWidgets import *
from PySide6.QtCore import *

from src.PageWorker.PageWorkerThread import PageWorkerThread
import time
import os
import subprocess

class PageWorkerThread(QThread):
    def __init__(self):
        super().__init__()
        self.flag:int = 0

    signal_usb_connected = Signal()
    signal_usb_disconnected = Signal()


    Slot()
    def slot_lsblk_set_point_a(self):
        '''Установление начального состояния. От этого состояния ищется разница'''
        subprocess.call("./CMD/lsblk/set_point_a.sh", shell=True, executable="bash")

    Slot()
    def slot_lsblk_set_point_b(self):
        '''Установление промежуточного состояния. Должно обновляться постоянно'''
        subprocess.call("./CMD/lsblk/set_point_b.sh", shell=True, executable="bash")

    Slot()
    def slot_lsblk_set_difference(self):
        '''Поиск разницы между 2-я состояниями (slot_set_point_a/slot_set_point_b)'''
        subprocess.call("./CMD/lsblk/get_difference.sh", shell=True, executable="bash")


    def loop_lsblk(self):
        '''Данная функция должна выполняться в цикле!!! 
        Отвечает за поиск подключения и отключения usb-накопителей. 
        Перед использованием ОБЯЗАТЕЛЬНО!!! выполнить функцию slot_lsblk_set_point_a'''
        self.slot_lsblk_set_point_b()
        self.slot_lsblk_set_difference()

        with open("./CMD/lsblk/files/difference", "r") as file:
            if len(file.readlines()) != 0:
                if self.flag != 1:
                    self.signal_usb_connected.emit()
                    self.flag = 1
            else:
                if self.flag != 2:
                    self.signal_usb_disconnected.emit()
                    self.flag = 2
                



    Slot()
    def slot_xinput_set_point_a(self):
        '''Установление начального состояния. От этого состояния ищется разница'''
        subprocess.call("./CMD/xinput/set_point_a.sh", shell=True, executable="bash")

    Slot()
    def slot_xinput_set_point_b(self):
        '''Установление промежуточного состояния. Должно обновляться постоянно'''
        subprocess.call("./CMD/xinput/set_point_b.sh", shell=True, executable="bash")

    Slot()
    def slot_xinput_set_difference_disable(self):
        '''Поиск разницы между 2-я состояниями (slot_set_point_a/slot_set_point_b) и блокировка новых устройств ввода.'''
        subprocess.call("./CMD/xinput/disable_difference.sh", shell=True, executable="bash")

    Slot()
    def slot_xinput_set_difference_enable(self):
        '''Поиск разницы между 2-я состояниями (slot_set_point_a/slot_set_point_b) и разблокировка новых устройств ввода.'''
        subprocess.call("./CMD/xinput/enable_difference.sh", shell=True, executable="bash")


    def loop_xinput(self):
        '''Данная функция должна выполняться в цикле!!!
        Поиск несанкционированного подключения устройств ввода и его обрыва.
        Перед использованием ОБЯЗАТЕЛЬНО!!! выполнить функцию slot_xinput_set_point_a'''
        self.slot_xinput_set_point_b()
        self.slot_xinput_set_difference_disable()


    def run(self):
        
        # Устанавливать начальные точки лучше где-то в другом месте. 
        # Возникает ошибка, если при запуске программы уже воткнута флешка.
        self.slot_lsblk_set_point_a()
        self.slot_xinput_set_point_a()
        
        
        while True:
            # поиск подключенных usb-накопителей
            self.loop_lsblk()
            self.loop_xinput()



class PageWorker(QWidget):

    Slot()
    def slot_userGreeting_btn_usb_clicked(self):
        self.qsLayout.setCurrentIndex(1)
        
    Slot()
    def slot_userGreeting_btn_tg_clicked(self):
        self.qsLayout.setCurrentIndex(2)


    Slot()
    def slot_usb_connected(self):
        if self.qsLayout.currentIndex() == 0:
            self.qsLayout.setCurrentIndex(1)

        print("slot_usb_connected")

    Slot()
    def slot_usb_disconnected(self):
        if self.qsLayout.currentIndex() == 1:
            self.qsLayout.setCurrentIndex(0)
        print("slot_usb_disconnected")


    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        from src.Pages.PageUserGreeting.page_user_greeting import PageUserGreeting
        self.userGreeting =  PageUserGreeting()
        self.userGreeting.signal_btn_usb_clicked.connect(self.slot_userGreeting_btn_usb_clicked)
        self.userGreeting.signal_btn_tg_clicked.connect(self.slot_userGreeting_btn_tg_clicked)


        from src.Pages.PageSelectingPrintSource.page_selecting_print_source import PageSelectingPrintSource
        self.selectingPrintSource = PageSelectingPrintSource()

        from src.Pages.PageQrTelegram.page_qr_telegram import PageQrTelegram
        self.pageQrTelegram = PageQrTelegram()

        from src.Pages.PageReviewReceivedDocument.page_review_received_document import PageReviewReceivedDocument
        self.reviewReceivedDocument = PageReviewReceivedDocument()

        from src.Pages.PagePaymentForPrinting.page_payment_for_printing import PagePaymentForPrinting
        self.paymentForPrinting = PagePaymentForPrinting()

        from src.Pages.PageWaitingForPrinting.page_waiting_for_printing import PageWaitingForPrinting
        self.waitingForPrinting = PageWaitingForPrinting()

        from src.Pages.PageFarewellToTheUser.page_farewell_to_the_user import PageFarewellToTheUser
        self.farewellToTheUser = PageFarewellToTheUser()

        from src.Pages.PageErrorMessage.page_error_message import PageErrorMessage
        self.errorMessage = PageErrorMessage()

        from src.Pages.PageAdministrative.page_administrative import PageAdministrative
        self.administrative = PageAdministrative()

        self.qsLayout = QStackedLayout(self)
        self.qsLayout.addWidget(self.userGreeting)              # Начальный виджет (tg/usb)
        self.qsLayout.addWidget(self.selectingPrintSource)      # Виджет для выбора файла(только usb)
        self.qsLayout.addWidget(self.pageQrTelegram)            # Виджет для отображения qr-код для телеграм
        self.qsLayout.addWidget(self.reviewReceivedDocument)    # Виджет для обзора документа и выбора способов печати
        self.qsLayout.addWidget(self.paymentForPrinting)        # Виджет для оплаты печати
        self.qsLayout.addWidget(self.waitingForPrinting)        # Виджет для ожидания выполнения печати
        self.qsLayout.addWidget(self.farewellToTheUser)         # Виджет для прощания с пользователем
        self.qsLayout.addWidget(self.errorMessage)              # Виджет для сообжения об ошибке и с контактами поддержки
        self.qsLayout.addWidget(self.administrative)            # Виджет для администраторов и разработчиков
        self.qsLayout.setCurrentIndex(0)


        self.wthread = PageWorkerThread()
        self.wthread.signal_usb_connected.connect(self.slot_usb_connected)
        self.wthread.signal_usb_disconnected.connect(self.slot_usb_disconnected)
        self.wthread.start()