import pytest
import json
from pageObjects.objects import PageObjects


with open ("test_data/test_data.json") as read:
    test_data = json.load(read)
    print(test_data)


@pytest.mark.regression
@pytest.mark.parametrize("testData", test_data["valid_credentials"])
def test_tc001_login_with_valid_credentials(browserInstance, testData):
    # page Objects
    pageObjects = PageObjects(browserInstance)

    pageObjects.loginPage.login_to_the_application(testData["user_name"], testData["password"])
    pageObjects.loginPage.validation_the_login()
    pageObjects.inventory.logout_from_the_application()


@pytest.mark.regression
@pytest.mark.parametrize("testData", test_data["invalid_credentials"])
def test_tc005_login_with_invalid_credentials(browserInstance, testData):
    # page Objects
    pageObjects = PageObjects(browserInstance)

    pageObjects.loginPage.login_to_the_application(testData["user_name"], testData["password"])
    pageObjects.loginPage.invalid_login_error_validation()
