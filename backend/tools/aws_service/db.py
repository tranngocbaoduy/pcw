import boto3
import base64
import pytz
import zlib
import json
import os
import sys

from scrapy import Selector
from datetime import datetime, date
from bs4 import BeautifulSoup
from lxml import etree
from json import JSONEncoder
from decimal import Decimal 


# import crawling_service.PCW.crawling.models as model

file_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(file_dir) 

dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')

pages_table = dynamodb.Table('pcw-dev-PAGES')
 
item = {
    "PK": 'Domain#aHR0cHM6Ly92b3NvLnZuLwo=',
    "SK": '2021-05-29T04:05:59.843Z#aHR0cHM6Ly92b3NvLnZuL2dpYS1vYWktMS1wMjU0NTkuaHRtbAo=',
    "category": 'tivi',
    "html_compressed": '123'
}

raw_item = {
    "domain": "https://voso.vn/",
    "URL": "https://voso.vn/gia-treo-khung-treo-tivi-3243inch-goc-xoay-2-thanh-don-hang-loai-1-p25459.html",
    
}

def urlsafre_encode(url):
    return base64.urlsafe_b64encode(url.encode("utf-8")).decode("utf-8").rstrip('=') if url else '' 

def urlsafre_decode(encoded_str):
    return base64.urlsafe_b64decode(encoded_str + '===').decode("utf-8") if encoded_str else '' 

def pre_handle_item(item):
    """
        handle item html raw to save to dynamodb
    """
    date_now = datetime.utcnow().isoformat()[:-3] + 'Z'
    domain_encoded = urlsafre_encode(item.get('domain',''))
    url_encoded = urlsafre_encode(item.get('URL','')) 
    xpathItems = item.get('parser','')
    is_from_api = item.get('is_from_api','')

    if len(domain_encoded) == 0 or len(url_encoded) == 0:
        return None 

    item = {
        "PK": "{0}".format(domain_encoded),
        "SK": url_encoded,
        "HTML_TEXT_COMPRESSED": item.get('html_text_compressed'),
        "CATEGORY": item.get('category'),
        "XPATH_ITEMS": json.dumps(xpathItems), 
        "IS_FROM_API": is_from_api
    }  
    return item

import re

def no_accent_vietnamese(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s

class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

def put_scrapy_item(item): 
    """
        save item after handling to dynamodb
    """

    today = str(date.today())
    date_now = datetime.utcnow().isoformat()[:-3] + 'Z'
    with open(os.path.join(root_dir, 'category.json'),'r') as f:
        cur_categories = json.load(f)
    
    new_item = pre_handle_item(item) 
    category = '_'.join(no_accent_vietnamese(new_item['CATEGORY']).split())
    for cur_cate, items in cur_categories.items():
        if category in items:
            classify_category = cur_cate
            break
    html_dir_data = os.path.join(root_dir, 'data/raw', today, classify_category, new_item['PK'], new_item['SK'])
    if not os.path.exists(html_dir_data): 
        os.makedirs(html_dir_data) 
 
    # html_str = zlib.decompress(new_item['HTML_TEXT_COMPRESSED']).decode('utf-8')
    # html_file= open(os.path.join(html_dir_data, "index.html"),'w') 
    # html_file.write(html_str)
    html_str_compressed = new_item['HTML_TEXT_COMPRESSED']
    with open(os.path.join(html_dir_data, 'index.txt'), 'wb') as f:
        f.write(html_str_compressed)
        f.close()

    del new_item['HTML_TEXT_COMPRESSED'] 

    with open(os.path.join(html_dir_data, 'index.json'), 'w') as f:
        json.dump(new_item, f, ensure_ascii=False, indent=4,cls=Encoder)
        f.close()

    print('successfully')


    # try:
    # if new_item: pages_table.put_item(Item= new_item) 
    # except:
    #     print('delete_item')
    #     pages_table.delete_item(
    #         Key={
    #             "PK": new_item['PK'],
    #             "SK": new_item['SK']
    #         }
    #     )      


# extract_item_from_html()  