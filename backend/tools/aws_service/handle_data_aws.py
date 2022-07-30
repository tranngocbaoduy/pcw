import boto3
import base64
import pytz
import zlib
import os
import sys
import json
import argparse
import time
import datetime

from scrapy import Selector
from datetime import datetime
from bs4 import BeautifulSoup
from lxml import etree

# add directory to path 
file_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(file_dir + '/../..')
sys.path.append(os.path.normpath(root_dir))
from tools.aws_service.helper import S3Helper

parser = argparse.ArgumentParser()
parser.add_argument('--force', action='store_true')
parser.add_argument('env_name', type=S3Helper.env_regex_type)
parser.add_argument('--project-name', default='pcw')
parser.add_argument('--profile', default='pcw-admin')
parser.add_argument('--use-container', action='store_true')

args = vars(parser.parse_args())  
start_time = time.time() 

s3_helper = S3Helper(root_dir=root_dir + '/tools/aws_service', args=args)
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1',)

pages_table = dynamodb.Table('pcw-dev-PAGES')
goods_table = dynamodb.Table('pcw-dev-GOODS')

def pre_handle_goods_item(raw_goods_item, page_item):
    """
        handle goods item html raw to save to dynamodb
    """ 

    date_now = datetime.utcnow().isoformat()[:-3] + 'Z'
    goods_item = {}
    for name, values in raw_goods_item.items():
        goods_item[name.upper()] = ' '.join(values)
        
    PK = page_item.get('PK').split('#')[-1]
    SK = page_item.get('SK')
    category = page_item.get('CATEGORY', '')
    update_at = date_now

    item = {
        "PK": PK,
        "SK": SK,
        "UPDATE_AT": update_at,
        **goods_item
    }  
    return item

def extract_goods_from_page_item(page_item):

    goods_item = {} 
    html_text = zlib.decompress(page_item['HTML_TEXT_COMPRESSED'].value).decode('utf-8')
    xpath_raw = page_item.get('XPATH_ITEMS',[])
    xpath_items = json.loads(xpath_raw) if xpath_raw else []
    parsed_html = BeautifulSoup(html_text, 'html.parser')
    dom = etree.HTML(str(parsed_html))
    
    for name, selector in xpath_items.items():
        goods_item[name] = dom.xpath('{}//text()'.format(selector))

    new_goods_item = pre_handle_goods_item(goods_item, page_item)
    count_invalid = 0
    total_attr = len(new_goods_item.keys())
    for key, value in new_goods_item.items(): 
        if len(value) <= 0: count_invalid += 1 
    # if missing too much information, shouldn't save it to db
    return new_goods_item if count_invalid / total_attr <= 0.4 else None


def scan_all_page_item(scan_kwargs):
    items = [] 
    done = False
    start_key = None
    while not done: 
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        result = pages_table.scan(**scan_kwargs)
        items.extend(result.get('Items',[])) 
        start_key = result.get('LastEvaluatedKey', None)
        done = start_key is None
    return items

 
def extract_item_from_html(): 
    """
        get data from html
    """  
    s3_helper.remove_old_files() 
    scan_kwargs = {
        "TableName":"pcw-dev-PAGES", 
        "FilterExpression":"begins_with(PK, :pk)",
        "ExpressionAttributeValues":{
            ":pk": "UNPROCESSED"
        },
    } 
    page_items = scan_all_page_item(scan_kwargs)
    print("Found: {} items unprocessed".format(len(page_items)))  
    # for i in page_items:
    #     print(i['PK'], i['SK'])
    is_upload_data = False
    count_upload_file = 0
    if len(page_items) != 0:
        # print('1')
        for page_item in page_items:  
            # extract neccessary information
            new_goods_item = extract_goods_from_page_item(page_item)
            if new_goods_item is not None: 
                if is_update_data(new_goods_item):
                    # upload good to s3 and save a new one 
                    is_upload_data = True
                    count_upload_file += 1
                    save_file_local(new_goods_item.copy(), page_item.copy())
                # update page_item to processed 
                update_batch_page_item(page_item)
                new_goods_item["CATEGORY"] = 'fan'
                put_goods_item_to_db(new_goods_item) 
            else: 
                delete_page_item_db(page_item)
        if is_upload_data:
            print('upload data {} items'.format(count_upload_file))
            s3_helper.build_function()
            s3_helper.upload_to_s3()
            s3_helper.remove_old_files() 
    else:
        print("There's nothing to do")

