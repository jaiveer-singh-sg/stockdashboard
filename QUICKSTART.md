# Stock Dashboard - Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Windows
```bash
# 1. Navigate to project
cd "D:\Sandbox\AI Code\StocksDashboard"

# 2. Create & activate environment
python -m venv venv
venv\Scripts\activate

# 3. Install and setup
pip install -r requirements.txt
playwright install

# 4. Copy environment config
copy .env.example .env

# 5. Run!
python run.py
```

### Mac/Linux
```bash
cd ~/path/to/StocksDashboard

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
playwright install

cp .env.example .env

python run.py
```

### Open Browser
```
http://localhost:5000
```

## 📋 What to Try

1. **Home Page**
   - Search for a ticker (try: AAPL, MSFT, NVDA)
   - Click "Analyze"

2. **Fundamentals Page**
   - See company info & market cap
   - View earnings impact analysis
   - Check last trading date & price

3. **Chart Page**
   - Interactive TradingView chart
   - Daily candles + volume
   - Moving averages (MA10/20/50/200)
   - MACD indicator

4. **Highlights Page**
   - 3-day price trend
   - MACD analysis
   - Support/Resistance levels
   - Gap detection

5. **Technicals Page**
   - Price vs. Moving Averages
   - Pivot points (R1/S1)
   - 52-week highs/lows
   - Trend assessment

6. **Whale Action Page**
   - Top institutional holders
   - Insider trading activity
   - Call & put options
   - Volume analysis

7. **Catalysts Page**
   - Market sentiment (Bullish/Bearish)
   - Upcoming events
   - Industry trends
   - Risk factors

## 🔧 Troubleshooting

### Port Already in Use
```
Change FLASK_PORT in .env to 5001 (or another number)
```

### Playwright Won't Install
```bash
# Windows
pip install playwright --upgrade
playwright install chromium

# Mac/Linux with Homebrew issues
conda install -c conda-forge playwright
```

### No Data Appears
- Check internet connection
- Verify NASDAQ ticker is valid
- Try another ticker (AAPL usually works)
- Check browser console for errors (F12)

## 📝 Key Files

| File | Purpose |
|------|---------|
| `run.py` | Start the application |
| `app/__init__.py` | Flask app factory |
| `app/routes.py` | API endpoints |
| `app/services/analysis_service.py` | Analysis logic |
| `app/data_sources/yahoo_finance.py` | Yahoo Finance integration |
| `requirements.txt` | Python packages |
| `.env` | Configuration (copy from .env.example) |

## 🔌 API Quick Test

```bash
# In another terminal while app is running
curl http://localhost:5000/api/health

# Search for ticker
curl "http://localhost:5000/api/search-tickers?q=APP"

# Get fundamentals
curl http://localhost:5000/api/stock/AAPL/fundamentals

# Get technical analysis
curl http://localhost:5000/api/stock/AAPL/technicals
```

## 📊 Sample NASDAQ Tickers

- **Tech Giants**: AAPL, MSFT, GOOGL, NVDA, META
- **Semiconductors**: INTC, AMD, QCOM, MU
- **Growth Stocks**: TSLA, NFLX, SQ, DDOG
- **Cloud**: CRWD, OKTA, SNOW, CRM
- **Healthcare**: GILD, MRNA, VRTX, BIIB

## 🎓 Learning Resources

- **TradingView Chart Guide**: www.tradingview.com
- **Moving Averages**: investopedia.com
- **MACD Indicator**: investopedia.com/terms/m/macd.asp
- **Technical Analysis**: en.wikipedia.org/wiki/Technical_analysis

## 📖 Full Documentation

- `README.md` - Full feature list & installation
- `DEPLOYMENT.md` - Production deployment
- `PROJECT_SUMMARY.md` - Architecture & design
- `GITHUB_SETUP.md` - GitHub integration

## ⚡ Common Commands

```bash
# Activate environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install packages
pip install -r requirements.txt

# Update packages
pip install --upgrade -r requirements.txt

# Install specific package
pip install yfinance

# Deactivate environment
deactivate

# Remove environment
rm -r venv  # Mac/Linux
rmdir /s venv  # Windows
```

## 🐛 Debug Mode

```
Set FLASK_ENV=development in .env
Errors will show detailed tracebacks in browser
```

## 🌐 Access Other Pages

**Direct URLs**:
- Home: `http://localhost:5000/`
- Fundamentals: `http://localhost:5000/fundamentals`
- Chart: `http://localhost:5000/chart`
- Highlights: `http://localhost:5000/highlights`
- Technicals: `http://localhost:5000/technicals`
- Whale Action: `http://localhost:5000/whale-action`
- Catalysts: `http://localhost:5000/catalysts`

## 💾 Using .env File

Create `.env` from `.env.example`:

```env
FLASK_ENV=development
FLASK_PORT=5000
SECRET_KEY=your-secret-key-here
CACHE_TIMEOUT=3600
```

## ✅ Everything Ready!

You now have:
- ✅ 6 interactive pages
- ✅ Real-time stock data
- ✅ Technical analysis tools
- ✅ Institutional data
- ✅ Options information
- ✅ Market catalysts
- ✅ Git repository
- ✅ Ready for GitHub

## 🎯 Next: Push to GitHub

Follow `GITHUB_SETUP.md` to:
1. Create GitHub repo
2. Push your code
3. Setup CI/CD
4. Enable collaborators

## 📞 Need Help?

1. Check browser console (F12) for errors
2. Check terminal output for logs
3. Verify internet connection
4. Check ticker validity on Yahoo Finance
5. Restart Flask app

---

**Happy Analyzing! 📊📈**
