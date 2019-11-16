from inference_demo import app, data_dictionary, dict_binaries

from flask import render_template, request, jsonify
from werkzeug.exceptions import HTTPException
from inference_demo.forms import CensusImputeForm


@app.route('/')
@app.route('/web_app', methods=["GET", "POST"])
def web_app():
    form = CensusImputeForm.make_form(data_dict=data_dictionary.data_dict,
                                      numeric_fields=dict_binaries['numeric_mappers'].keys(),
                                      recordname2description=dict_binaries['recordname2description'],
                                      request_form=request.form)
    if request.method == 'POST':
        return jsonify(request.form), 200
    #     #return jsonify(form.validate()),200
       # return 'Form submitted successfully', 200
    return render_template('webapp.html',
                           form=form)


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

