"""Flask routes for the Stock Dashboard application."""
from flask import Blueprint, render_template, jsonify, request, current_app
from app.data_sources.yahoo_finance import YahooFinanceDataSource
from app.data_sources.nasdaq_tickers import NasdaqTickerManager
from app.services.analysis_service import AnalysisService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Create blueprints
main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)

# Initialize data sources
yahoo_finance = YahooFinanceDataSource()
nasdaq_manager = NasdaqTickerManager()
analysis_service = AnalysisService(yahoo_finance)


@main_bp.route('/')
def index():
    """Home page - redirect to fundamentals."""
    return render_template('index.html')


@main_bp.route('/fundamentals')
def fundamentals():
    """Stock Fundamentals page."""
    return render_template('pages/fundamentals.html')


@main_bp.route('/chart')
def chart():
    """Candle Chart View page."""
    return render_template('pages/chart.html')


@main_bp.route('/highlights')
def highlights():
    """Chart Highlights page."""
    return render_template('pages/highlights.html')


@main_bp.route('/technicals')
def technicals():
    """Technicals Analysis page."""
    return render_template('pages/technicals.html')


@main_bp.route('/whale-action')
def whale_action():
    """Whale Action / Options page."""
    return render_template('pages/whale_action.html')


@main_bp.route('/catalysts')
def catalysts():
    """Catalyst Events page."""
    return render_template('pages/catalysts.html')


# API Routes

