import requests
import uuid
import json
import re
from datetime import datetime

GREEN_AGENT = "http://127.0.0.1:9009"
QA_FILE = "/home/sumay/tutorial/scenarios/debate/qa_pairs.json"
LOG_FILE = "evaluation.log"

with open(QA_FILE) as f:
    QA_PAIRS = json.load(f)["qa_pairs"]


def ask(question):
    """Ask the agent a question."""
    payload = {
        "jsonrpc": "2.0",
        "method": "message/send",
        "id": str(uuid.uuid4()),
        "params": {
            "message": {
                "messageId": str(uuid.uuid4()),
                "role": "user",
                "parts": [{"kind": "text", "text": question}]
            }
        }
    }
    
    try:
        r = requests.post(GREEN_AGENT, json=payload, timeout=30)
        return r.json()["result"]["artifacts"][0]["parts"][0]["text"]
    except:
        return "ERROR"


def extract_number(text):
    """Extract first number from text."""
    match = re.search(r'-?\d+', str(text))
    return int(match.group()) if match else -1


if __name__ == "__main__":
    correct = 0
    total = len(QA_PAIRS)
    
    with open(LOG_FILE, "w") as log:
        log.write(f"Evaluation: {datetime.now()}\n")
        log.write("=" * 50 + "\n\n")
        
        for qa in QA_PAIRS:
            qid = qa["id"]
            question = qa["question"]
            truth = qa["answer"]
            
            response = ask(question)
            agent_answer = extract_number(response)
            
            is_correct = agent_answer == truth
            if is_correct:
                correct += 1
            
            status = "✓" if is_correct else "✗"
            log.write(f"Q{qid}: {status} Agent={agent_answer}, Truth={truth}\n")
        
        log.write(f"\nSCORE: {correct}/{total}\n")
    
    print(f"SCORE: {correct}/{total}")
    print(f"Details saved to {LOG_FILE}")
