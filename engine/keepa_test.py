import pandas as pd
from engine.keepa import *


def test_fetch_jan():
    keepa = KeepaAPI()
    res = keepa.fetch_products(["B08Y927771","B01FJ9DY90","B08KGY97DT","B084TNH1CY"])
    print(res)    
