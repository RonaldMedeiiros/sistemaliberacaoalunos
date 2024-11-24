import base64
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

# Registrar o filtro b64encode
    @app.template_filter('b64encode')
    def b64encode_filter(data):
        if data:
            return base64.b64encode(data).decode('utf-8')
        return None

    with app.app_context():
        from . import models
        db.create_all()

        # Importando e registrando o blueprint
        from .routes import bp
        app.register_blueprint(bp)

    return app
