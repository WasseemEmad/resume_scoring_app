# tools/resume_tools.py
from langchain.tools import tool
import fitz
import spacy
import json
from openai import OpenAI
from resume.prompts import system_prompt, get_data_user_prompt
import config
from typing import List
from pydantic.v1 import BaseModel

class ResumeInput(BaseModel):
    resume_text: str
    

@tool("extract_skills_tool",args_schema=ResumeInput)
def extracted_data(resume_text: str) -> dict:
        """Useful to extract skills using a spaCy NER model from resume text."""
        extracted_data = []
        loaded_model = config.MODEL_NAME
        api_key = config.OPENAI_API_KEY
        openai = OpenAI(api_key=api_key)
        text_to_test = resume_text
        model = spacy.load('ner_model_2')
        doc_test = model(text_to_test)
        for ent in doc_test.ents:
            if ent.label_ == "SKILL":
                extracted_data.append(ent.text)
        prompt = get_data_user_prompt(extracted_data)

        response = openai.chat.completions.create(
            model=loaded_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        result = response.choices[0].message.content
        parsed_result = json.loads(result)

        # Save to file
        with open("parsed_resume_data.json", "w", encoding="utf-8") as f:
            json.dump(parsed_result, f, indent=4, ensure_ascii=False)

        return parsed_result
                
        





class ResumeTools:
    def __init__(self):
        self.load_model = spacy.load('ner_model_2')
        self.api_key = config.OPENAI_API_KEY
        self.model = config.MODEL_NAME
        self.openai = OpenAI(api_key=self.api_key)

    @tool("read_resume_tool")
    def read_resume(self) -> str:
        """Extract text content from a PDF resume file."""
        doc = fitz.open("saved_cv/cv.pdf")
        text = "".join([page.get_text() for page in doc])
        return " ".join(text.split('\n'))

