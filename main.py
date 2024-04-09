import streamlit as st
import fitz  # PyMuPDF
from io import StringIO
import cohere

if "text_extracted" not in st.session_state:
    st.session_state.text_extracted = False
if "pdf_body" not in st.session_state:
    st.session_state.pdf_body = ''

#######################################
# FUNCTION DEFINITIONS
#######################################    
def extract_job_duties(pdf_body):
    co = cohere.Client(st.secrets["COHERE_API_KEY"])
    message = f"You are analysing a resume and extracting information about a candidate's job experience and duties from their resume pdf content below. Respond only in the form of a python list with each element containing a unique job duty. DO NOT SIMPLY LIST THE CANDIDATE'S SKILLS BUT MAKE SURE TO FIND UNIQUE RESPONSIBILITIES AND ACOMPLISHMENTS. PDF CONTENT: {pdf_body}"
    response = co.chat(
        message= message.format(pdf_body),
        model= 'command-r'
    )
    return response.text


#######################################
# MAIN STREAMLIT APP
#######################################    

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
    st.session_state.pdf_body = text
    st.session_state["text_extracted"] = True

if st.session_state["text_extracted"]:
    if st.button("Extract job duties"):
        job_duties = extract_job_duties(st.session_state.pdf_body)
        st.write(job_duties)