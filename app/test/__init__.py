'''
app.test.__init__
-------------------

Testing for imputation.io flask front end app
'''

import pytest
from app import app, data_dictionary, binaries_dict
from app.test.utils import make_form_data

@pytest.fixture
def client():
    app.config['TESTING'] = True
    
    with app.test_client() as client:
       yield client

NUM_FUZZY_TRIES = 10 #how many times to try random input