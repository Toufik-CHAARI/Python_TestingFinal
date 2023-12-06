import pytest
from unittest.mock import patch
from server import app  
from bs4 import BeautifulSoup

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_successful_booking(mocker, client):
    
    mocker.patch('server.loadClubs', return_value=[{'name': 'Simply Lift', 'email': 'simply@example.com', 'points': '100'}])
    mocker.patch('server.loadCompetitions', return_value=[{'name': 'Spring Festival', 'numberOfPlaces': '50'}])

    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival', 
        'club': 'Simply Lift', 
        'places': '1'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Great-booking complete' in response.get_data(as_text=True)

def test_booking_more_than_club_points(mocker, client):
   
    mocker.patch('server.loadClubs', return_value=[{'name': 'Iron Temple', 'email': 'iron@example.com', 'points': '10'}])
    mocker.patch('server.loadCompetitions', return_value=[{'name': 'Spring Festival', 'numberOfPlaces': '100'}])

    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival', 
        'club': 'Iron Temple', 
        'places': '11'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Not enough points' in response.get_data(as_text=True)