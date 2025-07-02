import pytesseract
from pdf2image import convert_from_path
import os, time

def ocr_batch(pdf_path, output_dir, batch_size=50, dpi=300, max_pages=None):
    os.makedirs(output_dir, exist_ok=True)
    
    # Estimate total number of pages first
    print("[*] Estimating page count...")
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
    except:
        print("[!] Couldn't auto-detect page count. Using max_pages fallback.")
        total_pages = max_pages or 300

    print(f"[✓] Total pages: {total_pages}")

    for start in range(1, total_pages + 1, batch_size):
        end = min(start + batch_size - 1, total_pages)
        print(f"\n[*] Processing pages {start}–{end}...")
        start_time = time.time()

        try:
            images = convert_from_path(pdf_path, dpi=dpi, first_page=start, last_page=end)
        except Exception as e:
            print(f"[!] Error processing pages {start}–{end}: {e}")
            continue

        batch_text = ""
        for i, img in enumerate(images, start=start):
            page_start = time.time()
            text = pytesseract.image_to_string(img)
            batch_text += text + "\n\n"
            print(f"[✓] Page {i} done in {time.time() - page_start:.2f} sec")

        filename = f"textbook_{start}_{end}.txt"
        with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
            f.write(batch_text)

        print(f"[✓] Saved batch {start}-{end} in {time.time() - start_time:.2f} sec")

    print("\n✅ All batches complete.")

if __name__ == "__main__":
    pdf_path = "data/raw/socio-textbook.pdf"
    output_dir = "data/cleaned/batches"
    ocr_batch(pdf_path, output_dir, batch_size=50)