def save_file_local(new_goods_item, page_item): 
    domain_name = page_item['PK'].split('#')[-1]
    domain_url_name = page_item['SK']
    func_dir = root_dir + '/tools/aws_service/function'
    date_now = datetime.utcnow().isoformat()[:-3] + 'Z'

    func_dir_data = os.path.join(func_dir, domain_name, domain_url_name, date_now)
    if not os.path.exists(func_dir_data):
        os.makedirs(func_dir_data) 

    page_item['PK'] = page_item['PK'].replace('UNPROCESSED', 'FINISHED')
    page_item['XPATH_ITEMS'] = json.loads(page_item['XPATH_ITEMS'])
    html_str = zlib.decompress(page_item['HTML_TEXT_COMPRESSED'].value).decode('utf-8')
    html_file= open(os.path.join(func_dir_data, "index.html"),'w') 
    html_file.write(html_str)
    html_file.close()

    with open(os.path.join(func_dir_data, "index.json"),'w') as file:
        del page_item['HTML_TEXT_COMPRESSED']
        param = {
            "raw": page_item,
            "processed": new_goods_item
        }
        json.dump(param, file)
        file.close()

def put_goods_item_to_db(item): 
    """
        save item after handling to dynamodb
    """ 
    try:
        if item: goods_table.put_item(Item= item) 
    except: 
        print('delete')
        goods_table.delete_item(
            Key={
                "PK": item['PK'],
                "SK": item['SK']
            }
        )     

def delete_page_item_db(item): 
    """
        delete item after handling to dynamodb
    """  
    try:
        pages_table.delete_item(
            Key={
                "PK": item['PK'],
                "SK": item['SK']
            }
        )   
    except:
        return False
    return True  

def update_goods_item_to_db(item): 
    """
        update item 
    """  
    if item: goods_table.update_item(
        TableName="pcw-dev-PAGES",
        FilterExpression="PK = :pk and begins_with(SK, :sk)",
        ExpressionAttributeValues={
            ":pk": PK,
            ":sk": SK
        }) 

def update_batch_page_item(page_item):  
    with pages_table.batch_writer() as batch: 
        batch.put_item(
            Item={
                **page_item,
                "PK": page_item["PK"].replace("UNPROCESSED","FINISHED")
            }) 
        batch.delete_item(Key={
            "PK": page_item['PK'],
            "SK": page_item['SK']
        }) 

def update_backdata_batch_page_item(): 
    scan_kwargs = {
        "TableName":"pcw-dev-PAGES", 
        "FilterExpression":"begins_with(PK, :pk)",
        "ExpressionAttributeValues":{
            ":pk": "FINISHED"
        },
    } 
    page_items = scan_all_page_item(scan_kwargs) 
    print("Found: {} items FINISHED".format(len(page_items))) 
    count_success = 0 
    if len(page_items) != 0:
        for page_item in page_items :
            with pages_table.batch_writer() as batch: 
                batch.put_item(
                    Item={
                        **page_item,
                        "PK": page_item["PK"].replace("FINISHED","UNPROCESSED")
                    }) 
                batch.delete_item(Key={
                    "PK": page_item['PK'],
                    "SK": page_item['SK']
                }) 
            count_success +=1
    print("Backup success: {} items".format(count_success)) 

def scan_goods_item(PK, SK):
    return goods_table.scan(
        TableName="pcw-dev-PAGES",
        FilterExpression="PK = :pk and begins_with(SK, :sk)",
        ExpressionAttributeValues={
            ":pk": PK,
            ":sk": SK
        })['Items']

def query_goods_item(PK):
    return goods_table.query(
        TableName="pcw-dev-PAGES",
        KeyConditionExpression="PK = :pk",
        ExpressionAttributeValues={
            ":pk": PK
        })['Items']

def is_update_data(old):
    new = is_existing_item(old['PK'], old['SK']) 
    if not new: return new 
    for key in old.keys():
        if old.get(key) != new.get(key): 
            return True 
    return False

def is_existing_item(PK, SK):
    params = {
        "PK": PK,
        "SK": SK
    } 
    return goods_table.get_item(Key=params).get('Item', False) 


extract_item_from_html()
# update_backdata_batch_page_item()
print('\n\nElapsed time: {} seconds -- {}'.format(int(time.time() - start_time), os.path.realpath(__file__)))  # nopep8