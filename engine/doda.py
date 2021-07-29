import time

from common.selenium_manager import SeleniumManager
from models.job_offer import JobOffer

DODA_LOGIN_URL = ""
DODA_POST_PAGE_URL = ""

class DodaScraping():

    def __init__(self):
        self.manager = SeleniumManager()
        self.manager.start_chrome()

    def login(self, user_id: str, password: str):
        self.manager.chrome.get(DODA_LOGIN_URL)
        self.manager.chrome.find_element_by_css_selector("<username要素を指定>").send_keys("入力する文字列")
        self.manager.chrome.find_element_by_css_selector("<password要素を指定>").send_keys("入力する文字列")
        self.manager.chrome.find_element_by_css_selector("<loginボタン要素を指定>").click()

    def post_job_offer(self, job_offer: JobOffer):
        self.manager.chrome.get(DODA_POST_PAGE_URL)
        time.sleep(2)
        self.manager.chrome.find_element_by_css_selector("<要素を指定>").send_keys(job_offer.title)
        self.manager.chrome.find_element_by_css_selector("<要素を指定>").click()
