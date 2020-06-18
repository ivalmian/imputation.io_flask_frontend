'''
imputationflask.views
-------------------
Define routes render by flask
'''

# imports from our package
from imputationflask import app, predictor, census_form, binaries_dict
# external imports
from flask import render_template, request  # , jsonify
from werkzeug.exceptions import HTTPException
import numpy as np


@app.route('/')
@app.route('/web_app', methods=["GET", "POST"])
def web_app():

    form = census_form.get_instance(request_form=request.form)

    # we got some data, time to make predictions
    if request.method == 'POST':
        pred_description = predictor(request.form)
    else:
        pred_description = None

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
