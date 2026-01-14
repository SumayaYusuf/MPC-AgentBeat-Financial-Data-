from google.adk.agents import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.tools import FunctionTool
import uvicorn
import json
from dotenv import load_dotenv
from Data_extraction import load, fmt

load_dotenv()

ETF_DIR = "/home/sumay/tutorial/ETF_attributes_json"
QA_FILE = "/home/sumay/tutorial/scenarios/debate/qa_pairs.json"

# Load ETF data
etfs = load(ETF_DIR)
etf_data = fmt(etfs)

# Load Q&A pairs
with open(QA_FILE) as f:
    QA_PAIRS = {q["id"]: q for q in json.load(f)["qa_pairs"]}

def check_answer(question_id: int, my_answer: int) -> str:
    """Check if answer matches ground truth in qa_pairs.json"""
    if question_id not in QA_PAIRS:
        return f"Question {question_id} not found"
    
    truth = QA_PAIRS[question_id]["answer"]
    is_correct = my_answer == truth
    status = "✓ Correct" if is_correct else "✗ Wrong"
    
    return f"Q{question_id}: {status} (You said {my_answer}, Truth is {truth})"

def run_full_evaluation() -> str:
    """Run evaluation on all 30 questions and return score."""
    results = []
    
    for qid, qa in QA_PAIRS.items():
        truth = qa["answer"]
        results.append(f"Q{qid}: {qa['question']} → Truth: {truth}")
    
    return "\n".join(results) + f"\n\nTotal questions: {len(QA_PAIRS)}"

system_prompt = f'''
You are an ETF data analyst.

ETF Data:
{etf_data}

When asked a question, answer based on the ETF data above.
Answer with just the number when counting.
'''

def main():
    root_agent = Agent(
        name="green_evaluator",
        model="gemini-2.0-flash",
        description="Answers ETF questions.",
        instruction=system_prompt,
        tools=[
            FunctionTool(check_answer),
            FunctionTool(run_full_evaluation),
        ],
    )

    a2a_app = to_a2a(root_agent)
    uvicorn.run(a2a_app, host="127.0.0.1", port=9009)

if __name__ == "__main__":
    main()
