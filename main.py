import streamlit as st
import requests

API_URL = "http://65.0.85.20:8000"
API_KEY = "your-api-key"  # optional if you add auth

st.set_page_config(page_title="Smart Resume Tool", layout="wide")
st.title("📄 Smart Resume Analyzer")

st.markdown("## 🧠 Upload and Analyze Resume")

uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])

def render_resume_data(data):
    st.markdown("## 👤 Basic Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Name**")
        st.write(data.get("name", "N/A"))
    with col2:
        st.markdown("**Email**")
        st.write(data.get("email", "N/A"))
    with col3:
        st.markdown("**Phone**")
        st.write(data.get("mobile_number", "N/A"))

    col4, col5 = st.columns(2)
    with col4:
        st.markdown("**Experience**")
        st.write(f"{round(data.get('total_experience', 0), 2)} years")
    with col5:
        st.markdown("**Degree**")
        degree_list = data.get("degree", [])
        for deg in degree_list:
            st.write(deg)

    st.divider()

    st.markdown("## 💼 Work Experience")
    exp = data.get("experience", [])
    for i in range(0, len(exp), 4):
        with st.expander(f"**{exp[i+1] if i+1 < len(exp) else 'Role'}** @ {exp[i] if i < len(exp) else 'Company'}"):
            cols = st.columns(2)
            cols[0].markdown(f"📅 **Duration:** {exp[i+2] if i+2 < len(exp) else ''}")
            cols[1].markdown(f"📍 **Location:** {exp[i+3] if i+3 < len(exp) else ''}")
            for j in range(i+4, min(i+10, len(exp))):
                st.markdown(f"- {exp[j]}")

    st.divider()

    st.markdown("## 🧠 Skills")
    skills = data.get("skills", [])
    if skills:
        skill_tags = " ".join([
            f"<span style='color:#fff; background-color:#444; padding:6px 12px; "
            f"border-radius:16px; margin:4px; display:inline-block;'>{skill}</span>"
            for skill in skills
        ])
        st.markdown(f"<div style='line-height:2; flex-wrap:wrap'>{skill_tags}</div>", unsafe_allow_html=True)

    st.divider()

    st.markdown("## 🔗 Other Information")
    col6, col7 = st.columns(2)
    col6.markdown(f"**College Name:** {data.get('college_name', 'N/A')}")
    col7.markdown(f"**LinkedIn:** {data.get('linkedin', 'N/A')}")


if uploaded_file:
    if st.button("Parse Resume"):
        with st.spinner("Parsing resume..."):
            res = requests.post(
                f"{API_URL}/resumes/parse-advanced",
                files={"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            )
            data = res.json()
            render_resume_data(data)
