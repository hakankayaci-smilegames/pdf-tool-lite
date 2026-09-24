import pikepdf

def get_metadata(pdf_path: str) -> dict:
    """PDF dosyasının temel meta verilerini okur."""
    with pikepdf.Pdf.open(pdf_path) as pdf:
        meta = pdf.docinfo
        return {
            "title": str(meta.get("/Title", "")),
            "author": str(meta.get("/Author", "")),
            "subject": str(meta.get("/Subject", "")),
            "creator": str(meta.get("/Creator", "")),
            "producer": str(meta.get("/Producer", ""))
        }

def set_metadata(pdf_path: str, output_path: str, meta_dict: dict) -> bool:
    """PDF dosyasına yeni meta verileri yazar (Gizlilik için değerleri silebilir)."""
    with pikepdf.Pdf.open(pdf_path) as pdf:
        # Standart XMP metadatasını güncelle
        with pdf.open_metadata() as meta:
            if "title" in meta_dict: meta["dc:title"] = meta_dict["title"]
            if "author" in meta_dict: meta["dc:creator"] = [meta_dict["author"]]
            if "subject" in meta_dict: meta["dc:description"] = meta_dict["subject"]
            
        # Geleneksel DocInfo sözlüğünü güncelle (eski tip okuyucular için)
        if "title" in meta_dict: pdf.docinfo["/Title"] = meta_dict["title"]
        if "author" in meta_dict: pdf.docinfo["/Author"] = meta_dict["author"]
        if "subject" in meta_dict: pdf.docinfo["/Subject"] = meta_dict["subject"]
        if "creator" in meta_dict: pdf.docinfo["/Creator"] = meta_dict["creator"]
        if "producer" in meta_dict: pdf.docinfo["/Producer"] = meta_dict["producer"]
        
        pdf.save(output_path)
    return True
