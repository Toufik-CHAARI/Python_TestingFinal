import pytest
from unittest.mock import patch
from server import app  
from bs4 import BeautifulSoup

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_booking_too_many_places(mocker, client):
    
    mocker.patch('server.loadClubs', return_value=[{'name': 'She Lifts', 'email': 'test@example.com', 'points': '30'}])
    mocker.patch('server.loadCompetitions', return_value=[{'name': 'Fall Classic', 'numberOfPlaces': '15'}])

    response = client.post('/purchasePlaces', data={
        'competition': 'Fall Classic', 
        'club': 'She Lifts', 
        'places': '13'
    }, follow_redirects=True)
    assert response.status_code == 200  
    assert 'Cannot book more than 12 places' in response.get_data(as_text=True)

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
    
    
def test_booking_more_than_available(mocker, client):
   
    mocker.patch('server.loadClubs', return_value=[{'name': 'She Lifts', 'email': 'test@example.com', 'points': '20'}])
    mocker.patch('server.loadCompetitions', return_value=[{'name': 'TEST (<12 & available >)', 'numberOfPlaces': '8'}])

    response = client.post('/purchasePlaces', data={
        'competition': 'TEST (<12 & < available)', 
        'club': 'She Lifts', 
        'places': '9'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Not enough places available in the competition.' in response.get_data(as_text=True)

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
    
def test_booking_deducts_points(mocker, client):
    initial_points = 30  
    places_to_book = 5
    expected_points = initial_points - places_to_book

    
    mocker.patch('server.loadClubs', return_value=[{'name': 'Iron Temple', 'email': 'admin@irontemple.com', 'points': str(initial_points)}])
    mocker.patch('server.loadCompetitions', return_value=[{'name': 'Spring Festival','date': '2024-05-01 10:00:00', 'numberOfPlaces': '25'}])
    from server import load_data
    load_data(testing=True)
    # Make the booking
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival', 
        'club': 'Iron Temple', 
        'places': str(places_to_book)
    }, follow_redirects=True)

  
    assert response.status_code == 200

    
    soup = BeautifulSoup(response.data, 'html.parser')
    points_display = soup.find(id="club-points")
    print(soup)
    if points_display is not None:
        updated_points = int(points_display.text.strip())
        assert updated_points == expected_points
    else:
        raise AssertionError("The element with id 'club-points' was not found in the response.")

