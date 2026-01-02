Finance Agent 

This project builds on the AgentBeats Tutorial framework https://github.com/RDI-Foundation/agentbeats-tutorial

It's an ETF evaluation tool using Google's Gemini that scores Vanguard ETF data based on a custom evaluation metric 

Data_extraction.py
Pulls data from ETF JSON files and organizes it by attributes. Things like P/E ratio, P/B ratio, ROE, dividend yield, expense ratios, and more. The JSON files contain raw Vanguard ETF data, and this script makes it usable by extracting just the fields we care about.

Finance_Agent.py
This is the Gemini-powered agent. It takes the extracted ETF data and answers 15 questions about fundamentals. The agent runs as a server on port 9009 and waits for requests. When you ask it something like "How many ETFs have P/E < 20?", it looks at the data and responds.

receive.py
A simple client that talks to the agent. It sends the evaluation questions to the agent running on port 9009 and prints back whatever Gemini returns. This is how you actually interact with the agent once it's running.

scorer.py
The ground truth checker. It calculates the correct answers by going through the actual ETF data manually. You can use this to see if the agent is giving accurate responses or just making things up.

** This will be out of 100 currently only working on one of the metrics

The Evaluation Metric: 
The agent scores ETFs on fundamentals out of 30 points:
Earnings/Quality (12 pts) — P/E, P/B, ROE comparisons
Dividend/Yield (4 pts) — dividend yield analysis
Valuation vs Benchmarks (12 pts) — how ETFs stack up against S&P 500 averages (P/E of 22, P/B of 4, ROE of 13%)

15 questions total, 2 points each.

White Agent is under construction: 
White Agent Outline
Role: Evaluator/Judge
What it does:

Loads ground truth answers (from scorer.py logic)
Connects to green Finance Agent on port 9009
Asks all 15 questions one by one
Compares each answer to ground truth
