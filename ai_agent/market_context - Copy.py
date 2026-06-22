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
