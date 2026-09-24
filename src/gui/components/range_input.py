from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel
from PyQt6.QtCore import pyqtSignal
from src.core.splitter import parse_range_string
from src.core.i18n import trans

class RangeInput(QWidget):
    range_parsed = pyqtSignal(list)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.max_pages = 0
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.label = QLabel(trans.t("select_pages"))
        self.input_box = QLineEdit()
        self.input_box.textChanged.connect(self._on_text_changed)
        
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #f38ba8; font-size: 11px;")
        
        layout.addWidget(self.label)
        layout.addWidget(self.input_box)
        layout.addWidget(self.error_label)
        
    def set_max_pages(self, max_pages: int):
        self.max_pages = max_pages
        self._on_text_changed(self.input_box.text())
        
    def _on_text_changed(self, text: str):
        if self.max_pages <= 0: return
        parsed = parse_range_string(text, self.max_pages)
        if text.strip() and not parsed:
            self.error_label.setText("X")
            self.range_parsed.emit([])
        else:
            self.error_label.setText("")
            self.range_parsed.emit(parsed)
            
    def update_texts(self):
        self.label.setText(trans.t("select_pages"))
