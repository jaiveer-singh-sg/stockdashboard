"""TradingView web scraper using Playwright for technical data."""
import asyncio
from typing import Dict, Optional, List
import logging
from playwright.sync_api import sync_playwright, Page, Browser
import json
import re

logger = logging.getLogger(__name__)


class TradingViewScraper:
    """Scrapes technical and fundamental data from TradingView."""
    
    def __init__(self, headless: bool = True):
        """Initialize TradingView scraper."""
        self.headless = headless
        self.browser = None
        self.playwright = None
    
    def start_browser(self):
        """Start Playwright browser instance."""
        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=self.headless)
        except Exception as e:
            logger.error(f"Error starting browser: {e}")
            raise
    
    def stop_browser(self):
        """Stop Playwright browser instance."""
        try:
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
        except Exception as e:
            logger.error(f"Error stopping browser: {e}")
    
    def get_technicals(self, ticker: str, exchange: str = 'NASDAQ') -> Optional[Dict]:
        """Fetch technical analysis data from TradingView."""
        try:
            self.start_browser()
            
            url = f"https://www.tradingview.com/symbols/{exchange}-{ticker}/technicals/"
            page = self.browser.new_page()
            
            try:
                page.goto(url, wait_until='networkidle', timeout=60000)
                
                # Wait for content to load
                page.wait_for_selector('[data-testid="technicals"]', timeout=10000)
                
                # Extract technical data
                technicals = self._extract_technicals_data(page)
                
                return technicals
            finally:
                page.close()
                self.stop_browser()
        except Exception as e:
            logger.error(f"Error scraping technicals for {ticker}: {e}")
            self.stop_browser()
            return None
    
    def _extract_technicals_data(self, page: Page) -> Dict:
        """Extract technical indicators from page."""
        try:
            # Get technical summary
            technical_summary = {}
            
            # Try to extract moving averages comparison
            try:
                ma_data = page.evaluate("""
                    () => {
                        const data = {};
                        const rows = document.querySelectorAll('[data-test="technical-row"]');
                        rows.forEach(row => {
                            const label = row.querySelector('[data-test="label"]')?.textContent;
                            const value = row.querySelector('[data-test="value"]')?.textContent;
                            if (label && value) {
                                data[label.trim()] = value.trim();
                            }
                        });
                        return data;
                    }
                """)
                technical_summary.update(ma_data)
            except:
                pass
            
            return technical_summary
        except Exception as e:
            logger.error(f"Error extracting technical data: {e}")
            return {}
    
    def get_financial_data(self, ticker: str, exchange: str = 'NASDAQ') -> Optional[Dict]:
        """Fetch financial data from TradingView."""
        try:
            self.start_browser()
            
            url = f"https://www.tradingview.com/symbols/{exchange}-{ticker}/financials/"
            page = self.browser.new_page()
            
            try:
                page.goto(url, wait_until='networkidle', timeout=60000)
                
                # Wait for financial tables
                page.wait_for_selector('[data-testid="financials"]', timeout=10000)
                
                financial_data = self._extract_financial_data(page)
                
                return financial_data
            finally:
                page.close()
                self.stop_browser()
        except Exception as e:
            logger.error(f"Error scraping financial data for {ticker}: {e}")
            self.stop_browser()
            return None
    
    def _extract_financial_data(self, page: Page) -> Dict:
        """Extract financial data from page."""
        try:
            financial_summary = {}
            
            # Try to extract key financial metrics
            try:
                fin_data = page.evaluate("""
                    () => {
                        const data = {};
                        const rows = document.querySelectorAll('[data-test="financial-row"]');
                        rows.forEach(row => {
                            const label = row.querySelector('[data-test="label"]')?.textContent;
                            const value = row.querySelector('[data-test="value"]')?.textContent;
                            if (label && value) {
                                data[label.trim()] = value.trim();
                            }
                        });
                        return data;
                    }
                """)
                financial_summary.update(fin_data)
            except:
                pass
            
            return financial_summary
        except Exception as e:
            logger.error(f"Error extracting financial data: {e}")
            return {}
    
    def get_news(self, ticker: str, exchange: str = 'NASDAQ') -> Optional[List[Dict]]:
        """Fetch latest news from TradingView."""
        try:
            self.start_browser()
            
            url = f"https://www.tradingview.com/symbols/{exchange}-{ticker}/news/"
            page = self.browser.new_page()
            
            try:
                page.goto(url, wait_until='networkidle', timeout=60000)
                
                # Wait for news articles
                page.wait_for_selector('[data-testid="news-item"]', timeout=10000)
                
                news_items = self._extract_news(page)
                
                return news_items
            finally:
                page.close()
                self.stop_browser()
        except Exception as e:
            logger.error(f"Error scraping news for {ticker}: {e}")
            self.stop_browser()
            return None
    
    def _extract_news(self, page: Page) -> List[Dict]:
        """Extract news items from page."""
        try:
            news_data = page.evaluate("""
                () => {
                    const articles = [];
                    const items = document.querySelectorAll('[data-testid="news-item"]');
                    items.forEach(item => {
                        const title = item.querySelector('[data-testid="news-title"]')?.textContent;
                        const source = item.querySelector('[data-testid="news-source"]')?.textContent;
                        const time = item.querySelector('[data-testid="news-time"]')?.textContent;
                        const link = item.querySelector('a')?.href;
                        
                        if (title) {
                            articles.push({
                                title: title.trim(),
                                source: source?.trim() || 'Unknown',
                                time: time?.trim() || 'Unknown',
                                link: link || ''
                            });
                        }
                    });
                    return articles;
                }
            """)
            
            return news_data[:10]  # Return top 10 news items
        except Exception as e:
            logger.error(f"Error extracting news: {e}")
            return []
    
    def get_chart_data(self, ticker: str, exchange: str = 'NASDAQ') -> Optional[Dict]:
        """Fetch chart embedding URL and basic chart info."""
        chart_url = f"https://www.tradingview.com/chart/?symbol={exchange}:{ticker}"
        
        return {
            'url': chart_url,
            'ticker': ticker,
            'exchange': exchange,
            'embedded_url': self._get_embed_url(ticker, exchange)
        }
    
    def _get_embed_url(self, ticker: str, exchange: str) -> str:
        """Generate TradingView lightweight chart embed URL."""
        return f"https://www.tradingview.com/widgetembed/?symbol={exchange}:{ticker}"
    
    def get_resistance_support_levels(self, ticker: str, 
                                     exchange: str = 'NASDAQ') -> Optional[Dict]:
        """Extract support and resistance levels."""
        try:
            self.start_browser()
            
            url = f"https://www.tradingview.com/symbols/{exchange}-{ticker}/technicals/"
            page = self.browser.new_page()
            
            try:
                page.goto(url, wait_until='networkidle', timeout=60000)
                
                # Extract support/resistance data
                levels = self._extract_support_resistance(page)
                
                return levels
            finally:
                page.close()
                self.stop_browser()
        except Exception as e:
            logger.error(f"Error getting support/resistance for {ticker}: {e}")
            self.stop_browser()
            return None
    
    def _extract_support_resistance(self, page: Page) -> Dict:
        """Extract support and resistance levels from page."""
        try:
            levels = page.evaluate("""
                () => {
                    const data = {
                        resistance_levels: [],
                        support_levels: []
                    };
                    
                    // Try to find resistance and support sections
                    const rows = document.querySelectorAll('[data-test="level-row"]');
                    rows.forEach(row => {
                        const label = row.querySelector('[data-test="label"]')?.textContent;
                        const value = row.querySelector('[data-test="value"]')?.textContent;
                        
                        if (label && value) {
                            const level = { label: label.trim(), value: value.trim() };
                            if (label.toLowerCase().includes('resistance')) {
                                data.resistance_levels.push(level);
                            } else if (label.toLowerCase().includes('support')) {
                                data.support_levels.push(level);
                            }
                        }
                    });
                    
                    return data;
                }
            """)
            
            return levels
        except Exception as e:
            logger.error(f"Error extracting support/resistance: {e}")
            return {'resistance_levels': [], 'support_levels': []}
