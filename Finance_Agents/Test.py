import requests
import uuid
import re

URL = "http://127.0.0.1:9009"

def ask(question):
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
    r = requests.post(URL, json=payload)
    try:
        return r.json()["result"]["artifacts"][0]["parts"][0]["text"]
    except:
        return r.json()

if __name__ == "__main__":
    response = ask("Answer all 15 questions")
    print(response)
    
    # Extract TOTAL score
    m = re.search(r"TOTAL:\s*(\d+)/30", str(response))
    if m:
        print(f"\nFINAL SCORE: {m.group(1)}/30")