@api_bp.route('/validate-ticker/<ticker>', methods=['GET'])
def validate_ticker(ticker):
    """Validate if ticker is NASDAQ listed."""
    try:
        is_valid = nasdaq_manager.validate_ticker(ticker)
        
        if is_valid:
            company_info = nasdaq_manager.get_company_info(ticker)
            return jsonify({
                'valid': True,
                'ticker': ticker.upper(),
                'company_name': company_info.get('name', '') if company_info else ''
            })
        else:
            return jsonify({'valid': False, 'error': 'Ticker not found on NASDAQ'}), 404
    except Exception as e:
        logger.error(f"Error validating ticker {ticker}: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/search-tickers', methods=['GET'])
def search_tickers():
    """Search for NASDAQ tickers."""
    query = request.args.get('q', '').strip()
    
    if not query or len(query) < 1:
        return jsonify({'results': []})
    
    try:
        results = nasdaq_manager.search_tickers(query)
        return jsonify({'results': results})
    except Exception as e:
        logger.error(f"Error searching tickers: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/stock/<ticker>/fundamentals', methods=['GET'])
def get_fundamentals(ticker):
    """Get stock fundamental data."""
    try:
        ticker = ticker.upper()
        
        # Validate ticker
        if not nasdaq_manager.validate_ticker(ticker):
            return jsonify({'error': 'Invalid NASDAQ ticker'}), 400
        
        # Get stock info
        stock_info = yahoo_finance.get_stock_info(ticker)
        if not stock_info:
            return jsonify({'error': 'Unable to fetch stock information'}), 500
        
        # Get last trading date and LTP
        last_trading_date = yahoo_finance.get_last_trading_date(ticker)
        ltp_price = yahoo_finance.get_ltp_price(ticker)
        
        # Get earnings data
        earnings_dates = yahoo_finance.get_earnings_dates(ticker)
        
        # Analyze earnings impact
        earnings_analysis = analysis_service.analyze_earnings_impact(ticker)
        
        fundamentals = {
            **stock_info,
            'current_date': datetime.now().strftime('%Y-%m-%d'),
            'last_trading_date': last_trading_date,
            'ltp_price': ltp_price,
            'earnings_dates': earnings_dates,
            'earnings_analysis': earnings_analysis,
        }
        
        return jsonify(fundamentals)
    except Exception as e:
        logger.error(f"Error fetching fundamentals for {ticker}: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/stock/<ticker>/historical', methods=['GET'])
def get_historical_data(ticker):
    """Get historical price data with technical indicators."""
    try:
        ticker = ticker.upper()
        period = request.args.get('period', '1y')
        
        if not nasdaq_manager.validate_ticker(ticker):
            return jsonify({'error': 'Invalid NASDAQ ticker'}), 400
        
        df = yahoo_finance.get_historical_data(ticker, period=period)
        if df is None or df.empty:
            return jsonify({'error': 'No historical data available'}), 500
        
        # Convert to list of dicts for JSON serialization
        data = []
        for index, row in df.iterrows():
            data.append({
                'date': index.strftime('%Y-%m-%d'),
                'open': float(row['Open']) if not pd.isna(row['Open']) else None,
                'high': float(row['High']) if not pd.isna(row['High']) else None,
                'low': float(row['Low']) if not pd.isna(row['Low']) else None,
                'close': float(row['Close']) if not pd.isna(row['Close']) else None,
                'volume': int(row['Volume']) if not pd.isna(row['Volume']) else 0,
                'ma10': float(row['MA10']) if not pd.isna(row['MA10']) else None,
                'ma20': float(row['MA20']) if not pd.isna(row['MA20']) else None,
                'ma50': float(row['MA50']) if not pd.isna(row['MA50']) else None,
                'ma200': float(row['MA200']) if not pd.isna(row['MA200']) else None,
                'macd': float(row['MACD']) if not pd.isna(row['MACD']) else None,
                'signal': float(row['Signal']) if not pd.isna(row['Signal']) else None,
                'macd_histogram': float(row['MACD_Histogram']) if not pd.isna(row['MACD_Histogram']) else None,
            })
        
        return jsonify({'data': data})
    except Exception as e:
        logger.error(f"Error fetching historical data for {ticker}: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/stock/<ticker>/chart-highlights', methods=['GET'])
def get_chart_highlights(ticker):
    """Get chart highlights and key findings."""
    try:
        ticker = ticker.upper()
        
        if not nasdaq_manager.validate_ticker(ticker):
            return jsonify({'error': 'Invalid NASDAQ ticker'}), 400
        
        highlights = analysis_service.get_chart_highlights(ticker)
        
        return jsonify(highlights)
    except Exception as e:
        logger.error(f"Error getting chart highlights for {ticker}: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/stock/<ticker>/technicals', methods=['GET'])
def get_technicals(ticker):
    """Get technical analysis data."""
    try:
        ticker = ticker.upper()
        
        if not nasdaq_manager.validate_ticker(ticker):
            return jsonify({'error': 'Invalid NASDAQ ticker'}), 400
        
        technicals = analysis_service.get_technicals_analysis(ticker)
        
        return jsonify(technicals)
    except Exception as e:
        logger.error(f"Error getting technicals for {ticker}: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/stock/<ticker>/options', methods=['GET'])
def get_options(ticker):
    """Get options data."""
    try:
        ticker = ticker.upper()
        
        if not nasdaq_manager.validate_ticker(ticker):
            return jsonify({'error': 'Invalid NASDAQ ticker'}), 400
        
        options_data = yahoo_finance.get_option_chain(ticker)
        
        if not options_data:
            return jsonify({'error': 'No options data available'}), 404
        
        return jsonify(options_data)
    except Exception as e:
        logger.error(f"Error getting options for {ticker}: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/stock/<ticker>/whale-action', methods=['GET'])
def get_whale_action(ticker):
    """Get whale action and insider trading data."""
    try:
        ticker = ticker.upper()
        
        if not nasdaq_manager.validate_ticker(ticker):
            return jsonify({'error': 'Invalid NASDAQ ticker'}), 400
        
        institutional_holders = yahoo_finance.get_institutional_holdings(ticker)
        insider_transactions = yahoo_finance.get_insider_transactions(ticker)
        
        # Get options for calls/puts volume
        options_data = yahoo_finance.get_option_chain(ticker)
        
        whale_data = {
            'institutional_holders': institutional_holders or [],
            'insider_transactions': insider_transactions or [],
            'options_data': options_data or {},
        }
        
        return jsonify(whale_data)
    except Exception as e:
        logger.error(f"Error getting whale action for {ticker}: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/stock/<ticker>/catalysts', methods=['GET'])
def get_catalysts(ticker):
    """Get catalyst events and market sentiment."""
    try:
        ticker = ticker.upper()
        
        if not nasdaq_manager.validate_ticker(ticker):
            return jsonify({'error': 'Invalid NASDAQ ticker'}), 400
        
        catalysts = analysis_service.get_catalyst_events(ticker)
        
        return jsonify(catalysts)
    except Exception as e:
        logger.error(f"Error getting catalysts for {ticker}: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/stock/<ticker>/chart-url', methods=['GET'])
def get_chart_url(ticker):
    """Get TradingView chart URL for embedding."""
    try:
        ticker = ticker.upper()
        
        if not nasdaq_manager.validate_ticker(ticker):
            return jsonify({'error': 'Invalid NASDAQ ticker'}), 400
        
        chart_data = {
            'chart_url': f"https://www.tradingview.com/chart/?symbol=NASDAQ:{ticker}",
            'embed_url': f"https://www.tradingview.com/widgetembed/?symbol=NASDAQ:{ticker}",
            'ticker': ticker,
        }
        
        return jsonify(chart_data)
    except Exception as e:
        logger.error(f"Error getting chart URL for {ticker}: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


# Import pandas for type checking
import pandas as pd
