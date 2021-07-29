from logging import exception
import os
import sys
# プロジェクトルートをPATHに追加
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# 環境変数(.env)の読み込み
from dotenv import load_dotenv
load_dotenv()

# 自作モジュールを読み込み
from engine.doda import DodaScraping
from models.job_offer import JobOfferList, JobOffer

# ログ出力設定
from common.logger import set_logger
logger = set_logger(__name__)


def main():
    doda = DodaScraping()
    user_id = os.environ.get('DODA_USER_ID')
    password = os.environ.get('DODA_USER_PASSWORD')
    
    # UserID、パスワードの確認
    if not user_id or not password:
        logger.error("DODAのuser_idもしくはpasswordが設定されていません")
        return None

    # CSVから求人情報を読み込み
    job = JobOfferList()
    job.read_job_offer_from_csv("files/job_sample.csv")

    # 求人情報を登録
    doda.login(user_id, password)
    for i, job_offer in enumerate(job.job_offer_list):
        try:
            doda.post_job_offer(job_offer)
            logger.info(f"{i+1} 件目: 求人登録完了 | {job_offer.title}")
        except exception as e:
            logger.error(f"{i+1} 件目: ！求人登録エラー！ | {job_offer.title} | {e}")


main()