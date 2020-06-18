'''
imputationflask.test.func.test_views
-------------------
Functional tests to see that all views return appropraitely
'''

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

def test_route_webapp_post(client,form_data):

    rv = client.post('/web_app',data=form_data)
    assert rv.status_code==200
    assert "Imputation.io" in rv.data.decode()