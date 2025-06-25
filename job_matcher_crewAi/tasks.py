# To know more about the Task class, visit: https://docs.crewai.com/concepts/tasks
from crewai import Task
from textwrap import dedent
import json


from crewai import Task
from textwrap import dedent


      
def classify_resume_task(agent):
    return Task(
        description=dedent('''
        **Task**: Extract structured skills and details from a resume
        **Description**: 
        You are required to extract structured skill information from a candidate's resume. 
        To do this, you **must use the extract_skills_tool** which utilizes a custom NER model and OpenAI to parse the resume.

        **Instructions**:
        - Do **not** extract skills yourself.
        - Do **not** return a final answer directly.
        - You **must** call the extract_skills_tool and pass it the full resume text as input.
        - The tool will return structured data in JSON format, and also save it to a file automatically.

        **Goal**: Use the extract_skills_tool to extract and save structured resume data.
        '''),
        expected_output="A JSON object with two keys: 'Skills' and 'Details'",
        agent=agent,
    )
    
def job_scoring(agent, limit: int, job_title: str):
    return Task(
        description = dedent(
            f"""
            **Task**: Score a Resume Against Job Listings

            **Description**: Evaluate the given resume data by scoring it against {limit} relevant job listings based on the job title "{job_title}". 
            This task involves retrieving remote job postings and assigning scores to each based on how well the resume matches the job description. 
            Each score should include a breakdown of skills, experience, and soft skills alignment, along with a brief explanation and 
            actionable improvement suggestions.

            **Parameters**: 
            - Job Title: {job_title}
            - Job Limit: {limit}

            **Instructions**:
            1. Use the `job searching tool` to fetch remote jobs that match the provided job title.
            2. Log how many jobs were successfully retrieved and stored.
            3. Use the `Scoring the resume tool` to score the resume against each job
            for the scoring resume tool make sure that you give 1 inputs the limit.
            4. Return a list of job documents with:
                - Score (0–10)
                - Match breakdown (skills, experience, soft skills)
                - Explanation and suggestions for improvement
            """
        ),
        agent=agent,
    )
    
    
def send_suitable_jobs_via_message(agent):
    return Task(description=dedent('''
    **Task**: Automatically Send Messages for Suitable Job Matches

    **Objective**: You must call the **Messaging tool** without any input to send job recommendations that were highly matched to the candidate. This is **mandatory**.

    **Key Requirements**:
    - ✅ You **must always call** the Messaging tool. No condition or decision-making is needed.
    - ✅ Do **not** pass any input to the tool — call it with **no arguments**.
    - 🚫 Do **not** attempt to describe, summarize, or send the job yourself.
    - 🔁 The Messaging tool will automatically fetch, format, send, and update the job status to prevent duplicates.
    - 🧠 Do not try to replicate the logic inside the tool — trust it entirely.

    **Goal**: Ensure the candidate is notified once about each highly relevant job by invoking the Messaging tool directly.

    **Instruction Recap**:
    - Use the Messaging tool directly.
    - Do not include any manual text.
    - No logic or conditions — always call the tool.

    '''),
    agent=agent)