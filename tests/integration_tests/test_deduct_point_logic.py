import pytest
from server import app 
from bs4 import BeautifulSoup 


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client



def test_booking_deducts_points(client):
    
    initial_points = 13  
    places_to_book = 3
    expected_points = initial_points - places_to_book

    
    response = client.post('/purchasePlaces', data={
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': str(places_to_book)
    }, follow_redirects=True)
    assert response.status_code == 200

    
    follow_up_response = client.post('/showSummary', data={'email': 'john@simplylift.co'}, follow_redirects=True)
    assert follow_up_response.status_code == 200


    soup = BeautifulSoup(follow_up_response.data, 'html.parser')
    points_display = soup.find(id="club-points")
    if points_display:
        updated_points = int(points_display.text.strip())
        assert updated_points == expected_points
    else:
        raise AssertionError("The element with id 'club-points' was not found in the response.")
