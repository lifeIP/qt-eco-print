from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtPdf import QPdfBookmarkModel, QPdfDocument
import math
import sys

class PageReviewReceivedDocument(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        pass

class ZoomSelector(QWidget):

    zoom_mode_changed = Signal(QPdfView.ZoomMode)
    zoom_factor_changed = Signal(float)

    def __init__(self, parent):
        super().__init__(parent)
        # self.setEditable(True)

        # self.addItem("Fit Width")
        # self.addItem("Fit Page")
        # self.addItem("12%")
        # self.addItem("25%")
        # self.addItem("33%")
        # self.addItem("50%")
        # self.addItem("66%")
        # self.addItem("75%")
        # self.addItem("100%")
        # self.addItem("125%")
        # self.addItem("150%")
        # self.addItem("200%")
        # self.addItem("400%")

        # self.currentTextChanged.connect(self.on_current_text_changed)
        # self.lineEdit().editingFinished.connect(self._editing_finished)

    @Slot(float)
    def set_zoom_factor(self, zoomFactor):
        percent = int(zoomFactor * 100)
        # self.setCurrentText(f"{percent}%")

    @Slot()
    def reset(self):
        # self.setCurrentIndex(8)  # 100%
        pass

    @Slot(str)
    def on_current_text_changed(self, text):
        if text == "Fit Width":
            self.zoom_mode_changed.emit(QPdfView.ZoomMode.FitToWidth)
        elif text == "Fit Page":
            self.zoom_mode_changed.emit(QPdfView.ZoomMode.FitInView)
        elif text.endswith("%"):
            factor = 1.0
            zoom_level = int(text[:-1])
            factor = zoom_level / 100.0
            self.zoom_mode_changed.emit(QPdfView.ZoomMode.Custom)
            self.zoom_factor_changed.emit(factor)

    @Slot()
    def _editing_finished(self):
        # self.on_current_text_changed(self.lineEdit().text())
        pass


ZOOM_MULTIPLIER = math.sqrt(2.0)

class PDFViewer(QWidget):

    @Slot(QUrl)
    def open(self, doc_location):
        if doc_location.isLocalFile():
            self.m_pdf_document.load(doc_location.toLocalFile())
            document_title = self.m_pdf_document.metaData(QPdfDocument.MetaDataField.Title)
            self.setWindowTitle(document_title if document_title else "PDF Viewer")
            self.page_selected(0)
            # self.m_pageSelector.setMaximum(self.m_pdf_document.pageCount() - 1)
        else:
            message = f"{doc_location} is not a valid local file"
            print(message, file=sys.stderr)
            QMessageBox.critical(self, "Failed to open", message)

    @Slot(int)
    def page_selected(self, page):
        nav = self.m_pdf_view.pageNavigator()
        nav.jump(page, QPoint(), nav.currentZoom())

    @Slot()
    def on_actionOpen_triggered(self):
        if not self.m_fileDialog:
            directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
            self.m_fileDialog = QFileDialog(self, "Choose a PDF", directory)
            self.m_fileDialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
            self.m_fileDialog.setMimeTypeFilters(["application/pdf"])
        if self.m_fileDialog.exec() == QDialog.DialogCode.Accepted:
            to_open = self.m_fileDialog.selectedUrls()[0]
            if to_open.isValid():
                self.open(to_open)

    @Slot()
    def on_actionPrevious_Page_triggered(self):
        nav = self.m_pdf_view.pageNavigator()
        nav.jump(nav.currentPage() - 1, QPoint(), nav.currentZoom())

    @Slot()
    def on_actionNext_Page_triggered(self):
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
        self.m_zoomSelector.reset()
        self.m_pdf_view.zoomFactorChanged.connect(self.m_zoomSelector.set_zoom_factor)


        self.v_box_layout = QVBoxLayout(self)
        self.v_box_layout.addWidget(self.m_pdf_view)
        
    
class PrintPreview(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.m_pdf_viewer = PDFViewer()

        self.b_open = QPushButton("Открыть")
        self.b_open.clicked.connect(self.m_pdf_viewer.on_actionOpen_triggered)
    
        self.v_box_app_layout = QVBoxLayout()
        self.v_box_app_layout.addWidget(self.m_pdf_viewer)
        self.v_box_app_layout.addWidget(self.b_open)

        self.setLayout(self.v_box_app_layout)
