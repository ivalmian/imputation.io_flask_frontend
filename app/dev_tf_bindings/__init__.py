'''
app.dev_tf_bindings.__init__
-------------------
Dev TF bindings, shoulhd only be used in local testing
'''

from app import app, binaries_dict

#check that we are in dev, raise exception otherwise
if app.config['FLASK_ENV'] != 'dev': #pragma: no cover
    raise ValueError(f"Members of app.dev_env can only be called if "
                     "app.config['FLASK_ENV']=='dev', instead it is {app.config['FLASK_ENV']}")

#don't use GPU
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

#load python tf stuff
from app.dev_tf_bindings import tf_model
import tensorflow as tf

#this is a tf 1.x syntax. TODO: Move this to tf2.x
graph = tf.Graph()
with graph.as_default():
    session =  tf.compat.v1.keras.backend.get_session()
    mdl = tf_model.full_model(seq_len=11,
                              vocab_size=len(binaries_dict['val2ind']),
                              num_layers=4)

    mdl.load_weights(filepath=app.config['SAVED_MODEL_PATH'])
