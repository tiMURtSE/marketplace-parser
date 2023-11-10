import time
import re
from undetected_chromedriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from consts import TIMEOUT
from models.browser.Browser import Browser
from utils.create_review import create_review

class ProductPage(Browser):

    def __init__(self, browser: Chrome):
        self._browser = browser

    def scroll_down(self):
        REVIEWS_BOTTOM_PADDING = 4000
        SCROLL_DOWN_SCRIPT = f"window.scrollTo(0, document.body.scrollHeight - {REVIEWS_BOTTOM_PADDING})"

        review_count = self._get_review_count()

        while True:
            self._browser.execute_script(SCROLL_DOWN_SCRIPT)
            time.sleep(1)

            current_review_count = len(self.find_review_elements())

            if review_count == current_review_count or current_review_count > 90:
                break

    def _get_review_count(self):
        REVIEW_COUNT_OUTER_CLASS = "pv4"
        REVIEW_COUNT_INNER_CLASS = "a2429-e7"

        wait = WebDriverWait(self._browser, TIMEOUT)
        review_count_outer_element = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, REVIEW_COUNT_OUTER_CLASS)))
        review_count_inner_element = review_count_outer_element[0].find_elements(By.CLASS_NAME, REVIEW_COUNT_INNER_CLASS)
        
        if review_count_inner_element:
            text = review_count_inner_element[0].text

            return int(text.split(" ")[0])
        else:
            raise EOFError("Не найдено количество отзывов на странице товара")

    def find_review_elements(self):
        REVIEW_CLASS = "up9"

        review_elements = self._browser.find_elements(By.CLASS_NAME, REVIEW_CLASS)

        return review_elements
        
    def get_review_content(self, review_parts: list[WebElement]):
        TITLE_CLASS = "pu4"
        CONTENT_CLASS = "u3p"

        review = create_review()

        for part in review_parts:
            part_title = part.find_elements(By.CLASS_NAME, TITLE_CLASS)
            content_element = part.find_element(By.CLASS_NAME, CONTENT_CLASS)
            content = content_element.text.strip()

            if part_title:
                title = part_title[0].text.strip()

                review = self._identify_review_part(title, content, review)
            else:
                review["comment"] = content

        return review
    
    def find_customer_name(self, review_element: WebElement):
        CUSTOMER_NAME_CLASS = "r5p"

        customer_name_element = review_element.find_element(By.CLASS_NAME, CUSTOMER_NAME_CLASS)
        customer_name = customer_name_element.text.strip()
        
        return customer_name
    
    def find_rating(self, review_element: WebElement):
        RATING_CLASS = "e1317-b.e1317-a2"

        rating_element = review_element.find_element(By.CLASS_NAME, RATING_CLASS)
        style_attribute = rating_element.get_attribute("style")

        match = re.search(r'(\d+)%', style_attribute)

        if match:
            percent_value = match.group(1)  # Получает найденное значение
            rating = int(percent_value) // 20  # Преобразует в целое число

        return rating

    def _identify_review_part(self, title: str, content: str, review: dict):
        if title == "Достоинства":
            review["pros"] = content
        elif title == "Недостатки":
            review["cons"] = content
        elif title == "Комментарий":
            review["comment"] = content
        else:
            raise EOFError("Несуществующий заголовок для компонента отзыва")
        
        return review