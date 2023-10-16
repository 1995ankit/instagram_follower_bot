from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep
import os
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException


CHROME_DRIVER_PATH = ChromeDriverManager().install()
# Provide the account name on Instagram whose followers you want to follow
SIMILAR_ACCOUNT = 'yahoofinance'
# Save your facebook username and password as 'username' and 'pass' in environment variables.
USERNAME = os.environ.get('username')
PASSWORD = os.environ.get('pass')

# Creating a class to perform the necessary actions.
class InstaFollower:
    def __init__(self, driver_path):
        self.driver = webdriver.Chrome(service=Service(driver_path))

    # This function will allow us to login to our instagram account through facebook Id and password
    def login(self):
        self.driver.get('https://www.instagram.com/accounts/login/')
        sleep(3)

        fb = self.driver.find_element(By.XPATH, value='//*[@id="loginForm"]/div/div[5]/button/span[2]')
        fb.click()
        sleep(3)
        # The below code will automatically input username and password saved in environment variables
        username = self.driver.find_element(By.XPATH, value='//*[@id="email"]')
        username.send_keys(os.environ.get('username'))
        password = self.driver.find_element(By.XPATH, value='//*[@id="pass"]')
        password.send_keys(os.environ.get('pass'))
        password.send_keys(Keys.ENTER)
        sleep(10)
        # The code below will auto cancel the notification button, if any
        try:
            notification = self.driver.find_element(By.XPATH, value='/html/body/div[3]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]')
            notification.click()
        except NoSuchElementException:
            pass

# The code below opens the follower list pop-up based on the account we choose
    def find_followers(self):
        self.driver.get(f'https://www.instagram.com/{SIMILAR_ACCOUNT}')
        sleep(5)
        followers_list = self.driver.find_element(By.CSS_SELECTOR, value='.xl565be a')
        followers_list.click()
        sleep(5)

# The code below will automatically start following everyone (first 100) on the follower list
    def follow(self):
        for i in range(100):
            try:
                button = self.driver.find_element(By.XPATH, value=f'/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/'
                                                                  f'div[2]/div/div/div[2]/div[2]/div/div[{i+1}]/div/div/div/div[3]/div/button')
                button.click()
                sleep(1)
            # If a person is already our connection, or there is a pending request, a notification will pop up. This exception is handled by the below code.
            except ElementClickInterceptedException:
                cancel_button = self.driver.find_element(By.XPATH, value='/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/div/button[2]')
                cancel_button.click()
                sleep(1)

bot = InstaFollower(CHROME_DRIVER_PATH)
bot.login()
bot.find_followers()
bot.follow()

