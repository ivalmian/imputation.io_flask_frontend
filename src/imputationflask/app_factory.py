'''
imputationflask.app_factory
-------------------
Provides methods for building the app
'''

from flask import Flask
from werkzeug.exceptions import HTTPException
from collections import namedtuple

# we store some objects across requests TODO: reconsider this?
PersistentObjects = namedtuple(
    'PersistentObjects', ['binaries_dict', 'predictor', 'census_form'])


def application(name=__name__):

    from imputationflask import secrets
    from imputationflask.views import frontend, handle_error

    # The app is born
    app = Flask(name, instance_relative_config=True)
    app.config.from_object('imputationflask.config')  # prod config

    app.config['SECRET_KEY'] = secrets.csrf_key(app.config)

    try:
        app.config.from_pyfile('config.py')  # dev config overrides prod
        # should never have instance.config in prod
        assert app.config['ENV'] != 'prod'
    except FileNotFoundError:  # pragma: no cover
        pass

    # db connection, currently only in dev
    if app.config['ENV'] == 'dev':
        from imputationflask.model import db
        db.init_app(app)

    app.persistent = PersistentObjects(*load_persistent(app.config))

    app.register_blueprint(frontend)
    app.register_error_handler(HTTPException, handle_error)

    return app


def load_persistent(config):

    # have no dependency on app
    from imputationflask import make_prediction, data_dictionary, load_binaries, forms

    # load data
    binaries_dict = load_binaries.load_binaries(config)
    # initialize predictors
    clf = make_prediction.Predict(config, binaries_dict)
    predictor = make_prediction.MakePrediction(
        clf, data_dictionary.data_dict, binaries_dict)
    # form object
    census_form = forms.CensusImputeForm(data_dict=data_dictionary.data_dict,
                                         numeric_fields=binaries_dict['numeric_mappers'].keys(
                                         ),
                                         recordname2description=binaries_dict['recordname2description'])

    return binaries_dict, predictor, census_form
