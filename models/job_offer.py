import pandas as pd

from common.logger import set_logger
logger = set_logger(__name__)

class JobOffer():

    def __init__(self, title: str, description: str, sarary: str):
        self.title = title
        self.description = description
        self.sarary = sarary

class JobOfferList():

    def __init__(self):
        self.job_offer_list: list[JobOffer] = []

    
    def read_job_offer_from_csv(self, csv_path: str):
        df = pd.read_csv(csv_path)
        for index, row in df.iterrows():
            self.job_offer_list.append(
                JobOffer(title=str(row["title"]), description=str(row["description"]), sarary=str(row["sarary"]))
            )
        logger.info(f"求人情報を {len(df)} 件 読み込みました")