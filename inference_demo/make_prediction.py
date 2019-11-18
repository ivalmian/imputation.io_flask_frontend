from inference_demo import binaries_dict, graph, mdl, session
import numpy as np

import tensorflow as tf


def predict(form_data):

    pred_vector = list()
    all_keys = list()
    for key, mapper in binaries_dict['numeric_mappers'].items():
        all_keys.append(key)
        if form_data.get('mask_'+key, 'n') == 'y':
            pred_vector.append(0)
        else:

            pred_vector.append(
                binaries_dict['val2ind'].get((key,
                                              int(form_data[key])),
                                             0))

    for key in binaries_dict['recordname2description'].keys():
        if key in form_data and key not in all_keys:
            all_keys.append(key)
            if form_data.get('mask_'+key, 'n') == 'y':
                pred_vector.append(0)
            else:
                pred_vector.append(
                    binaries_dict['val2ind'].get((key,
                                                  int(form_data[key])),
                                                 0))

    pred_vector = np.array(pred_vector)

    inferred = np.argwhere(pred_vector==0)
    out = np.expand_dims(pred_vector, axis=0)

    with graph.as_default():
        tf.keras.backend.set_session(session)
        pred = mdl.predict(out)
    return pred, inferred.flatten(), all_keys
