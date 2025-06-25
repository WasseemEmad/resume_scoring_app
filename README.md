# 📄 Resume-to-Job Matching System

This system matches a candidate’s resume with live job listings by extracting skills, classifying them, scoring match quality using a language model, and sending notifications for high matches.

---
## **version 1 fast-api**
## 🚀 Features

- ✅ **Upload Resume (PDF)**
- 🧠 **Extract & Classify Resume Data** using custom-trained spaCy NER + OpenAI
- 🔍 **Scrape or Search Live Job Listings** and store them in MongoDB
- 📊 **Score Resumes vs Jobs** using GPT-based reasoning
- 🔔 **Send Notifications** for high-matching jobs via Pushover
- 🌐 **FastAPI-powered API** with auto-generated Swagger Docs

---

## 🔄 API Endpoints:
| Method   | Endpoint                 | Description                     |
| -------- | ------------------------ | ------------------------------- |
| `GET`    | `/jobs/search?limit=10`  | View jobs from DB               |
| `POST`   | `/jobs/fetch`            | Scrape/search jobs with keyword |
| `POST`   | `/upload-pdf/`           | Upload resume (PDF)             |
| `POST`   | `/get_score/`            | Score resume vs scraped jobs    |
| `POST`   | `/compare_job`           | Compare resume with custom job  |
| `POST`   | `/get_high_scored_jobs/` | View highly-matching jobs       |
| `DELETE` | `/clear_collection/`     | Clear job DB                    |
| `POST`   | `/send_message`          | Notify user of top jobs         |

## 🧪 Example Workflow
 - Upload your resume as a PDF
 - Fetch jobs related to your skills
 - Score the jobs
 - View or receive notifications for top matches

## **version 2 using crew ai**
## 🤖 CrewAI-Powered Version

This version leverages [CrewAI](https://crewai.com) to orchestrate specialized AI agents for each task in the resume-to-job matching workflow.

### 🔧 Key CrewAI Agents

- **resume_agent**: Parses resumes and classifies content into skills and experience
- **job_scorer_agent**: Scores the resume against live jobs using GPT-based logic
- **messaging_agent**: Sends notifications for high-quality matches

### 🛠️ Tools Used by Agents
- `SearchTool`: Search for jobs and return them
- `extracted_data`, extracts structured data using spaCy + GPT
- `ResumeTools`: Reads PDFs
- `ScoringTools`: Matches resume with job descriptions and rates compatibility
- `Messaging`: Sends alerts via Pushover

### 🌀 Crew Workflow
- User Uploads Resume:
  The process begins when a user uploads their resume to the system.

- ResumeAgent Takes Over:
  The ResumeAgent receives the resume and is responsible for processing it.

- Skills & Information Extracted:
  The agent uses NLP tools (spaCy + OpenAI) to extract skills, experiences, and relevant personal info from the resume.

- JobScorerAgent Engages:
  This extracted data is passed to the JobScorerAgent, whose role is to find matching jobs and score their relevance.

- SearchTool Activated:
  The JobScorerAgent invokes the SearchTool to search or scrape live job listings relevant to the candidate's profile.

- Jobs Are Scored:
  The system evaluates how well each job matches the resume using GPT-based reasoning and scoring.

- MessagingAgent Takes Over:
  Once scoring is complete, the MessagingAgent filters the top matches.

- Top Jobs Notified to User:
  The user receives a push notification (via Pushover) listing the best-matching jobs for them.

## 📦 Tech Stack
 - FastAPI – API Framework
 - CrewAI – Multi-agent task orchestration (New Version)
 - Streamlit - Frontend
 - MongoDB – Job storage
 - spaCy – Custom NER for skill extraction
 - OpenAI GPT (e.g. gpt-4o-mini) – Reasoning + rating + classification
 - Pushover – Notification system


## ⚖️ FastAPI Version vs CrewAI Version

| 🔧 Feature              | ⚡ FastAPI Version                           | 🤖 CrewAI Version                             |
|------------------------|---------------------------------------------|-----------------------------------------------|
| 🧠 Intelligence         | Centralized in API endpoints                | Decentralized via autonomous AI agents        |
| 🧰 Tool Integration     | Manually handled inside routes/functions    | Modular tools defined and used by agents      |
| 📡 Orchestration        | Sequential, procedural API calls            | Dynamic multi-agent planning & execution      |
| 🧾 Resume Parsing       | spaCy + OpenAI via endpoint                 | Handled by dedicated resume agent             |
| 🧮 Job Scoring          | Triggered manually via POST request         | Done by reasoning agent with LLM evaluation   |
| 🔔 Notification         | Pushover via explicit endpoint              | Messaging agent sends push notifications      |


> ✅ **Use the FastAPI version** if you want a REST API interface or integration into web apps.  
> 🤖 **Use the CrewAI version** if you're exploring LLM agents that autonomously collaborate on tasks.
