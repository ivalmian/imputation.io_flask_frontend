'''
Author: Ilya Valmianski
Email: ivalmian@gmail.com
-------------------

Front end for imputation.io using Flask
'''

from flask import Flask

from app.version import __version__

# These two imports rely on app.config
from app import make_prediction
from app.load_binaries import load_binaries 


# Load config
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config') #prod config

try:
    app.config.from_pyfile('config.py') #dev config overrides prod
except FileNotFoundError: #pragma: no cover
    pass


binaries_dict = load_binaries(app.config)
clf = make_prediction.Predict(app.config, binaries_dict)

#circular import of views, TODO: could this be improved?
from app import views
