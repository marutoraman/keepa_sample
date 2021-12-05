# -*- coding: utf-8 -*-
from datetime import datetime as dt
from bs4 import BeautifulSoup as bs
import requests
import re
import ssl
import urllib.request
import urllib.error
import io
import boto3

def now_timestamp():
    return dt.now().strftime("%Y-%m-%d_%H_%M_%S")

def list_to_bool(l:list):
    bool_list=[]
    for item in l:
        bool_list.append(False if item == "0" or item == 0 else True)
    
    return bool_list

def create_proxy_dict(id,password,host,port,proxy_flg=True):
    if proxy_flg:
        proxy_url=f"http://{id}:{password}@{host}:{port}"
        return {
            "http": proxy_url,
            "https": proxy_url
        }
    else:
        return {}

def get_global_ip():
    #return socket.gethostbyname(socket.gethostname())
    try:
        res = requests.get("http://inet-ip.info/")
        soup = bs(res.text, "html.parser")
        return soup.select_one("table tbody tr td:nth-child(2)").text
    except Exception as e:
        print(e)
        return None
    
    
def split_list(l, n):
    """
    リストをサブリストに分割する
    :param l: リスト
    :param n: サブリストの要素数
    :return: 
    """
    for idx in range(0, len(l), n):
        yield l[idx:idx + n]


def fetch_currency_rate(base: str, to: str):
    res = requests.get("http://fx.mybluemix.net/")
    res.raise_for_status()
    res_dict = res.json()
    try:
        return res_dict["result"]["rate"][base + to]
    except:
        raise Exception(f"exchange currency error: {base}->{to}")
    

def min_ignore_none(input: list):
    try:
        return min(value for value in input if value is not None)
    except:
        return None
    


def re_search(pettern: str, target: str):
    try:
        m = re.search(pettern, target)
        if m == None:
            return None
        else:
            try:
                return m.group(1)
            except:
                return None
    except:
        return None
    
def datetime_to_string(input_datetime, format: str="%Y-%m-%d %H:%M:%S"):
    return dt.strftime(input_datetime, format)


def download_image_to_byte(url: str):
    try:
        ext = url.split(".")[-1]
    except:
        ext = ""
        
    # 画像URLからダウンロード
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        with urllib.request.urlopen(url) as web_file:
            return io.BytesIO(web_file.read())
    except urllib.error.URLError as e:
        print(e)
        raise Exception(f"image download error: {e}")