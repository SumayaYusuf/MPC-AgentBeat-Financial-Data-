from google.adk.agents import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
import uvicorn
from dotenv import load_dotenv
from Data_extraction import load, fmt

load_dotenv()

ETF_DIR = "/home/sumay/tutorial/ETF_attributes_json"

system_prompt = '''
You are an ETF evaluator. Answer these 15 questions to score fundamentals (30 pts total, 2 pts each).

ETF Data:
{etf_data}

Questions:

1.1 Earnings/Quality (12 pts)
Q1: How many ETFs have P/E < 20?
Q2: How many ETFs have P/B < 3?
Q3: How many ETFs have ROE > 15%?
Q4: Which ETF has the lowest P/E?
Q5: Which ETF has the highest ROE?
Q6: How many ETFs have P/E < 25 AND P/B < 4?

1.2 Dividend/Yield (4 pts)
Q7: How many ETFs have dividend yield > 2%?
Q8: Which ETF has the highest dividend yield?

1.3 Valuation vs Benchmarks (12 pts)
Q9: How many ETFs have P/E < 22? (S&P avg)
Q10: How many ETFs have P/B < 4? (market avg)
Q11: How many ETFs have ROE > 13%? (benchmark)
Q12: Which ETF has best valuation? (lowest P/E + P/B)
Q13: How many value ETFs? (P/E < 18 AND P/B < 2.5)
Q14: What is the average P/E?
Q15: What is the average ROE?

Answer format:
Q1: [answer]
Q2: [answer]
...
Q15: [answer]
TOTAL: X/30
'''

def main():
    etfs = load(ETF_DIR)
    
    root_agent = Agent(
        name="finance_evaluator",
        model="gemini-2.0-flash",
        description="Score ETF fundamentals out of 30.",
        instruction=system_prompt.format(etf_data=fmt(etfs)),
    )

    a2a_app = to_a2a(root_agent)
    uvicorn.run(a2a_app, host="127.0.0.1", port=9009)

if __name__ == "__main__":
    main()