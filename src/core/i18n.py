import locale

class I18n:
    def __init__(self):
        self.lang = "en"
        try:
            sys_loc = locale.getdefaultlocale()[0]
            if sys_loc and sys_loc.startswith("tr"):
                self.lang = "tr"
        except:
            pass

        self.texts = {
            "tr": {
                "app_title": "PDF Tool Lite",
                "splitter": "Sayfa Ayırıcı",
                "merger": "Birleştirici",
                "organizer": "Sayfa Düzenleyici",
                "to_image": "Görsele Dönüştür",
                "metadata": "Meta Düzenleyici",
                "load_pdf": "PDF Yükle",
                "add_pdfs": "PDF Ekle",
                "save": "Kaydet",
                "save_selected": "Seçilenleri Ayır ve Kaydet",
                "merge_save": "Birleştir ve Kaydet",
                "export_images": "Görsel Olarak Aktar",
                "ready": "Hazır",
                "loading": "İşleniyor...",
                "saved": "Başarıyla kaydedildi!",
                "error": "Hata oluştu",
                "select_pages": "Aralık Seç (örn: 1-5, 8, tek):",
                "no_file": "Dosya yüklenmedi (PDF sürükleyip bırakabilirsiniz)",
                "pages": "Sayfa",
                "files": "Dosya",
                "delete": "Sil (Delete)",
                "move_left": "Sola Taşı (Ctrl+Sol)",
                "move_right": "Sağa Taşı (Ctrl+Sağ)",
                "rotate_cw": "90° Sağa Döndür (CW)",
                "rotate_ccw": "90° Sola Döndür (CCW)",
                "wipe_metadata": "Tüm Meta Verileri Temizle",
                "move_up": "Yukarı Taşı",
                "move_down": "Aşağı Taşı",
                "success": "İşlem Başarılı"
            },
            "en": {
                "app_title": "PDF Tool Lite",
                "splitter": "Splitter",
                "merger": "Merger",
                "organizer": "Organizer",
                "to_image": "To Image",
                "metadata": "Metadata",
                "load_pdf": "Load PDF",
                "add_pdfs": "Add PDFs",
                "save": "Save",
                "save_selected": "Split & Save Selected",
                "merge_save": "Merge & Save",
                "export_images": "Export as Images",
                "ready": "Ready",
                "loading": "Processing...",
                "saved": "Successfully saved!",
                "error": "Error occurred",
                "select_pages": "Range (e.g. 1-5, 8, odd):",
                "no_file": "No file loaded (Drag & drop PDF here)",
                "pages": "Pages",
                "files": "Files",
                "delete": "Delete (Delete)",
                "move_left": "Move Left (Ctrl+Left)",
                "move_right": "Move Right (Ctrl+Right)",
                "rotate_cw": "Rotate 90° Clockwise",
                "rotate_ccw": "Rotate 90° Counter-Clockwise",
                "wipe_metadata": "Wipe All Metadata",
                "move_up": "Move Up",
                "move_down": "Move Down",
                "success": "Success"
            }
        }

    def t(self, key: str) -> str:
        return self.texts.get(self.lang, self.texts["en"]).get(key, key)
        
    def set_lang(self, lang: str):
        if lang in self.texts:
            self.lang = lang

trans = I18n()
