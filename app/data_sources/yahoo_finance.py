"""Yahoo Finance data source for stock information."""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class YahooFinanceDataSource:
    """Fetches data from Yahoo Finance using yfinance library."""
    
    def __init__(self, cache_timeout=3600):
        """Initialize Yahoo Finance data source."""
        self.cache = {}
        self.cache_timeout = cache_timeout
        self.cache_timestamps = {}
    
    def get_stock_info(self, ticker: str) -> Optional[Dict]:
        """Fetch comprehensive stock information."""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return {
                'ticker': ticker,
                'company_name': info.get('longName', ''),
                'industry': info.get('industry', ''),
                'sector': info.get('sector', ''),
                'market_cap': info.get('marketCap', 0),
                'fifty_two_week_high': info.get('fiftyTwoWeekHigh', 0),
                'fifty_two_week_low': info.get('fiftyTwoWeekLow', 0),
                'current_price': info.get('currentPrice', 0),
                'previous_close': info.get('previousClose', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'peg_ratio': info.get('pegRatio', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'employees': info.get('fullTimeEmployees', 0),
                'website': info.get('website', ''),
                'description': info.get('longBusinessSummary', ''),
            }
        except Exception as e:
            logger.error(f"Error fetching stock info for {ticker}: {e}")
            return None
    
    def get_historical_data(self, ticker: str, period: str = '1y', 
                          interval: str = '1d') -> Optional[pd.DataFrame]:
        """Fetch historical price data."""
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period, interval=interval)
            
            if df.empty:
                return None
            
            # Add technical indicators
            df['MA10'] = df['Close'].rolling(window=10).mean()
            df['MA20'] = df['Close'].rolling(window=20).mean()
            df['MA50'] = df['Close'].rolling(window=50).mean()
            df['MA200'] = df['Close'].rolling(window=200).mean()
            
            # MACD
            df = self._calculate_macd(df)
            
            return df
        except Exception as e:
            logger.error(f"Error fetching historical data for {ticker}: {e}")
            return None
    
    def _calculate_macd(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate MACD indicator."""
        try:
            ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
            ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
            
            df['MACD'] = ema_12 - ema_26
            df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
            df['MACD_Histogram'] = df['MACD'] - df['Signal']
            
            return df
        except Exception as e:
            logger.error(f"Error calculating MACD: {e}")
            return df
    
    def get_earnings_dates(self, ticker: str) -> Optional[List[Dict]]:
        """Fetch upcoming earnings dates."""
        try:
            stock = yf.Ticker(ticker)
            earnings_dates = stock.info.get('earningsDate', [])
            
            if isinstance(earnings_dates, list) and len(earnings_dates) > 0:
                return [
                    {
                        'date': datetime.fromtimestamp(ts).strftime('%Y-%m-%d') 
                        if isinstance(ts, (int, float)) else str(ts)
                    }
                    for ts in earnings_dates[:2]
                ]
            return []
        except Exception as e:
            logger.error(f"Error fetching earnings dates for {ticker}: {e}")
            return []
    
    def get_option_chain(self, ticker: str, expiration: str = None) -> Optional[Dict]:
        """Fetch options data."""
        try:
            stock = yf.Ticker(ticker)
            expirations = stock.options
            
            if not expirations:
                return None
            
            if expiration is None:
                expiration = expirations[0]
            
            if expiration not in expirations:
                expiration = expirations[0]
            
            opt = stock.option_chain(expiration)
            
            return {
                'expiration': expiration,
                'calls': self._process_option_data(opt.calls),
                'puts': self._process_option_data(opt.puts),
            }
        except Exception as e:
            logger.error(f"Error fetching option chain for {ticker}: {e}")
            return None
    
    def _process_option_data(self, df: pd.DataFrame) -> List[Dict]:
        """Process option data into list of dicts."""
        try:
            # Get top 10 by volume or open interest
            df = df.sort_values('volume', ascending=False).head(10)
            
            return df[[
                'strike', 'lastPrice', 'bid', 'ask', 'volume', 
                'openInterest', 'impliedVolatility'
            ]].to_dict('records')
        except Exception as e:
            logger.error(f"Error processing option data: {e}")
            return []
    
    def get_last_trading_date(self, ticker: str) -> Optional[str]:
        """Get the last trading date."""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period='5d', interval='1d')
            
            if hist.empty:
                return None
            
            last_date = hist.index[-1]
            return last_date.strftime('%Y-%m-%d')
        except Exception as e:
            logger.error(f"Error getting last trading date for {ticker}: {e}")
            return None
    
    def get_ltp_price(self, ticker: str) -> Optional[float]:
        """Get last traded price."""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Try different price fields
            ltp = (info.get('currentPrice') or 
                   info.get('regularMarketPrice') or
                   info.get('lastPrice') or
                   0)
            
            return ltp if ltp > 0 else None
        except Exception as e:
            logger.error(f"Error getting LTP for {ticker}: {e}")
            return None
    
    def get_institutional_holdings(self, ticker: str) -> Optional[List[Dict]]:
        """Fetch top institutional holders."""
        try:
            stock = yf.Ticker(ticker)
            holders = stock.institutional_holders
            
            if holders is None or holders.empty:
                return None
            
            return holders.head(10).to_dict('records')
        except Exception as e:
            logger.error(f"Error fetching institutional holders for {ticker}: {e}")
            return None
    
    def get_insider_transactions(self, ticker: str) -> Optional[List[Dict]]:
        """Fetch insider trading data."""
        try:
            stock = yf.Ticker(ticker)
            insider = stock.insider_transactions
            
            if insider is None or insider.empty:
                return None
            
            return insider.head(20).to_dict('records')
        except Exception as e:
            logger.error(f"Error fetching insider transactions for {ticker}: {e}")
            return None
    
    def validate_ticker(self, ticker: str) -> bool:
        """Validate if ticker exists and is accessible."""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Check if we got valid data
            if 'regularMarketPrice' in info or 'currentPrice' in info:
                return True
            
            return False
        except Exception as e:
            logger.error(f"Error validating ticker {ticker}: {e}")
            return False
