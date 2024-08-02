from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:p%40stgress@localhost:5433/flaskdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    MAIL_SERVER = 'localhost'  # Dummy server
    MAIL_PORT = 8025  # Dummy port
    MAIL_USE_TLS = False
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_DEFAULT_SENDER = 'dummy@example.com'
    SWAGGER = {
        'title': 'Your API',
        'uiversion': 3,
        'specs_route': '/swagger/',
        'security': [{"JWT": []}],
        'securityDefinitions': {
            "JWT": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"'
            }
        }
    }