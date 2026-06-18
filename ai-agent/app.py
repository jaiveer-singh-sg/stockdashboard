from fastapi import FastAPI
from pydantic import BaseModel

from agents.swing_agent import analyze_stock


app = FastAPI()


class TradeRequest(BaseModel):
    ticker:str
    timeframe:str="Swing Trade"


@app.get("/")
def home():
    return {
        "status":"AI Trading Agent Running"
    }


@app.post("/analyze")
def analyze(req:TradeRequest):

    result = analyze_stock(
        req.ticker,
        req.timeframe
    )

    return result