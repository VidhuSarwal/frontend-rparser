import streamlit as st
import requests

API_URL = "http://65.0.85.20:8000"
API_KEY = "your-api-key"  # optional if you add auth

st.set_page_config(page_title="Smart Resume Tool", layout="wide")

st.title("📄 Resume Analyzer")

st.header("🧠 Parse Resume")
uploaded_file = st.file_uploader("Upload PDF resume", type=["pdf"])
if uploaded_file:
    if st.button("Parse Resume"):
        res = requests.post(f"{API_URL}/resumes/parse-advanced", 
                           files={"file": (uploaded_file.name, uploaded_file, "application/pdf")})
        st.json(res.json())
