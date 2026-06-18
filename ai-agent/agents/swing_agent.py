from ollama_client import ask_ollama
from prompts import swing_prompt
import yfinance as yf
import asyncio


def get_market_data(ticker):

    stock = yf.Ticker(ticker)

    hist = stock.history(
        period="6mo"
    )

    latest = hist.iloc[-1]

    data = {

        "price": round(latest.Close,2),

        "volume": int(latest.Volume),

        "52week_high": round(hist.High.max(),2),

        "52week_low": round(hist.Low.min(),2)

    }

    return data



async def analyze_stock(
        ticker,
        timeframe
):

    indicators = get_market_data(
        ticker
    )


    prompt = swing_prompt(
        ticker,
        indicators
    )


    # run blocking Ollama call outside event loop
    result = await asyncio.to_thread(
        ask_ollama,
        prompt
    )


    return result