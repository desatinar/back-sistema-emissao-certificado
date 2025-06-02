from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    allowed_origins = [
        "http://localhost:5173",
        "https://desatinar.pythonanywhere.com",
        "https://emissao-certificados.netlify.app"
    ]

    db.init_app(app)

    CORS(
        app, 
        origins=allowed_origins,
        supports_credentials=True,
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"]
    )

    from app.models.user import User
    from app.models.course import Course
    from app.models.student import Student
    from app.models.certificate import Certificate

    from .routes.admin_routes import admin_bp
    from .routes.auth_routes import auth_bp
    from .routes.public_routes import public_bp

    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(public_bp, url_prefix="/api/public")

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        return response

    with app.app_context():
        db.create_all()
        print("Tabelas inicializadas!")

    @app.route("/ping")
    def ping():
        return "pong!"

    @app.route('/debug-cors', methods=['GET', 'OPTIONS'])
    def debug_cors():
        origin = request.headers.get('Origin')
        return {
            'received_origin': origin,
            'allowed_origins': allowed_origins,
            'access_control_allow_origin': response.headers.get('Access-Control-Allow-Origin') if 'response' in locals() else None
        }, 200
    
    return app