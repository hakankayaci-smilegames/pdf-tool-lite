import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QListWidget, QListWidgetItem, QFileDialog, QMessageBox, QLabel, 
                             QAbstractItemView, QApplication)
from PyQt6.QtCore import Qt
from src.core.merger import merge_pdfs
from src.core.i18n import trans

class MergerListWidget(QListWidget):
    """Masaüstünden sürüklenen PDF'leri doğrudan listeye ekleyen widget."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.lower().endswith(".pdf") and os.path.exists(file_path):
                    item = QListWidgetItem(f"📄 {os.path.basename(file_path)}")
                    item.setToolTip(file_path)
                    item.setData(Qt.ItemDataRole.UserRole, file_path)
                    self.addItem(item)
            event.acceptProposedAction()
            if hasattr(self.parent(), "_update_ui"):
                self.parent()._update_ui()
        else:
            super().dropEvent(event)


class MergerView(QWidget):
    def __init__(self, status_callback=None, parent=None):
        super().__init__(parent)
        self.status_callback = status_callback
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        left_layout = QVBoxLayout()
        self.btn_add = QPushButton(trans.t("add_pdfs"))
        self.btn_add.setObjectName("PrimaryBtn")
        self.btn_add.clicked.connect(self._add_files)
        
        self.list_widget = MergerListWidget(self)
        
        # Sıralama Butonları
        btn_box = QHBoxLayout()
        self.btn_up = QPushButton(f"▲ {trans.t('move_up')}")
        self.btn_up.clicked.connect(self._move_up)
        self.btn_down = QPushButton(f"▼ {trans.t('move_down')}")
        self.btn_down.clicked.connect(self._move_down)
        btn_box.addWidget(self.btn_up)
        btn_box.addWidget(self.btn_down)
        
        left_layout.addWidget(self.btn_add)
        left_layout.addWidget(self.list_widget)
        left_layout.addLayout(btn_box)
        
        right_panel = QWidget()
        right_panel.setFixedWidth(260)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(15, 0, 0, 0)
        
        self.header = QLabel(trans.t("merger"))
        self.header.setObjectName("HeaderLabel")
        
        self.lbl_info = QLabel(f"0 {trans.t('files')}")
        
        lbl_hint = QLabel("PDF dosyalarını masaüstünden buraya da sürükleyip bırakabilirsiniz.")
        lbl_hint.setWordWrap(True)
        lbl_hint.setStyleSheet("color: #7f849c; font-size: 11px;")
        
        self.btn_remove = QPushButton(trans.t("delete"))
        self.btn_remove.setObjectName("DangerBtn")
        self.btn_remove.clicked.connect(self._remove_selected)
        
        self.btn_save = QPushButton(trans.t("merge_save"))
        self.btn_save.setObjectName("PrimaryBtn")
        self.btn_save.setEnabled(False)
        self.btn_save.clicked.connect(self._save_merged)
        
        right_layout.addWidget(self.header)
        right_layout.addWidget(self.lbl_info)
        right_layout.addWidget(lbl_hint)
        right_layout.addSpacing(10)
        right_layout.addWidget(self.btn_remove)
        right_layout.addStretch()
        right_layout.addWidget(self.btn_save)
        
        layout.addLayout(left_layout)
        layout.addWidget(right_panel)

    def _add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, trans.t("add_pdfs"), "", "PDF (*.pdf)")
        if files:
            for f in files:
                item = QListWidgetItem(f"📄 {os.path.basename(f)}")
                item.setToolTip(f)
                item.setData(Qt.ItemDataRole.UserRole, f)
                self.list_widget.addItem(item)
            self._update_ui()
            
    def _move_up(self):
        row = self.list_widget.currentRow()
        if row > 0:
            item = self.list_widget.takeItem(row)
            self.list_widget.insertItem(row - 1, item)
            self.list_widget.setCurrentRow(row - 1)
            
    def _move_down(self):
        row = self.list_widget.currentRow()
        if row < self.list_widget.count() - 1 and row >= 0:
            item = self.list_widget.takeItem(row)
            self.list_widget.insertItem(row + 1, item)
            self.list_widget.setCurrentRow(row + 1)

    def _remove_selected(self):
        for item in self.list_widget.selectedItems():
            idx = self.list_widget.row(item)
            self.list_widget.takeItem(idx)
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
            
            # Doğrudan UserRole'daki mutlak dosya yolunu al (Aynı isimli dosya çakışmasını kökten çözer)
            ordered_paths = [self.list_widget.item(i).data(Qt.ItemDataRole.UserRole) for i in range(self.list_widget.count())]
                        
            if self.status_callback: self.status_callback(trans.t("loading"))
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            try:
                merge_pdfs(ordered_paths, save_path)
                QMessageBox.information(self, trans.t("success"), trans.t("saved"))
                if self.status_callback: self.status_callback(trans.t("ready"))
            except Exception as e:
                QMessageBox.critical(self, trans.t("error"), str(e))
                if self.status_callback: self.status_callback(trans.t("error"))
            finally:
                QApplication.restoreOverrideCursor()
                
    def update_texts(self):
        self.header.setText(trans.t("merger"))
        self.btn_add.setText(trans.t("add_pdfs"))
        self.btn_remove.setText(trans.t("delete"))
        self.btn_save.setText(trans.t("merge_save"))
        self.btn_up.setText(f"▲ {trans.t('move_up')}")
        self.btn_down.setText(f"▼ {trans.t('move_down')}")
        self._update_ui()
