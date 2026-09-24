import fitz
import os

def export_pages_to_images(pdf_path: str, output_dir: str, page_indices: list[int], dpi: int = 300) -> bool:
    """PDF sayfalarını yüksek çözünürlüklü PNG görselleri olarak dışa aktarır."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    doc = fitz.open(pdf_path)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    # 72 DPI referansına göre yakınlaştırma (Zoom) hesapla
    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)
    
    for idx in page_indices:
        if 0 <= idx < len(doc):
            page = doc.load_page(idx)
            pix = page.get_pixmap(matrix=matrix)
            out_file = os.path.join(output_dir, f"{base_name}_sayfa_{idx+1}.png")
            pix.save(out_file)
            
    doc.close()
    return True
