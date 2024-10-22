import pdfplumber
import streamlit as st

class PDFExtractor:
    def __init__(self):
        self.text = ""

    def extract_text(self, pdf_files):
        self.text = ""
        for pdf_file in pdf_files:
            try:
                with pdfplumber.open(pdf_file) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            self.text += page_text
                        else:
                            st.warning(f"Page {pdf.pages.index(page)} is blank.")
            except Exception as e:
                st.error(f"Error processing {pdf_file.name}: {e}")
        return self.text

