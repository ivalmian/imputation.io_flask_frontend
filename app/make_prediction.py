'''
app.make_prediction
-------------------
Create a predictor. In dev use local tf bindings, in prod use google api
'''

import numpy as np
from app.utils import single_get_closest_value, timenlog, rem_duplicates, smooth


class Predict():

    def __init__(self, config, binaries_dict):
        self.predictor = self._build_predictor(config)
        self.binaries_dict = binaries_dict
        return

    # builds self.predictor based on this being a dev or prod env
    def _build_predictor(self, config):
        assert config['FLASK_ENV'] == 'dev' or config['FLASK_ENV'] == 'prod'

        if config['FLASK_ENV'] == 'dev':
            
            from app.dev_tf_bindings import tf, graph, mdl, session

            @timenlog
            def predictor(inp_vec):
                inp_vec = np.expand_dims(inp_vec, axis=0)
                with graph.as_default():
                    tf.compat.v1.keras.backend.set_session(session)
                    pred = mdl.predict(inp_vec)
                return pred

        elif config['FLASK_ENV'] == 'prod': #pragma: no cover

            from googleapiclient.discovery import build

            service = build('ml', 'v1')
            name = f"projects/{config['PROJECT']}/models/{config['TF_MODEL']}"

            @timenlog
            def predictor(inp_vec):
                instances = [{'input': inp_vec.astype(int).tolist()}]

                pred = service.projects().predict(
                    name=name,
                    body={'instances': instances}
                ).execute()
                pred = np.expand_dims(
                    np.array(pred['predictions'][0]['output']), axis=0)
                return pred
        else: 
            raise ValueError(
                f"Improper call to _build_predictor with env set to {config['FLASK_ENV']}")

        return predictor

    def predict(self, data):
        '''
        Maps form data into predictions for masked/empty data elements
        Args
        ---
        data: dict
            Form data. See form made by .forms.CensusImputeForm
        
        Returns
        ---
        pred: np.ndarray[float]
            Predicted probability distirbution for each key in all_keys. The ones that are
            inferred are selected by mask `inferred`. Data to generate pred is in `pred_vector`
        inferred: np.ndarray[bool]
            Binary mask of inferred elements (the ones for whom prediction is meaningful)
        all_keys List[str]
            Data keys for which either data or prediction is possible 
        pred_vector: List[int]
            Mostly for debug purpose, this is what is passed to Predict.predictor which returns pred
        '''
        pred_vector = list()
        all_keys = list()
        for key, mapper in self.binaries_dict['numeric_mappers'].items():
            all_keys.append(key)
            if data.get('mask_'+key, 'n') == 'y' or not str(data[key]).isnumeric():
                pred_vector.append(0)
            else:
                val = single_get_closest_value(
                    float(data[key]), self.binaries_dict['numeric_mappers'][key]['forward'])
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



class MakePrediction():

    def __init__(self, clf, data_dict, binaries_dict):
        self.clf = clf
        self.data_dict = data_dict
        self.binaries_dict = binaries_dict
        
    def __call__(self, form_data):

        pred, inferred, all_keys, _ = self.clf.predict(form_data)
        pred_description = dict()

        for inferred_ind in inferred:
            key = all_keys[inferred_ind]
            ind2val = {i: (t[0],
                           (self.data_dict[t[0]].get(t[1], t[1])
                            if t[0] in self.data_dict else t[1]))
                       for t, i in self.binaries_dict['val2ind'].items() if t[0] == key}
            x, y = zip(*[(pred_desc[1], pred[0, inferred_ind, ind])
                         for ind, pred_desc in ind2val.items()])

            y = list(np.array(y) / sum(y))
            x = list(x)
            if key in self.binaries_dict['numeric_mappers'].keys():

                x = [single_get_closest_value(e, self.binaries_dict['numeric_mappers'][key]['backward'])
                     if isinstance(e, int) else e for e in x]

                x, y = zip(*sorted(rem_duplicates(zip(x, y)),
                                   key=lambda t: t[0] if isinstance(t[0], int) else -1))

                x = np.asarray(x)
                mid_w = np.zeros(len(x))
                mid_w[0] = x[1]-x[0]
                mid_w[-1] = (x[-1]-x[-2])
                mid_w[1:-1] = (x[2:] - x[:-2])/2
                y = y/mid_w

                y = smooth(x, y)
            pred_description[key] = {'x': x, 'y': list(y)}

        return pred_description
