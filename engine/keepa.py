import os
import requests
import datetime
import logging
from dotenv import load_dotenv
load_dotenv() 

from models.local.local_amazon_product import LocalAmazonProduct


class KeepaAPI():
    PRODUCT_API = "https://api.keepa.com/product"
    RANKING_API = "https://api.keepa.com/bestsellers"
    STATUS_API = "https://api.keepa.com/token"

    BASE_TIME_STAMP = 1293807600 # 2011/01/01


    def __init__(self, get_logger=logging.getLogger):
        '''
        クラスをインスタンス化すると最初に呼ばれる
        '''
        # API_KEYは.envファイルから読み込む
        self._key = os.environ["KEEPA_API_KEY"]
        self._logger:logging.Logger = get_logger(__name__)


    def fetch_ranking(self, category_id: str,):
        '''
        ランキングを取得する
        '''
        params = {
            "key": self._key,
            "domain": 5,
            "category": category_id,
            "range": 30 # 30日平均
        }
        res = requests.get(self.RANKING_API, params=params)
        if not(300 > res.status_code >= 200):
            self._logger.error(f"API connection error: {res.text}")
            return None
        res_dict = res.json()
        
        try:
            return res_dict["bestSellersList"]["asinList"]
        except:
            return None


    def _fetch_products(self, asins: list):
        '''
        商品情報を取得する
        '''
        params = {
            "key": os.environ["KEEPA_API_KEY"],
            "domain": 5,
            "days": 90,
            "asin": ",".join(asins)
        }
        self._logger.info(f"tokens left(before): {self.get_tokens_left()}")
        res = requests.get(self.PRODUCT_API, params=params)
        self._logger.info(f"tokens left(after): {self.get_tokens_left()}")
        
        res.raise_for_status()
        res_dict = res.json()
        try:
            return res_dict["products"]
        except:
            return None


    def fetch_products(self, asins: list):
        '''
        商品の情報を取得する
        '''
        try:
            products = self._fetch_products(asins)
        except Exception as e:
            raise Exception(f"API Error | {e}")
        if not products:
            return []
        self._logger.info(f"products count: {len(products)}")
        
        res_products: list[LocalAmazonProduct] = []
        for product in products:
            amazon_price_history = None
            amazon_price_history_timestamp = None
            new_price_history = None
            new_price_history_timestamp = None
            amazon_not_sales_rate = None
            if not product.get("csv"):
                pass #fba_price_history = None
            else:
                if len(product["csv"]) >= 1 and product["csv"][0]:
                    amazon_price_history = list(map(lambda x: str(x), product["csv"][0][1::2]))
                    # KeepaTime(2011/01/01ベースのTimestamp(分)) → TimeStamp(秒)
                    amazon_price_history_timestamp = list(map(lambda x: str(x*60 + self.BASE_TIME_STAMP), product["csv"][0][0::2]))
                    amazon_not_sales_rate = len(list(filter(lambda x: x == '-1', amazon_price_history))) / len(amazon_price_history)
                if len(product["csv"]) >= 2 and product["csv"][1]:
                    new_price_history = list(map(lambda x: str(x), product["csv"][1][1::2]))
                    new_price_history_timestamp = list(map(lambda x: str(x*60 + self.BASE_TIME_STAMP), product["csv"][1][0::2]))
                #fba_price_history = product["csv"][10][1::2] if len(product["csv"]) >= 11 and product["csv"][10] else None
            res_products.append(
                LocalAmazonProduct(
                    title = product["title"],
                    asin = product["asin"],
                    jan = product["eanList"][0] if product["eanList"] else None,
                    price = int(new_price_history[-1]),
                    amazon_price_history = amazon_price_history,
                    new_price_history = new_price_history,
                )
            )
            
        return res_products
    
    
    def get_tokens_left(self):
        params = {
            "key": self._key
        }
        res = requests.get(self.STATUS_API, params=params)
        if not(300 > res.status_code >= 200):
            raise Exception(f"API connection error: {res.text}")
        return res.json()["tokensLeft"]
