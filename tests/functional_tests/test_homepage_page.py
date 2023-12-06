import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

class GUDLFTRegistrationTest(unittest.TestCase):

    def setUp(self):
        
        os.environ['PATH']+=r"/Users/chaaritoufik/Desktop/dev/chromedriver-mac-x64"
        self.driver = webdriver.Chrome()

    def test_form_and_table(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")  
        main_header = driver.find_element(By.TAG_NAME, "h1").text
        self.assertEqual("Welcome to the GUDLFT Registration Portal!", main_header)
        table_header = driver.find_element(By.XPATH, "//h1[contains(text(), 'Club Points Table')]").text
        self.assertEqual("Club Points Table", table_header)

        
        email_input = driver.find_element(By.NAME, "email")
        self.assertIsNotNone(email_input)

        
        email_input.send_keys("admin@irontemple.com")
        email_input.send_keys(Keys.RETURN)

     

    def tearDown(self):
        self.driver.close()


