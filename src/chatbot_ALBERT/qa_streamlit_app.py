import streamlit as st
from pdf_extractor import PDFExtractor
from albert_qa import AlbertQA

class QAStreamlitApp:
    def __init__(self):
        self.pdf_extractor = PDFExtractor()
        self.qa_model = AlbertQA()
        self.document_text = ""

    def extract_text_from_files(self, uploaded_files):
        """Extracts text from uploaded PDFs."""
        return self.pdf_extractor.extract_text(uploaded_files)

    def run(self):
        st.title("ALBERT-Powered PDF Question-Answering Bot")

        # Display instructions
        st.write("Upload PDFs and ask questions based on their content.")

        # File uploader for PDFs
        uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

        # Extract text from uploaded PDFs
        if uploaded_files:
            self.document_text = self.extract_text_from_files(uploaded_files)
            st.success("Text extracted from PDFs successfully!")

            # Display the extracted text
            with st.expander("Show extracted text"):
                st.write(self.document_text[:1000])  # Show a preview of the text, limited to 1000 characters

        # Text area to input the question
        question = st.text_area("Enter your question:")

        # Button to submit the question
        if st.button("Get Answer"):
            if question and self.document_text:
                with st.spinner("Processing..."):
                    answer = self.qa_model.answer_question(question, self.document_text)
                    st.write(f"**Answer:** {answer}")
            elif not question:
                st.warning("Please enter a question.")
            elif not self.document_text:
                st.warning("Please upload PDFs first.")
