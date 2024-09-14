from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtPdf import QPdfBookmarkModel, QPdfDocument
import math
import sys
import shutil
from time import time

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

    @Slot(str)
    def slot_open(self, doc_location):
        self.m_pdf_document.load(doc_location)
        self.slot_page_selected(0)

    @Slot(int)
    def slot_page_selected(self, page):
        nav = self.m_pdf_view.pageNavigator()
        nav.jump(page, QPoint(), nav.currentZoom())


    @Slot()
    def slot_prev_page(self):
        nav = self.m_pdf_view.pageNavigator()
        nav.jump(nav.currentPage() - 1, QPoint(), nav.currentZoom())

    @Slot()
    def slot_next_page(self):
        nav = self.m_pdf_view.pageNavigator()
        nav.jump(nav.currentPage() + 1, QPoint(), nav.currentZoom())


    def __init__(self):
        super().__init__()

        self.m_fileDialog = None
        
        self.m_pdf_document = QPdfDocument(self)
        self.m_pdf_view = QPdfView(self)
        self.m_pdf_view.setDocument(self.m_pdf_document)

        self.m_zoomSelector = ZoomSelector(self)
        self.m_zoomSelector.setMaximumWidth(150)
        self.m_zoomSelector.zoom_mode_changed.connect(self.m_pdf_view.setZoomMode)
        self.m_zoomSelector.zoom_factor_changed.connect(self.m_pdf_view.setZoomFactor)
        self.signal_fit_width.connect(self.m_zoomSelector.slot_fit_width)

        self.v_box_layout = QVBoxLayout(self)
        self.v_box_layout.addWidget(self.m_pdf_view)
        self.signal_fit_width.emit()
        
  


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
        self.initUI()

    def initUI(self):
        self.m_pdf_viewer = PDFViewer()
        
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addWidget(self.m_pdf_viewer)