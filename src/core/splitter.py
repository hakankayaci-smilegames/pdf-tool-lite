import os
import pikepdf

def parse_range_string(range_str: str, max_pages: int) -> list[int]:
    """
    Sayfa aralığı string'ini (örn: '1-3, 5, tek') ayrıştırır ve 
    benzersiz, sıralı (0-indexed) sayfa numaraları listesi döner.
    Hatalı girdiler sessizce yoksayılır.
    """
    if not range_str or not range_str.strip():
        return []

    range_str = range_str.lower().strip()
    
    if range_str == "hepsi":
        return list(range(max_pages))
    if range_str == "tek":
        return [i for i in range(max_pages) if i % 2 == 0]
    if range_str == "çift":
        return [i for i in range(max_pages) if i % 2 != 0]

    pages = set()
    parts = range_str.split(",")
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
            
        if "-" in part:
            bounds = part.split("-")
            if len(bounds) == 2 and bounds[0].isdigit() and bounds[1].isdigit():
                start = int(bounds[0]) - 1
                end = int(bounds[1]) - 1
                
                # Sınırları kontrol et
                start = max(0, min(start, max_pages - 1))
                end = max(0, min(end, max_pages - 1))
                
                if start <= end:
                    pages.update(range(start, end + 1))
        elif part.isdigit():
            page_idx = int(part) - 1
            if 0 <= page_idx < max_pages:
                pages.add(page_idx)
                
    return sorted(list(pages))

def split_pdf(input_path: str, output_path: str, page_indices: list[int]) -> bool:
    """
    Belirtilen sayfa indekslerini (0-indexed) asıl dosyadan kopartıp yeni bir dosyaya kaydeder.
    pikepdf ile kayıpsız ve yüksek hızda çalışır.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Dosya bulunamadı: {input_path}")
        
    if not page_indices:
        raise ValueError("Çıkarılacak sayfa belirtilmedi.")

    with pikepdf.Pdf.open(input_path) as pdf:
        new_pdf = pikepdf.Pdf.new()
        
        max_pages = len(pdf.pages)
        for idx in page_indices:
            if 0 <= idx < max_pages:
                new_pdf.pages.append(pdf.pages[idx])
            else:
                raise ValueError(f"Geçersiz sayfa indeksi: {idx}")
                
        new_pdf.save(output_path)
        
    return True
