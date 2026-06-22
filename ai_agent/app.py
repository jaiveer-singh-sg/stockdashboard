from fastapi import FastAPI
from pydantic import BaseModel
# 1. Import the CORS middleware module
from fastapi.middleware.cors import CORSMiddleware

from agents.swing_agent import analyze_stock


app = FastAPI()

# 2. Add the CORS configuration right below your app definition
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allows requests from any frontend address
    allow_credentials=True,
    allow_methods=["*"],      # Allows POST, OPTIONS, GET, etc.
    allow_headers=["*"],      # Allows Content-Type and other custom headers
)

class TradeRequest(BaseModel):
    ticker:str
    timeframe:str="Swing Trade"


@app.get("/")
def home():
    return {
        "status":"AI Trading Agent Running"
    }


@app.post("/analyze")
async def analyze(req:TradeRequest):

    result = await analyze_stock(
        req.ticker,
        req.timeframe
    )

    return result