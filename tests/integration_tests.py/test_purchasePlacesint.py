import pytest
from server import app 
from bs4 import BeautifulSoup 

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_booking_too_many_places(client):
   
    response = client.post('/purchasePlaces', data={
        'competition': 'Fall Classic', 
        'club': 'Simply Lift', 
        'places': '13'
    }, follow_redirects=True)
    assert response.status_code == 200  
    assert 'Cannot book more than 12 places' in response.get_data(as_text=True)


def test_successful_booking(client):
   
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival', 
        'club': 'Simply Lift', 
        'places': '6'
    }, follow_redirects=True)
    assert response.status_code == 200  
    assert 'Great-booking complete' in response.get_data(as_text=True)


def test_booking_more_than_club_points(client):

    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival', 
        'club': 'Iron Temple', 
        'places': '6'  
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Not enough points' in response.get_data(as_text=True)