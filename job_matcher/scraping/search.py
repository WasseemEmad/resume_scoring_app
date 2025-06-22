import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import config



class searching:
    def __init__(self):
        self.client = MongoClient(config.MONGO_URI)
        self.db = self.client[config.DB_NAME]
        self.collection = self.db[config.COLLECTION_NAME]
        
    def clean_description(self,html_text):
        return BeautifulSoup(html_text, "html.parser").get_text().strip()


    def search_jobs(self,job_title,limit):
        query = job_title
        url = f"https://remotive.com/api/remote-jobs?search={query.replace(' ', '+')}"
        response = requests.get(url)
        count = 0
        if response.status_code == 200:
            jobs = response.json().get("jobs", [])

            for job in jobs:
                job_url = job["url"]
                
                # Skip if this job already exists in the collection
                if self.collection.find_one({"url": job_url}):
                    print(f"Skipped (duplicate): {job['title']}")
                    continue

                cleaned_job = {
                    "title": job["title"],
                    "company": job["company_name"],
                    "location": job["candidate_required_location"],
                    "url": job_url,
                    "description": self.clean_description(job["description"])
                }
                count += 1
                self.collection.insert_one(cleaned_job)
                print(f"Saved: {cleaned_job['title']}")
        else:
            print("API error:", response.status_code)
        
        if count > 0:
            jobs = self.collection.find({}, {"_id": 0, "title": 1, "company": 1, "location": 1, "url": 1}).limit(limit)
            return list(jobs) if jobs else []

