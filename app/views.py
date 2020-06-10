# imports from our package
from app import app, data_dictionary, binaries_dict, clf, census_form
from app.utils import single_get_closest_value, rem_duplicates, smooth
# external imports
from flask import render_template, request  # , jsonify
from werkzeug.exceptions import HTTPException
import numpy as np



@app.route('/')
@app.route('/web_app', methods=["GET", "POST"])
def web_app():

    form = census_form.get_instance(request_form=request.form)

    pred_description = None

    if request.method == 'POST':
        pred, inferred, all_keys, _ = clf.predict(request.form)
        # return str(pred_vector), 200
        pred_description = dict()

        for inferred_ind in inferred:
            key = all_keys[inferred_ind]
            ind2val = {i: (t[0],
                           (data_dictionary.data_dict[t[0]].get(t[1], t[1])
                            if t[0] in data_dictionary.data_dict else t[1]))
                       for t, i in binaries_dict['val2ind'].items() if t[0] == key}
            x, y = zip(*[(pred_desc[1], pred[0, inferred_ind, ind])
                         for ind, pred_desc in ind2val.items()])

            y = list(np.array(y) / sum(y))
            x = list(x)
            if key in binaries_dict['numeric_mappers'].keys():

                x = [single_get_closest_value(e, binaries_dict['numeric_mappers'][key]['backward'])
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

    return render_template('webapp.html',
                           form=form,
                           pred_description=pred_description,
                           description_dict=binaries_dict['recordname2description'],
                           numeric_keys=list(binaries_dict['numeric_mappers'].keys()))


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
    return render_template('error.html', error_code=code), code
