# Stock Dashboard Web Application

A comprehensive web-based stock analysis dashboard for NASDAQ stocks with real-time data from TradingView and Yahoo Finance.

## Features

### 📈 Pages & Functionality

1. **Stock Fundamentals** (Page 1, Section 1)
   - Company information (name, industry, sector, market cap)
   - 52-week highs and lows
   - Next earnings dates
   - Last 2 earnings analysis
   - Price validation against Yahoo Finance
   - Last trading date and LTP price

2. **Candle Chart View** (Page 2, Section 1)
   - Embedded TradingView chart with daily candles
   - Volume indicator
   - Technical indicators: Triple MA (MA10, MA20, MA50, MA200) & MACD

3. **Chart Highlights** (Page 3, Section 1)
   - 3 consecutive days price increase detection
   - MACD trend analysis (rising/falling)
   - Price gap detection (gap up/down)
   - Support & resistance identification

4. **Technical Analysis** (Page 4, Section 1)
   - Price level assessment vs MA10, MA20, MA50, MA200
   - Pivot point calculations (R1, S1)
   - 52-week highs and lows
   - 20-day highs and lows

5. **Whale Action / Options** (Page 4, Section 2)
   - Top 10 institutional holdings
   - Insider trading activity (past 2 months)
   - Strike points with contracts & volume
   - Calls and puts data

6. **Catalyst Events** (Page 5, Section 1)
   - Market sentiment analysis (Bullish/Bearish)
   - Upcoming catalyst events (next 2 months)
   - Industry events and peer stock analysis
   - Earnings announcements

## Data Sources

- **TradingView**: Charts, technical analysis, financial data
- **Yahoo Finance**: Stock data, options, institutional holdings, insider transactions
- **Python yfinance**: Alternative data source for validation

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Data Collection**: Playwright (headless browser), yfinance, requests
- **Database**: In-memory cache with configurable timeout
- **Deployment**: Gunicorn, Flask development server

## Installation

### Requirements
- Python 3.8+
- pip or conda

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd StocksDashboard
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   playwright install  # Install browsers for Playwright
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Open in browser**
   ```
   http://localhost:5000
   ```

## Project Structure

```
StocksDashboard/
├── ai-agent
│   │
│   ├── app.py                <-- FastAPI endpoint
│   │
│   ├── ollama_client.py      <-- Hermes/Ollama connector
│   │
│   ├── market_context.py     <-- collect indicators
│   │
│   ├── prompts.py            <-- AI prompts
│   │
│   ├── requirements.txt      <--  data libraries dependencies
│   │
│   └── agents
│       └── swing_agent.py    <-- Market data, AI LLM Prompt
├── app/
│   ├── __init__.py                 # Flask app factory
│   ├── routes.py                   # Route handlers
│   ├── data_sources/
│   │   ├── __init__.py
│   │   ├── yahoo_finance.py        # Yahoo Finance data fetcher
│   │   ├── tradingview_scraper.py  # TradingView scraper
│   │   └── nasdaq_tickers.py       # NASDAQ ticker manager
│   ├── services/
│   │   ├── __init__.py
│   │   └── analysis_service.py     # Market data aanalysis logic 
│   ├── templates/
│   │   ├── base.html               # Base template
│   │   ├── index.html              # Home page
│   │   └── pages/
│   │       ├── fundamentals.html
│   │       ├── chart.html
│   │       ├── highlights.html
│   │       ├── technicals.html
│   │       ├── whale_action.html
│   │       └── catalysts.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       ├── js/
│       │   ├── main.js
│       │   └── ticker-search.js
│       └── images/
├── tests/                          # Test files
├── run.py                          # Application entry point
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## Configuration

Create `.env` file from `.env.example`:

```env
FLASK_ENV=development
FLASK_PORT=5000
SECRET_KEY=your-secret-key
YAHOO_FINANCE_ENABLED=true
TRADINGVIEW_HEADLESS_BROWSER=true
CACHE_TIMEOUT=3600
```

## Usage

1. **Navigate to Home Page**: Start at the dashboard home
2. **Search Ticker**: Enter NASDAQ ticker symbol (e.g., AAPL, MSFT, NVDA)
3. **View Analysis**: Click on any page to see different analyses
4. **Update Ticker**: Use the search box on any page to analyze different stocks

## API Endpoints

### Validation & Search
- `GET /api/validate-ticker/<ticker>` - Validate NASDAQ ticker
- `GET /api/search-tickers?q=<query>` - Search for tickers

### Stock Data
- `GET /api/stock/<ticker>/fundamentals` - Company fundamentals
- `GET /api/stock/<ticker>/historical?period=1y` - Historical data with indicators
- `GET /api/stock/<ticker>/chart-highlights` - Chart analysis
- `GET /api/stock/<ticker>/technicals` - Technical analysis
- `GET /api/stock/<ticker>/options` - Options data
- `GET /api/stock/<ticker>/whale-action` - Institutional & insider data
- `GET /api/stock/<ticker>/catalysts` - Catalyst events & sentiment
- `GET /api/stock/<ticker>/chart-url` - TradingView chart URL

### System
- `GET /api/health` - Health check

## Data Accuracy

The application validates data by:
- Cross-referencing LTP prices with Yahoo Finance
- Validating last trading dates
- Checking NASDAQ ticker validity
- Comparing technical indicators across multiple timeframes

## AI Agent Insights empowered by LLM 

The application uses Hermes3 model end point (which can be run locally or in cloud ):
- Entry, Target, Stop Loss price points & Risk Reward Ratio
- Bullish scenario and explanation
- Bearish scenario and explanation

## Future Enhancements

- [ ] Real-time WebSocket updates
- [ ] User accounts and watchlists
- [ ] Advanced charting with TradingView Lightweight Charts
- [ ] ML-based price predictions
- [ ] Portfolio tracking
- [ ] Custom alerts
- [ ] Export to PDF/CSV
- [ ] Mobile app

## Key Signals for Swing Insights

- [ ] MACD
- [ ] RSI
- [ ] VIX
- [ ] PCR
- [ ] ATH
- [ ] 52WK high/low
- [ ] YTD
- [ ] volume
- [ ] trend

## Troubleshooting

### Playwright Not Installing
```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt-get install -y libglib2.0-0 libpangocairo-1.0-0

# Or use conda
conda install -c conda-forge playwright
```

### Port Already in Use
```bash
# Change port in .env
FLASK_PORT=5001
```

### Yahoo Finance Rate Limiting
- Requests are cached for configured timeout
- Adjust CACHE_TIMEOUT in .env if needed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
1. Check existing issues on GitHub
2. Create a new issue with detailed description
3. Include error messages and environment details

## Disclaimer

This application is for educational and informational purposes only. It is not financial advice. Always do your own research before making investment decisions.
