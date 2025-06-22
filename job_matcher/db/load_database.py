from pymongo import MongoClient
import config




class mongo:
    def __init__(self):
        self.client = MongoClient(config.MONGO_URI)
        self.db = self.client[config.DB_NAME]
        self.collection = self.db[config.COLLECTION_NAME]
        
    def search_mongo(self,limit):
        jobs = self.collection.find({}, {"_id": 0, "title": 1, "company": 1, "location": 1, "url": 1}).limit(limit)
        return list(jobs) if jobs else []

    def get_docs(self,limit):
        docs = []
        doc_count = self.collection.count_documents({})
        jobs = self.collection.find(
            {"rating": {"$exists": False}},  # filter: rating does not exist
            {"_id": 0, "title": 1, "company": 1, "location": 1, "url": 1, "description": 1}  # projection
        ).limit(limit)
        
        for doc in jobs:
            docs.append(doc)
            
        return docs

    def update(self,data,results):
        self.collection.update_one(
            {'url': data['url']},
            {'$set': {"rating": results['rating'],
                    'reason': results['reason'],
                    'breakdown':results['breakdown'],
                    'recommendation':results['recommendation'],
                    'reason_type':results['reason_type']}}
        )
        
    def get_scored_docs(self):
        score_docs = list(self.collection.find({
        'rating': {'$exists': True}
        },{"_id": 0, "description":0}))
        
        return score_docs

    def get_high_scored_docs(self):
        high_score_docs = list(self.collection.find({
        'rating': {'$exists': True,'$gte': 6}
        },{"_id": 0, "description":0}))
        
        return high_score_docs

    def clear_collection(self):
        self.collection.delete_many({})  # Clear existing data


    def update_send(self,data):
        self.collection.update_one(
            {'url': data['url']},
            {'$set': {"sent":"true"}}
        )
    def get_high_scored_docs_to_send(self):
        high_score_docs = list(self.collection.find({
        'rating': {'$exists': True,'$gte': 6},
        'sent' : {'$exists': False}
        },{"_id": 0, "description":0}))
        
        return high_score_docs
    
    
    