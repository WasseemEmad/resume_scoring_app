from langchain.tools import tool
import config
import pymongo
from typing import List, Union
from pydantic.v1 import BaseModel
from scraping.search import searching
from db.load_database import mongo
from rating.get_score import rater
import json

db = mongo()
rating_llm = rater()

@tool("Scoring the resume tool")
def get_score(limit: Union[int, str]) -> dict:
    """
    Score the resume against job descriptions.
    
    Parameters:
    - limit (int): Number of jobs to score.
    - resume_data (dict): Parsed resume details (skills, experience, etc.)
    """
    limit = int(limit)
    with open("parsed_resume_data.json", "r", encoding="utf-8") as f:
        resume_data = json.load(f)
    data = resume_data
    docs = db.get_docs(limit)
    
    num_docs = len(docs)
    
    for i in range(num_docs):
        rating = rating_llm.get_rating(data,docs[i]['description'])
        db.update(docs[i],rating)
        
    scored_docs = db.get_scored_docs()
    
    return {"rated docs": scored_docs}
    