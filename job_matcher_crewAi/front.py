import streamlit as st
import os
from resume_crew import ResumeCrew
import json
from db.load_database import mongo

db = mongo()

st.set_page_config(page_title="Resume Analyzer", layout="wide")
st.title("🧠 Resume-to-Job Matcher")

st.markdown("Upload your resume and provide job details to find the best matches.")

# Upload CV
uploaded_file = st.file_uploader("📄 Upload your CV (PDF)", type=["pdf"])

# Save the uploaded file
if uploaded_file:
    os.makedirs("saved_cv", exist_ok=True)
    file_path = os.path.join("saved_cv", "cv.pdf")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success("✅ Resume uploaded and saved successfully!")

# Job input
job_title = st.text_input("Job Title", value="Machine Learning Engineer")
limit = st.slider("Number of jobs to fetch", min_value=1, max_value=50, value=5)

# Run analysis
if st.button("Run Resume Analyzer"):
    if not uploaded_file:
        st.error("❌ Please upload your CV before running the analyzer.")
    else:
        analyzer = ResumeCrew()
        results = analyzer.run(job_title=job_title, limit=limit)

        jobs = db.get_high_scored_docs()

        for job in jobs:
            st.markdown(f"""
                ---
                ### [{job['title']}]({job['url']})
                **Company:** {job['company']}  
                **Location:** {job['location']}  
                **Rating:** {job.get('rating', 'N/A')}  
                **Reason:** {job.get('reason', 'N/A')}  
                **Reason Type:** {job.get('reason_type', 'N/A')}  
                **Recommendation:** {job.get('recommendation', 'N/A')}  

                **Breakdown:**  
                - Skills Match: {job.get('breakdown', {}).get('skills_match', 'N/A')}  
                - Experience Match: {job.get('breakdown', {}).get('experience_match', 'N/A')}  
                - Soft Skills Match: {job.get('breakdown', {}).get('soft_skills_match', 'N/A')}  
            """)
