from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import fitz
import google.generativeai as genai

# Configure API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input, pdf_content, prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text_parts = [page.get_text() for page in document]
        return " ".join(text_parts)
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App
st.set_page_config(page_title="ATS Resume Expert")

st.header("ATS Tracking System")
st.subheader("Paste Your Job Description & Upload Your Resume")
input_text = st.text_area("Job Description: ")
uploaded_file = st.file_uploader("Upload your Resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")
    pdf_content = input_pdf_setup(uploaded_file)
    
    # Button to get ATS Score
    if st.button("Get ATS Score"):
        response = get_gemini_response("Provide an exact ATS match percentage (only the percentage).", pdf_content, input_text)
        try:
            score = float(response.strip().replace("%", ""))
            st.subheader("ATS Score")
            st.write(f"{score:.2f}%")
        except ValueError:
            st.write("Error: Unable to retrieve an exact percentage.")
    
    # Button to check reasons for low score
    if st.button("Why is my score low?"):
        response = get_gemini_response("Explain why the ATS match percentage is low.", pdf_content, input_text)
        st.subheader("Reasons for Low Score")
        st.write(response)
    
    # Button to show matched skills
    if st.button("Matched Skills"):
        response = get_gemini_response("List the skills from the resume that match the job description.", pdf_content, input_text)
        st.subheader("Matched Skills")
        st.write(response)
    
    # Button to show missing skills
    if st.button("Missing Skills"):
        response = get_gemini_response("List the skills missing in the resume compared to the job description.", pdf_content, input_text)
        st.subheader("Missing Skills")
        st.write(response)
    
    # Button to generate HR questions
    if st.button("HR Questions"):
        response = get_gemini_response("Generate interview questions based on the resume and job description.", pdf_content, input_text)
        st.subheader("HR Interview Questions")
        st.write(response)
    if st.button("Cover Letter"):
        response=get_gemini_response("Generate cover letter based on the resume and job description.", pdf_content, input_text)
        st.subheader("Cover Letter")
        st.write(response)

footer = """
---
#### Developed By [Manjunathareddy]
*Let's Connect-6300138360*
"""
st.markdown(footer, unsafe_allow_html=True)
