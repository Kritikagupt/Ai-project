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
