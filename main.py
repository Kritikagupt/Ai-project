import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


st.set_page_config(page_title="AT-Resume Critiquer",page_icon="📃", layout="centered")
st.title("📃 AT-Resume Critiquer")
st.markdown("Upload your resume in PDF or TXT file and get instant AI-Powered feedback to enhance your job application!")
openai_api_key = os.getenv("OPEN_API_KEY")
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

        client = OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides resume feedback."},
                {"role": "user", "content": prompt}
            ],

            temperature=0.7,
            max_tokens=1500,
        )
        
        st.markdown("###  Analysis Result :")
        st.markdown(response.choices[0].message.content)

    except Exception as e:
        st.error(f"An error occurred: {e}")
 