import os
import sys
import json
import boto3
import argparse
import time

from decimal import Decimal
from json import JSONEncoder 
from get_code_from_product import GetCodeFromProduct


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


def put_pages_item_to_db(item): 
    """
        save item after handling to dynamodb
    """  
    if item: pages_table.put_item(Item= item)  

def put_goods_item_to_db(item): 
    """
        save item after handling to dynamodb
    """  
    if item: goods_table.put_item(Item= item)  

def build_item():

    helper = GetCodeFromProduct()
    helper.build()
    
    count_err_item = 0
    stat_code = {}
    stat_SK = {}
    count = 0
    for id_cate, items in helper.NEW_CATEGORY_ITEM_SET.items():
        for item in items:
            if item["CODE_PRODUCT"] == "NO_FOUND" or item["CODE_PRODUCT"] == "" or "CODE_PRODUCT" not in item.keys():
                count_err_item+=1 
            else:
                if "{}@{}".format(id_cate ,item["CODE_PRODUCT"]) not in stat_code.keys():
                    stat_code["{}@{}".format(id_cate, item["CODE_PRODUCT"])] = 1
                    stat_SK["{}@{}".format(id_cate, item["CODE_PRODUCT"])] = [item["SK"]]
                else:
                    stat_code["{}@{}".format(id_cate, item["CODE_PRODUCT"])] += 1 
                    stat_SK["{}@{}".format(id_cate, item["CODE_PRODUCT"])].append(item["SK"])
    total_count = 0
    brand_product_save = []
    category_save = []
    count_product_has_more_than_2_item=0
    count_single_item=0
    error = 0
    stat(stat_code, stat_SK, helper)
    total_product = 0
    all_item_save = [] 
    SK2ITEM_DICT = helper.SK2ITEM_DICT.copy()
    brands = []
    for cate_and_code, list_SK in stat_SK.items():
        quantity = len(list_SK)
        total_product += quantity
        if(quantity > 1):
            item_save = {}
            item_save['PK'] = 'PRODUCT'
            
            stores = []
            category = ''
            code_product = cate_and_code.split('@')[1]
            images = []
            domains = []
            brands 
            for sk in list_SK:
                item = SK2ITEM_DICT[sk]
                new_item = {}
                new_item['PK'] = item.get('PK','')
                new_item['SK'] = item.get('SK','')
                new_item['UPDATE_AT'] = item.get('UPDATE_AT','')
                new_item['NAME'] = item.get('NAME','')
                new_item['THUMBNAIL_URL'] = item.get('THUMBNAIL_URL','')
                new_item['PRICE'] = item.get('PRICE','')
                new_item['LIST_PRICE'] = item.get('LIST_PRICE','')
                new_item['DISCOUNT_RATE'] = item.get('DISCOUNT_RATE','')
                new_item['BRAND'] = item.get('BRAND','')
                if type(new_item['BRAND']) == dict: 
                    new_item['BRAND'] = new_item['BRAND']['name']
                new_item['RATING_AVERAGE'] = item.get('RATING_AVERAGE','')
                new_item['RATING_REAL'] = item.get('RATING_REAL','')
                new_item['CATEGORY'] = item.get('CATEGORY','')
                new_item['IS_MANY_STORE'] = item.get('IS_MANY_STORE','')
                new_item['DISCOUNT'] = item.get('DISCOUNT','')
                new_item['CONFIDENT_RATE'] = item.get('CONFIDENT_RATE','')
                new_item['IS_CONFIDENT'] = item.get('IS_CONFIDENT','')
                new_item['LIST_CODE_PRODUCT'] = item.get('LIST_CODE_PRODUCT','')
                new_item['CODE_PRODUCT'] = item.get('CODE_PRODUCT','')
                new_item['IMAGES'] = item.get('IMAGES','')
                new_item['DESCRIPTION'] = item.get('DESCRIPTION','')
                new_item['COMMENT'] = item.get('COMMENT','')
                images.extend(item.get('IMAGES',''))
                domains.append(item['PK'])
                stores.append(new_item)
                brands.append(new_item['BRAND'])
            item_save['STORE'] = stores
            item_save['DOMAIN'] = list(set(domains))
            item_save['CATEGORY'] = category 
            all_item_save.append(item_save) 
            
    # for k, v in stat_code.items(): 
    #     try:
    #         # if v != 1:
    #             count_product_has_more_than_2_item+=1
    #             total_count += len(stat_SK[k])
    #             code = k.split('@')[-1]
    #             for sk in stat_SK[k]:
    #                 try:
    #                     item = json.loads(json.dumps(helper.SK2ITEM_DICT[sk]), parse_float=Decimal) 
    #                     item["PK"] = item['CODE_PRODUCT']
        
    #                     if 'BRAND' in item.keys() and item['BRAND'] not in brand_product_save:
    #                         brand_product_save.append(item['BRAND']) 
    #                     del item['CODE_PRODUCT']
    #                     if item['CATEGORY'] not in category_save:
    #                         category_save.append(item['CATEGORY'])
    #                     # put_goods_item_to_db(item) 
    #                 except:
    #                     error+=1
    #                     print(sk)
    #                 # for k, v in item.items():
    #                 #     print(k, v)
    #                 # break
    #             # break
    #         # else:
    #         #     count_single_item +=1
    #     except:
    #         print(k, v)
    #             #   
    # # for brand in brand_product_save:
    # #     put_pages_item_to_db({
    # #             'PK': 'BRAND',
    # #             'SK': '{}'.format(brand),
    # #     })
    
    # # for category in category_save:
    # #     put_pages_item_to_db({
    # #             'PK': 'CATEGORY',
    # #             'SK': '{}'.format(category),
    # #     })

    print('\t\t\t===Total', len(helper.SK2ITEM_DICT.keys()),'handled items')
    print('In',len(stat_code.keys()), 'product found code, there\'re:')
    print('\t- upper_2_in_product', count_product_has_more_than_2_item, 'total_item',total_count)
    print('\t- 1_in_product', count_single_item, 'total_item', count_single_item)
    print('\t- count_err_item', count_err_item)
    print('\t===\t') 
    

def stat(stat_code, stat_SK, helper):

    stat = {}
    for k, v in stat_code.items(): 
        if v != 1: 
            _id = k.split('@')[0]
            if _id not in stat:
                stat[_id] =1
            else:
                stat[_id] +=1
            for sk in stat_SK[k]:
                item = helper.SK2ITEM_DICT[sk] 
                if '{}@{}'.format(_id,item['CATEGORY']) not in stat:
                    stat['{}@{}'.format(_id,item['CATEGORY'])] =1
                else:
                    stat['{}@{}'.format(_id,item['CATEGORY'])] +=1
    print('STAT:',stat) 

def scan_all_item():
    scan_kwargs = {
        "TableName":"pcw-dev-PAGES", 
        "FilterExpression":"begins_with(PK, :pk)",
        "ExpressionAttributeValues":{
            ":pk": "UNPROCESSED"
        },
    } 
    items = scan_all_good_item(scan_kwargs)
    # filter

def scan_all_good_item(scan_kwargs):
    items = [] 
    done = False
    start_key = None
    while not done: 
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        result = goods_table.scan(**scan_kwargs)
        items.extend(result.get('Items',[])) 
        start_key = result.get('LastEvaluatedKey', None)
        done = start_key is None
    return items
if __name__ == "__main__":
    build_item()