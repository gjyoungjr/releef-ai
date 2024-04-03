import fitz


def extract_text(file_stream, file_type) -> str:
    """
    Extracts text from a PDF file
    """
    doc = fitz.open(stream=file_stream, filetype=file_type)

    text = ""
    for page in doc:
        text += page.get_text().encode("utf8").decode("utf8")

    return text.strip()

