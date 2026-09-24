import os
import pikepdf

def parse_range_string(range_str: str, max_pages: int) -> list[int]:
    """
    Sayfa aralığı string'ini (örn: '1-3, 5, tek') ayrıştırır ve 
    benzersiz, sıralı (0-indexed) sayfa numaraları listesi döner.
    """
    if not range_str or not range_str.strip():
        return []

    range_str = range_str.lower().strip()
    
    if range_str in ("hepsi", "all"):
        return list(range(max_pages))
    if range_str in ("tek", "odd"):
        return [i for i in range(max_pages) if i % 2 == 0]
    if range_str in ("çift", "even"):
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
                
                start = max(0, min(start, max_pages - 1))
                end = max(0, min(end, max_pages - 1))
                
                if start <= end:
                    pages.update(range(start, end + 1))
        elif part.isdigit():
            page_idx = int(part) - 1
            if 0 <= page_idx < max_pages:
                pages.add(page_idx)
                
    return sorted(list(pages))

def indices_to_range_string(indices: list[int]) -> str:
    """
    0-indexed sayfa listesini (örn: [0, 1, 2, 4, 7]) 
    kullanıcı dostu aralık stringine ('1-3, 5, 8') çevirir.
    """
    if not indices:
        return ""
        
    sorted_unique = sorted(list(set(indices)))
    one_indexed = [idx + 1 for idx in sorted_unique]
    
    ranges = []
    start = one_indexed[0]
    prev = start
    
    for num in one_indexed[1:]:
        if num == prev + 1:
            prev = num
        else:
            if start == prev:
                ranges.append(str(start))
            else:
                ranges.append(f"{start}-{prev}")
            start = num
            prev = num
            
    if start == prev:
        ranges.append(str(start))
    else:
        ranges.append(f"{start}-{prev}")
        
    return ", ".join(ranges)

def split_pdf(input_path: str, output_path: str, page_indices: list[int], rotations: list[int] = None) -> bool:
    """
    Belirtilen sayfa indekslerini asıl dosyadan kopartıp yeni bir dosyaya kaydeder.
    Opsiyonel olarak her sayfa için açısal döndürme (0, 90, 180, 270) uygular.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Dosya bulunamadı: {input_path}")
        
    if not page_indices:
        raise ValueError("Çıkarılacak sayfa belirtilmedi.")

    with pikepdf.Pdf.open(input_path) as pdf:
        new_pdf = pikepdf.Pdf.new()
        max_pages = len(pdf.pages)
        
        for i, idx in enumerate(page_indices):
            if 0 <= idx < max_pages:
                new_page = new_pdf.pages.append(pdf.pages[idx])
                if rotations and i < len(rotations) and rotations[i] != 0:
                    current_rot = int(new_page.get('/Rotate', 0))
                    new_page.Rotate = (current_rot + rotations[i]) % 360
            else:
                raise ValueError(f"Geçersiz sayfa indeksi: {idx}")
                
        new_pdf.save(output_path)
        
    return True
