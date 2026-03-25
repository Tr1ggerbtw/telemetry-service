from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from app.db import db, jwt
from app.routes.auth import auth
from app.routes.locations import locations
# from app.routes.sensors import sensors
# from app.routes.telemetry import telemetry

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    jwt.init_app(app)
    
    app.register_blueprint(auth)
    app.register_blueprint(locations)
    # app.register_blueprint(sensors)
    # app.register_blueprint(telemetry)

    return app

