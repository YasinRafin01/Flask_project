from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flasgger import Swagger

# Local imports
from config import Config
from models import db
from utils import s
from auth_routes import auth_bp
from user_routes import user_bp
from admin_routes import admin_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)
#mail.init_app(app)
swagger = Swagger(app)

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)