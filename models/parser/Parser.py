from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from models.browser.Browser import Browser
from models.browser.search_page.SearchPage import SearchPage
from models.browser.product_page.ProductPage import ProductPage
from models.excel.Excel import Excel
from models.adapter.Adapter import Adapter

from consts import IMPORT_FILE_PATH, IMPORT_FILE_COLUMNS, IMPORT_FILE_TITLES, MOCK_PRODUCTS
from utils.check_substring import check_substring

class Parser:
    
    def __init__(self):
        self._browser = Browser()
        self.search_page = SearchPage(self._browser._browser)
        self.product_page = ProductPage(self._browser._browser)
        self.excel = Excel(IMPORT_FILE_PATH)
        self.adapter = Adapter(self.excel, IMPORT_FILE_TITLES)

    def run(self):
        # products = MOCK_PRODUCTS
        products = self.adapter.get_columns_data(IMPORT_FILE_COLUMNS)
        print(products)

        for product in products:
            reviews = []
            article = product["article"]

            # Поиск товара по артикулу
            self._browser.search_product(article)

            # Получения всех ссылок товаров, которые подходят по артикулу и имеют отзывы
            valid_product_links = self._get_valid_product_links(article)
            
            # Переход на страницу каждого товара
            if valid_product_links:
                for link in valid_product_links:
                    reviews_from_single_product = []

                    self._browser.open_page(link)
                    self.product_page.scroll_down()

                    # Получение всех DOM-элементов отзывов с одного товара
                    review_elements = self.product_page.find_review_elements()

                    for review_element in review_elements:
                        review = self.parse_review(review_element)

                        if review:
                            reviews_from_single_product.append(review)

                    print(reviews_from_single_product)

                    reviews.extend(reviews_from_single_product)
            else:
                print(f"Нет товаров с отзывами по артикулу {article}")
                continue
                
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
    
    def parse_review(self, review_element: WebElement):
        REVIEW_PART_CLASS = "p4u"

        review_parts = review_element.find_elements(By.CLASS_NAME, REVIEW_PART_CLASS)


        if review_parts:
            review = self.product_page.get_review_content(review_parts)

            try:
                review["customer_name"] = self.product_page.find_customer_name(review_element)
                review["rating"] = self.product_page.find_rating(review_element)    
            except:
                print(f"Ошибка в {review}")
        
            return review