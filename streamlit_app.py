# streamlit_app.py

from analyzer import analyze_resume, JOB_ROLE_MAP
from recommender import recommend_role_semantically
from extractor import extract_text_from_pdf
from pdf_generator import generate_pdf_report
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests




st.set_page_config(page_title="Resume Analyzer", layout="wide")
st.title("📄 Resume Analyzer")

st.markdown("### Select the Target Job Role")
role = st.selectbox("Choose a role to match your resume against:", list(JOB_ROLE_MAP.keys()))


uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    # Extract resume text
    resume_text = extract_text_from_pdf(uploaded_file)

    # Analyze the resume
    analysis_result = analyze_resume(resume_text, role)

    
    # After extracting resume_text from PDF/Docx
    recommended_roles = recommend_role_semantically(resume_text, top_n=3)
    st.subheader("📌 Top Recommended Job Roles:")
    for role, score in recommended_roles:
        st.markdown(f"- **{role}** (Score: {score:.2f})")


    # Display the results
    st.subheader("🔍 ATS Analysis Results")

    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("✅ ATS Score", f"{analysis_result['ats_score']}%")
        st.metric("💰 Estimated Salary", analysis_result['estimated_salary'])

    with col2:
        st.write("🎯 **Matched Skills**")
        st.success(", ".join(analysis_result["matched_skills"]) or "None")

        st.write("❌ **Missing Skills**")
        st.error(", ".join(analysis_result.get("missing_skills", [])) or "None")

    if analysis_result.get("suggested_skills"):
        st.info("💡 Suggestions:")
        for suggestion in analysis_result["suggested_skills"]:
            st.markdown(f"- {suggestion}")
        st.subheader("📈 Skill Matching Summary (Chart)")
        skill_data = {
            "Matched Skills": len(analysis_result["matched_skills"]),
            "Suggested Skills": len(analysis_result["suggested_skills"])
        }
        skill_df = pd.DataFrame(skill_data.items(), columns=["Skill Type", "Count"])
        fig_bar, ax_bar = plt.subplots(figsize=(4, 3))  # Width x Height in inches
        ax_bar.bar(skill_df["Skill Type"], skill_df["Count"], color=['#00c853', '#ff9800'])
        ax_bar.set_ylabel("Count")
        ax_bar.set_title("Skill Matching Summary")
        st.pyplot(fig_bar, use_container_width=False)


        # ATS Compatibility Pie Chart
        st.subheader("📊 ATS Score Distribution")
        ats_score = analysis_result["ats_score"]
        labels = ['Matched', 'Unmatched']
        sizes = [ats_score, 100 - ats_score]
        colors = ['#00c853', '#ff5252']
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)



    st.write("🧠 **Recommended Job Roles:**")
    for job in analysis_result["job_recommendations"]:
        st.markdown(f"- {job}")
    st.write("📝 **Resume Text Snippet:**")
    st.code(analysis_result["resume_text_snippet"], language="markdown")

    st.markdown("---")
    if st.checkbox("✅ I want to download the PDF report"):
        pdf_bytes = generate_pdf_report(analysis_result)
        st.download_button(
            label="📥 Download Report as PDF",
            data=pdf_bytes,
            file_name="resume_report.pdf",
            mime="application/pdf"
        )

else:  # ✅ This 'else' matches with 'if uploaded_file is not None:'
    st.info("Please upload a PDF resume to start analysis.")


st.title("Resume Analyzer")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"], key="resumer_uploader")

if uploaded_file is not None:
    with st.spinner("Analyzing..."):
        response = requests.post(
            "https://resume-analyzer-bt0n.onrender.com/upload",
            files={"file": uploaded_file.getvalue()},
        )

        if response.status_code == 200:
            result = response.json()
            st.success("Analysis Complete!")
            st.json(result["analysis"])
        else:
            st.error("Failed to analyze resume.")