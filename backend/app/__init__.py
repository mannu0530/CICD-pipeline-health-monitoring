from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from dotenv import load_dotenv
import os

def create_app(config_name='development'):
    """Application factory pattern for Flask app"""
    
    # Load environment variables
    load_dotenv()
    
    app = Flask(__name__)
    
    # Configuration
    from config import config
    app.config.from_object(config.get(config_name, config['default']))
    
    # Initialize extensions
    CORS(app)
    api = Api(app)
    
    # Register blueprints
    from .routes import pipelines, builds, metrics, alerts, webhooks, config
    app.register_blueprint(pipelines.bp)
    app.register_blueprint(builds.bp)
    app.register_blueprint(metrics.bp)
    app.register_blueprint(alerts.bp)
    app.register_blueprint(webhooks.bp)
    app.register_blueprint(config.bp)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'cicd-dashboard'}
    
    return app
