import datetime


class LocalAmazonProduct():
    '''
    ローカル用のAmazonProduct管理用
    '''
    
    def __init__(self, 
                 asin: str, jan: str, price: int, amazon_price_history: list, new_price_history: list,
                 title: str):
        self.title= title
        self.asin = asin
        self.jan = jan
        self.price = price
        self.amazon_price_history = amazon_price_history
        self.new_price_history = new_price_history
