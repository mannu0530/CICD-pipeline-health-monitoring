#!/usr/bin/env python3
"""
CI/CD Pipeline Health Dashboard - Main Application
"""

import os
import logging
from flask import Flask
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def create_app():
    """Create and configure Flask application"""

    # Import here to avoid circular imports
    from app import create_app as create_flask_app

    # Get configuration from environment
    config_name = os.environ.get('FLASK_ENV', 'development')

    # Create Flask app
    app = create_flask_app(config_name)
    
    # Initialize database
    from utils.database import init_database
    
    mongodb_uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/cicd_dashboard')
    mongodb_db = os.environ.get('MONGODB_DB', 'cicd_dashboard')
    
    if init_database(mongodb_uri, mongodb_db):
        logger.info("Database initialized successfully")
    else:
        logger.error("Failed to initialize database")
    
    return app

def main():
    """Main application entry point"""
    
    app = create_app()
    
    # Get configuration
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    
    logger.info(f"Starting CI/CD Dashboard on {host}:{port}")
    logger.info(f"Debug mode: {debug}")
    
    # Run application
    app.run(
        host=host,
        port=port,
        debug=debug,
        use_reloader=debug
    )

if __name__ == '__main__':
    main()
