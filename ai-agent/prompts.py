def swing_prompt(
        ticker,
        indicators
):

    return f"""

You are a professional equity swing trader.

Analyze:

Ticker:
{ticker}


Market Data:

{indicators}


Provide JSON:

{{
"trend":"",
"technical_score":0,
"entry":"",
"stop_loss":"",
"target":"",
"risk_reward":"",
"bull_case":[],
"bear_case":[],
"final_view":""
}}

Rules:

- Do not predict certainty
- Identify risk
- Use technical evidence
- Prefer capital preservation

"""