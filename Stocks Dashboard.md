# Develop a Stock Dashbaord Web Application #

Use TradingView public data to get stock latest financial, technical & news data. Use Web Scraping (using Playwright headless browser) to refer data for given ticker
When data is not avaialble via Tradingview, use Yahoo Finance APIs, web screens or Python yfinance packages to extract data. Do validate current date, last trading date and LTP price accuracy.
## Data Reference Sources ##
	Refer below TradingView, Barrons and Yahoo Finance URL for stock details e.g. AMZN
	• Chart: https://www.tradingview.com/chart/?symbol=NASDAQ:AMZN
	• Technical Analysis: https://www.tradingview.com/symbols/NASDAQ-AMZN/technicals/
	• Financial Data: https://www.tradingview.com/symbols/NASDAQ-AMZN/financials/
	Option Data -    https://www.tradingview.com/chart/Eba80tgA/?symbol=NASDAQ%3AAMZN
	Technical Data - 	https://www.tradingview.com/chart/Eba80tgA/?symbol=NASDAQ%3AAMZN
	Financial Data - https://www.tradingview.com/chart/Eba80tgA/?symbol=NASDAQ%3AAMZN
	Forecast/ Target  - https://www.tradingview.com/chart/Eba80tgA/?symbol=NASDAQ%3AAMZN
	Earnings https://www.tradingview.com/symbols/NASDAQ-NVDA/financials-earnings/?earnings-period=FY&revenues-period=FY
	
	• News:
	•	 https://www.tradingview.com/symbols/NASDAQ-AMZN/news/
		Stock News - https://www.tradingview.com/chart/Eba80tgA/?symbol=NASDAQ%3AAMZN
	•	https://www.barrons.com/market-data/stocks/amzn
	•	https://finance.yahoo.com/quote/AMZN/

* Dashboard Page have multiple pages with 1 or 2 sections * 
## Page 1: Section 1 Stocks Fundamentals ##
- Allow stock ticker name selection only from Nasdaq exchange tickers , 
	Show Company name, industry, Marketcap, Stock 52W High & Low Price, Next Earning Date
	for last 2 earnings dates - price increased more than 5% or not on next trading day, did volume went up above weekly average
	Stock today date, last trading date (RTH) and LTP Price. Validate LTP price against Yahoo Finance for last traded date
	
## Page 2: Section 1  Candle Chart View ##
+Shows Tradingview Chart embedded with daily candles and volume, triple MA & MACD indicator on right section . 
## Page 3: Section 1 Chart Highlights ##
Add chart key highligths 
+ is last 3 consecutive days price is increasing
+ is MACD is rising or falling
+ any other key findings e.g. price gap up or down 
## Page 4: Section 1 Technicals ##
+ Assess if price level against MA10, MA20, MA50 and MA200
+ Resistance and Support Levels
## Page 4: Section 2 Whale Action/ Options ##
+ Show changes in top 10 institutional holdings since last 2 months
+ Insider Trading volume in past 2 months
+ Resistance and Support Levels
+ strike points with contracts & volume for calls & puts data

## Page 5: Section 1 Catalyst Events  for Industry ##
+ Market Sentiment : Bullish or Bearish
- list catalyst events in next 2 months which may swing price up or down 
- cite key events for peer stocks 

