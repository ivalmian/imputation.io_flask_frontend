# config.py global config

DEBUG = False  # Turns on debugging features in Flask

import os
SECRET_KEY = os.urandom(32)
FLASK_ENV = "prod"
