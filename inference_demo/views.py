# imports from our package
from inference_demo import app, data_dictionary, binaries_dict, make_prediction
from inference_demo.forms import CensusImputeForm

# external imports
from flask import render_template, request  # , jsonify
from werkzeug.exceptions import HTTPException
import numpy as np


@app.route('/')
@app.route('/web_app', methods=["GET", "POST"])
def web_app():

    form = CensusImputeForm.make_form(data_dict=data_dictionary.data_dict,
                                      numeric_fields=binaries_dict['numeric_mappers'].keys(),
                                      recordname2description=binaries_dict['recordname2description'],
                                      request_form=request.form)

    pred_description = None

    if request.method == 'POST':
        pred, inferred, all_keys = make_prediction.predict(request.form)
        pred_description = dict()

        for inferred_ind in inferred:
            key = all_keys[inferred_ind]
            ind2val = {i: (t[0],
                           (data_dictionary.data_dict[t[0]].get(t[1], t[1])
                            if t[0] in data_dictionary.data_dict else t[1]))
                       for t, i in binaries_dict['val2ind'].items() if t[0] == key}
            x, y = zip(*[(pred_desc[1], pred[0, inferred_ind, ind])
                         for ind, pred_desc in ind2val.items()])
            y = np.array(y) / sum(y)
            pred_description[key] = {'x': list(x), 'y': list(y)}

    return render_template('webapp.html',
                           form=form,
                           pred_description=pred_description,
                           description_dict=binaries_dict['recordname2description'])


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


@app.route('/how_it_works')
def how_it_works():
    return render_template('under_construction.html')


@app.route('/about_api')
def about_api():
    return render_template('under_construction.html')


@app.errorhandler(404)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return render_template('error.html', error_code=code)
