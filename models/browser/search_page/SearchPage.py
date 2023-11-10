from undetected_chromedriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from consts import TIMEOUT
from models.browser.Browser import Browser

class SearchPage(Browser):

    def __init__(self, browser: Chrome):
        self.browser = browser
    
    def find_product_cards(self):
        PRODUCT_CARD_CLASS = "ui8"

        wait = WebDriverWait(self.browser, TIMEOUT)
        product_cards = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, PRODUCT_CARD_CLASS)))

        return product_cards
        
    def find_product_review_info(self, card: WebElement):
        REVIEW_INFO_CLASS = "t2.t3.t4.tsBodyMBold"

        return self.find_element_by_class(target=card, class_name=REVIEW_INFO_CLASS)
    
    def find_product_title(self, card: WebElement):
        PRODUCT_TITLE_CLASS = "tsBody500Medium"

        title_element = self.find_element_by_class(target=card, class_name=PRODUCT_TITLE_CLASS)
        title = title_element.text

        return title
    
    def find_product_link(self, card: WebElement):
        PRODUCT_LINK_CLASS = "tile-hover-target"

        link_element = self.find_element_by_class(target=card, class_name=PRODUCT_LINK_CLASS)
        link = link_element.get_attribute("href")

        return link