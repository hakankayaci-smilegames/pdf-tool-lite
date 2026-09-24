import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QPushButton, QLabel, QFileDialog, QStackedWidget)
from PyQt6.QtCore import Qt

from src.gui.theme import get_stylesheet
from src.gui.components.sidebar import Sidebar
from src.gui.views.splitter_view import SplitterView
from src.gui.views.merger_view import MergerView
from src.gui.views.organizer_view import OrganizerView
from src.gui.views.to_image_view import ToImageView
from src.gui.views.metadata_view import MetadataView
from src.core.i18n import trans

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(trans.t("app_title"))
        self.resize(1150, 720)
        
        self.setAcceptDrops(True)
        self.is_dark_mode = True
        self.setStyleSheet(get_stylesheet(self.is_dark_mode))
        
        self.current_global_pdf = None
        self._setup_ui()
        
    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- Top Bar ---
        self.top_bar = QWidget()
        self.top_bar.setObjectName("TopBar")
        self.top_bar.setFixedHeight(65)
        top_layout = QHBoxLayout(self.top_bar)
        top_layout.setContentsMargins(20, 0, 20, 0)
        
        self.lbl_title = QLabel("PDF Tool Lite")
        self.lbl_title.setObjectName("TitleLabel")
        
        self.btn_load_global = QPushButton(trans.t("load_pdf"))
        self.btn_load_global.setObjectName("PrimaryBtn")
        self.btn_load_global.setFixedWidth(180)
        self.btn_load_global.clicked.connect(self._load_global_pdf)
        
        self.lbl_active_file = QLabel(trans.t("no_file"))
        self.lbl_active_file.setStyleSheet("font-style: italic; font-weight: bold;")
        
        self.btn_lang = QPushButton("EN" if trans.lang == "tr" else "TR")
        self.btn_lang.setFixedWidth(40)
        self.btn_lang.clicked.connect(self._toggle_lang)
        
        self.btn_theme = QPushButton("☀️")
        self.btn_theme.setFixedWidth(40)
        self.btn_theme.clicked.connect(self._toggle_theme)
        
        top_layout.addWidget(self.lbl_title)
        top_layout.addSpacing(30)
        top_layout.addWidget(self.btn_load_global)
        top_layout.addSpacing(15)
        top_layout.addWidget(self.lbl_active_file)
        top_layout.addStretch()
        top_layout.addWidget(self.btn_theme)
        top_layout.addWidget(self.btn_lang)
        
        # --- Body ---
        body_widget = QWidget()
        body_layout = QHBoxLayout(body_widget)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)
        
        self.sidebar = Sidebar()
        self.sidebar.module_selected.connect(self._switch_module)
        
        self.stack = QStackedWidget()
        self.views = {
            "splitter": SplitterView(self.set_status),
            "merger": MergerView(self.set_status),
            "organizer": OrganizerView(self.set_status),
            "to_image": ToImageView(self.set_status),
            "metadata": MetadataView(self.set_status)
        }
        for view in self.views.values():
            self.stack.addWidget(view)
            
        body_layout.addWidget(self.sidebar)
        body_layout.addWidget(self.stack)
        
        main_layout.addWidget(self.top_bar)
        main_layout.addWidget(body_widget)
        
        self.statusBar().showMessage(trans.t("ready"))

    def set_status(self, msg: str):
        self.statusBar().showMessage(msg)
        
    def _load_pdf_path(self, file_path: str):
        """Merkezi PDF dosyasını yükler ve tüm ilgili modüllere iletir."""
        if not file_path or not os.path.exists(file_path):
            return
            
        try:
            self.current_global_pdf = file_path
            self.lbl_active_file.setText(f"📄 {os.path.basename(file_path)}")
            for key, view in self.views.items():
                if hasattr(view, "set_pdf"):
                    view.set_pdf(file_path)
            self.set_status(trans.t("ready"))
        except Exception as e:
            import traceback
            traceback.print_exc()
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, trans.t("error"), f"PDF okunamadı:\n{str(e)}")

    def _load_global_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, trans.t("load_pdf"), "", "PDF (*.pdf)")
        if file_path:
            self._load_pdf_path(file_path)

    def dragEnterEvent(self, event):
        """Masaüstünden dosya sürüklendiğinde kabul eder."""
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
        """Masaüstünden bırakılan PDF dosyasını anında açar."""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            # Eğer Birleştirici (Merger) sekmesindeysek dosyaları oraya yolla
            if self.stack.currentIndex() == 1:
                merger_view = self.views["merger"]
                for url in urls:
                    f = url.toLocalFile()
                    if f.lower().endswith(".pdf") and os.path.exists(f):
                        from PyQt6.QtWidgets import QListWidgetItem
                        item = QListWidgetItem(f"📄 {os.path.basename(f)}")
                        item.setToolTip(f)
                        item.setData(Qt.ItemDataRole.UserRole, f)
                        merger_view.list_widget.addItem(item)
                merger_view._update_ui()
                event.acceptProposedAction()
                return

            # Diğer sekmelerde ilk PDF'i merkezi olarak yükle
            for url in urls:
                f = url.toLocalFile()
                if f.lower().endswith(".pdf") and os.path.exists(f):
                    self._load_pdf_path(f)
                    event.acceptProposedAction()
                    break

    def _switch_module(self, module_id: str):
        mapping = {"splitter": 0, "merger": 1, "organizer": 2, "to_image": 3, "metadata": 4}
        self.stack.setCurrentIndex(mapping.get(module_id, 0))
        
    def _toggle_lang(self):
        new_lang = "en" if trans.lang == "tr" else "tr"
        trans.set_lang(new_lang)
        self.btn_lang.setText("TR" if new_lang == "en" else "EN")
        self.setWindowTitle(trans.t("app_title"))
        self.btn_load_global.setText(trans.t("load_pdf"))
        self.set_status(trans.t("ready"))
        if not self.current_global_pdf:
            self.lbl_active_file.setText(trans.t("no_file"))
        self.sidebar.update_texts()
        for view in self.views.values():
            if hasattr(view, "update_texts"):
                view.update_texts()

    def _toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.btn_theme.setText("🌙" if self.is_dark_mode else "☀️")
        self.setStyleSheet(get_stylesheet(self.is_dark_mode))
