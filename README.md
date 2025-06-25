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
  A[User Uploads Resume] --> B[ResumeAgent]
  B --> C[Extracted Skills & Info]
  C --> D[JobScorerAgent]
  D --> E[SearchTool]
  E --> F[Scored Jobs]
  F --> G[MessagingAgent]
  G --> H[Top Jobs Notified to User]

## 📦 Tech Stack
 - FastAPI – API Framework
 - CrewAI – Multi-agent task orchestration (New Version)
 - Streamlit - Frontend
 - MongoDB – Job storage
 - spaCy – Custom NER for skill extraction
 - OpenAI GPT (e.g. gpt-4o) – Reasoning + rating + classification
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
