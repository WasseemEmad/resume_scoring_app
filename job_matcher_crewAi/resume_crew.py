from crewai import Crew
from textwrap import dedent
from agents import resume_agent,job_scorer_agent,messaging_agent
from tasks import classify_resume_task,job_scoring,send_suitable_jobs_via_message
import json
from dotenv import load_dotenv
import re
load_dotenv()



class ResumeCrew:
    def extract_json(self, text):
        """Extract and parse JSON from a raw output string."""
        try:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
        return None

    def run(self, job_title: str, limit: int):
        print("## Welcome to Resume Analyzer Crew")
        print('----------------------------------')
        

        # 1. Setup Agents
        classification_agent = resume_agent
        scoring_agent = job_scorer_agent
        sender_agent = messaging_agent
        
        # 2. Create First Task (Classify Resume)
        classify_resume = classify_resume_task(agent=classification_agent)

        # 3. Run Crew with First Task Only to get classified resume data
        first_crew = Crew(
            agents=[classification_agent],
            tasks=[classify_resume],
            verbose=True
        )
        classified_resume_data = first_crew.kickoff()

        # 4. Extract valid JSON
        if isinstance(classified_resume_data, str):
            resume_data = classified_resume_data
        else:
            resume_data = classified_resume_data

        # 5. Create Second Task (Score Resume against Jobs)
        
        score_resume_task = job_scoring(
            agent=scoring_agent,
            limit=limit,
            job_title=job_title,
        )
        
        sending_task = send_suitable_jobs_via_message(agent=sender_agent)

        # 6. Run Crew with Second Task
        full_crew = Crew(
            agents=[scoring_agent,sender_agent],
            tasks=[score_resume_task,sending_task],
            verbose=True
        )
        scored_results = full_crew.kickoff()

        return {
            "classified_resume": resume_data,
            "scored_jobs": scored_results
        }

"""
# CLI Entry Point
if __name__ == "__main__":
    resume_crew = ResumeCrew()
    result = resume_crew.run()

    print("########################")
    print("## 🎯 Final Output")
    print("########################")
    print(json.dumps(result, indent=2))

"""

