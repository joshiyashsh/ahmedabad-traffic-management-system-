"""
Main Flask application entry point for ASTMS.
"""

from flask import Flask
from config import Config

# Import modular route registration functions
from routes.auth import register_auth_routes
from routes.dashboard import register_dashboard_routes
from routes.junction import register_junction_routes

# Initialize the Flask application
app = Flask(__name__)

# Load configuration from Config class
app.config.from_object(Config)

# Register routes
register_auth_routes(app)
register_dashboard_routes(app)
register_junction_routes(app)

if __name__ == '__main__':
    # Start the application
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
