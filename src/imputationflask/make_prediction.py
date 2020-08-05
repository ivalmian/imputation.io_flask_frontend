'''
imputationflask.make_prediction
-------------------

Implements two classes

Predict
    Create a predictor. In dev use local tf bindings, in prod use google api

MakePrediction
    Transforms the output of Predict.predict into pred_description that can be rendered

'''

import numpy as np
from imputationflask.utils import single_get_closest_value, timenlog, rem_duplicates, smooth

from googleapiclient.discovery import build


class Predict():

    def __init__(self, config, binaries_dict):
        self.predictor = self._build_predictor(config)
        self.binaries_dict = binaries_dict

        return

    # builds self.predictor based on this being a dev or prod env
    def _build_predictor(self, config):
        assert config['ENV'] == 'dev' or config['ENV'] == 'prod'

        service = build('ml', 'v1')
        name = f"projects/{config['PROJECT_NAME']}/models/{config['TF_MODEL']}"

        @timenlog
        def predictor(inp_vec, pos_vec):
            instances = [{'input': inp_vec.astype(int).tolist(),
                          'input_pos': pos_vec.astype(int).tolist()}]

            print(instances)
            pred = service.projects().predict(  # pylint: disable=no-member
                name=name,
                body={'instances': instances}
            ).execute()
            pred = np.expand_dims(
                np.array(pred['predictions'][0]['output']), axis=0)
            return pred

        return predictor

    def predict(self, data, data_dict):
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
            if data.get('mask_' + key, 'n') == 'y' or not str(data[key]).isnumeric():
                pred_vector.append(0)
            else:
                numeric_entry = float(data[key])
                val = single_get_closest_value(
                    numeric_entry, mapper['forward'])
                full_key = (key, val)
                mapped_value = self.binaries_dict['val2ind'].get(full_key, 0)

                print(f'Attempting to map the following numerical value: {numeric_entry}, '
                      f'precentile mapped key: {full_key}, got the following mapping: {mapped_value}')

                pred_vector.append(mapped_value)

        for key in data_dict.keys():
            if key in data and key not in all_keys:
                all_keys.append(key)
                if data.get('mask_' + key, 'n') == 'y':
                    pred_vector.append(0)
                else:
                    full_key = (key, data_dict[key].get(
                        int(data[key]), 'No Mapping'))
                    mapped_value = self.binaries_dict['val2ind'].get(
                        full_key, 0)
                    print(
                        f'Attempting to map the following categorical key: {full_key}, got the following mapping: {mapped_value}')
                    pred_vector.append(mapped_value)

        pred_vector_np = np.array(pred_vector)
        pos_vector_np = np.arange(len(pred_vector_np))

        inferred = np.argwhere(pred_vector_np == 0).flatten()
        print(all_keys)
        pred = self.predictor(pred_vector_np, pos_vector_np)
        return pred, inferred, all_keys, pred_vector


class MakePrediction():

    def __init__(self, clf, data_dict, binaries_dict):
        self.clf = clf
        self.data_dict = data_dict
        self.binaries_dict = binaries_dict

    # TODO: this was whole-sale taken from view.web_app, but might need to be further refactored
    def __call__(self, form_data):

        pred, inferred, all_keys, _ = self.clf.predict(
            form_data, self.data_dict)
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
                mid_w[0] = x[1] - x[0]
                mid_w[-1] = (x[-1] - x[-2])
                mid_w[1:-1] = (x[2:] - x[:-2]) / 2
                y = y / mid_w

                y = smooth(x, y)
            pred_description[key] = {'x': x, 'y': list(y)}

        return pred_description
