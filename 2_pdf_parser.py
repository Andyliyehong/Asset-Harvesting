import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page_num, page in enumerate(doc):
        full_text += f"\n--- Page {page_num + 1} ---\n"
        full_text += page.get_text()
    return full_text

if __name__ == "__main__":
    content = extract_text_from_pdf('AI&D Project Spotlight April 2026 - Slide Deck.pdf')
    with open('2_source_content.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Source content extracted to 2_source_content.txt")