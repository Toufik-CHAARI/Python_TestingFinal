import pytest
from server import app as flask_app  

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

def test_show_summary_with_valid_email(client):
    # use a an email 'clubs.json'
    valid_email = 'john@simplylift.co'
    response = client.post('/showSummary', data={'email': valid_email})
    assert response.status_code == 200
    

def test_show_summary_with_invalid_email(client):

    invalid_email = 'notfound@example.com'
    response = client.post('/showSummary', data={'email': invalid_email})
    assert response.status_code == 302 
    with client.session_transaction() as sess:
        assert 'No club found with that email address.' in sess['_flashes'][0][1]
