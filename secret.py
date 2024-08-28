import secrets

secret_key = secrets.token_hex(16)

SECRET_KEY = secret_key
SQLALCHEMY_DATABASE_URI = 'sqlite:///task-manager.db'
