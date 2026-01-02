"""
Fundamentals Scorer

15 Questions = 30 Points (2 pts each)

Uses your Data_extraction.py to load ETF data.
"""

import sys
sys.path.insert(0, "/home/sumay/tutorial/scenarios/debate")

from Data_extraction import load, get

ETF_DIR = "/home/sumay/tutorial/ETF_attributes_json"


QUESTIONS = [
    # 1.1 Earnings/Quality (12 pts)
    "Q1:  How many ETFs have P/E < 20?",
    "Q2:  How many ETFs have P/B < 3?",
    "Q3:  How many ETFs have ROE > 15%?",
    "Q4:  Which ETF has the lowest P/E?",
    "Q5:  Which ETF has the highest ROE?",
    "Q6:  How many ETFs have P/E < 25 AND P/B < 4?",
    
    # 1.2 Dividend/Yield (4 pts)
    "Q7:  How many ETFs have dividend yield > 2%?",
    "Q8:  Which ETF has the highest dividend yield?",
    
    # 1.3 Valuation vs Benchmarks (12 pts)
    "Q9:  How many ETFs have P/E < 22? (S&P avg)",
    "Q10: How many ETFs have P/B < 4? (market avg)",
    "Q11: How many ETFs have ROE > 13%? (benchmark)",
    "Q12: Which ETF has best valuation? (lowest P/E + P/B)",
    "Q13: How many value ETFs? (P/E < 18 AND P/B < 2.5)",
    "Q14: What is the average P/E?",
    "Q15: What is the average ROE?",
]


def calculate_answers(etfs):
    """Calculate ground truth answers."""
    
    # Get ETFs with valid data
    with_pe = [e for e in etfs if "pe" in e]
    with_pb = [e for e in etfs if "pb" in e]
    with_roe = [e for e in etfs if "roe" in e]
    with_div = [e for e in etfs if "div" in e]
    with_pe_pb = [e for e in etfs if "pe" in e and "pb" in e]
    
    answers = {}
    
    # Q1: P/E < 20
    answers["Q1"] = len([e for e in with_pe if e["pe"] < 20])
    
    # Q2: P/B < 3
    answers["Q2"] = len([e for e in with_pb if e["pb"] < 3])
    
    # Q3: ROE > 15%
    answers["Q3"] = len([e for e in with_roe if e["roe"] > 15])
    
    # Q4: Lowest P/E
    if with_pe:
        answers["Q4"] = min(with_pe, key=lambda e: e["pe"])["tk"]
    else:
        answers["Q4"] = "N/A"
    
    # Q5: Highest ROE
    if with_roe:
        answers["Q5"] = max(with_roe, key=lambda e: e["roe"])["tk"]
    else:
        answers["Q5"] = "N/A"
    

if __name__ == "__main__":
    
    # Load ETFs
    etfs = load(ETF_DIR)
    print(f"Loaded {len(etfs)} ETFs\n")
    
    # Show ETF data
    print("ETF DATA:")
   