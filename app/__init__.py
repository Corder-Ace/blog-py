from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # # 捕获上下文异常
    # with app.app_context():
    #     db.init_app(app)
    #     db.create_all()
    return app

