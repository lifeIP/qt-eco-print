from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtPdf import QPdfBookmarkModel, QPdfDocument

import math
import sys
import shutil
import time
from PyPDF2 import PdfReader
import os.path
from manage_service_data import get_service_data_from_file, set_service_data_into_file

from werkzeug.utils import secure_filename
import subprocess

def generate_pdf(doc_path, path):

    subprocess.call(['soffice',
                 # '--headless',
                 '--convert-to',
                 'pdf',
                 '--outdir',
                 path,
                 doc_path])
    return doc_path

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
    def slot_open(self, doc_location:str):
        if "documents/documents/" in doc_location:
            doc_location = "documents/" + doc_location.split("/")[-1]
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

    signal_change_count_of_pages = Signal(int)

    Slot(str)
    def slot_document_selected_for_printing(self, fullPath:str):
        print(fullPath)
        self.dst = fullPath
        end = fullPath.split('.')[-1]
        if end == 'pdf':
            self.flag = False
            self.m_pdf_viewer.slot_open(self.dst)

        set_service_data_into_file("file_path", f"{fullPath}")
        set_service_data_into_file("bot_request", "0")
        # elif end == 'docx' or end == 'doc':
        #     self.dst = "documents/" + str(int(time())) + ".pdf"
        #     print(generate_pdf(fullPath, self.dst))
        #     self.flag = False
        #     self.m_pdf_viewer.slot_open(self.dst)


        with open(fullPath, "rb") as filehandle:  
            pdf = PdfReader(filehandle)
            self.count_of_pages = len(pdf.pages)


        
        self.e1.setText("1")
        self.e2.setText(str(self.count_of_pages))


    Slot(str)
    def slot_document_selected_for_printing_usb(self, fullPath:str):
        print(fullPath)
        end = fullPath.split('.')[-1]
        if end == 'pdf':
            self.dst = "documents/" + str(int(time.time())) + ".pdf"
            shutil.copy(fullPath, self.dst)
            self.flag = False
            self.m_pdf_viewer.slot_open(self.dst)

        set_service_data_into_file("file_path", f"{fullPath}")
        # elif end == 'docx' or end == 'doc':
        #     self.dst = "documents/" + str(int(time())) + ".pdf"
        #     print(generate_pdf(fullPath, self.dst))
        #     self.flag = False
        #     self.m_pdf_viewer.slot_open(self.dst)


        with open(self.dst, "rb") as filehandle:  
            pdf = PdfReader(filehandle)
            self.count_of_pages = len(pdf.pages)


        
        self.e1.setText("1")
        self.e2.setText(str(self.count_of_pages))
        

    def __init__(self):
        super().__init__()
        self.dst = ""

        self.flag = True
        self.left_arrow_pixmap = QPixmap()
        self.right_arrow_pixmap = QPixmap()
        self.exit_pixmap = QPixmap()
        self.printer_pixmap = QPixmap()

        self.left_arrow_pixmap.load("./icons/left-arrow.png")
        self.right_arrow_pixmap.load("./icons/right-arrow.png")
        self.exit_pixmap.load("./icons/left-arrow-pages.png")
        self.printer_pixmap.load("./icons/printing.png")


        self.font_label = QFont()
        self.font_label.setPixelSize(45)

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
        self.start_page = int(page)
        
        self.count_of_pages = all_page


    signal_page_selected = Signal(int)

    Slot()
    def slot_ot_editing_finished(self):
        if self.e1.text() == "":
            self.e1.setText("1")
        
        if self.e2.text() == "":
            self.e2.setText(str(self.count_of_pages))


        index = int(self.e1.text())

        if index > self.count_of_pages:
            self.e1.setText(str(self.count_of_pages))
        
        elif index < 1:
            self.e1.setText("1")

        if index > int(self.e2.text()):
            self.e1.setText(self.e2.text())
            

        self.signal_page_selected.emit(int(self.e1.text()) - 1)

    Slot()
    def slot_po_editing_finished(self):
        if self.e1.text() == "":
            self.e1.setText("1")
        
        if self.e2.text() == "":
            self.e2.setText(str(self.count_of_pages))
        
        
        index = int(self.e2.text())
        
        if index > self.count_of_pages:
            self.e2.setText(str(self.count_of_pages))
        
        elif index < 1:
            self.e2.setText("1")

        if index < int(self.e1.text()):
            self.e2.setText(self.e1.text())

        self.signal_page_selected.emit(int(self.e2.text()) - 1)



    signal_start_printing = Signal(int, int, str)
    Slot()
    def slot_start_printing(self):
        self.signal_change_count_of_pages.emit(int(self.e2.text()) - int(self.e1.text()) + 1)
        self.signal_start_printing.emit(int(self.e1.text()), int(self.e2.text()), self.dst)
        
       

   
    def initUI(self):

        self.count_of_pages = 0

        self.btn_come_back = QPushButton(" ")
        self.btn_come_back.setIcon(self.exit_pixmap)
        self.btn_come_back.clicked.connect(self.slot_back_clicked)
        self.btn_come_back.setIconSize(QSize(60, 60))

        self.btn_prev_page = QPushButton()
        self.btn_prev_page.clicked.connect(self.slot_prev_page)
        self.btn_prev_page.setIcon(self.left_arrow_pixmap)
        self.btn_prev_page.setIconSize(QSize(60, 60))

        self.btn_next_page = QPushButton()
        self.btn_next_page.clicked.connect(self.slot_next_page)
        self.btn_next_page.setIcon(self.right_arrow_pixmap)
        self.btn_next_page.setIconSize(QSize(60, 60))


        self.btn_start_print = QPushButton(" Начать печать")
        self.btn_start_print.clicked.connect(self.slot_start_printing)
        self.btn_start_print.setIcon(self.printer_pixmap)
        self.btn_start_print.setIconSize(QSize(60, 60))
        self.btn_start_print.setFont(self.font_label)


        
        self.label_page = QLabel()
        self.label_page.setFont(self.font_label)
        


        placeholder_v = QWidget()
        placeholder_v.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        placeholder_v_1 = QWidget()
        placeholder_v_1.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)



        self.label_ot = QLabel("Начиная с ")
        self.label_ot.setFont(QFont("Arial", 21))

        self.label_po = QLabel(" по ")
        self.label_po.setFont(QFont("Arial", 21))

        self.e1 = QLineEdit()
        self.e1.setValidator(QIntValidator())
        self.e1.setMaxLength(3)
        self.e1.editingFinished.connect(self.slot_ot_editing_finished)
        self.e1.setMaximumWidth(100)
        self.e1.setMinimumHeight(60)
        self.e1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.e1.setFont(self.font_label)
        
        self.e2 = QLineEdit()
        self.e2.setValidator(QIntValidator())
        self.e2.setMaxLength(3)
        self.e2.editingFinished.connect(self.slot_po_editing_finished)
        self.e2.setMaximumWidth(100)
        self.e2.setMinimumHeight(60)
        self.e2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.e2.setFont(self.font_label)
        
        h_layout_1 = QHBoxLayout()
        h_layout_1.addWidget(self.btn_come_back)
        h_layout_1.addWidget(placeholder_v)
        h_layout_1.addWidget(self.label_ot)
        h_layout_1.addWidget(self.e1)
        h_layout_1.addWidget(self.label_po)
        h_layout_1.addWidget(self.e2)

        h_layout = QHBoxLayout()
        h_layout.addWidget(placeholder_v_1)
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
        self.signal_page_selected.connect(self.m_pdf_viewer.slot_page_selected)
        
        mainLayout = QVBoxLayout(self)
        mainLayout.addLayout(v_layout)
        mainLayout.addWidget(self.m_pdf_viewer)
        mainLayout.addWidget(self.btn_start_print)
        