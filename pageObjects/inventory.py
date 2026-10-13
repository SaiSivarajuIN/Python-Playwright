import logging
import configparser
from playwright.sync_api import Page



class Inventory:

    def __init__(self, page:Page):
        self.page = page

    config = configparser.ConfigParser()
    config.read("properties.ini")
    url = config["settings"]["url"]

    MENU_BTN = '#react-burger-menu-btn'
    LOGOUT_LINK = '#logout_sidebar_link'
    INVENTORY_ITEM = '//div[@class="inventory_item"]'  # All product containers

    def logout_from_the_application(self):
        self.page.locator(self.MENU_BTN).click()
        self.page.locator(self.LOGOUT_LINK).click()
        self.page.wait_for_url(self.url)
        logging.info("Logged out successfully.")

    def add_single_product(self, action, product_name):
        product = self.page.locator(self.INVENTORY_ITEM).filter(has_text=product_name).first

        button = product.locator("button").filter(has_text=action)
        button.click()

        self.page.wait_for_timeout(1000)  # Wait 1 second
        logging.info(f"{action} clicked on {product_name} items.")

    def add_all_items(self, action):
        products = self.page.locator(self.INVENTORY_ITEM)
        items_added = 0

        for i in range(products.count()):
            button = products.nth(i).locator("button").filter(has_text=action)

            if button.count() > 0:
                button.first.click()
                items_added += 1
                self.page.wait_for_timeout(1000)  # Wait 1 second

        logging.info(f"{action} clicked on {items_added} items.")
        return items_added

    def add_multiple_products_at_a_time( self, product_names: list[str]):
        
        items_added = 0

        for name in product_names:
            product = self.page.locator( self.INVENTORY_ITEM).filter(has_text=name).first

            if product.count() > 0:
                button = product.get_by_role("button", name="Add to cart")

                if button.count() > 0:
                    button.click()
                    items_added += 1
        logging.info(f"{product_names} items are Added to cart.")
        return items_added