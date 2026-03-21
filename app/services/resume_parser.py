import io
import os

import fitz  # PyMuPDF
import pdfplumber
import docx
from app.utils.logger import get_logger

logger = get_logger("resume_parser")


def extract_text_from_file(file_path: str) -> str:
    ext = file_path.rsplit(".", 1)[-1].lower()
    if ext == "pdf":
        return _extract_pdf(file_path)
    if ext == "docx":
        return _extract_docx(file_path)
    if ext == "txt":
        return _extract_txt(file_path)
    raise ValueError(f"Unsupported file type: .{ext}")


def _extract_pdf(path: str) -> str:
    try:
        doc = fitz.open(path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        logger.info("PDF parsed successfully", path=path)
        return text.strip()
    except Exception as exc:
        logger.warning("PyMuPDF failed, trying pdfplumber", exc=str(exc))
        return _extract_pdf_fallback(path)


def _extract_docx(path: str) -> str:
    doc = docx.Document(path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    logger.info("DOCX parsed", paragraphs_count=len(paragraphs))
    return "\n\n".join(paragraphs)


def _extract_pdf_fallback(path: str) -> str:
    with pdfplumber.open(path) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    logger.info("PDF fallback parsed")
    return text.strip()


def _extract_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read().strip()

