import os

class Config:
    DEBUG = True
    SECRET_KEY = os.urandom(24)
    TEMPLATE_FOLDER = 'templates'  # Specify the path to your HTML templates folder
