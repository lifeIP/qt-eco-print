from PySide6.QtWidgets import *
from PySide6.QtCore import *

# from src.PageWorker.PageWorkerThread import PageWorkerThread
import time
import os
import subprocess

from manage_service_data import set_service_data_into_file, get_service_data_from_file

class SessionThread(QThread):
    
    def __init__(self):
        super().__init__()
        self.session_status:bool = 0 # 1 - занято, 0 - свободно
        self.session_id:str = ''
    
    Slot(int)
    def slot_set_session_status(self, session_status):
        print("session_status: ", session_status)
        self.session_status = session_status
        set_service_data_into_file("app_status", "busy" if self.session_status else "free")


    Slot(str)
    def slot_set_session_id(self, session_id:str):
        print("slot_set_session_id: ", session_id)
        self.session_id = session_id

    signal_fileChanged = Signal(str)

    
    def run(self):
        while True:
            set_service_data_into_file("session_id", str(self.session_id))
            self.session_status = get_service_data_from_file("app_status") == "busy"
            
            bot_request = get_service_data_from_file("bot_request")

            if bot_request == "path":
                self.signal_fileChanged.emit(get_service_data_from_file("file_path"))

            # elif bot_request == "newuser":
                # self.session_status = False
                # set_service_data_into_file("app_status", "busy" if self.session_status else "free")


            

