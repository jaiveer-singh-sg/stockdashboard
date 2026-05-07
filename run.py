#!/usr/bin/env python
"""
Stock Dashboard Application Entry Point
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create and run Flask app
if __name__ == '__main__':
    from app import create_app
    
    # Get configuration from environment
    config_name = os.getenv('FLASK_ENV', 'development')
    debug = config_name == 'development'
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    # Create app
    app = create_app(config_name)
    
    # Run development server
    print(f"Starting Stock Dashboard on {host}:{port}")
    print(f"Environment: {config_name}")
    print(f"Debug mode: {debug}")
    print(f"Open http://localhost:{port} in your browser")
    
    app.run(
        host=host,
        port=port,
        debug=debug,
        use_reloader=debug,
        threaded=True
    )
