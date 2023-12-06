import json
from flask import Flask,render_template,request,redirect,flash,url_for
from flask import session
from datetime import datetime, timedelta

def loadClubs():
    """
    Load and return a list of clubs from a JSON file.
    """
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    """
    Load and return a list of competitions from a JSON file.    
    """
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

def load_data(testing=False):
    """    
    This function loads data from JSON files into global
    variables 'clubs' and 'competitions'.It can operate in
    a normal mode or a testing mode, which is controlled 
    by the 'testing' parameter.The function calls 'loadClubs'
    and 'loadCompetitions' to load data from the respective 
    JSON files.    
    """
    global clubs, competitions
    if testing:
        clubs = loadClubs()
        competitions = loadCompetitions()
    else:
        clubs = loadClubs()
        competitions = loadCompetitions()

load_data()

@app.route('/')
def index():
    clubs = loadClubs()    
    return render_template('index.html', clubs=clubs)



@app.route('/showSummary', methods=['GET', 'POST'])
def showSummary():
    """
    This route handles both GET and POST requests. 
    For a POST request, it processes the submitted 'email' from the form, 
    searches for the matching club, and sets a session variable with the club's email. 
    If no matching club is found, it flashes a message and redirects to the 'index' route.
    For a GET request, it retrieves the club information based on the 'club_email' stored
    in the session.
    When club data are successfully retrieved, it renders the 'welcome.html' template with the club 
    and competitions information.    
    """
    if request.method == 'POST':
        email = request.form['email']
        matching_clubs = [club for club in clubs if club['email'] == email]
        if not matching_clubs:
            flash('No club found with that email address.')
            return redirect(url_for('index'))
        club = matching_clubs[0]
        
        session['club_email'] = club['email']
    else:
       
        club_email = session.get('club_email')
        club = get_club_by_email(club_email)

    return render_template('welcome.html', club=club, competitions=competitions)

def get_club_by_email(club_email):
    '''
    Retrieve a club object from a list of clubs based on the provided email address.
    This function iterates over a global list 'clubs' and returns the first club whose 'email' 
    attribute matches the provided 'club_email'. 

    '''
    return next((club for club in clubs if club['email'] == club_email), None)

@app.route('/book/<competition>/<club>')
def book(competition,club):
    '''
    This route displays a booking page for a specific competition and club.
    It extracts the 'competition' and 'club' parameters from the URL, searches for the corresponding
    competition and club in the global lists 'competitions' and 'clubs', respectively, and then
    renders the booking page with their details.    
    '''
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    '''
    Process the booking of places for a club in a competition.
    This route handles the POST request to book a specified number
    of places in a competition for a club.
    It validates the requested number of places against the competition's availability, the club's points,
    and other constraints like booking more than 12 places at a time or booking for past competitions.
    The function updates the number of places available in the competition and the points of the club 
    accordingly, if the booking is successful.      
    '''
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    print("Debug - Club Points:", club['points'])  
    print("Debug - Places Required:", placesRequired)
    
    #optionnal code / not identified as an issue
    if placesRequired > int(competition['numberOfPlaces']):
            flash('Not enough places available in the competition.')
            return redirect(url_for('book', competition=competition['name'], club=club['name']))
    
    if placesRequired > 12:
        flash('Cannot book more than 12 places at a time.')
        return redirect(url_for('book', competition=competition['name'], club=club['name']))
    
    if placesRequired > int(club['points']):
        flash('Not enough points to book that many places.')
        return redirect(url_for('book', competition=competition['name'], club=club['name']))            
    
    competition_date = datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S")
    if datetime.now() > competition_date:
        flash("Cannot book for past competitions.")
        return redirect(url_for('index', competition=competition['name'], club=club['name']))
    
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    club['points'] = int(club['points']) - placesRequired

    flash('Great-booking complete!')
    session['club_email'] = club['email']
    return render_template('welcome.html', club=club, competitions=competitions)




@app.route('/logout')
def logout():
    '''
    Handle the logout process.
    It handles the redirection of the user to the 'index' page
    after performing cleanup actions such as clearing session data or cookies.
    '''
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)