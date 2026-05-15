import PyPDF2
from docx import Document


def extract_text(file):

    text = ""

    # PDF
    if file.name.endswith(".pdf"):

        pdf_reader = PyPDF2.PdfReader(file)

        for page in pdf_reader.pages:
            text += page.extract_text()

    # DOCX
    elif file.name.endswith(".docx"):

        doc = Document(file)

        for para in doc.paragraphs:
            text += para.text + "\n"

    # TXT
    elif file.name.endswith(".txt"):

        text = file.read().decode("utf-8")

    return text