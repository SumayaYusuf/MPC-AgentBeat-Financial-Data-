Finance Agent 

Overview
An AI agent that analyzes Vanguard ETF data and answers questions about fund attributes. The agent is evaluated against 30 ground truth questions to measure accuracy.
Data Layer

Source: 7 Vanguard ETF JSON files (MUNY, VAW, VEA, VIG, VIGI, VTG, VV)
Extraction: Data_extraction.py parses nested JSON and extracts 15 attributes
Note: MUNY and VTG are bond/sector funds with null PE, PB, and ROE values

15 Extracted Attributes

Fundamentals: pe, pb, roe, div, distfreq
Cost: exp, fee
Liquidity: turn, aum
Diversification: hold
Performance: r1y, r3y, r5y, sharpe, beta

Agent Layer

Green_Agent.py runs on port 9009
Uses Google Gemini LLM
Receives questions via A2A protocol (JSON-RPC)
ETF data is embedded in the system prompt

Evaluation Layer

qa_pairs.json: 30 questions with ground truth answers
receive.py: Sends questions to agent, extracts numeric answers, compares to ground truth
Output: Results logged to evaluation.log, final score printed to screen

