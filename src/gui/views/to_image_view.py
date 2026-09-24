import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QMessageBox, QLineEdit, QFormLayout)
from PyQt6.QtCore import Qt
from src.gui.components.thumbnail_grid import ThumbnailGrid
from src.core.image_exporter import export_pages_to_images
from src.core.i18n import trans

class ToImageView(QWidget):
    def __init__(self, status_callback=None, parent=None):
        super().__init__(parent)
        self.status_callback = status_callback
        self.current_pdf_path = None
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.grid = ThumbnailGrid()
        layout.addWidget(self.grid)
        
        right_panel = QWidget()
        right_panel.setFixedWidth(250)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(15, 0, 0, 0)
        
        self.header = QLabel(trans.t("to_image"))
        self.header.setObjectName("HeaderLabel")
        self.lbl_info = QLabel(trans.t("no_file"))
        
        form = QFormLayout()
        self.inp_dpi = QLineEdit("300")
        form.addRow("DPI:", self.inp_dpi)
        
        self.btn_export = QPushButton(trans.t("export_images"))
        self.btn_export.setObjectName("PrimaryBtn")
        self.btn_export.setEnabled(False)
        self.btn_export.clicked.connect(self._export_images)
        
        right_layout.addWidget(self.header)
        right_layout.addWidget(self.lbl_info)
        right_layout.addSpacing(10)
        right_layout.addLayout(form)
        right_layout.addStretch()
        right_layout.addWidget(self.btn_export)
        
        layout.addWidget(right_panel)
        
    def set_pdf(self, file_path):
        self.current_pdf_path = file_path
        self.grid.load_pdf(file_path)
        self.lbl_info.setText(f"{self.grid.count()} {trans.t('pages')}")
        self.btn_export.setEnabled(True)

    def _export_images(self):
        if not self.current_pdf_path: return
        out_dir = QFileDialog.getExistingDirectory(self, trans.t("save"))
        if out_dir:
            if self.status_callback: self.status_callback(trans.t("loading"))
            try:
                dpi = int(self.inp_dpi.text())
                selected = [item.data(Qt.ItemDataRole.UserRole) for item in self.grid.selectedItems()]
                indices = selected if selected else list(range(self.grid.count()))
                
                export_pages_to_images(self.current_pdf_path, out_dir, indices, dpi)
                QMessageBox.information(self, trans.t("success"), trans.t("saved"))
                if self.status_callback: self.status_callback(trans.t("ready"))
            except Exception as e:
                QMessageBox.critical(self, trans.t("error"), str(e))
                if self.status_callback: self.status_callback(trans.t("error"))
                
    def update_texts(self):
        self.header.setText(trans.t("to_image"))
        self.btn_export.setText(trans.t("export_images"))
        if not self.current_pdf_path:
            self.lbl_info.setText(trans.t("no_file"))
        else:
            self.lbl_info.setText(f"{self.grid.count()} {trans.t('pages')}")
