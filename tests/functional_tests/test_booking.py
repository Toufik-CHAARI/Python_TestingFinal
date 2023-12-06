import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BookingTest(unittest.TestCase):

    def setUp(self):
        os.environ['PATH']+=r"/Users/chaaritoufik/Desktop/dev/chromedriver-mac-x64"
        self.driver = webdriver.Chrome()

    def test_booking_form_submission(self):
        driver = self.driver        
        competition_name = "Spring Festival"
        club_name = "Simply Lift"
        driver.get(f"http://127.0.0.1:5000/book/{competition_name}/{club_name}")
        
    def test_booking_form_submission(self):
            driver = self.driver
            
            competition_name = "Spring Festival"
            club_name = "Simply Lift"
            driver.get(f"http://127.0.0.1:5000/book/{competition_name}/{club_name}")
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h2"))
        )
    
            competition_header = driver.find_element(By.TAG_NAME, "h2").text
            self.assertIn(competition_name, competition_header)

           
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//strong[contains(text(), 'Places available')]"))
            )
            places_info = driver.find_element(By.XPATH, "//strong[contains(text(), 'Places available')]").text
            self.assertIn("Places available", places_info)

            
            places_input = driver.find_element(By.NAME, "places")
            self.assertIsNotNone(places_input)
            places_input.send_keys("2")  
            places_input.send_keys(Keys.RETURN)
        
    
            
    def tearDown(self):
        self.driver.close()

