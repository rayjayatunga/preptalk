import streamlit as st
import fitz  # PyMuPDF

# Enable PDF upload
uploaded_resume = st.file_uploader("Upload your resume", type=['pdf'])

if uploaded_resume is not None:
    # Read the uploaded file into a bytes object
    uploaded_bytes = uploaded_resume.read()
    
    # Initialize a PDF reader with the bytes object
    doc = fitz.open("resume", uploaded_bytes)
    text = ""
    for page in doc:
        text += page.get_text()
    st.text_area("Extracted Text", text, height=300)