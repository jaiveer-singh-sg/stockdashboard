import yfinance as yf


def analyze_ticker(ticker):

    df = yf.Ticker(ticker).history(
        period="6mo"
    )


    close = df["Close"]


    ema12 = close.ewm(
        span=12
    ).mean()

    ema26 = close.ewm(
        span=26
    ).mean()


    macd = ema12 - ema26

    signal = macd.ewm(
        span=9
    ).mean()


    return {

        "ticker": ticker,

        "price":
        round(close.iloc[-1],2),


        "macd":
        "Bullish"
        if macd.iloc[-1] > signal.iloc[-1]
        else "Bearish",


        "52_week_high":
        round(close.max(),2),


        "52_week_low":
        round(close.min(),2)

    }