#!/usr/bin/env python
"""
Stock Dashboard Application Entry Point
"""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
log_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(log_dir, 'app.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Create and run Flask app
if __name__ == '__main__':
    from app import create_app
    
    config_name = os.getenv('FLASK_ENV', 'development')
    debug = config_name == 'development'
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    app = create_app(config_name)
    
    print(f"Starting Stock Dashboard on {host}:{port}")
    print(f"Environment: {config_name}")
    print(f"Debug mode: {debug}")
    print(f"Log file: {log_file}")
    print(f"Open http://localhost:{port} in your browser")
    print("Playwright Protection: Auto-reloader is DISABLED.")    
    
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True, 
        use_reloader=False  # <-- This stops Flask from restarting when Playwright runs
 #       use_reloader=debug,
    )