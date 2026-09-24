import locale

class I18n:
    def __init__(self):
        self.lang = "en"
        # İşletim sistemi dilini alıp Türkçeyse varsayılanı TR yapıyoruz
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
                "loading": "Yükleniyor...",
                "saved": "Başarıyla kaydedildi!",
                "error": "Hata oluştu",
                "select_pages": "Aralık Seç (örn: 1-5, 8, tek):",
                "no_file": "Dosya yüklenmedi",
                "pages": "Sayfa",
                "files": "Dosya",
                "delete": "Sil",
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
                "loading": "Loading...",
                "saved": "Successfully saved!",
                "error": "Error occurred",
                "select_pages": "Range (e.g. 1-5, 8, odd):",
                "no_file": "No file loaded",
                "pages": "Pages",
                "files": "Files",
                "delete": "Delete",
                "success": "Success"
            }
        }

    def t(self, key: str) -> str:
        return self.texts.get(self.lang, self.texts["en"]).get(key, key)
        
    def set_lang(self, lang: str):
        if lang in self.texts:
            self.lang = lang

trans = I18n()
