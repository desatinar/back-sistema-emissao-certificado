from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

db = SQLAlchemy()

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    CORS(app)

    with app.app_context():
        db.create_all()
        print("Banco de dados inicializado")

    @app.route("/ping")
    def ping():
        return "pong!"
    
    return app