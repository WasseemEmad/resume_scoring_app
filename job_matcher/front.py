import streamlit as st
import requests

st.set_page_config(page_title="Remote Job Finder", layout="centered")

st.markdown("## 💼 Remote Job Finder")

st.markdown("""
    <style>
    /* Uniform button width inside sidebar */
    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        height: 3em;
        font-weight: bold;
        margin-bottom: 0.5em;
        background-color: #9CAF88;
        color: black;
        transition: 0.3s;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: transparent;
        color: #4CAF50;
        border: 2px solid #4CAF50;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

query = st.text_input("Enter job keyword", "machine learning")
job_desc = st.text_input("Enter job describtion")
limit = st.slider("Number of jobs to retrieve", 1, 50, 10)

# Create space to display results
job_display_placeholder = st.container()



# BASE_URL for FastAPI backend
BASE_URL = "http://localhost:8000"  # Change if deployed elsewhere

# ----------------- Existing Buttons -----------------
with st.sidebar:
    st.markdown("## 🔧 Actions")

    if st.button("Search from Database"):
        with st.spinner("Searching database..."):
            try:
                res = requests.get(f"{BASE_URL}/jobs/search", params={"limit": limit})
                jobs = res.json()
                if isinstance(jobs, list) and jobs:
                    with job_display_placeholder:
                        st.success(f"Found {len(jobs)} job(s) from the database.")
                        for job in jobs:
                            st.markdown(f"""
                            ---
                            ### [{job['title']}]({job['url']})
                            **Company:** {job['company']}  
                            **Location:** {job['location']}  
                            """)
                else:
                    with job_display_placeholder:
                        st.warning(jobs.get("message", "No jobs found."))
            except Exception as e:
                st.error(f"Error: {e}")

    if st.button("Fetch New Jobs from Web"):
        with st.spinner("Fetching..."):
            try:
                res = requests.post(f"{BASE_URL}/jobs/fetch", json={"keyword": query}, params={"limit": limit})
                jobs = res.json()
                if isinstance(jobs, list) and jobs:
                    with job_display_placeholder:
                        st.success(f"Fetched and saved {len(jobs)} new job(s).")
                        for job in jobs:
                            st.markdown(f"""
                            ---
                            ### [{job['title']}]({job['url']})
                            **Company:** {job['company']}  
                            **Location:** {job['location']}  
                            """)
                else:
                    with job_display_placeholder:
                        st.warning(jobs.get("message", "No new jobs found."))
            except Exception as e:
                st.error(f"Error: {e}")

    if st.button("Get Scores"):
        with st.spinner("Scoring CV..."):
            try:
                res = requests.post(f"{BASE_URL}/get_score/", params={"limit": limit})
                if res.status_code == 200:
                    result = res.json()
                    scored_jobs = result.get("rated docs", [])
                    if not scored_jobs:
                        with job_display_placeholder:
                            st.info("No jobs were scored.")
                    else:
                        with job_display_placeholder:
                            st.success(f"{len(scored_jobs)} jobs scored.")
                            for job in scored_jobs:
                                st.markdown(f"""
                                ---
                                ### [{job.get('title', 'No Title')}]({job.get('url', '#')})
                                **Company:** {job.get('company', 'N/A')}  
                                **Location:** {job.get('location', 'N/A')}  
                                **Rating:** {job.get('rating', 'N/A')}  
                                **Reason:** {job.get('reason', 'N/A')}  
                                **Reason Type:** {job.get('reason_type', 'N/A')}  
                                **Recommendation:** {job.get('recommendation', 'N/A')}  

                                **Breakdown:**  
                                - Skills Match: {job.get('breakdown', {}).get('skills_match', 'N/A')}  
                                - Experience Match: {job.get('breakdown', {}).get('experience_match', 'N/A')}  
                                - Soft Skills Match: {job.get('breakdown', {}).get('soft_skills_match', 'N/A')}  
                                """)
                else:
                    with job_display_placeholder:
                        st.error("Scoring failed.")
            except Exception as e:
                with job_display_placeholder:
                    st.error(f"Error: {e}")
                    
    if st.button("Compare job"):
        with st.spinner("getting the score..."):
            try:
                res = requests.post(f"{BASE_URL}/compare_job", params={"job": job_desc})
                if res.status_code == 200:
                    result = res.json()
                    scored_job = result.get("rating", [])
                    if not scored_job:
                        with job_display_placeholder:
                            st.info("No jobs were scored.")
                    else:
                        with job_display_placeholder:
                            st.success(f"1 job scored.")
                            st.markdown(f"""
                                ---
                                ###
                                **Rating:** {scored_job.get('rating', 'N/A')}  
                                **Reason:** {scored_job.get('reason', 'N/A')}  
                                **Reason Type:** {scored_job.get('reason_type', 'N/A')}  
                                **Recommendation:** {scored_job.get('recommendation', 'N/A')}  

                                **Breakdown:**  
                                - Skills Match: {scored_job.get('breakdown', {}).get('skills_match', 'N/A')}  
                                - Experience Match: {scored_job.get('breakdown', {}).get('experience_match', 'N/A')}  
                                - Soft Skills Match: {scored_job.get('breakdown', {}).get('soft_skills_match', 'N/A')}  
                                """)
                else:
                    with job_display_placeholder:
                        st.error("Scoring failed.")
            except Exception as e:
                with job_display_placeholder:
                    st.error(f"Error: {e}")

    if st.button("High Scores"):
        with st.spinner("Fetching high scored jobs..."):
            try:
                res = requests.post(f"{BASE_URL}/get_high_scored_jobs/")
                if res.status_code == 200:
                    jobs = res.json().get("high_rated_docs", [])
                    if not jobs:
                        with job_display_placeholder:
                            st.info("No high scored jobs found.")
                    else:
                        with job_display_placeholder:
                            st.success(f"Found {len(jobs)} high scored job(s).")
                            for job in jobs:
                                st.markdown(f"""
                                ---
                                ### [{job['title']}]({job['url']})
                                **Company:** {job['company']}  
                                **Location:** {job['location']}  
                                **Rating:** {job.get('rating', 'N/A')}  
                                """)
                else:
                    with job_display_placeholder:
                        st.error("Failed to fetch high scored jobs.")
            except Exception as e:
                with job_display_placeholder:
                    st.error(f"Error: {e}")

    if st.button("Clear DB"):
        with st.spinner("Clearing database..."):
            try:
                res = requests.delete(f"{BASE_URL}/clear_collection/")
                if res.status_code == 200:
                    with job_display_placeholder:
                        st.success("Database cleared.")
                else:
                    with job_display_placeholder:
                        st.error("Failed to clear the database.")
            except Exception as e:
                with job_display_placeholder:
                    st.error(f"Error: {e}")
    
    if st.button("Send message"):
        with st.spinner("sending the message..."):
            try:
                res = requests.post(f"{BASE_URL}/send_message")
                if res.status_code == 200:
                    r = res.json().get("result")
                    if r == 'message is sent':
                        with job_display_placeholder:
                            st.success("message is sent.")
                    else:
                        with job_display_placeholder:
                            st.info("no new jobs")
                else:
                    with job_display_placeholder:
                        st.error("Failed to clear the database.")
            except Exception as e:
                with job_display_placeholder:
                    st.error(f"Error: {e}")
    
                    
                    

uploaded_file = st.file_uploader("Upload CV", type=["pdf"])
if uploaded_file is not None:
    if st.button("Upload CV"):
        with st.spinner("Uploading..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                res = requests.post(f"{BASE_URL}/upload-pdf/", files=files)
                if res.status_code == 200:
                    with job_display_placeholder:
                        st.success("CV uploaded successfully.")
                else:
                    with job_display_placeholder:
                        st.error("Failed to upload CV.")
            except Exception as e:
                with job_display_placeholder:
                    st.error(f"Error: {e}")