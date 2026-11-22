from io import BytesIO

from pypdf import PdfReader


def extract_resume_text(filename: str, content: bytes) -> str:
    """Extract text from a PDF or UTF-8 text resume held in memory."""
    suffix = filename.rsplit(".", maxsplit=1)[-1].lower() if "." in filename else ""
    if suffix == "pdf":
        text = "\n".join(page.extract_text() or "" for page in PdfReader(BytesIO(content)).pages)
    elif suffix == "txt":
        text = content.decode("utf-8-sig")
    else:
        raise ValueError("Resume must be a PDF or TXT file.")

    text = text.strip()
    if not text:
        raise ValueError("No readable text was found. Scanned PDFs need OCR before use.")
    return text