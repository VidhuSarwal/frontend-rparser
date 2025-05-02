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
        with st.spinner("Analyzing resume..."):
            res = requests.post(f"{API_URL}/resumes/parse-advanced", 
                            files={"file": (uploaded_file.name, uploaded_file, "application/pdf")})
            
            if res.status_code == 200:
                data = res.json()
                
                # Create two columns for layout
                col1, col2 = st.columns([2, 1])
                
                # Column 1 - Personal info and Experience
                with col1:
                    # Personal Information Section
                    st.subheader("📋 Personal Information")
                    if data.get("name"):
                        st.write(f"**Name:** {data['name']}")
                    if data.get("email"):
                        st.write(f"**Email:** {data['email']}")
                    if data.get("mobile_number"):
                        st.write(f"**Phone:** {data['mobile_number']}")
                    if data.get("linkedin"):
                        st.write(f"**LinkedIn:** {data['linkedin']}")
                    
                    # Education Section
                    if data.get("degree"):
                        st.subheader("🎓 Education")
                        for degree in data["degree"]:
                            st.write(f"• {degree}")
                    
                    # Experience Section
                    if data.get("experience") and len(data["experience"]) > 0:
                        st.subheader("💼 Professional Experience")
                        
                        # Process experience data
                        i = 0
                        while i < len(data["experience"]):
                            company = data["experience"][i]
                            i += 1
                            if i < len(data["experience"]):
                                role = data["experience"][i]
                                i += 1
                            else:
                                role = ""
                                
                            if i < len(data["experience"]):
                                duration = data["experience"][i]
                                i += 1
                            else:
                                duration = ""
                                
                            if i < len(data["experience"]):
                                location = data["experience"][i]
                                i += 1
                            else:
                                location = ""
                                
                            # Display the job info
                            st.markdown(f"**{role} at {company}**")
                            st.markdown(f"_{duration} | {location}_")
                            
                            # Display responsibilities
                            responsibilities = []
                            while i < len(data["experience"]) and data["experience"][i].startswith("•"):
                                responsibilities.append(data["experience"][i])
                                i += 1
                                
                            if responsibilities:
                                for resp in responsibilities:
                                    st.write(resp)
                                    
                            st.write("---")
                
                # Column 2 - Skills and Other Info
                with col2:
                    # Skills Section
                    if data.get("skills"):
                        st.subheader("🔧 Skills")
                        # Display skills in a more readable format with chips/badges
                        skills_html = ""
                        for skill in data["skills"]:
                            skills_html += f"""
                                <span style="background-color: #f0f2f6; 
                                            padding: 4px 12px; 
                                            border-radius: 16px; 
                                            margin: 4px; 
                                            display: inline-block;
                                            font-size: 0.9em;">
                                    {skill}
                                </span>
                            """
                        st.markdown(skills_html, unsafe_allow_html=True)
                    
                    # Summary Info
                    st.subheader("📊 Summary")
                    if data.get("total_experience") is not None:
                        years = int(data["total_experience"])
                        months = int((data["total_experience"] - years) * 12)
                        if years > 0:
                            experience_text = f"{years} year{'s' if years != 1 else ''}"
                            if months > 0:
                                experience_text += f", {months} month{'s' if months != 1 else ''}"
                        else:
                            experience_text = f"{months} month{'s' if months != 1 else ''}"
                        st.write(f"**Total Experience:** {experience_text}")
                    
                    if data.get("no_of_pages"):
                        st.write(f"**Resume Length:** {data['no_of_pages']} page{'s' if data['no_of_pages'] != 1 else ''}")
            else:
                st.error("Failed to analyze resume. Please try again.")