import app 
import app.test as test
from app.test import client

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
    
    for _ in range(test.NUM_FUZZY_TRIES): #make_from_data randomly generates data, we do several runs
        data = test.make_from_data(data_dict=app.data_dictionary.data_dict,
                                        numeric_fields=app.binaries_dict['numeric_mappers'].keys())
        rv = client.post('/web_app',data=data)
        assert rv.status_code==200
        assert "Imputation.io" in rv.data.decode()