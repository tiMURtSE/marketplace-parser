URL = "https://ozon.ru"

IMPORT_FILE_PATH = "C:/Users/user10/Desktop/Выгрузка товаров.xlsx"
IMPORT_FILE_COLUMNS = ["p:id", "c:vendor_sku"]
IMPORT_FILE_TITLES = ["id", "article"]

MOCK_PRODUCTS = [
    # { "id": "65212", "article": "A7972PL-1WH", "series": "ARTE Lamp" },
    { "id": "65212", "article": "A1408AP-1WH", "series": "Mizar" },
]

EXPORT_FILE_PATH = "C:/Users/user10/Desktop/Отзывы из Ozon.xlsx"
EXPORT_FILE_COLUMNS = [
    "id",
    "product_id",
    "customer_id",
    "customer_name",
    "virtual_customer_status",
    "review",
    "plus",
    "minus",
    "review_status",
    "moderation_user_id",
    "rate",
    "comment",
    "order_id",
    "type"
]

TIMEOUT = 5