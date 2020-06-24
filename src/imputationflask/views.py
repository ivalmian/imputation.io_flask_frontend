'''
imputationflask.views
-------------------
Define routes render by flask
'''


# external imports
from flask import render_template, request, current_app, Blueprint
from werkzeug.exceptions import HTTPException
from matplotlib import cm
import json

frontend = Blueprint('frontend', __name__)


def make_graph_data(pred_description):

    colormap_name = 'tab20c'
    graph_data = dict()

    for key, pred in pred_description.items():

        if key in current_app.persistent.binaries_dict['numeric_mappers'].keys():

            graph_data[key] = json.dumps([{'label': current_app.persistent.binaries_dict['recordname2description'][key],
                                'data': [{'x': x, 'y': y} for x, y in zip(pred['x'], pred['y'])],
                                'showLine': True,
                                'pointRadius': 0,
                                'borderColor': "#00468C",
                                'borderWidth': 1,
                                'backgroundColor': "#3e95cdcc"}])

        else:

            l = len(pred['y'])
            cmap = cm.get_cmap(colormap_name, l)
            colors = [f'#{"".join(str(hex(int(255*c))[2:]) for c in color[:3] )}'
                      for color in cmap.colors]  # TODO: This probably has a more elegant solution
            graph_data[key] = json.dumps([{
                'label': pred['x'][i],
                'data': [pred['y'][i]],
                'backgroundColor': colors[i],
                'borderWidth': 1}

                for i in range(l)])


    return graph_data


@frontend.route('/')
@frontend.route('/web_app', methods=["GET", "POST"])
def web_app():

    form = current_app.persistent.census_form.get_instance(
        request_form=request.form)

    # we got some data, time to make predictions
    if request.method == 'POST':
        pred_description = current_app.persistent.predictor(request.form)
        graph_data = make_graph_data(pred_description)
    else:
        pred_description = None
        graph_data = None

    return render_template('webapp.html',
                           form=form,
                           pred_description=pred_description,
                           graph_data=graph_data,
                           description_dict=(current_app
                                             .persistent
                                             .binaries_dict['recordname2description']),
                           numeric_keys=list(current_app
                                             .persistent
                                             .binaries_dict['numeric_mappers']
                                             .keys()))


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
