from models.excel.Excel import Excel

class Adapter:

    def __init__(self, adaptee: Excel, column_titles: list[str]):
        self._adaptee = adaptee
        self._column_titles = column_titles

    def get_columns_data(self, columns: list[str], start_pos: int = 2, end_pos: int = 9999):
        data = self._adaptee.get_columns_data(columns, start_pos, end_pos)

        if self._is_valid_column_titles(data):
            products = self._adapt_data_to_products(data)

            return products
        else:
            raise Exception("Количество столбцов и количество значений не совпадают")

    def _adapt_data_to_products(self, data: list):
        products = []

        for row in data:
            product = {}

            for i, column_title in enumerate(self._column_titles):
                product[column_title] = row[i]

            products.append(product)

        return products
    
    def _is_valid_column_titles(self, data: list):
        return len(data[0]) == len(self._column_titles)



    
