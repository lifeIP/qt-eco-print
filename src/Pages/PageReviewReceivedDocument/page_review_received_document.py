from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtPdf import QPdfBookmarkModel, QPdfDocument
import math
import sys
import shutil
from time import time
from PyPDF2 import PdfReader

class ZoomSelector(QWidget):

    zoom_mode_changed = Signal(QPdfView.ZoomMode)
    zoom_factor_changed = Signal(float)

    def __init__(self, parent):
        super().__init__(parent)

    Slot()
    def slot_fit_width(self):
        self.zoom_mode_changed.emit(QPdfView.ZoomMode.FitToWidth)

    Slot()
    def slot_fit_in_view(self):
        self.zoom_mode_changed.emit(QPdfView.ZoomMode.FitInView)

    @Slot(int)
    def slot_change_zoom(self, zoom_in_percent: int):
        factor = 1.0
        factor = zoom_in_percent / 100.0
        self.zoom_mode_changed.emit(QPdfView.ZoomMode.Custom)
        self.zoom_factor_changed.emit(factor)


ZOOM_MULTIPLIER = math.sqrt(2.0)

class PDFViewer(QWidget):

    signal_fit_width = Signal()
    signal_change_zoom = Signal(int)

    Slot(str)
    def slot_open(self, doc_location):
        self.m_pdf_document.load(doc_location)
        self.slot_page_selected(0)

        with open(doc_location, "rb") as filehandle:  
            pdf = PdfReader(filehandle)
            self.count_of_pages = len(pdf.pages)

            nav = self.m_pdf_view.pageNavigator()
            self.signal_page_nav_label.emit(nav.currentPage() + 1, self.count_of_pages)
            


    Slot(int)
    def slot_page_selected(self, page):
        nav = self.m_pdf_view.pageNavigator()
        nav.jump(page, QPoint(), nav.currentZoom())

        self.signal_page_nav_label.emit(nav.currentPage() + 1, self.count_of_pages)


    Slot()
    def slot_prev_page(self):
        nav = self.m_pdf_view.pageNavigator()

        if nav.currentPage() > 0:
            nav.jump(nav.currentPage() - 1, QPoint(), nav.currentZoom())

        self.signal_page_nav_label.emit(nav.currentPage() + 1, self.count_of_pages)

    Slot()
    def slot_next_page(self):
        nav = self.m_pdf_view.pageNavigator()
        if nav.currentPage() < self.count_of_pages - 1:
           nav.jump(nav.currentPage() + 1, QPoint(), nav.currentZoom())

        self.signal_page_nav_label.emit(nav.currentPage() + 1, self.count_of_pages)


    signal_page_nav_label = Signal(int, int)

    def __init__(self):
        super().__init__()

        self.count_of_pages = 0
        self.m_fileDialog = None
        
        self.m_pdf_document = QPdfDocument(self)
        self.m_pdf_view = QPdfView(self)
        self.m_pdf_view.setDocument(self.m_pdf_document)

        self.m_zoomSelector = ZoomSelector(self)
        self.m_zoomSelector.setMaximumWidth(150)
        self.m_zoomSelector.zoom_mode_changed.connect(self.m_pdf_view.setZoomMode)
        self.m_zoomSelector.zoom_factor_changed.connect(self.m_pdf_view.setZoomFactor)
        self.signal_fit_width.connect(self.m_zoomSelector.slot_fit_width)
        self.signal_change_zoom.connect(self.m_zoomSelector.slot_change_zoom)

        self.v_box_layout = QVBoxLayout(self)
        self.v_box_layout.addWidget(self.m_pdf_view)
        self.signal_change_zoom.emit(50)
        
  


class PageReviewReceivedDocument(QWidget):

    Slot(str)
    def slot_document_selected_for_printing(self, fullPath):
        end = fullPath.split('.')[-1]
        if end == 'pdf' or end == 'doc' or end == 'docx' or end == 'odt':
            dst = "../documents/" + str(int(time())) + f".{end}"
            shutil.copy(fullPath, dst)
            
            self.m_pdf_viewer.slot_open(fullPath)
            

    def __init__(self):
        super().__init__()

        self.left_arrow_pixmap = QPixmap()
        self.right_arrow_pixmap = QPixmap()

        self.left_arrow_pixmap.load("./icons/left-arrow.png")
        self.right_arrow_pixmap.load("./icons/right-arrow.png")

        self.m_pdf_viewer = PDFViewer()
        self.initUI()



    signal_back_clicked = Signal()




    signal_prev_page = Signal()
    Slot()
    def slot_prev_page(self):
        self.signal_prev_page.emit()

    
    signal_next_page = Signal()
    Slot()
    def slot_next_page(self):
        self.signal_next_page.emit()



    Slot()
    def slot_back_clicked(self):
        self.signal_back_clicked.emit()




    Slot(int, int)
    def slot_page_nav_label(self, page, all_page):
        self.label_page.setText(f"{page}/{all_page}")


    def initUI(self):

        self.btn_come_back = QPushButton("Назад")
        self.btn_come_back.clicked.connect(self.slot_back_clicked)
        
        self.btn_prev_page = QPushButton()
        self.btn_prev_page.clicked.connect(self.slot_prev_page)
        self.btn_prev_page.setIcon(self.left_arrow_pixmap)
        self.btn_prev_page.setIconSize(QSize(50, 50))

        self.btn_next_page = QPushButton()
        self.btn_next_page.clicked.connect(self.slot_next_page)
        self.btn_next_page.setIcon(self.right_arrow_pixmap)
        self.btn_next_page.setIconSize(QSize(50, 50))

        self.label_page = QLabel()

        placeholder_v = QWidget()
        placeholder_v.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        placeholder_v_1 = QWidget()
        placeholder_v_1.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)


        self.e1 = QLineEdit()
        self.e1.setValidator(QIntValidator())
        self.e1.setMaxLength(4)
        self.e1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.e1.setFont(QFont("Arial",20))
        
        self.e2 = QLineEdit()
        self.e2.setValidator(QIntValidator())
        self.e2.setMaxLength(4)
        self.e2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.e2.setFont(QFont("Arial",20))
        
        h_layout_1 = QHBoxLayout()
        h_layout_1.addWidget(placeholder_v_1)
        h_layout_1.addWidget(self.e1)
        h_layout_1.addWidget(self.e2)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.btn_come_back)
        h_layout.addWidget(placeholder_v)
        h_layout.addWidget(self.btn_prev_page)
        h_layout.addWidget(self.label_page)
        h_layout.addWidget(self.btn_next_page)


        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout_1)
        v_layout.addLayout(h_layout)

        self.m_pdf_viewer = PDFViewer()
        self.signal_next_page.connect(self.m_pdf_viewer.slot_next_page)
        self.signal_prev_page.connect(self.m_pdf_viewer.slot_prev_page)
        self.m_pdf_viewer.signal_page_nav_label.connect(self.slot_page_nav_label)
        
        mainLayout = QVBoxLayout(self)
        mainLayout.addLayout(v_layout)
        mainLayout.addWidget(self.m_pdf_viewer)
        