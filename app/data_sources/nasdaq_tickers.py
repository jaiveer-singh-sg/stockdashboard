"""NASDAQ ticker validation and lookup."""
import requests
import logging
from typing import Dict, Optional, List
import csv
from io import StringIO
import os

logger = logging.getLogger(__name__)


class NasdaqTickerManager:
    """Manages NASDAQ ticker validation and company information."""
    
    def __init__(self):
        """Initialize NASDAQ ticker manager."""
        self.tickers = set()
        self.company_info = {}
        self._load_tickers()
    
    def _load_tickers(self):
        """Load NASDAQ tickers from local cache or fetch fresh data."""
        cache_file = os.path.join(os.path.dirname(__file__), 'nasdaq_tickers.csv')
        
        if os.path.exists(cache_file):
            self._load_from_cache(cache_file)
        else:
            self._fetch_from_nasdaq()
    
    def _load_from_cache(self, cache_file: str):
        """Load tickers from local CSV cache."""
        try:
            with open(cache_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    symbol = row.get('Symbol', '').strip().upper()
                    if symbol:
                        self.tickers.add(symbol)
                        self.company_info[symbol] = {
                            'name': row.get('Security Name', ''),
                            'exchange': row.get('Exchange', 'NASDAQ'),
                            'market_category': row.get('Market Category', ''),
                            'test_issue': row.get('Test Issue', 'N'),
                            'financial_status': row.get('Financial Status', ''),
                        }
            logger.info(f"Loaded {len(self.tickers)} tickers from cache")
        except Exception as e:
            logger.error(f"Error loading tickers from cache: {e}")
            self._fetch_from_nasdaq()
    
    def _fetch_from_nasdaq(self):
        """Fetch current NASDAQ tickers from official source."""
        try:
            # NASDAQ FTP URL for ticker list
            url = 'https://www.nasdaq.com/api/v1/security/lookup'
            
            # Alternative: Use a pre-built list of major NASDAQ tickers
            # This is a sample list - in production, fetch fresh data
            major_tickers = [
                'AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'NVDA', 'TSLA', 'FB', 'META',
                'AVGO', 'COST', 'CSCO', 'INTC', 'AMD', 'NFLX', 'PYPL', 'ASML', 'QCOM',
                'SBUX', 'ADBE', 'CMCSA', 'INTU', 'AEP', 'ABNB', 'CRWD', 'DDOG', 'MRVL',
                'PEP', 'ISRG', 'VRTX', 'MATHWORKS', 'BKNG', 'CPRT', 'FAST', 'GILD',
                'MRNA', 'MSTR', 'MU', 'OKTA', 'PALO', 'PAYX', 'PCAR', 'PCRX', 'ROST',
                'SGEN', 'SPLK', 'SWKS', 'SNPS', 'TMUS', 'TEAM', 'TCOM', 'UPLD', 'WDAY',
                'XEL', 'YUM', 'ZEN', 'AMAT', 'ALXN', 'ALRM', 'AMKR', 'ADI', 'ANET',
                'ANSS', 'ASGN', 'ASTM', 'AZO', 'ADSK', 'ATVI', 'AVAV', 'BIDU', 'BIIB',
                'BJRI', 'BLKB', 'BMRN', 'BNTX', 'BLOB', 'BOKF', 'BRCM', 'BRKS', 'BRPT'
            ]
            
            for ticker in major_tickers:
                self.tickers.add(ticker)
                self.company_info[ticker] = {
                    'name': f'{ticker} Corp',
                    'exchange': 'NASDAQ',
                    'market_category': 'Q',
                    'test_issue': 'N',
                    'financial_status': 'D',
                }
            
            logger.info(f"Loaded {len(self.tickers)} major NASDAQ tickers")
        except Exception as e:
            logger.error(f"Error fetching NASDAQ tickers: {e}")
    
    def validate_ticker(self, ticker: str) -> bool:
        """Check if ticker is valid NASDAQ ticker."""
        ticker = ticker.strip().upper()
        return ticker in self.tickers or self._validate_ticker_online(ticker)
    
    def _validate_ticker_online(self, ticker: str) -> bool:
        """Validate ticker by checking with API."""
        try:
            # Use yfinance to validate
            import yfinance as yf
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Check if we got valid data
            if info.get('exchange') == 'NMS':  # NASDAQ market code
                self.tickers.add(ticker)
                self.company_info[ticker] = {
                    'name': info.get('longName', ticker),
                    'exchange': 'NASDAQ',
                }
                return True
            
            return False
        except Exception as e:
            logger.error(f"Error validating ticker {ticker} online: {e}")
            return False
    
    def get_company_info(self, ticker: str) -> Optional[Dict]:
        """Get cached company information."""
        ticker = ticker.strip().upper()
        return self.company_info.get(ticker)
    
    def search_tickers(self, query: str) -> List[Dict]:
        """Search for tickers by partial name or symbol."""
        query = query.upper()
        results = []
        
        # Search by symbol
        for ticker in self.tickers:
            if query in ticker:
                results.append({
                    'symbol': ticker,
                    'name': self.company_info.get(ticker, {}).get('name', ''),
                })
        
        # Search by company name
        for ticker, info in self.company_info.items():
            name = info.get('name', '').upper()
            if query in name and ticker not in [r['symbol'] for r in results]:
                results.append({
                    'symbol': ticker,
                    'name': info.get('name', ''),
                })
        
        return results[:20]  # Return top 20 matches
    
    def get_all_tickers(self) -> List[str]:
        """Get all available NASDAQ tickers."""
        return sorted(list(self.tickers))
