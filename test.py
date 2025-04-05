from dotenv import load_dotenv
import streamlit as st
import os
import fitz  # PyMuPDF
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Cache PDF extraction to avoid re-reading
@st.cache_data(show_spinner=False)
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text_parts = [page.get_text() for page in document]
        return " ".join(text_parts)
    else:
        raise FileNotFoundError("No file uploaded")

# Gemini response function with error handling
def get_gemini_response(instruction, pdf_content, job_description):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([instruction, pdf_content, job_description])
        return response.text.strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="ATS Resume Expert")
st.header("📄 ATS Resume Scanner")
st.subheader("🔍 Paste your job description and upload your resume to get insights")

input_text = st.text_area("📌 Job Description")
uploaded_file = st.file_uploader("📁 Upload your Resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.success("✅ PDF Uploaded Successfully")
    pdf_content = input_pdf_setup(uploaded_file)

    with st.expander("📖 Preview Resume Text"):
        st.write(pdf_content[:3000])  # Limit preview to first 3000 characters

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📊 Get ATS Score"):
            with st.spinner("Calculating ATS Score..."):
                response = get_gemini_response(
                    "Provide an exact ATS match percentage (only the percentage).",
                    pdf_content, input_text
                )
                try:
                    score = float(response.replace("%", "").strip())
                    st.subheader("✅ ATS Score")
                    st.write(f"{score:.2f}%")
                except ValueError:
                    st.error("❌ Error: Unable to retrieve an exact percentage.")
                    st.text(response)

        if st.button("🔍 Why is my score low?"):
            with st.spinner("Analyzing reasons..."):
                response = get_gemini_response(
                    "Explain why the ATS match percentage is low.",
                    pdf_content, input_text
                )
                st.subheader("📉 Reasons for Low Score")
                st.write(response)

        if st.button("✅ Matched Skills"):
            with st.spinner("Extracting matched skills..."):
                response = get_gemini_response(
                    "List the skills from the resume that match the job description.",
                    pdf_content, input_text
                )
                st.subheader("🧩 Matched Skills")
                st.write(response)

    with col2:
        if st.button("❌ Missing Skills"):
            with st.spinner("Finding missing skills..."):
                response = get_gemini_response(
                    "List the skills missing in the resume compared to the job description.",
                    pdf_content, input_text
                )
                st.subheader("🚫 Missing Skills")
                st.write(response)

        if st.button("💬 HR Questions"):
            with st.spinner("Generating HR interview questions..."):
                response = get_gemini_response(
                    "Generate interview questions based on the resume and job description.",
                    pdf_content, input_text
                )
                st.subheader("🗣 HR Interview Questions")
                st.write(response)

        if st.button("✉️ Cover Letter"):
            with st.spinner("Creating cover letter..."):
                response = get_gemini_response(
                    "Generate a professional cover letter based on the resume and job description.",
                    pdf_content, input_text
                )
                st.subheader("📄 Cover Letter")
                st.write(response)

                # Allow user to download it
                st.download_button(
                    label="📥 Download Cover Letter",
                    data=response,
                    file_name="Cover_Letter.txt",
                    mime="text/plain"
                )

# Footer
footer = """
---
#### 👨‍💻 Developed By [Manjunathareddy]
📞 Let's Connect - 6300138360
"""
st.markdown(footer, unsafe_allow_html=True)
