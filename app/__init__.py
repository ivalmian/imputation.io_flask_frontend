'''
app.__init__
-------------------
Author: Ilya Valmianski
Email: ivalmian@gmail.com
-------------------

Front end for imputation.io using Flask
'''

from flask import Flask

from app.version import __version__

# These imports are used during initialization
from app import make_prediction, data_dictionary, load_binaries, forms

# The app is born
app = Flask(__name__, instance_relative_config=True)

# Load config
# TODO: should be loading from google secret storage if in prod, in dev secrets are in instance/config.py

app.config.from_object('config') #prod config

try:
    app.config.from_pyfile('config.py') #dev config overrides prod
    assert app.config['FLASK_ENV']!='prod' #should never have instance.config in prod
except FileNotFoundError: #pragma: no cover
    pass

# Run initialization , TODO: is __init__ really the place to run heavy initializations?
binaries_dict = load_binaries.load_binaries(app.config)
clf = make_prediction.Predict(app.config, binaries_dict)
predictor = make_prediction.MakePrediction(clf, data_dictionary.data_dict, binaries_dict)
census_form = forms.CensusImputeForm(data_dict=data_dictionary.data_dict,
                                      numeric_fields=binaries_dict['numeric_mappers'].keys(),
                                      recordname2description=binaries_dict['recordname2description'])

#circular import of views, TODO: could this be improved?
from app import views
