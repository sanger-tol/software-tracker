import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')
from api import *

@pytest.fixture
def client():
    global app
    app.config['TESTING'] = True
    return app.test_client()
