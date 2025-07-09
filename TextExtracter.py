import os
import pdfplumber

def extract_text_from_pdf(pdf_path, remove_headers_footers=True):
    full_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            if remove_headers_footers:
                top_margin = 60
                bottom_margin = 60
                cropped = page.within_bbox((0, top_margin, page.width, page.height - bottom_margin))
                text = cropped.extract_text()
            else:
                text = page.extract_text()

            if text:
                full_text += text + "\n\n"
    
    return full_text

def extract_text_from_all_pdfs(folder_path, output_folder="extracted_texts"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            print(f"📄 Extracting from {filename}...")
            text = extract_text_from_pdf(pdf_path)
            
            output_filename = os.path.splitext(filename)[0] + ".txt"
            output_path = os.path.join(output_folder, output_filename)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
            
            print(f"✅ Saved extracted text to {output_path}")

