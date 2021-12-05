import os
import sys
import pathlib
import fire

# ルート以外のファイルを直接実行し、かつ自作ライブラリを読み込む場合は、PATHが見つからなく以下の１行が必須
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from common.logger import set_logger
from engine.keepa import KeepaAPI

logger = set_logger(__name__)


def crawle_by_asin():
    # ASINを指定
    asins = ["B08Y927771","B01FJ9DY90","B08KGY97DT","B084TNH1CY"]
    
    keepa = KeepaAPI(set_logger)
    products = keepa.fetch_products(asins)
    
    for product in products:
        logger.info(f"asin={product.asin}, title={product.title}")
    

if __name__ == "__main__":
    fire.Fire(crawle_by_asin)