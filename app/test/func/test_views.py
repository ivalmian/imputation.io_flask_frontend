'''
app.test.func.test_views
-------------------
Functional tests to see that all views return appropraitely
'''

from app.test.conftest import client, make_form_data, NUM_FUZZY_TRIES
from app import data_dictionary, binaries_dict

from flask import request

def test_route_privacy_get(client):
    
    rv = client.get('/privacy')
    assert rv.status_code==200
    assert "Imputation.io" in rv.data.decode()

def test_route_how_it_works_get(client):
    
    rv = client.get('/how_it_works')
    assert rv.status_code==200
    assert "Imputation.io" in rv.data.decode()

def test_route_about_api_get(client):
    
    rv = client.get('/about_api')
    assert rv.status_code==200
    assert "Imputation.io" in rv.data.decode()

def test_bad_route_get(client):
    
    rv = client.get('/waqerawfrwaere')
    assert rv.status_code==404
    assert "Imputation.io" in rv.data.decode()

def test_route_none_get(client):
    
    rv = client.get('/')
    assert rv.status_code==200
    assert "Imputation.io" in rv.data.decode()

def test_route_webapp_post(client):
    
    for _ in range(NUM_FUZZY_TRIES): #make_from_data randomly generates data, we do several runs
        data = make_form_data(data_dict=data_dictionary.data_dict,
                              numeric_fields=binaries_dict['numeric_mappers'].keys())
        rv = client.post('/web_app',data=data)
        assert rv.status_code==200
        assert "Imputation.io" in rv.data.decode()