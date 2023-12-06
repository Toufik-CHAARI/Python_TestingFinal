import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

class GUDLFTRegistrationTest(unittest.TestCase):

    def setUp(self):
        
        os.environ['PATH']+=r"/Users/chaaritoufik/Desktop/dev/chromedriver-mac-x64"
        self.driver = webdriver.Chrome()
        

    def test_form_submission(self):
        driver = self.driver
        driver.implicitly_wait(2)
        driver.get("http://127.0.0.1:5000/")     

       
        header_text = driver.find_element(By.TAG_NAME, "h1").text
        self.assertEqual("Welcome to the GUDLFT Registration Portal!", header_text)
        
        email_input = driver.find_element(By.NAME, "email")
        self.assertIsNotNone(email_input)       
        table_header = driver.find_element(By.XPATH, "//h1[contains(text(), 'Club Points Table')]")
        self.assertIsNotNone(table_header)    
        email_input.send_keys("john@simplylift.co")
        email_input.send_keys(Keys.RETURN)        

    def tearDown(self):
       self.driver.close()
