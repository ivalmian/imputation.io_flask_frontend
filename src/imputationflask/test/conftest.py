'''
imputationflask.test.conftest
-------------------
Utilities and configuration for testing
'''

import pytest
from imputationflask import app, db
from numpy.random import choice
from imputationflask import data_dictionary, binaries_dict

NUM_FUZZY_TRIES = 10 #how many times to try random input

@pytest.fixture(params=range(NUM_FUZZY_TRIES))
def form_data(request):
    
    data = dict()

    for key in binaries_dict['numeric_mappers'].keys():

        data[key]=str(choice(list(range(100))))
        data['mask_' + key]=choice(['y','n'])

    for key in data_dictionary.data_dict.keys():

        data[key]=choice([-1,0,1])
        data['mask_' + key]=choice(['y','n'])

    return data


@pytest.fixture
def client():
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client

@pytest.fixture
def database():
    with app.app_context():
        db.create_all()
        yield database
        db.drop_all()
