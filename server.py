import json
from flask import Flask,render_template,request,redirect,flash,url_for
from flask import session

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
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

def get_club_by_email(club_email):
    '''
    Retrieve a club object from a list of clubs based on the provided email address.
    This function iterates over a global list 'clubs' and returns the first club whose 'email' 
    attribute matches the provided 'club_email'. 

    '''
    return next((club for club in clubs if club['email'] == club_email), None)

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


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)