from pathlib import Path
import PyPDF2
from docx import Document


def extract_pdf_text(file_path):
    text = ""

    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

    return text


def extract_docx_text(file_path):
    doc = Document(file_path)

    text = "\n".join([para.text for para in doc.paragraphs])

    return text


def extract_resume_text(file_path):
    path = Path(file_path)

    if path.suffix == ".pdf":
        return extract_pdf_text(file_path)

    elif path.suffix == ".docx":
        return extract_docx_text(file_path)

    elif path.suffix == ".txt":
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    else:
        return "Unsupported File Format"