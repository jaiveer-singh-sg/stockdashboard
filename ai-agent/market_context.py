import yfinance as yf


def get_context(ticker):

    stock = yf.Ticker(ticker)

    hist = stock.history(
        period="6mo"
    )


    latest = hist.iloc[-1]


    context = {

        "ticker": ticker,

        "price":
            round(latest.Close,2),

        "volume":
            int(latest.Volume),


        "52_week_high":
            round(hist.High.max(),2),


        "52_week_low":
            round(hist.Low.min(),2),


        "trend":

            "above 50DMA"
            if latest.Close >
            hist.Close.rolling(50).mean().iloc[-1]
            else
            "below 50DMA"

    }


    return context