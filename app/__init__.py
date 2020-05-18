from app.load_binaries import load_binaries
from app.version import __version__
from app import make_prediction

from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')

try:
    app.config.from_pyfile('config.py')
except FileNotFoundError:
    pass


binaries_dict = load_binaries(app)

# setting up tf model in development, for production we call out to a model serving API
if app.config['FLASK_ENV'] == 'dev':
    import os

    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    import tensorflow as tf
    from app import tf_model

    graph = tf.Graph()
    with graph.as_default():
        session = tf.keras.backend.get_session()
        mdl = tf_model.full_model(seq_len=11,
                                  vocab_size=len(binaries_dict['val2ind']),
                                  num_layers=4)

        mdl.load_weights(filepath=app.config['SAVED_MODEL_PATH'])

clf = make_prediction.Predict(app, binaries_dict)

from app import views
