import spacy
import sys, fitz

class resume_parser:
    def __init__(self):
        self.load_model = spacy.load('ner_model_2')
        
    def read_resume(self,file):
        doc = fitz.open(file)
        text = ""
        for page in doc:
            text = text + str(page.get_text())

        tx = " ".join(text.split('\n'))
        return tx
        

    def extracted_data(self,data):
        extracted_data = []
        text_to_test = data
        doc_test = self.load_model(text_to_test)
        for ent in doc_test.ents:
            if ent.label_ == "SKILL":
                extracted_data.append(ent.text)
                
        return extracted_data
    

