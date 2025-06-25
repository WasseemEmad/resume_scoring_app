from crewai import Agent
from tools.resume_tools import ResumeTools,extracted_data
from langchain_openai import ChatOpenAI
from tools.search_tool import fetch_jobs
from tools.job_scoring_tool import get_score
from tools.message_tools import Messaging

resume_agent = Agent(
    role="Resume Classification Specialist",
    goal="Analyze resume data and classify it into skills and personal details",
    backstory=(
        "You are a skilled AI assistant trained to understand and organize resumes. "
        "Your job is to extract meaningful information and return it in a clean JSON structure. "
        "You work with NER models and language models to enhance data quality and fill in missing details."
    ),
    tools=[extracted_data,ResumeTools.read_resume],
    llm=ChatOpenAI(model="gpt-4o-mini"), 
    verbose=True
)


job_scorer_agent = Agent(
    role="Resume Scoring Specialist",
    goal="Analyze resume data and job description then give a score to the resume in respect to the job",
    backstory=(
        "You are a skilled Hr manager with experience in choosing the right resume to the job. "
        "Your job is to score the resume according to the job description and return the job information with the score. "
    ),
    tools=[fetch_jobs,get_score],
    llm=ChatOpenAI(model="gpt-4o-mini"), 
    verbose=True
)

messaging_agent = Agent(
    role="Messaging Specialist",
    goal="Find if there is suitable jobs with score hire than a certain level then send a message about this job",
    backstory=(
        "You are a skilled Hr manager with experience in choosing the right resume to the job. "
        "Your job is to send message for the job with a high score"
    ),
    tools=[Messaging.send_message],
    llm=ChatOpenAI(model="gpt-4o-mini"), 
    verbose=True
)
