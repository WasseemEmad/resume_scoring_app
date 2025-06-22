# 📄 Resume-to-Job Matching System

This system automates the process of matching a candidate’s resume with live job listings by extracting skills, classifying them, scoring match quality using a language model, and sending notifications for high matches.

---

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

## 📦 Tech Stack
 - FastAPI – API Framework
 - Streamlit - Frontend
 - MongoDB – Job storage
 - spaCy – Custom NER for skill extraction
 - OpenAI GPT (e.g. gpt-4o) – Reasoning + rating + classification
 - Pushover – Notification system

