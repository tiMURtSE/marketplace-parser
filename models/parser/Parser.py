from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from models.browser.Browser import Browser
from models.browser.search_page.SearchPage import SearchPage
from models.browser.product_page.ProductPage import ProductPage
from models.excel.Excel import Excel
from models.adapter.Adapter import Adapter

from consts import (
    IMPORT_FILE_PATH,
    IMPORT_FILE_COLUMNS,
    IMPORT_FILE_TITLES,
    MOCK_PRODUCTS,
    EXPORT_FILE_PATH,
    EXPORT_FILE_COLUMNS,
)
from utils.check_substring import check_substring

class Parser:
    
    def __init__(self):
        self._browser = Browser()
        self.search_page = SearchPage(self._browser._browser)
        self.product_page = ProductPage(self._browser._browser)
        self.import_file = Excel(IMPORT_FILE_PATH)
        self.export_file = Excel(EXPORT_FILE_PATH)
        self.adapter = Adapter(self.import_file, IMPORT_FILE_TITLES)
        self.adapter2 = Adapter(self.export_file)

    def run(self):
        start_pos = int(input("Стартовая позиция: "))
        end_pos = int(input("Конечная позиция: "))

        # products = MOCK_PRODUCTS
        products = self.adapter.get_columns_data(IMPORT_FILE_COLUMNS, start_pos, end_pos)

        for product in products:
            reviews = []
            id = product["id"]
            article = product["article"]
            print(f"article: {article}")

            # Поиск товара по артикулу
            self._browser.search_product(article)

            # Получения всех ссылок товаров, которые подходят по артикулу и имеют отзывы
            try:
                valid_product_links = self._get_valid_product_links(article)
            except TimeoutException:
                continue
            
            # Переход на страницу каждого товара
            if valid_product_links:
                for link in valid_product_links:
                    reviews_from_single_product = []

                    self._browser.open_page(link)
                    self.product_page.scroll_down()

                    # Получение всех DOM-элементов отзывов с одного товара
                    review_elements = self.product_page.find_review_elements()

                    for review_element in review_elements:
                        review = self._parse_review(id, review_element)

                        if review:
                            reviews_from_single_product.append(review)

                    reviews.extend(reviews_from_single_product)
            else:
                print(f"Нет товаров с отзывами по артикулу {article}")
                continue

            # Запись отзывов в Excel-файл
            self.adapter2.write_data(EXPORT_FILE_COLUMNS, reviews)
            print(reviews)

        self._browser.quit()

    def _get_valid_product_links(self, article: str):
        valid_product_links = []

        product_cards = self.search_page.find_product_cards()
        
        for card in product_cards:
            if not self.search_page.find_product_review_info(card):
                break

            title = self.search_page.find_product_title(card)

            if check_substring(main_string=title, substring=article):
                product_link = self.search_page.find_product_link(card)
                valid_product_links.append(product_link)

        print(f"У артикула {article} {len(valid_product_links)} товара/товаров")
        return valid_product_links
    
    def _parse_review(self, id: str, review_element: WebElement):
        REVIEW_PART_CLASS = "p4u"

        review_parts = review_element.find_elements(By.CLASS_NAME, REVIEW_PART_CLASS)

        if review_parts:
            review = self.product_page.get_review_content(review_parts)

            try:
                review["id"] = id
                review["customer_name"] = self.product_page.find_customer_name(review_element)
                review["rate"] = self.product_page.find_rating(review_element)
            except:
                print(f"Ошибка в {review}")
        
            return review