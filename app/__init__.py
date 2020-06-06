from app.load_binaries import load_binaries
from app.version import __version__
from app import make_prediction

from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')

try:
    app.config.from_pyfile('config.py')
except FileNotFoundError: #pragma: no cover
    pass


binaries_dict = load_binaries(app)

clf = make_prediction.Predict(app, binaries_dict)

from app import views
