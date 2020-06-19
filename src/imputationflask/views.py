'''
imputationflask.views
-------------------
Define routes render by flask
'''


# external imports
from flask import render_template, request, current_app, Blueprint
from werkzeug.exceptions import HTTPException

frontend = Blueprint('frontend', __name__)


@frontend.route('/')
@frontend.route('/web_app', methods=["GET", "POST"])
def web_app():

    form = current_app.persistent.census_form.get_instance(
        request_form=request.form)

    # we got some data, time to make predictions
    if request.method == 'POST':
        pred_description = current_app.persistent.predictor(request.form)
    else:
        pred_description = None

    return render_template('webapp.html',
                           form=form,
                           pred_description=pred_description,
                           description_dict=current_app.persistent.binaries_dict[
                               'recordname2description'],
                           numeric_keys=list(current_app.persistent.binaries_dict['numeric_mappers'].keys()))


@frontend.route('/privacy')
def privacy():
    return render_template('privacy.html')


@frontend.route('/how_it_works')
def how_it_works():
    return render_template('under_construction.html')


@frontend.route('/about_api')
def about_api():
    return render_template('under_construction.html')


def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return render_template('error.html', error_code=code), code
