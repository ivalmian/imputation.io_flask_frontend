import numpy as np

def _single_get_closest_value(num, data):
    return data[num] if num in data else data[min(data.keys(), key=lambda k: abs(k - num))]


class Predict():

    def __init__(self,app,binaries_dict):
        self.predictor = self._build_predictor(app)
        self.binaries_dict = binaries_dict
        return

    #builds self.predictor based on this being a dev or prod env
    def _build_predictor(self,app):
        assert app.config['FLASK_ENV']=='dev' or app.config['FLASK_ENV']=='prod'

        if app.config['FLASK_ENV']=='dev':

            from app import graph, mdl, session
            import tensorflow as tf

            def predictor(inp_vec):
                inp_vec = np.expand_dims(inp_vec, axis=0)
                with graph.as_default():
                    tf.keras.backend.set_session(session)
                    pred = mdl.predict(inp_vec)
                return pred

        elif app.config['FLASK_ENV']=='prod':

            import googleapiclient

            service = googleapiclient.discovery.build('ml', 'v1')
            name = f"projects/{app.config['PROJECT']}/models/{app.config['TF_MODEL']}"

            def predictor(inp_vec):
                instances = [{'input': list(inp_vec)}]

                pred = service.projects().predict(
                    name=name,
                    body={'instances': instances}
                ).execute()
                pred = np.expand_dims(np.array(pred['predictions'][0]['output']), axis=0)
                return pred
        else:
            raise ValueError(f"Improper call to _build_predictor with env set to {app.config['FLASK_ENV']}")

        return predictor

    def predict(self,data):
        pred_vector = list()
        all_keys = list()
        for key, mapper in self.binaries_dict['numeric_mappers'].items():
            all_keys.append(key)
            if data.get('mask_'+key, 'n') == 'y' or not str(data[key]).isnumeric():
                pred_vector.append(0)
            else:
                val = _single_get_closest_value(float(data[key]), self.binaries_dict['numeric_mappers'][key]['forward'])
                pred_vector.append(
                    self.binaries_dict['val2ind'].get((key,
                                                val),
                                                0))

        for key in self.binaries_dict['recordname2description'].keys():
            if key in data and key not in all_keys:
                all_keys.append(key)
                if data.get('mask_'+key, 'n') == 'y':
                    pred_vector.append(0)
                else:
                    pred_vector.append(
                         self.binaries_dict['val2ind'].get((key,
                                                    int(data[key])),
                                                    0))

        pred_vector_np = np.array(pred_vector)
        inferred = np.argwhere(pred_vector_np == 0).flatten()

        pred = self.predictor(pred_vector_np)
        return pred, inferred, all_keys, pred_vector

