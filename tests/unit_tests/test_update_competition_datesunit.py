import pytest
from server import app as flask_app
from datetime import datetime, timedelta

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_future_competition_booking(client, mocker):
    
    future_date = datetime.now() + timedelta(days=30)  
    future_competitions = [{
        "name": "Future Competition",
        "date": future_date.strftime("%Y-%m-%d %H:%M:%S"),
        "numberOfPlaces": "25"
    }]

    
    mocker.patch('server.loadCompetitions', return_value=future_competitions)
    from server import load_data
    load_data() 
    
    post_data = {
        'competition': 'Future Competition',  
        'club': 'Simply Lift',  
        'places': '1'
    }

    
    response = client.post('/purchasePlaces', data=post_data, follow_redirects=True)

    assert response.status_code == 200
    