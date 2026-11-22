from io import BytesIO

import pytest
from pypdf import PdfWriter

from resume_review.documents import extract_resume_text


def test_extracts_utf8_text():
    assert extract_resume_text("resume.txt", b"  Python developer  ") == "Python developer"


def test_rejects_unsupported_file_type():
    with pytest.raises(ValueError, match="PDF or TXT"):
        extract_resume_text("resume.docx", b"resume")


def test_rejects_empty_text():
    with pytest.raises(ValueError, match="No readable text"):
        extract_resume_text("resume.txt", b"  ")


def test_rejects_scanned_pdf_without_extractable_text():
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    pdf = BytesIO()
    writer.write(pdf)

    with pytest.raises(ValueError, match="Scanned PDFs need OCR"):
        extract_resume_text("resume.pdf", pdf.getvalue())