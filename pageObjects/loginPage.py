import logging
import configparser
from playwright.sync_api import Page, expect

class LoginPage:

    def __init__(self, page:Page):
        self.page = page

    config = configparser.ConfigParser()
    config.read("properties.ini")
    inventory_url = config["settings"]["inventory_url"]

    # Locatros
    USER_NAME = '#user-name'
    PASSWORD = '#password'
    LOGIN_BTN = '#login-button'
    ERROR_MESSAGE = '[data-test="error"]'
    

    def login_to_the_application(self, user_name, password):
        self.page.locator(self.USER_NAME).fill(user_name)
        self.page.locator(self.PASSWORD).fill(password)
        self.page.locator(self.LOGIN_BTN).click()
        
    def validation_the_login(self):
        self.page.wait_for_url(self.inventory_url)
        logging.info("Login successful.")

    def invalid_login_error_validation (self):
        expect(self.page.locator(self.ERROR_MESSAGE)).to_contain_text("Epic sadface: Username and password do not match any user in this service")

