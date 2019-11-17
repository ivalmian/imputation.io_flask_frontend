from inference_demo.version import __version__

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from flask import Flask

import tensorflow as tf
from inference_demo import tf_model

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

from inference_demo.load_binaries import load_binaries


_, dict_binaries = load_binaries(app)


with tf.device('/device:cpu:0'):
    graph = tf.Graph()
    with graph.as_default():
        session = tf.keras.backend.get_session()
        mdl = tf_model.full_model(seq_len=11,
                                  vocab_size=len(dict_binaries['val2ind']),
                                  num_layers=4)

        mdl.load_weights(filepath=app.config['SAVED_MODEL_PATH'])

tf_binaries = {'mdl': mdl, 'graph': graph}

from inference_demo import views
