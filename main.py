import streamlit as st
import requests

API_URL = "http://65.0.85.20:8000"
API_KEY = "your-api-key"  # optional if you add auth

st.set_page_config(page_title="Smart Resume Tool", layout="wide")

st.title("📄 Resume Analyzer & Expert Matcher")

tab1, tab2, tab3 = st.tabs(["🔍 Basic Parser", "🧠 Advanced Parser", "🤝 Expert Matching"])

with tab1:
    st.header("🔍 Parse Basic Resume")
    uploaded_file = st.file_uploader("Upload a PDF resume", type=["pdf"], key="basic")
    if uploaded_file:
        if st.button("Parse Basic"):
            files = {"file": uploaded_file.getvalue()}
            res = requests.post(f"{API_URL}/resumes/parse-basic", files={"file": (uploaded_file.name, uploaded_file, "application/pdf")})
            st.json(res.json())

with tab2:
    st.header("🧠 Parse Advanced Resume")
    adv_file = st.file_uploader("Upload PDF resume for advanced parsing", type=["pdf"], key="advanced")
    if adv_file:
        if st.button("Parse Advanced"):
            res = requests.post(f"{API_URL}/resumes/parse-advanced", files={"file": (adv_file.name, adv_file, "application/pdf")})
            st.json(res.json())

with tab3:
    st.header("🤝 Match Candidate with Expert")
    data_input = st.text_area("Paste profile and expert data as JSON", height=300)
    if st.button("Get Matching Score"):
        try:
            data = eval(data_input)  # safer: use json.loads with try-except
            res = requests.post(f"{API_URL}/matching/expert-score", json=data)
            st.success("🎯 Matching Score:")
            st.json(res.json())
        except Exception as e:
            st.error(f"Invalid input! Error: {str(e)}")

    if st.button("Get Verbose Matching"):
        try:
            data = eval(data_input)
            res = requests.post(f"{API_URL}/matching/expert-verbose", json=data)
            st.success("📋 Full Matching Report:")
            st.json(res.json())
        except Exception as e:
            st.error(f"Invalid input! Error: {str(e)}")
st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
        }
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)
