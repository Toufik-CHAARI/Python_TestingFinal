import pytest
from server import app as flask_app

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

def test_show_summary_with_valid_email(mocker, client):
    
    mocker.patch('server.loadClubs', return_value=[{'name': 'Simply Lift', 'email': 'john@simplylift.co', 'points': '100'}])
    from server import load_data
    load_data(testing=True)

    valid_email = 'john@simplylift.co'
    response = client.post('/showSummary', data={'email': valid_email})
    assert response.status_code == 200


def test_show_summary_with_invalid_email(mocker, client):
    
    mocker.patch('server.loadClubs', return_value=[{'name': 'Simply Lift', 'email': 'john@simplylift.co', 'points': '100'}])

    invalid_email = 'notfound@example.com'
    response = client.post('/showSummary', data={'email': invalid_email})
    assert response.status_code == 302 
    with client.session_transaction() as sess:
        assert 'No club found with that email address.' in sess['_flashes'][0][1]
