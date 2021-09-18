

import os
import sys
import fire
import pandas as pd

# 環境変数(.env)の読み込み
from dotenv import load_dotenv
load_dotenv()

# プロジェクトルートをPATHに追加
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from common.utility import now_timestamp
from engine.aliexpress import AliexpressScraping
from engine.aliexpress_requests import AliexpressRequests

# ログ出力設定
from common.logger import set_logger
logger = set_logger(__name__)


def selenium(url :str, page_limit: int=5):
    logger.info(f"url: {url} | page_limit: {page_limit}")
    aliexpress = AliexpressScraping()
    items = aliexpress.fetch_items(url, page_limit)

    df = pd.DataFrame()
    for item in items:
        df = df.append(
            item.to_dict(), ignore_index=True
        )
    df.to_csv(f"item_{now_timestamp()}.csv", mode="w", encoding="utf-8_sig")


def requests(url :str, page_limit: int=5):
    logger.info(f"url: {url} | page_limit: {page_limit}")
    aliexpress = AliexpressRequests()
    items = aliexpress.fetch_items(url, page_limit)

    df = pd.DataFrame()
    for item in items:
        df = df.append(
            item.to_dict(), ignore_index=True
        )
    df.to_csv(f"item_{now_timestamp()}.csv", mode="w", encoding="utf-8_sig")


if __name__ == "__main__":
    fire.Fire()