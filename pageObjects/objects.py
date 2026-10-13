from pageObjects.inventory import Inventory
from pageObjects.loginPage import LoginPage


class PageObjects:
    def __init__(self, page):
        self.page = page
        self.loginPage = LoginPage(page)
        self.inventory = Inventory(page)
