from PyQt6.QtWidgets import QListWidget, QListWidgetItem
from PyQt6.QtCore import pyqtSignal
from src.core.i18n import trans

class Sidebar(QListWidget):
    module_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(200)
        
        self.module_defs = [
            ("splitter", "splitter"),
            ("merger", "merger"),
            ("organizer", "organizer"),
            ("to_image", "to_image"),
            ("metadata", "metadata")
        ]
        
        for lang_key, _ in self.module_defs:
            self.addItem(QListWidgetItem(trans.t(lang_key)))
            
        self.currentRowChanged.connect(self._on_row_changed)
        self.setCurrentRow(0)
        
    def _on_row_changed(self, index: int):
        if 0 <= index < self.count():
            module_id = self.module_defs[index][1]
            self.module_selected.emit(module_id)
            
    def update_texts(self):
        for i, (lang_key, _) in enumerate(self.module_defs):
            self.item(i).setText(trans.t(lang_key))
