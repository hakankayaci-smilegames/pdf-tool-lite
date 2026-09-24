import os
import fitz  # PyMuPDF
from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView, QMenu
from PyQt6.QtGui import QPixmap, QImage, QIcon, QAction
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from src.core.i18n import trans

class ThumbnailGrid(QListWidget):
    """
    PDF sayfalarını küçük resim olarak listeleyen bileşen.
    Sürükle-bırak hatalarını önlemek için Klavye ve Sağ Tık destekli sıralama sunar.
    """
    order_changed = pyqtSignal()
    pages_deleted = pyqtSignal(list)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pdf_document = None
        self._setup_ui()

    def _setup_ui(self):
        self.setViewMode(QListWidget.ViewMode.IconMode)
        self.setIconSize(QSize(150, 200))
        self.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.setSpacing(15)
        # Serbest hareketi kapatıyoruz, ızgara mükemmel hizalanacak
        self.setMovement(QListWidget.Movement.Static)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

    def load_pdf(self, pdf_path: str):
        self.clear()
        if not os.path.exists(pdf_path): return
            
        if self.pdf_document:
            self.pdf_document.close()
            
        self.pdf_document = fitz.open(pdf_path)
        
        for page_num in range(len(self.pdf_document)):
            page = self.pdf_document.load_page(page_num)
            pix = page.get_pixmap(matrix=fitz.Matrix(0.2, 0.2))
            
            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
            qpixmap = QPixmap.fromImage(img)
            
            item = QListWidgetItem()
            item.setIcon(QIcon(qpixmap))
            item.setText(f"{trans.t('pages')} {page_num + 1}")
            item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
            item.setData(Qt.ItemDataRole.UserRole, page_num)
            
            self.addItem(item)

    def _show_context_menu(self, position):
        if not self.selectedItems():
            return
            
        menu = QMenu()
        
        # Sadece tekli seçimde kaydırma izni
        if len(self.selectedItems()) == 1:
            action_left = QAction("Sola Taşı (Ctrl+Sol)", self)
            action_left.triggered.connect(self._move_left)
            menu.addAction(action_left)
            
            action_right = QAction("Sağa Taşı (Ctrl+Sağ)", self)
            action_right.triggered.connect(self._move_right)
            menu.addAction(action_right)
            
            menu.addSeparator()
            
        delete_action = QAction(trans.t("delete"), self)
        delete_action.triggered.connect(self._delete_selected)
        menu.addAction(delete_action)
        
        menu.exec(self.mapToGlobal(position))

    def _move_left(self):
        row = self.currentRow()
        if row > 0:
            item = self.takeItem(row)
            self.insertItem(row - 1, item)
            self.setCurrentRow(row - 1)
            self.order_changed.emit()

    def _move_right(self):
        row = self.currentRow()
        if row < self.count() - 1 and row >= 0:
            item = self.takeItem(row)
            self.insertItem(row + 1, item)
            self.setCurrentRow(row + 1)
            self.order_changed.emit()

    def _delete_selected(self):
        selected_items = self.selectedItems()
        if not selected_items: return
            
        deleted_indices = []
        for item in selected_items:
            deleted_indices.append(item.data(Qt.ItemDataRole.UserRole))
            row = self.row(item)
            self.takeItem(row)
            
        self.pages_deleted.emit(deleted_indices)
        self.order_changed.emit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            self._delete_selected()
        elif event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_Left:
                self._move_left()
            elif event.key() == Qt.Key.Key_Right:
                self._move_right()
        else:
            super().keyPressEvent(event)

    def get_current_order(self) -> list[int]:
        return [self.item(i).data(Qt.ItemDataRole.UserRole) for i in range(self.count())]

    def closeEvent(self, event):
        if self.pdf_document:
            self.pdf_document.close()
        super().closeEvent(event)
