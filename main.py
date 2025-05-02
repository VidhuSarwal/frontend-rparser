import streamlit as st
import requests

API_URL = "http://65.0.85.20:8000" #placeholder hai
API_KEY = "your-api-key"  # optional if you add auth

st.set_page_config(page_title="Smart Resume Tool", layout="wide")
st.title("📄 Smart Resume Analyzer")

st.header("🧠 Upload Resume")
uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])

def render_resume_data(data):
    st.subheader("👤 Basic Information")
    col1, col2 = st.columns(2)
    col1.markdown(f"**Name:** {data.get('name', 'N/A')}")
    col1.markdown(f"**Email:** {data.get('email', 'N/A')}")
    col2.markdown(f"**Phone:** {data.get('mobile_number', 'N/A')}")
    col2.markdown(f"**Total Experience:** {round(data.get('total_experience', 0), 2)} years")

    st.markdown("---")
    st.subheader("💼 Experience")
    exp = data.get("experience", [])
    for i in range(0, len(exp), 4):
        with st.expander(f"{exp[i+1] if i+1 < len(exp) else 'Role'} at {exp[i] if i < len(exp) else 'Company'}"):
            st.markdown(f"**Duration:** {exp[i+2] if i+2 < len(exp) else ''}")
            st.markdown(f"**Location:** {exp[i+3] if i+3 < len(exp) else ''}")
            for j in range(i+4, min(i+10, len(exp))):
                st.markdown(f"- {exp[j]}")

    st.markdown("---")
    st.subheader("🎓 Education")
    degrees = data.get("degree", [])
    for degree in degrees:
        st.markdown(f"- {degree}")

    st.markdown("---")
    st.subheader("🧠 Skills")
    skills = data.get("skills", [])
    if skills:
        st.markdown(
            ", ".join([f"`{skill}`" for skill in skills])
        )

if uploaded_file:
    if st.button("Parse Resume"):
        with st.spinner("Parsing resume..."):
            res = requests.post(
                f"{API_URL}/resumes/parse-advanced",
                files={"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            )
            data = res.json()
            render_resume_data(data)
