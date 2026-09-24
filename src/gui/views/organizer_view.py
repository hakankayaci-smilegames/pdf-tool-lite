import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QMessageBox, QApplication)
from src.gui.components.thumbnail_grid import ThumbnailGrid
from src.core.splitter import split_pdf
from src.core.i18n import trans

class OrganizerView(QWidget):
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
        right_panel.setFixedWidth(260)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(15, 0, 0, 0)
        
        self.header = QLabel(trans.t("organizer"))
        self.header.setObjectName("HeaderLabel")
        self.lbl_info = QLabel(trans.t("no_file"))
        
        self.lbl_hint = QLabel("• Döndürmek için: Sağ tık menüsü (90° Sağa/Sola)\n• Sıralamak için: Ctrl + Sol/Sağ Ok tuşları\n• Silmek için: Delete tuşu")
        self.lbl_hint.setWordWrap(True)
        self.lbl_hint.setStyleSheet("color: #7f849c; font-size: 12px; margin-top: 10px; line-height: 1.4;")
        
        self.btn_save = QPushButton(trans.t("save"))
        self.btn_save.setObjectName("PrimaryBtn")
        self.btn_save.setEnabled(False)
        self.btn_save.clicked.connect(self._save_pdf)
        
        right_layout.addWidget(self.header)
        right_layout.addWidget(self.lbl_info)
        right_layout.addWidget(self.lbl_hint)
        right_layout.addStretch()
        right_layout.addWidget(self.btn_save)
        
        layout.addWidget(right_panel)
        
    def set_pdf(self, file_path):
        self.current_pdf_path = file_path
        self.grid.load_pdf(file_path)
        self.lbl_info.setText(f"{self.grid.count()} {trans.t('pages')}")
        self.btn_save.setEnabled(True)

    def _save_pdf(self):
        if not self.current_pdf_path: return
        save_path, _ = QFileDialog.getSaveFileName(self, trans.t("save"), "", "PDF (*.pdf)")
        if save_path:
            if not save_path.lower().endswith('.pdf'): save_path += '.pdf'
            if self.status_callback: self.status_callback(trans.t("loading"))
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            try:
                indices = self.grid.get_current_order()
                rotations = self.grid.get_item_rotations()
                split_pdf(self.current_pdf_path, save_path, indices, rotations)
                QMessageBox.information(self, trans.t("success"), trans.t("saved"))
                if self.status_callback: self.status_callback(trans.t("ready"))
            except Exception as e:
                QMessageBox.critical(self, trans.t("error"), str(e))
                if self.status_callback: self.status_callback(trans.t("error"))
            finally:
                QApplication.restoreOverrideCursor()
                
    def update_texts(self):
        self.header.setText(trans.t("organizer"))
        self.btn_save.setText(trans.t("save"))
        if not self.current_pdf_path:
            self.lbl_info.setText(trans.t("no_file"))
        else:
            self.lbl_info.setText(f"{self.grid.count()} {trans.t('pages')}")
