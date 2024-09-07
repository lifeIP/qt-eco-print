from PySide6.QtWidgets import *
from PySide6.QtCore import *

class PageWorker(QWidget):
    '''
    Данный класс является графической оболочкой для другого класса(PageWorkerThread).
    '''

    @Slot(int)
    def slot_setCurrentIndex(self, index:int):
        '''
        Слот для перемещения по страницам PageWorker
        '''
        self.qsLayout.setCurrentIndex(index)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        from src.Pages.PageUserGreeting.page_user_greeting import PageUserGreeting
        self.userGreeting =  PageUserGreeting()

        from src.Pages.PageSelectingPrintSource.page_selecting_print_source import PageSelectingPrintSource
        self.selectingPrintSource = PageSelectingPrintSource()

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
        self.qsLayout.addWidget(self.reviewReceivedDocument)    # Виджет для обзора документа и выбора способов печати
        self.qsLayout.addWidget(self.paymentForPrinting)        # Виджет для оплаты печати
        self.qsLayout.addWidget(self.waitingForPrinting)        # Виджет для ожидания выполнения печати
        self.qsLayout.addWidget(self.farewellToTheUser)         # Виджет для прощания с пользователем
        self.qsLayout.addWidget(self.errorMessage)              # Виджет для сообжения об ошибке и с контактами поддержки
        self.qsLayout.addWidget(self.administrative)            # Виджет для администраторов и разработчиков

        self.qsLayout.setCurrentIndex(0)