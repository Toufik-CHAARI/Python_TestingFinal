from locust import HttpUser, task, between
import random

class ProjectPerfTest(HttpUser):
    wait_time = between(1, 5)
    
    def on_start(self):
        """ Called when a Locust start before any task is scheduled """
        self.login()

    def login(self):      
        response = self.client.post("/showSummary", {"email": "john@simplylift.co"})
        if response.status_code != 200:
            print("Failed to log in with john@simplylift.co")

    @task(6)
    def home_and_booking(self):
        
        self.client.get("/")
        self.client.get("/showSummary")

        competitions = ["Spring Festival", "Fall Classic"]
        clubs = ["Simply Lift", "Iron Temple", "She Lifts"]
        places = random.randint(1, 2)
        competition = random.choice(competitions)
        club = random.choice(clubs)

        self.client.post("/purchasePlaces", {
            "competition": competition,
            "club": club,
            "places": places
        })
    @task(6)
    def book_competition(self):
        competitions = ["Spring Festival", "Fall Classic"]
        clubs = ["Simply Lift", "Iron Temple", "She Lifts"]

        competition = random.choice(competitions)
        club = random.choice(clubs)

        self.client.get(f"/book/{competition}/{club}")
        
    @task
    def logout(self):
        self.client.get("/logout")  
   
        