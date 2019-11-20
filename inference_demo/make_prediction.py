from inference_demo import app, binaries_dict

import numpy as np


def single_get_closest_value(num, data):
    return data[num] if num in data else data[min(data.keys(), key=lambda k: abs(k - num))]


def predict(form_data):

    pred_vector = list()
    all_keys = list()
    for key, mapper in binaries_dict['numeric_mappers'].items():
        all_keys.append(key)
        if form_data.get('mask_'+key, 'n') == 'y' or not str(form_data[key]).isnumeric():
            pred_vector.append(0)
        else:
            val = single_get_closest_value(float(form_data[key]), binaries_dict['numeric_mappers'][key]['forward'])
            pred_vector.append(
                binaries_dict['val2ind'].get((key,
                                              val),
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

    pred_vector_np = np.array(pred_vector)

    inferred = np.argwhere(pred_vector_np == 0).flatten()
    out = np.expand_dims(pred_vector_np, axis=0)

    pred = None

    if app.config['FLASK_ENV'] == 'dev':
        from inference_demo import graph, mdl, session
        import tensorflow as tf

        with graph.as_default():
            tf.keras.backend.set_session(session)
            pred = mdl.predict(out)

    elif app.config['FLASK_ENV'] == 'prod':
        import googleapiclient

        service = googleapiclient.discovery.build('ml', 'v1')
        name = f"projects/{app.config['PROJECT']}/models/{app.config['TF_MODEL']}"

        instances = [{'input': pred_vector}]

        pred = service.projects().predict(
            name=name,
            body={'instances': instances}
        ).execute()
        pred = np.expand_dims(np.array(pred['predictions'][0]['output']), axis=0)

    return pred, inferred, all_keys, pred_vector
