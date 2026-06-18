from ollama_client import ask_ollama
from prompts import swing_prompt
# Example inside swing_agent.py
# response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=30)

import yfinance as yf


def get_market_data(ticker):


    stock=yf.Ticker(ticker)


    hist=stock.history(
        period="6mo"
    )


    latest=hist.iloc[-1]


    data={

    "price":
        round(latest.Close,2),

    "volume":
        int(latest.Volume),

    "52week_high":
        round(hist.High.max(),2),

    "52week_low":
        round(hist.Low.min(),2)

    }


    return data


# old line -->  def analyze_stock(
async def analyze_stock(
        ticker,
        timeframe
):


    indicators=get_market_data(
        ticker
    )


    prompt=swing_prompt(
        ticker,
        indicators
    )


    result=ask_ollama(
        prompt
    )


    return result