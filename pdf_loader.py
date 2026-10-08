from pypdf import PdfReader

def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    pdf_title = reader.metadata.title if reader.metadata.title else "未命名PDF"
    for page in reader.pages:
        text += page.extract_text()
    return {pdf_title: text}