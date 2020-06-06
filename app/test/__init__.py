import pytest
import app
from app.test.utils import make_from_data

@pytest.fixture
def client():
    app.app.config['TESTING'] = True
    
    with app.app.test_client() as client:
       yield client

NUM_FUZZY_TRIES = 10 #how many times to try random input