def get_context(ticker):

    return {

    "ticker": ticker,

    "technical":{

        "macd":"bullish",
        "rsi":62,
        "trend":"above 50 DMA"

    },

    "market":{

        "vix":18,
        "pcr":0.92

    },

    "price":{

        "ath":200,
        "52week_high":190

    }

}
import yfinance as yf
import pandas as pd


def get_market_context():

    # VIX
    vix = yf.Ticker("^VIX")
    vix_price = vix.history(period="1d")["Close"].iloc[-1]

    # PCR 1. Fetch current CBOE Put/Call Ratios - (Using CBOE's public daily text file data as a reliable proxy)
    try:
        url = "https://cboe.com"
        df = pd.read_csv(url, skiprows=2)
        latest_pcr = float(df.iloc[-1]['Total'])
    except Exception:
        latest_pcr = 0.95  # Fallback baseline market average if request blocks

    # Nasdaq
    qqq = yf.Ticker("QQQ")

    df = qqq.history(period="6mo")

    # MACD
    ema12 = df["Close"].ewm(span=12).mean()
    ema26 = df["Close"].ewm(span=26).mean()

    macd = ema12 - ema26
    signal = macd.ewm(span=9).mean()

    macd_status = (
        "Bullish"
        if macd.iloc[-1] > signal.iloc[-1]
        else "Bearish"
    )


    return {

        "vix": round(vix_price,2),
        "pcr": latest_pcr,
        "macd": macd_status,

        "trend":
            "Uptrend"
            if df["Close"].iloc[-1] >
               df["Close"].rolling(50).mean().iloc[-1]
            else "Downtrend"
    }
