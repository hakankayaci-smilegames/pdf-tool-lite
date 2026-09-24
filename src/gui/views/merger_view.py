import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QListWidget, QFileDialog, QMessageBox, QLabel, QAbstractItemView)
from src.core.merger import merge_pdfs
from src.core.i18n import trans

class MergerView(QWidget):
    def __init__(self, status_callback=None, parent=None):
        super().__init__(parent)
        self.status_callback = status_callback
        self.file_paths = []
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        left_layout = QVBoxLayout()
        self.btn_add = QPushButton(trans.t("add_pdfs"))
        self.btn_add.setObjectName("PrimaryBtn")
        self.btn_add.clicked.connect(self._add_files)
        
        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        
        left_layout.addWidget(self.btn_add)
        left_layout.addWidget(self.list_widget)
        
        right_panel = QWidget()
        right_panel.setFixedWidth(250)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(15, 0, 0, 0)
        
        self.header = QLabel(trans.t("merger"))
        self.header.setObjectName("HeaderLabel")
        
        self.lbl_info = QLabel(f"0 {trans.t('files')}")
        
        self.btn_remove = QPushButton(trans.t("delete"))
        self.btn_remove.setObjectName("DangerBtn")
        self.btn_remove.clicked.connect(self._remove_selected)
        
        self.btn_save = QPushButton(trans.t("merge_save"))
        self.btn_save.setObjectName("PrimaryBtn")
        self.btn_save.setEnabled(False)
        self.btn_save.clicked.connect(self._save_merged)
        
        right_layout.addWidget(self.header)
        right_layout.addWidget(self.lbl_info)
        right_layout.addWidget(self.btn_remove)
        right_layout.addStretch()
        right_layout.addWidget(self.btn_save)
        
        layout.addLayout(left_layout)
        layout.addWidget(right_panel)

    def _add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, trans.t("add_pdfs"), "", "PDF (*.pdf)")
        if files:
            for f in files:
                self.list_widget.addItem(os.path.basename(f))
                self.file_paths.append(f)
            self._update_ui()
            
    def _remove_selected(self):
        for item in self.list_widget.selectedItems():
            idx = self.list_widget.row(item)
            self.list_widget.takeItem(idx)
            self.file_paths.pop(idx)
        self._update_ui()
        
    def _update_ui(self):
        count = self.list_widget.count()
        self.lbl_info.setText(f"{count} {trans.t('files')}")
        self.btn_save.setEnabled(count > 1)
        
    def _save_merged(self):
        if self.list_widget.count() < 2: return
        save_path, _ = QFileDialog.getSaveFileName(self, trans.t("save"), "", "PDF (*.pdf)")
        if save_path:
            if not save_path.lower().endswith('.pdf'): save_path += '.pdf'
            ordered_paths = []
            for i in range(self.list_widget.count()):
                item_name = self.list_widget.item(i).text()
                for p in self.file_paths:
                    if os.path.basename(p) == item_name:
                        ordered_paths.append(p)
                        break
                        
            if self.status_callback: self.status_callback(trans.t("loading"))
            try:
                merge_pdfs(ordered_paths, save_path)
                QMessageBox.information(self, trans.t("success"), trans.t("saved"))
                if self.status_callback: self.status_callback(trans.t("ready"))
            except Exception as e:
                QMessageBox.critical(self, trans.t("error"), str(e))
                if self.status_callback: self.status_callback(trans.t("error"))
                
    def update_texts(self):
        self.header.setText(trans.t("merger"))
        self.btn_add.setText(trans.t("add_pdfs"))
        self.btn_remove.setText(trans.t("delete"))
        self.btn_save.setText(trans.t("merge_save"))
        self._update_ui()
