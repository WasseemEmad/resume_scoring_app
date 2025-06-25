from langchain.tools import tool
import config
import pymongo
from typing import List
from pydantic.v1 import BaseModel
from scraping.search import searching


@tool("job searching tool")
def fetch_jobs(job_title: str) -> str:
    """ This tool is used to search for jobs using the given job title as an input, 
    then returns a message telling how much jobs is saved or if there was an error. """
    search_instance = searching()
    result = search_instance.search_jobs(job_title=job_title)
    
    return result
