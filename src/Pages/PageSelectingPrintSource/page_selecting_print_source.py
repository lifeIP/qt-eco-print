from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import os


class File(QWidget):
    def __init__(self, type, fileName, fullFilePath, btnClicked, docClicked):
        super().__init__()
        self.q_pixmap = QPixmap()
        self.fullFilePath = fullFilePath
        self.fileName = fileName
        self.fileName_1 = ''
        self.btnClicked = btnClicked
        self.docClicked = docClicked
        self.type = type

        if len(fileName) > 9:
            self.fileName_1 = fileName[0:7] + "..."
        else: self.fileName_1 = fileName


        if type == "folder":
            self.q_pixmap.load("./icons/folder.png")
        elif type == "pdf":
            self.q_pixmap.load("./icons/pdf.png")
        elif type == "doc":
            self.q_pixmap.load("./icons/doc.png")
        self.initUI()


    Slot()
    def slot_btn_clicked(self):

        if self.type == "folder":
            self.btnClicked(self.fullFilePath)
        else: 
            self.docClicked(self.fullFilePath)
            

    def initUI(self):
        self.icon = QPushButton(self.fileName_1)
        self.icon.setIcon(self.q_pixmap)
        self.icon.clicked.connect(self.slot_btn_clicked)
        self.icon.setIconSize(QSize(80, 80))
    
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.icon)    


class PageSelectingPrintSource(QWidget):

    def __init__(self):
        super().__init__()
        self.page_id = 0

        self.kuchaFilov = [[]]

        self.fullPath = ''

        self.arrowpix = QPixmap()
        self.arrowpix.load("./icons/arrow.png")
        self.initUI()

    def get_FULL_NAME_files_in_usb(self, directory):
        try:
            files = os.listdir(directory)

            all_files = list()
            

            for file in files:
                splt = file.split(".")[-1]
                if os.path.isdir(directory + file):
                    all_files.append({"type": "folder", "fileName":file, "fullFileName": directory + file})
                elif splt == "pdf":
                    all_files.append({"type": "pdf", "fileName":file, "fullFileName": directory + file})
                elif splt == "doc":
                    all_files.append({"type": "doc", "fileName":file, "fullFileName": directory + file})
                

                    
            return all_files
        except: return None


    signal_review_doc_changed = Signal()


    Slot(str)
    def slot_loadFiles(self, path:str):
        if len(path.split('/')) <= 2: return
        for file in self.kuchaFilov[self.page_id]:
            # self.grid.removeWidget(file)
            file.setParent(None)
        
        self.page_id = 0
        self.fullPath = path
        self.label_full_path.setText(path)
        

        files = self.get_FULL_NAME_files_in_usb(path.rstrip() + "/")
        # print(path)
        if files is None: return

        kucha = []
        kucha_in = []
        for file in files:
            if len(kucha_in) >= 14:
                kucha.append(kucha_in)
                kucha_in = list()
            one_file = File(type=file["type"], fileName=file["fileName"], fullFilePath=file["fullFileName"], btnClicked=self.slot_loadFiles, docClicked=self.slot_doc_clicked)            
            kucha_in.append(one_file)
        
        kucha.append(kucha_in)


        self.kuchaFilov = kucha
        if len(self.kuchaFilov) > 1: self.button_next.setDisabled(False)

        index_x = 0
        index_y = 0

        for file in self.kuchaFilov[self.page_id]:
            file.setMinimumWidth(int(self.width()*0.4))
            self.grid.addWidget(file, index_y, index_x)
    
            index_x += 1
            if index_x == 2:
                index_y += 1
                index_x = 0

        if self.page_id == len(self.kuchaFilov) - 1: self.button_next.setDisabled(True)
        if self.page_id > 0: self.button_prev.setDisabled(False)


    Slot()
    def nextPage(self):
        for file in self.kuchaFilov[self.page_id]:
            # self.grid.removeWidget(file)
            file.setParent(None)
            
            
        index_x = 0
        index_y = 0
        
        for file in self.kuchaFilov[self.page_id + 1]:
            file.setMinimumWidth(int(self.width()*0.4))
            self.grid.addWidget(file, index_y, index_x)
    
            index_x += 1
            if index_x == 2:
                index_y += 1
                index_x = 0

        self.page_id += 1

        if self.page_id == len(self.kuchaFilov) - 1: self.button_next.setDisabled(True)
        if self.page_id > 0: self.button_prev.setDisabled(False)
        

    Slot()
    def prevPage(self):
        for file in self.kuchaFilov[self.page_id]:
            # self.grid.removeWidget(file)
            file.setParent(None)
            
        index_x = 0
        index_y = 0
        
        for file in self.kuchaFilov[self.page_id - 1]:
            file.setMinimumWidth(int(self.width()*0.4))
            self.grid.addWidget(file, index_y, index_x)
    
            index_x += 1
            if index_x == 2:
                index_y += 1
                index_x = 0

        self.page_id -= 1

        if self.page_id == 0: self.button_prev.setDisabled(True)
        if self.page_id < (len(self.kuchaFilov) - 1): self.button_next.setDisabled(False)


    Slot()
    def slot_button_prev_dir_clicked(self):
        spltsz = len(self.fullPath.split("/")[-1])
        if len(self.fullPath.split('/')) <= 2: return
        self.slot_loadFiles(self.fullPath[:-spltsz - 1])



    signal_document_selected_for_printing = Signal(str)
    
    Slot(str)
    def slot_doc_clicked(self, fullPath):
        self.signal_document_selected_for_printing.emit(fullPath)
        self.signal_review_doc_changed.emit()


    def initUI(self):
        self.grid = QGridLayout()
        
        

        self.placeholder = QWidget()
        self.placeholder.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)

        self.label_full_path = QLabel("/")
        self.label_full_path.setWordWrap(True)
        self.button_prev_dir = QPushButton()
        self.button_prev_dir.clicked.connect(self.slot_button_prev_dir_clicked)
        self.button_prev_dir.setIcon(self.arrowpix)
        self.button_prev_dir.setIconSize(QSize(30, 30))
        self.h_nav_layout = QHBoxLayout()
        self.h_nav_layout.addWidget(self.label_full_path, 4)
        self.h_nav_layout.addWidget(self.button_prev_dir, 1)



        self.button_prev = QPushButton("Назад")
        self.button_prev.clicked.connect(self.prevPage)
        self.button_next = QPushButton("Вперёд")
        self.button_next.clicked.connect(self.nextPage)
        self.button_cancel = QPushButton("Отмена")
        self.placeholder_1 = QWidget()
        self.placeholder_1.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.button_cancel)
        self.h_layout.addWidget(self.placeholder_1)
        self.h_layout.addWidget(self.button_prev)
        self.h_layout.addWidget(self.button_next)
        self.downPanel = QWidget()
        self.downPanel.setLayout(self.h_layout)

        if len(self.kuchaFilov) > 1:
            self.button_prev.setDisabled(True)
            self.button_next.setDisabled(False)
        else: 
            self.button_prev.setDisabled(True)
            self.button_next.setDisabled(True)

        mainLayout = QVBoxLayout(self)
        mainLayout.addLayout(self.h_nav_layout)
        mainLayout.addLayout(self.grid)
        mainLayout.addWidget(self.placeholder, alignment=Qt.AlignmentFlag.AlignBottom)
        mainLayout.addWidget(self.downPanel, alignment=Qt.AlignmentFlag.AlignBottom)
        