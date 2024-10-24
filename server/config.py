import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://root:ragu 16-10-2004@localhost/admin_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
