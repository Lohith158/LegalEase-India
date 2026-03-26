import json
import datetime
import os

def log_collection(question: str, answer: str, sources: list) -> None:
    log = {
        "question": question,
        "answer": answer,
        "sources": sources,
        "timestamp": datetime.datetime.now().isoformat()
    }
    if os.path.exists("logs.json"):
        with open("logs.json", "r") as f:
            logs_list = json.load(f)
    else :
        logs_list = []
        
    logs_list.append(log)

    with open("logs.json", "w") as f:
        json.dump(logs_list, f)