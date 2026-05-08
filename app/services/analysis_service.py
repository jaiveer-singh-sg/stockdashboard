"""Analysis service for stock technical and fundamental analysis."""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class AnalysisService:
    """Provides analytical insights on stocks."""
    
    def __init__(self, data_source):
        """Initialize with data source."""
        self.data_source = data_source
    
    def analyze_earnings_impact(self, ticker: str) -> Optional[Dict]:
        """Analyze impact of last 2 earnings on price."""
        try:
            # Get historical data
            df = self.data_source.get_historical_data(ticker, period='1y')
            
            if df is None or df.empty:
                return None
            
            # Get earnings dates
            earnings_dates = self.data_source.get_earnings_dates(ticker)
            
            if not earnings_dates:
                return {'earnings_history': []}
            
            earnings_history = []
            
            for earning_date_str in earnings_dates[:2]:  # Last 2 earnings
                try:
                    # Parse earnings date
                    earning_date = pd.to_datetime(earning_date_str['date'])
                    
                    # Find next trading day
                    next_trading_day = None
                    for i in range(1, 5):
                        next_date = earning_date + timedelta(days=i)
                        if next_date in df.index:
                            next_trading_day = next_date
                            break
                    
                    if next_trading_day is None or earning_date not in df.index:
                        continue
                    
                    # Get prices
                    earning_day_close = df.loc[earning_date, 'Close']
                    next_day_close = df.loc[next_trading_day, 'Close']
                    next_day_volume = df.loc[next_trading_day, 'Volume']
                    
                    # Calculate metrics
                    price_change_pct = ((next_day_close - earning_day_close) / earning_day_close) * 100
                    
                    # Get weekly average volume
                    week_start = next_trading_day - timedelta(days=7)
                    week_data = df[week_start:next_trading_day]
                    avg_volume = week_data['Volume'].mean() if not week_data.empty else 0
                    volume_increase = next_day_volume > avg_volume
                    
                    earnings_history.append({
                        'date': earning_date.strftime('%Y-%m-%d'),
                        'price_change_pct': round(price_change_pct, 2),
                        'price_up_5pct': price_change_pct > 5,
                        'volume_above_avg': volume_increase,
                        'next_day_volume': int(next_day_volume),
                        'avg_weekly_volume': int(avg_volume),
                    })
                except Exception as e:
                    logger.warning(f"Error analyzing earnings for {earning_date_str}: {e}")
            
            return {'earnings_history': earnings_history}
        except Exception as e:
            logger.error(f"Error analyzing earnings impact for {ticker}: {e}")
            return None
    
    def get_chart_highlights(self, ticker: str) -> Optional[Dict]:
        """Get key chart highlights with comprehensive analysis."""
        try:
            df = self.data_source.get_historical_data(ticker, period='3mo')
            
            if df is None or df.empty:
                return None
            
            current_price = float(df['Close'].iloc[-1])
            
            # 1. Check 3 consecutive days increase
            three_days_increasing = False
            last_3_days = df.tail(3)
            if len(last_3_days) >= 3:
                closes = last_3_days['Close'].values
                three_days_increasing = bool(
                    closes[0] < closes[1] and 
                    closes[1] < closes[2]
                )
            
            # 2. MACD trend analysis
            macd_analysis = {'rising': False, 'falling': False, 'crossed': False, 'strength': 'Neutral'}
            if len(df) >= 26:
                macd = float(df['MACD'].iloc[-1]) if pd.notna(df['MACD'].iloc[-1]) else 0
                signal = float(df['Signal'].iloc[-1]) if pd.notna(df['Signal'].iloc[-1]) else 0
                macd_prev = float(df['MACD'].iloc[-2]) if pd.notna(df['MACD'].iloc[-2]) else 0
                signal_prev = float(df['Signal'].iloc[-2]) if pd.notna(df['Signal'].iloc[-2]) else 0
                
                macd_analysis['rising'] = bool(macd > macd_prev)
                macd_analysis['falling'] = bool(macd < macd_prev)
                
                # Check for crossover
                macd_analysis['crossed'] = bool((macd_prev < signal_prev and macd > signal) or \
                                               (macd_prev > signal_prev and macd < signal))
                
                # Determine strength
                if macd > signal and macd > 0:
                    macd_analysis['strength'] = 'Strong Bullish'
                elif macd > signal:
                    macd_analysis['strength'] = 'Bullish'
                elif macd < signal and macd < 0:
                    macd_analysis['strength'] = 'Strong Bearish'
                else:
                    macd_analysis['strength'] = 'Bearish'
            
            # 3. Gap detection
            gap_analysis = {'has_gap': False, 'type': None, 'percentage': 0.0, 'gap_amount': 0.0}
            if len(df) >= 2:
                prev_close = float(df['Close'].iloc[-2])
                curr_open = float(df['Open'].iloc[-1])
                gap_pct = ((curr_open - prev_close) / prev_close) * 100
                gap_amount = curr_open - prev_close
                
                if abs(gap_pct) > 1:
                    gap_analysis['has_gap'] = True
                    gap_analysis['type'] = 'gap_up' if gap_pct > 0 else 'gap_down'
                    gap_analysis['percentage'] = round(abs(gap_pct), 2)
                    gap_analysis['gap_amount'] = round(gap_amount, 2)
                    gap_analysis['prev_close'] = round(prev_close, 2)
                    gap_analysis['curr_open'] = round(curr_open, 2)
            
            # 4. Support and resistance levels
            recent_highs = df['High'].tail(20)
            recent_lows = df['Low'].tail(20)
            
            resistance_levels = []
            support_levels = []
            
            # Find local highs (resistance)
            for i in range(2, len(df)-2):
                if float(df['High'].iloc[i]) > float(df['High'].iloc[i-1]) and \
                   float(df['High'].iloc[i]) > float(df['High'].iloc[i+1]):
                    resistance_levels.append(float(df['High'].iloc[i]))
            
            # Find local lows (support)
            for i in range(2, len(df)-2):
                if float(df['Low'].iloc[i]) < float(df['Low'].iloc[i-1]) and \
                   float(df['Low'].iloc[i]) < float(df['Low'].iloc[i+1]):
                    support_levels.append(float(df['Low'].iloc[i]))
            
            # Get nearest resistance above current price
            nearest_resistance = current_price
            for res in sorted(resistance_levels):
                if res > current_price:
                    nearest_resistance = res
                    break
            if nearest_resistance == current_price:
                nearest_resistance = float(recent_highs.max())
            
            # Get nearest support below current price
            nearest_support = current_price
            for sup in sorted(support_levels, reverse=True):
                if sup < current_price:
                    nearest_support = sup
                    break
            if nearest_support == current_price:
                nearest_support = float(recent_lows.min())
            
            # 5. Distance calculations
            dist_to_resistance = ((nearest_resistance - current_price) / current_price) * 100
            dist_to_support = ((current_price - nearest_support) / current_price) * 100
            
            # Last 3 closes with dates
            last_3_data = []
            for i in range(3):
                idx = len(df) - 3 + i
                if idx >= 0:
                    last_3_data.append({
                        'date': df.index[idx].strftime('%Y-%m-%d'),
                        'close': round(float(df['Close'].iloc[idx]), 2),
                        'change': round(float(df['Close'].iloc[idx]) - float(df['Open'].iloc[idx]), 2) if pd.notna(df['Open'].iloc[idx]) else 0.0
                    })
            
            highlights = {
                'current_price': round(current_price, 2),
                'consecutive_days': {
                    'increasing_3': three_days_increasing,
                    'trend': 'Uptrend' if three_days_increasing else 'No Uptrend'
                },
                'macd': macd_analysis,
                'gap': gap_analysis,
                'resistance_support': {
                    'nearest_resistance': round(nearest_resistance, 2),
                    'nearest_support': round(nearest_support, 2),
                    'all_resistances': [round(r, 2) for r in sorted(set(resistance_levels))[-5:]],
                    'all_supports': [round(s, 2) for s in sorted(set(support_levels))[:5]]
                },
                'distances': {
                    'to_resistance_pct': round(dist_to_resistance, 2),
                    'to_support_pct': round(dist_to_support, 2),
                    'to_resistance_amount': round(nearest_resistance - current_price, 2),
                    'to_support_amount': round(current_price - nearest_support, 2)
                },
                'last_3_days': last_3_data,
                'overall_status': self._get_overall_status(three_days_increasing, macd_analysis, gap_analysis)
            }
            
            return highlights
        except Exception as e:
            logger.error(f"Error getting chart highlights for {ticker}: {e}")
            return None
    
    def _get_overall_status(self, three_days, macd, gap):
        """Calculate overall market status."""
        score = 0
        reasons = []
        
        if three_days:
            score += 2
            reasons.append('3-Day Uptrend')
        
        if macd.get('rising'):
            score += 2
            reasons.append('MACD Rising')
        elif macd.get('falling'):
            score -= 1
        
        if gap.get('type') == 'gap_up':
            score += 2
            reasons.append('Gap Up')
        elif gap.get('type') == 'gap_down':
            score -= 2
            reasons.append('Gap Down')
        
        if score >= 4:
            return {'status': 'Strong Bullish', 'score': int(score), 'reasons': reasons}
        elif score >= 2:
            return {'status': 'Bullish', 'score': int(score), 'reasons': reasons}
        elif score <= -2:
            return {'status': 'Bearish', 'score': int(score), 'reasons': reasons}
        else:
            return {'status': 'Neutral', 'score': int(score), 'reasons': reasons}
    
    def get_technicals_analysis(self, ticker: str) -> Optional[Dict]:
        """Get technical analysis with moving averages and support/resistance."""
        try:
            df = self.data_source.get_historical_data(ticker, period='1y')
            
            if df is None or df.empty:
                return None
            
            current_price = float(df['Close'].iloc[-1])
            
            # Get latest moving averages
            ma10 = float(df['MA10'].iloc[-1]) if pd.notna(df['MA10'].iloc[-1]) else None
            ma20 = float(df['MA20'].iloc[-1]) if pd.notna(df['MA20'].iloc[-1]) else None
            ma50 = float(df['MA50'].iloc[-1]) if pd.notna(df['MA50'].iloc[-1]) else None
            ma200 = float(df['MA200'].iloc[-1]) if pd.notna(df['MA200'].iloc[-1]) else None
            
            # Determine price position relative to MAs
            price_vs_mas = {
                'vs_ma10': 'above' if current_price > ma10 else 'below' if ma10 else 'N/A',
                'vs_ma20': 'above' if current_price > ma20 else 'below' if ma20 else 'N/A',
                'vs_ma50': 'above' if current_price > ma50 else 'below' if ma50 else 'N/A',
                'vs_ma200': 'above' if current_price > ma200 else 'below' if ma200 else 'N/A',
            }
            
            # Calculate support and resistance levels
            high_52w = df['Close'].tail(252).max()
            low_52w = df['Close'].tail(252).min()
            high_20d = df['Close'].tail(20).max()
            low_20d = df['Close'].tail(20).min()
            
            # Pivot points (simple calculation)
            yesterday_high = float(df['High'].iloc[-2]) if len(df) > 1 else 0
            yesterday_low = float(df['Low'].iloc[-2]) if len(df) > 1 else 0
            yesterday_close = float(df['Close'].iloc[-2]) if len(df) > 1 else 0
            
            pivot = (yesterday_high + yesterday_low + yesterday_close) / 3
            r1 = (2 * pivot) - yesterday_low
            s1 = (2 * pivot) - yesterday_high
            
            technicals = {
                'current_price': round(current_price, 2),
                'moving_averages': {
                    'ma10': round(ma10, 2) if ma10 else None,
                    'ma20': round(ma20, 2) if ma20 else None,
                    'ma50': round(ma50, 2) if ma50 else None,
                    'ma200': round(ma200, 2) if ma200 else None,
                },
                'price_vs_mas': price_vs_mas,
                'resistance_levels': {
                    '20d_high': round(float(high_20d), 2),
                    '52w_high': round(float(high_52w), 2),
                    'r1_pivot': round(r1, 2),
                },
                'support_levels': {
                    '20d_low': round(float(low_20d), 2),
                    '52w_low': round(float(low_52w), 2),
                    's1_pivot': round(s1, 2),
                },
            }
            
            return technicals
        except Exception as e:
            logger.error(f"Error getting technicals for {ticker}: {e}")
            return None
    
    def get_catalyst_events(self, ticker: str) -> Optional[Dict]:
        """Get upcoming catalyst events and market sentiment."""
        try:
            # Get stock info for sentiment
            stock_info = self.data_source.get_stock_info(ticker)
            
            # Get earnings dates as catalyst events
            earnings_dates = self.data_source.get_earnings_dates(ticker)
            
            # Get recent price action for sentiment
            df = self.data_source.get_historical_data(ticker, period='3mo')
            
            # Determine market sentiment
            sentiment = 'NEUTRAL'
            if df is not None and not df.empty:
                recent_closes = df['Close'].tail(20)
                high = recent_closes.max()
                low = recent_closes.min()
                current = recent_closes.iloc[-1]
                
                # Simple sentiment: if price in upper half of 20-day range = bullish
                mid_point = (high + low) / 2
                if current > mid_point:
                    sentiment = 'BULLISH'
                else:
                    sentiment = 'BEARISH'
            
            # Sample catalyst events (in production, fetch from earnings calendar)
            catalyst_events = []
            
            # Add earnings as catalysts
            for earning in earnings_dates:
                catalyst_events.append({
                    'date': earning['date'],
                    'event': 'Earnings Report',
                    'type': 'earnings',
                    'impact': 'High',
                })
            
            # Add dividend dates (if applicable)
            if stock_info and stock_info.get('dividend_yield', 0) > 0:
                next_dividend = datetime.now() + timedelta(days=90)
                catalyst_events.append({
                    'date': next_dividend.strftime('%Y-%m-%d'),
                    'event': 'Dividend Payment',
                    'type': 'dividend',
                    'impact': 'Medium',
                })
            
            catalysts = {
                'market_sentiment': sentiment,
                'catalyst_events': catalyst_events[:10],  # Top 10 events
                'industry': stock_info.get('industry', '') if stock_info else '',
                'sector': stock_info.get('sector', '') if stock_info else '',
            }
            
            return catalysts
        except Exception as e:
            logger.error(f"Error getting catalysts for {ticker}: {e}")
            return None
