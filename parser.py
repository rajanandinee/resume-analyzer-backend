import fitz  # PyMuPDF

def extract_text_from_pdf(file) -> str:
    try:
        text = ""
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()
    except Exception as e:
        return f"Error extracting text: {str(e)}"
