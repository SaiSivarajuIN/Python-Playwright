import pytest
import json
from pageObjects.objects import PageObjects


with open ("test_data/test_data.json") as read:
    test_data = json.load(read)

@pytest.mark.regression
@pytest.mark.parametrize("testData", test_data["add_product_cart"])
def test_tc_002_add_single_product_to_cart(browserInstance, testData):
    # page Objects
    pageObjects = PageObjects(browserInstance)

    pageObjects.loginPage.login_to_the_application(testData["user_name"], testData["password"])
    pageObjects.inventory.add_single_product(testData["action"], testData["product_name"])
    pageObjects.inventory.logout_from_the_application()


@pytest.mark.regression
@pytest.mark.parametrize("testData", test_data["all_items"])
def test_tc_003_add_all_products_to_cart(browserInstance, testData):
    # page Objects
    pageObjects = PageObjects(browserInstance)

    pageObjects.loginPage.login_to_the_application(testData["user_name"], testData["password"])
    pageObjects.inventory.add_all_items(testData["action"])
    pageObjects.inventory.logout_from_the_application()

@pytest.mark.regression
@pytest.mark.parametrize("testData", test_data["add_multiple"])
def test_tc_004_add_multiple_products_to_cart_at_time(browserInstance, testData):
    # page Objects
        pageObjects = PageObjects(browserInstance)
    
        pageObjects.loginPage.login_to_the_application(testData["user_name"], testData["password"])
        pageObjects.inventory.add_multiple_products_at_a_time(testData["product_names"])
        pageObjects.inventory.logout_from_the_application()
