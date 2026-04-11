import io
from pypdf import PdfReader

def extract_text_from_pdf_content(content: bytes) -> str:
    """
    Extracts text from the raw bytes of a PDF file.
    """
    reader = PdfReader(io.BytesIO(content))
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text() or ""
    return extracted_text
