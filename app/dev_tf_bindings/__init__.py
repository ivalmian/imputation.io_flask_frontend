from app.dev_tf_bindings import tf_model
import tensorflow as tf
from app import app, binaries_dict

if app.config['FLASK_ENV'] != 'dev':
    raise ValueError(f"Members of app.dev_env can only be called if "
                     "app.config['FLASK_ENV']=='dev', instead it is {app.config['FLASK_ENV']}")

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

graph = tf.Graph()
with graph.as_default():
    session = tf.keras.backend.get_session()
    mdl = tf_model.full_model(seq_len=11,
                              vocab_size=len(binaries_dict['val2ind']),
                              num_layers=4)

    mdl.load_weights(filepath=app.config['SAVED_MODEL_PATH'])
