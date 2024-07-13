import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
import fitz
from io import BytesIO

# Function to combine PDFs
def combine_pdfs(pdf_list):
    pdf_writer = PdfWriter()

    for pdf in pdf_list:
        pdf_reader = PdfReader(pdf)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)

    combined_pdf = BytesIO()
    pdf_writer.write(combined_pdf)
    combined_pdf.seek(0)  # Move the cursor to the beginning of the BytesIO object
    return combined_pdf

# Function to extract text from all pages of a PDF
def extract_text_from_all_pages(pdf_stream):
    pdf_document = fitz.open(stream=pdf_stream, filetype="pdf")
    total_pages = pdf_document.page_count
    extracted_text = ""

    for page_number in range(total_pages):
        page = pdf_document.load_page(page_number)
        text = page.get_text()
        extracted_text += f'--- Page {page_number + 1} ---\n{text}\n\n'

    return extracted_text

# Streamlit app
st.title("Combine PDF Files and Extract Text")

# File uploader for multiple PDFs
uploaded_files = st.file_uploader("Upload multiple PDF files", type=["pdf"], accept_multiple_files=True)

# Button to trigger PDF combining and text extraction
if st.button("Combine PDFs and Extract Text") and uploaded_files:
    pdf_list = [BytesIO(file.read()) for file in uploaded_files]
    combined_pdf = combine_pdfs(pdf_list)
    
    # Extract text from the combined PDF
    extracted_text = extract_text_from_all_pages(combined_pdf)

    # Provide download link for the combined PDF
    st.markdown("### Download Combined PDF")
    st.write("Click below to download the combined PDF file")
    st.download_button(
        label="Download Combined PDF",
        data=combined_pdf.getvalue(),
        file_name="combined_output.pdf",
        mime="application/pdf"
    )

    # Provide download link for the extracted text
    st.markdown("### Download Extracted Text")
    st.write("Click below to download the extracted text file")
    st.download_button(
        label="Download Extracted Text",
        data=extracted_text,
        file_name="extracted_text.txt",
        mime="text/plain"
    )
