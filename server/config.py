import os

class Config:
    # Fetch the DATABASE_URL environment variable or use the default MySQL connection string.
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://root:santhosh090405@localhost/admin_db')
    
    # Disables Flask-SQLAlchemy's event system which unnecessarily tracks modifications.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
