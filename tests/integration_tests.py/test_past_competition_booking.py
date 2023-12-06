import pytest
from datetime import datetime, timedelta
from server import app as flask_app


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_booking_past_competition(client):
    
    past_competition_name = "TEST (<12 & < available)"
    club_name = "Simply Lift"

    
    booking_data = {
        'competition': past_competition_name,
        'club': club_name,
        'places': '1'
    }

    
    response = client.post('/purchasePlaces', data=booking_data, follow_redirects=True)

    
    assert response.status_code == 200
    assert "Cannot book for past competitions." in response.get_data(as_text=True)
