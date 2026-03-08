import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from src.routes.api import api_bp
from src.services.cleanup import start_cleanup_thread

def create_app():
    # Use the absolute path for the static folder (public)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_folder = os.path.join(BASE_DIR, 'public')
    
    app = Flask(__name__, static_folder=static_folder, static_url_path='')
    CORS(app)

    # Register API blueprint
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')
        
    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory(app.static_folder, path)

    # Start cleanup thread if running locally (not ideal for Vercel, but safe to launch)
    start_cleanup_thread()

    return app
