import streamlit as st
import PyPDF2
import io
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()


st.set_page_config(page_title="AI-Resume Critiquer",page_icon="📃", layout="centered")
st.title("📃 AT-Resume Critiquer")
st.markdown("Upload your resume in PDF or TXT file and get instant AI-Powered feedback to enhance your job application!")
genai_api_key = os.getenv("GEMINI_API_KEY")
uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role you are applying for(optional):")    
analyze = st.button("Analyze Resume")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

if analyze and uploaded_file :

    if genai_api_key is None:
        st.error("API key not found. Please set the GEMINI_API_KEY environment variable.")
        st.stop()

    try:
        file_content = extract_text_from_file(uploaded_file)
          
        if not file_content.strip():
            st.error("The uploaded file is empty. Please upload a valid resume.")
            st.stop()

        prompt=f"""Please analyze this resume and provide constructive feedback.

        Focus on the following aspects:
        1. Content clarity and impact
        2.Skills presentation
        3.Experience description
        4.Specific improvements for{job_role if job_role else 'general applications'}
        
        Resume Content:
        {file_content}
        Please provide your analysis in a clear structure format with specific recommendations for improvement."""

        client = genai.Client(api_key=genai_api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "temperature": 0.7,
                "max_output_tokens": 1500,
            }
        ) 
        
        st.markdown("###  Analysis Result :")
        st.markdown(response.outputs[0].content[0].text)

    except Exception as e:
        st.error(f"An error occurred: {e}")
 