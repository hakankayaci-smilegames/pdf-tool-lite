import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QMessageBox, QLineEdit, QFormLayout, QApplication)
from src.core.metadata import get_metadata, set_metadata
from src.core.i18n import trans

class MetadataView(QWidget):
    def __init__(self, status_callback=None, parent=None):
        super().__init__(parent)
        self.status_callback = status_callback
        self.current_pdf_path = None
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        
        self.header = QLabel(trans.t("metadata"))
        self.header.setObjectName("HeaderLabel")
        
        self.lbl_info = QLabel(trans.t("no_file"))
        self.lbl_info.setStyleSheet("margin-bottom: 20px; font-weight: bold;")
        
        form = QFormLayout()
        self.inp_title = QLineEdit()
        self.inp_author = QLineEdit()
        self.inp_subject = QLineEdit()
        self.inp_creator = QLineEdit()
        self.inp_producer = QLineEdit()
        
        form.addRow("Title:", self.inp_title)
        form.addRow("Author:", self.inp_author)
        form.addRow("Subject:", self.inp_subject)
        form.addRow("Creator:", self.inp_creator)
        form.addRow("Producer:", self.inp_producer)
        
        # Butonlar
        btn_layout = QHBoxLayout()
        self.btn_wipe = QPushButton(f"🧹 {trans.t('wipe_metadata')}")
        self.btn_wipe.setObjectName("DangerBtn")
        self.btn_wipe.setEnabled(False)
        self.btn_wipe.clicked.connect(self._wipe_metadata)
        
        self.btn_save = QPushButton(trans.t("save"))
        self.btn_save.setObjectName("PrimaryBtn")
        self.btn_save.setEnabled(False)
        self.btn_save.clicked.connect(self._save_metadata)
        
        btn_layout.addWidget(self.btn_wipe)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_save)
        
        layout.addWidget(self.header)
        layout.addWidget(self.lbl_info)
        layout.addLayout(form)
        layout.addStretch()
        layout.addLayout(btn_layout)
        
    def set_pdf(self, file_path):
        self.current_pdf_path = file_path
        self.lbl_info.setText(f"📄 {os.path.basename(file_path)}")
        
        meta = get_metadata(file_path)
        self.inp_title.setText(meta.get("title", ""))
        self.inp_author.setText(meta.get("author", ""))
        self.inp_subject.setText(meta.get("subject", ""))
        self.inp_creator.setText(meta.get("creator", ""))
        self.inp_producer.setText(meta.get("producer", ""))
        
        self.btn_save.setEnabled(True)
        self.btn_wipe.setEnabled(True)

    def _wipe_metadata(self):
        """Tüm meta veri kutularını tek tıkla boşaltır."""
        self.inp_title.clear()
        self.inp_author.clear()
        self.inp_subject.clear()
        self.inp_creator.clear()
        self.inp_producer.clear()
        if self.status_callback:
            self.status_callback("Tüm meta alanları temizlendi. Kaydedebilirsiniz.")

    def _save_metadata(self):
        if not self.current_pdf_path: return
        save_path, _ = QFileDialog.getSaveFileName(self, trans.t("save"), "", "PDF (*.pdf)")
        if save_path:
            if not save_path.lower().endswith('.pdf'): save_path += '.pdf'
            if self.status_callback: self.status_callback(trans.t("loading"))
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            
            meta_dict = {
                "title": self.inp_title.text(),
                "author": self.inp_author.text(),
                "subject": self.inp_subject.text(),
                "creator": self.inp_creator.text(),
                "producer": self.inp_producer.text()
            }
            try:
                set_metadata(self.current_pdf_path, save_path, meta_dict)
                QMessageBox.information(self, trans.t("success"), trans.t("saved"))
                if self.status_callback: self.status_callback(trans.t("ready"))
            except Exception as e:
                QMessageBox.critical(self, trans.t("error"), str(e))
                if self.status_callback: self.status_callback(trans.t("error"))
            finally:
                QApplication.restoreOverrideCursor()
                
    def update_texts(self):
        self.header.setText(trans.t("metadata"))
        self.btn_save.setText(trans.t("save"))
        self.btn_wipe.setText(f"🧹 {trans.t('wipe_metadata')}")
        if not self.current_pdf_path:
            self.lbl_info.setText(trans.t("no_file"))