class PageWorkerThread(QThread):
    def __init__(self):
        super().__init__()
        self.flag:int = 0

    signal_usb_connected = Signal(str)
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
            lines = file.readlines()
            if len(lines) != 0:
                if self.flag != 1:
                    self.signal_usb_connected.emit(lines[0])
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
        self.signal_set_session_status.emit(0)
        self.signal_generate_tg_qr.emit()


    Slot(str)
    def slot_usb_connected(self, path:str):
        # Связано с PageWorkerThread
        if self.qsLayout.currentIndex() == 0:
            self.qsLayout.setCurrentIndex(1)
            self.signal_loadFiles.emit(path)
            # print("slot: ", path)

        print("slot_usb_connected")
        self.userGreeting.slot_set_flag(1)
        self.usb_is_connected = True
        self.signal_set_session_status.emit(1)

    Slot()
    def slot_usb_disconnected(self):
        # Связано с PageWorkerThread
        if self.qsLayout.currentIndex() == 1:
            self.qsLayout.setCurrentIndex(0)
        print("slot_usb_disconnected")
        self.userGreeting.slot_set_flag(0)
        self.usb_is_connected = False
        self.signal_set_session_status.emit(1)





    signal_review_document_changed = Signal(str)

    Slot(str)
    def slot_tg_file_changed(self, filePath):
        self.signal_review_document_changed.emit(f"documents/{filePath}")
        
        self.qsLayout.setCurrentIndex(3)
        self.signal_set_session_status.emit(1)


    Slot()
    def slot_back_clicked(self):
        self.qsLayout.setCurrentIndex(1)


    Slot()
    def slot_btn_back_clicked(self):
        self.qsLayout.setCurrentIndex(0)
        self.signal_set_session_status.emit(1)


    Slot()
    def slot_review_doc_changed(self):
        self.signal_set_session_status.emit(1)
        self.qsLayout.setCurrentIndex(3)


    signal_loadFiles = Signal(str)

    Slot()
    def slot_review_back_clicked(self):
        if self.usb_is_connected:
            self.qsLayout.setCurrentIndex(1)
        else: 
            self.qsLayout.setCurrentIndex(0)
            self.signal_set_session_status.emit(1)


    Slot()
    def slot_payment_back_clicked(self):
        if self.usb_is_connected:
            self.qsLayout.setCurrentIndex(3)
        else: 
            self.qsLayout.setCurrentIndex(0)
            self.signal_set_session_status.emit(1)


    Slot(int, int, str)
    def slot_start_print_pressed_in_review_page(self, start_id, end_id, path):
        self.qsLayout.setCurrentIndex(4)
        self.signal_generate_payment_qr.emit()
        print(start_id, end_id, path)
    


    signal_generate_tg_qr = Signal()
    signal_generate_payment_qr = Signal()




    signal_set_session_id = Signal(int)
    Slot(int)
    def slot_set_session_id(self, session_id):
        self.signal_set_session_id.emit(session_id)


    signal_set_session_status = Signal(int)


    signal_change_count_of_pages = Signal(float)


    Slot()
    def slot_back_to_greeting_page(self):
        self.qsLayout.setCurrentIndex(0)


    def start_printing_file(self, file_name):
        # Путь к вашему shell-скрипту
        script_path = './CMD/lp/print.sh'
        
        try:
            # Вызываем shell-скрипт с помощью subprocess.call
            result = subprocess.call([script_path, file_name])
            
            # Проверяем код возврата
            if result == 0:
                print(f"Файл '{file_name}' успешно отправлен на печать.")
            else:
                print(f"Ошибка при отправке файла '{file_name}' на печать. Код возврата: {result}")

        except Exception as e:
            print(f"Произошла ошибка: {e}")


    signal_start_countdown = Signal()
    Slot()
    def slot_payment_done(self):
        path = get_service_data_from_file("file_path")
        self.start_printing_file(path)        
        self.qsLayout.setCurrentIndex(5)
        self.signal_start_countdown.emit()
        


    Slot(int)
    def slot_change_count_of_pages(self, count):
        self.count_of_pages = count
        self.signal_change_count_of_pages.emit(self.count_of_pages)


    def __init__(self):
        super().__init__()
        self.usb_is_connected = False
        self.count_of_pages = 0
        self.initUI()

    def initUI(self):
        
        from pages.PageUserGreeting.page_user_greeting import PageUserGreeting
        self.userGreeting =  PageUserGreeting()
        self.userGreeting.signal_btn_usb_clicked.connect(self.slot_back_clicked)
        self.userGreeting.signal_btn_usb_clicked.connect(self.slot_userGreeting_btn_usb_clicked)
        self.userGreeting.signal_btn_tg_clicked.connect(self.slot_userGreeting_btn_tg_clicked)


        from pages.PageSelectingPrintSource.page_selecting_print_source import PageSelectingPrintSource
        self.selectingPrintSource = PageSelectingPrintSource()
        self.selectingPrintSource.signal_back_clicked.connect(self.slot_btn_back_clicked)
        self.signal_loadFiles.connect(self.selectingPrintSource.slot_loadFiles)
        self.selectingPrintSource.signal_review_doc_changed.connect(self.slot_review_doc_changed)


        from pages.PageQrTelegram.page_qr_telegram import PageQrTelegram
        self.pageQrTelegram = PageQrTelegram()
        self.pageQrTelegram.signal_back_clicked.connect(self.slot_btn_back_clicked)
        self.signal_generate_tg_qr.connect(self.pageQrTelegram.slot_generate_qr)
        self.pageQrTelegram.signal_set_session_id.connect(self.slot_set_session_id)

        from pages.PageReviewReceivedDocument.page_review_received_document import PageReviewReceivedDocument
        self.reviewReceivedDocument = PageReviewReceivedDocument()
        self.selectingPrintSource.signal_document_selected_for_printing.connect(self.reviewReceivedDocument.slot_document_selected_for_printing_usb)
        self.signal_review_document_changed.connect(self.reviewReceivedDocument.slot_document_selected_for_printing)
        self.reviewReceivedDocument.signal_back_clicked.connect(self.slot_review_back_clicked)
        self.reviewReceivedDocument.signal_start_printing.connect(self.slot_start_print_pressed_in_review_page)
        self.reviewReceivedDocument.signal_change_count_of_pages.connect(self.slot_change_count_of_pages)


        from pages.PagePaymentForPrinting.page_payment_for_printing import PagePaymentForPrinting
        self.paymentForPrinting = PagePaymentForPrinting()
        self.paymentForPrinting.signal_back_clicked.connect(self.slot_payment_back_clicked)
        self.paymentForPrinting.signal_payment_done.connect(self.slot_payment_done)
        self.signal_generate_payment_qr.connect(self.paymentForPrinting.slot_generate_qr)
        self.signal_change_count_of_pages.connect(self.paymentForPrinting.slot_change_count_of_pages)


        from pages.PageFarewellToTheUser.page_farewell_to_the_user import PageFarewellToTheUser
        self.farewellToTheUser = PageFarewellToTheUser()
        self.farewellToTheUser.signal_back_to_greeting_page.connect(self.slot_back_to_greeting_page)
        self.signal_start_countdown.connect(self.farewellToTheUser.slot_start_countdown)
    

        from pages.PageErrorMessage.page_error_message import PageErrorMessage
        self.errorMessage = PageErrorMessage()

        from pages.PageAdministrative.page_administrative import PageAdministrative
        self.administrative = PageAdministrative()

        self.qsLayout = QStackedLayout(self)
        self.qsLayout.addWidget(self.userGreeting)              # Начальный виджет (tg/usb)
        self.qsLayout.addWidget(self.selectingPrintSource)      # Виджет для выбора файла(только usb)
        self.qsLayout.addWidget(self.pageQrTelegram)            # Виджет для отображения qr-код для телеграм
        self.qsLayout.addWidget(self.reviewReceivedDocument)    # Виджет для обзора документа и выбора способов печати
        self.qsLayout.addWidget(self.paymentForPrinting)        # Виджет для оплаты печати
        self.qsLayout.addWidget(self.farewellToTheUser)         # Виджет для прощания с пользователем
        self.qsLayout.addWidget(self.errorMessage)              # Виджет для сообжения об ошибке и с контактами поддержки
        self.qsLayout.addWidget(self.administrative)            # Виджет для администраторов и разработчиков
        self.qsLayout.setCurrentIndex(0)


        self.wthread = PageWorkerThread()
        self.wthread.signal_usb_connected.connect(self.slot_usb_connected)
        self.wthread.signal_usb_disconnected.connect(self.slot_usb_disconnected)
        self.wthread.start()


        self.sthread = SessionThread()
        self.sthread.signal_fileChanged.connect(self.slot_tg_file_changed)
        self.signal_set_session_id.connect(self.sthread.slot_set_session_id)
        self.signal_set_session_status.connect(self.sthread.slot_set_session_status)
        self.sthread.start()