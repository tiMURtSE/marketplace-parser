import undetected_chromedriver as uc
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

class Browser:

    def __init__(self):
        self._start_page = "https://www.ozon.ru"
        self._browser = uc.Chrome()

    def open_page(self, url: str):
        self._browser.get(url)

    def search_product(self, article: str):
        url = f"{self._start_page}/search/?from_global=true&sorting=rating&text={article}"
        self._browser.get(url)
        print(f"Поиск по артикулу: {article}")

    def find_element_by_class(self, target: WebElement, class_name):
        try:
            element = target.find_element(By.CLASS_NAME, class_name)

            return element
        except:
            return False

    def quit(self):
        self._browser.quit()
