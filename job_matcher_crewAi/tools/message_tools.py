from db.load_database import mongo
from notify.message import Message
from langchain.tools import tool


db = mongo()
messages = Message()


class Messaging:
    @tool('Messaging tool')
    def send_message(self):
        """ This tool is used to send suitable jobs details via message"""
        high_scored_docs = db.get_high_scored_docs_to_send()
        if high_scored_docs:
            for i in range(len(high_scored_docs)):
                messages.push(high_scored_docs[i])
                db.update_send(high_scored_docs[i])
                
            return {"result": "message is sent"}
        else:
            return {"result": "no new suitable jobs"}