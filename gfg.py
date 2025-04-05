from dotenv import load_dotenv
import streamlit as st
import os
import fitz  # PyMuPDF for PDF reading
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text_parts = [page.get_text() for page in document]
        return " ".join(text_parts)
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit UI setup
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
st.subheader("Paste Your Job Description & Upload Your Resume")

input_text = st.text_area("Job Description: ")
uploaded_file = st.file_uploader("Upload your Resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")
    pdf_content = input_pdf_setup(uploaded_file)

    if st.button("Get ATS Score"):
        prompt = f"Compare the following resume to the job description and provide an exact ATS match percentage only (e.g., 87%).\n\nResume:\n{pdf_content}\n\nJob Description:\n{input_text}"
        response = get_gemini_response(prompt)
        try:
            score = float(response.strip().replace("%", ""))
            st.subheader("ATS Score")
            st.write(f"{score:.2f}%")
        except ValueError:
            st.write("Error: Unable to retrieve an exact percentage.\nResponse:")
            st.write(response)

    if st.button("Why is my score low?"):
        prompt = f"Explain in detail why the ATS match percentage might be low based on the following resume and job description.\n\nResume:\n{pdf_content}\n\nJob Description:\n{input_text}"
        response = get_gemini_response(prompt)
        st.subheader("Reasons for Low Score")
        st.write(response)

    if st.button("Matched Skills"):
        prompt = f"List the skills from the resume that match the job description.\n\nResume:\n{pdf_content}\n\nJob Description:\n{input_text}"
        response = get_gemini_response(prompt)
        st.subheader("Matched Skills")
        st.write(response)

    if st.button("Missing Skills"):
        prompt = f"List the skills that are mentioned in the job description but are missing from the resume.\n\nResume:\n{pdf_content}\n\nJob Description:\n{input_text}"
        response = get_gemini_response(prompt)
        st.subheader("Missing Skills")
        st.write(response)

    if st.button("HR Questions"):
        prompt = f"Generate a list of possible HR interview questions based on this resume and job description.\n\nResume:\n{pdf_content}\n\nJob Description:\n{input_text}"
        response = get_gemini_response(prompt)
        st.subheader("HR Interview Questions")
        st.write(response)

footer = """
---
#### Developed By [Manjunathareddy]
*Let's Connect - 6300138360*
"""
st.markdown(footer, unsafe_allow_html=True)
