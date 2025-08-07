# extractor.py

import fitz  # PyMuPDF

def extract_text_from_pdf(file):
    """
    Extracts text from a PDF file object using PyMuPDF.

    Parameters:
    - file: A file-like object (e.g., uploaded file in Streamlit)

    Returns:
    - A string containing all the extracted text from the PDF
    """
    try:
        # Open the PDF from the file stream
        pdf_document = fitz.open(stream=file.read(), filetype="pdf")
        extracted_text = ""

        # Loop through each page and extract text
        for page in pdf_document:
            extracted_text += page.get_text()

        pdf_document.close()
        return extracted_text.strip()

    except Exception as e:
        print(f"Error while extracting PDF text: {e}")
        return ""
