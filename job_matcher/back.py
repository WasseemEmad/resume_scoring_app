from fastapi import FastAPI, File, UploadFile, HTTPException
from scraping.search import searching
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from resume.extract_data import resume_parser
from resume.specify_data import classifier
from db.load_database import mongo
from rating.get_score import rater
from notify.message import Message

db = mongo()
resume_reader = resume_parser()
messages = Message()
searcher = searching()
data_classifier = classifier()
rating_llm = rater()

SAVE_DIR = 'saved_cv'
app = FastAPI()

class JobQuery(BaseModel):
    keyword: str
    
@app.get("/jobs/search")
def search_jobs_db(limit: int ):
    results = db.search_mongo(limit)
    
    if results:
        return results
    else:
        return {"message": "No jobs found in the database or an error occurred"}

@app.post("/jobs/fetch")
def fetch_jobs(query: JobQuery, limit: int = 10):
    result = searcher.search_jobs(query.keyword, limit)
    
    if result:
        return result
    else:
        return {"message": "No new jobs found or an error occurred"}
    
@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
     
    save_path = os.path.join(SAVE_DIR, 'cv.pdf')

    with open(save_path, "wb") as f:
        f.write(await file.read())

    return JSONResponse(content={"filename": file.filename, "status": "received"}, status_code=200)


@app.post("/get_score/")
async def get_score(limit: int):
    ratings = []
    file_path = os.path.join(SAVE_DIR, 'cv.pdf')
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    text = resume_reader.read_resume(file_path)
    
    data = resume_reader.extracted_data(text)
    
    result = data_classifier.get_info(data)
    
    docs = db.get_docs(limit)
    
    num_docs = len(docs)
    
    for i in range(num_docs):
        rating = rating_llm.get_rating(result,docs[i]['description'])
        db.update(docs[i],rating)
        
    scored_docs = db.get_scored_docs()
    
    return JSONResponse(content={"rated docs": scored_docs, "status": "extracted data"}, status_code=200)

@app.post("/compare_job") 
async def compare(job:str):
    file_path = os.path.join(SAVE_DIR, 'cv.pdf')
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    text = resume_reader.read_resume(file_path)
    
    data = resume_reader.extracted_data(text)
    
    result = data_classifier.get_info(data)
    rating = rating_llm.get_rating(result,job)
    
    return JSONResponse(content={"rating": rating, "status": "extracted data"}, status_code=200)

@app.post("/get_high_scored_jobs/")
async def get_high_score():
    high_scored_docs = db.get_high_scored_docs()
    
    return JSONResponse(content={"high_rated_docs": high_scored_docs}, status_code=200)


@app.delete("/clear_collection/")
async def clear_data():
    db.clear_collection()
    
    return JSONResponse(content={"result": "database is empty"}, status_code=200)



@app.post("/send_message")
async def send_message():
    high_scored_docs = db.get_high_scored_docs_to_send()
    if high_scored_docs:
        for i in range(len(high_scored_docs)):
            messages.push(high_scored_docs[i])
            db.update_send(high_scored_docs[i])
            
        return JSONResponse(content={"result": "message is sent"}, status_code=200)
    else:
        return JSONResponse(content={"result": "no new jobs"}, status_code=200)