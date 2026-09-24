import pikepdf

def merge_pdfs(input_paths: list[str], output_path: str) -> bool:
    """Birden fazla PDF'i sırasıyla tek bir dosyada birleştirir."""
    if not input_paths:
        raise ValueError("Birleştirilecek dosya seçilmedi.")
        
    pdf_out = pikepdf.Pdf.new()
    for path in input_paths:
        with pikepdf.Pdf.open(path) as pdf:
            pdf_out.pages.extend(pdf.pages)
            
    pdf_out.save(output_path)
    return True
