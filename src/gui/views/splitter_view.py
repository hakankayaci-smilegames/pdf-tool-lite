import os
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, 
                             QPushButton, QLabel, QFileDialog, QMessageBox, QApplication)
from PyQt6.QtCore import Qt

from src.gui.components.thumbnail_grid import ThumbnailGrid
from src.gui.components.range_input import RangeInput
from src.core.splitter import split_pdf, indices_to_range_string
from src.core.i18n import trans

class SplitterView(QWidget):
    def __init__(self, status_callback=None, parent=None):
        super().__init__(parent)
        self.status_callback = status_callback
        self.current_pdf_path = None
        self.selected_indices = []
        self._is_syncing = False
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.grid = ThumbnailGrid()
        self.grid.itemSelectionChanged.connect(self._on_grid_selection_changed)
        layout.addWidget(self.grid)
        
        right_panel = QWidget()
        right_panel.setFixedWidth(260)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(15, 0, 0, 0)
        
        self.header = QLabel(trans.t("splitter"))
        self.header.setObjectName("HeaderLabel")
        self.lbl_info = QLabel(trans.t("no_file"))
        
        self.range_input = RangeInput()
        self.range_input.range_parsed.connect(self._on_range_parsed)
        
        self.btn_save = QPushButton(trans.t("save_selected"))
        self.btn_save.setObjectName("PrimaryBtn")
        self.btn_save.setEnabled(False)
        self.btn_save.clicked.connect(self._save_pdf)
        
        right_layout.addWidget(self.header)
        right_layout.addWidget(self.lbl_info)
        right_layout.addSpacing(20)
        right_layout.addWidget(self.range_input)
        right_layout.addStretch()
        right_layout.addWidget(self.btn_save)
        
        layout.addWidget(right_panel)
        
    def set_pdf(self, file_path):
        self.current_pdf_path = file_path
        self.grid.load_pdf(file_path)
        max_pages = self.grid.count()
        self.lbl_info.setText(f"{max_pages} {trans.t('pages')}")
        self.range_input.set_max_pages(max_pages)
        self.btn_save.setEnabled(True)
        
    def _on_grid_selection_changed(self):
        """Kullanıcı fare ile grid üzerinden sayfa seçtiğinde aralık kutusunu senkronize eder."""
        if self._is_syncing:
            return
            
        self._is_syncing = True
        try:
            selected_items = self.grid.selectedItems()
            selected = sorted([item.data(Qt.ItemDataRole.UserRole) for item in selected_items])
            self.selected_indices = selected
            
            # Kutuya metin olarak yansıt
            range_str = indices_to_range_string(selected)
            self.range_input.input_box.setText(range_str)
        finally:
            self._is_syncing = False

    def _on_range_parsed(self, indices: list[int]):
        """Kullanıcı metin kutusuna aralık girdiğinde grid üzerindeki seçimi senkronize eder."""
        if self._is_syncing:
            return
            
        self._is_syncing = True
        try:
            self.grid.clearSelection()
            for i in range(self.grid.count()):
                item = self.grid.item(i)
                original_idx = item.data(Qt.ItemDataRole.UserRole)
                if original_idx in indices:
                    item.setSelected(True)
            self.selected_indices = indices
        finally:
            self._is_syncing = False

    def _save_pdf(self):
        if not self.current_pdf_path or not self.selected_indices:
            return
            
        save_path, _ = QFileDialog.getSaveFileName(self, trans.t("save"), "", "PDF (*.pdf)")
        if save_path:
            if not save_path.lower().endswith('.pdf'):
                save_path += '.pdf'
                
            if self.status_callback:
                self.status_callback(trans.t("loading"))
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            
            try:
                # Seçilen sayfaların dönüş açılarını topla
                rotations = []
                for item in self.grid.selectedItems():
                    rotations.append(item.data(Qt.ItemDataRole.UserRole + 1) or 0)
                    
                split_pdf(self.current_pdf_path, save_path, self.selected_indices, rotations)
                QMessageBox.information(self, trans.t("success"), trans.t("saved"))
                if self.status_callback:
                    self.status_callback(trans.t("ready"))
            except Exception as e:
                QMessageBox.critical(self, trans.t("error"), str(e))
                if self.status_callback:
                    self.status_callback(trans.t("error"))
            finally:
                QApplication.restoreOverrideCursor()
                
    def update_texts(self):
        self.header.setText(trans.t("splitter"))
        self.btn_save.setText(trans.t("save_selected"))
        if not self.current_pdf_path:
            self.lbl_info.setText(trans.t("no_file"))
        else:
            self.lbl_info.setText(f"{self.grid.count()} {trans.t('pages')}")
