'''
app.test.conftest
-------------------
Utilities and configuration for testing
'''

import pytest
from app import app
from numpy.random import choice


NUM_FUZZY_TRIES = 10 #how many times to try random input

def make_form_data( data_dict, numeric_fields):
 
    data = dict()

    for key in numeric_fields:

        data[key]=str(choice(list(range(100))))
        data['mask_' + key]=choice(['y','n'])

    for key in data_dict:

        data[key]=choice([-1,0,1])
        data['mask_' + key]=choice(['y','n'])

    return data


@pytest.fixture
def client():
    app.config['TESTING'] = True
    
    with app.test_client() as client:
       yield client
