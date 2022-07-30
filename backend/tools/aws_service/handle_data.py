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
import glob

from re import sub
from decimal import *
from scrapy import Selector
from datetime import datetime
from bs4 import BeautifulSoup
from lxml import etree
from tqdm import tqdm

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
# dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1',)

# pages_table = dynamodb.Table('pcw-dev-PAGES')
# goods_table = dynamodb.Table('pcw-dev-GOODS')

def pre_handle_goods_item(raw_goods_item, page_item):
    """
        handle goods item html raw to save to dynamodb
    """ 

    date_now = datetime.utcnow().isoformat()[:-3] + 'Z'
    goods_item = {}
    for name, values in raw_goods_item.items(): 
        if name == 'rating_real':
            goods_item[name.upper()] = values
        elif name == 'images':
            goods_item[name.upper()] = [ i.strip() for i in values] 
        else:
            goods_item[name.upper()] = ' '.join(values).strip()
        
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
 

def handle_money(money_text):
    money_text = sub(r'[^\d\-.]', '', money_text.strip())
    return money_text

def extract_goods_from_page_item(page_item, is_pattern_xpath= False, is_save_html=False,):

    goods_item = {} 
    html_text = zlib.decompress(page_item['HTML_TEXT_COMPRESSED']).decode('utf-8')
    xpath_raw = page_item.get('XPATH_ITEMS',[])
    xpath_items = json.loads(xpath_raw) if xpath_raw else []
    parsed_html = BeautifulSoup(html_text, 'html.parser')
    if is_save_html:
        with open(os.path.join(file_dir,"output.html"), "w", encoding='utf-8') as file:
            file.write(str(parsed_html))
    if is_pattern_xpath:
        xpath_items = {}
        encode_url = page_item["PK"]
        decode_url = urlsafre_decode(encode_url)
        with open(os.path.join(file_dir,"model/common","xpath_{}-{}.json".format(encode_url,decode_url)), "r", encoding='utf-8') as file:
            items = json.load(file)
            for item in items:
                xpath_items[item['name']] = item['selector']
    dom = etree.HTML(str(parsed_html))
    
    count_invalid = 0
    if 'IS_FROM_API' in page_item.keys() and page_item['IS_FROM_API']: 
        try:
            site_json=json.loads(parsed_html.text)
            goods_item_from_tiki_json = handle_tiki_json(site_json)  
            new_goods_item = pre_handle_goods_item(goods_item, page_item) 
            new_goods_item['CATEGORY'] = page_item['CATEGORY_CUSTOM']
            new_goods_item["URL_API"] = urlsafre_decode(page_item["SK"]) 
            new_goods_item["DOMAIN"] = new_goods_item["PK"]
            new_goods_item.update(goods_item_from_tiki_json)
            total_attr = len(new_goods_item.keys())
            for key, value in new_goods_item.items(): 
                if value is None: count_invalid += 1  
            # if missing too much information, shouldn't save it to db
            new_goods_item["CONFIDENT_RATE"] = (total_attr-count_invalid) / total_attr
            new_goods_item["IS_CONFIDENT"] = True if (total_attr-count_invalid) / total_attr > 0.5 else False
            return new_goods_item
        except:
            return None
    else:
        # try:
            for name, selector in xpath_items.items(): 
                if name == 'price' or name == 'list_price':
                    price = 0
                    allowed_word = ['liên hệ']
                    for sel in selector:
                        price = dom.xpath('{}//text()'.format(sel))
                        if price:
                            price = ''.join(price).replace('/n','').strip() 
                            if price.lower() in allowed_word:  
                                goods_item[name] =  price
                                return None
                            if handle_money(price): 
                                goods_item[name] =  [handle_money(price)] if price else [''] 
                                break
                        else:  
                            for item_del in dom.cssselect('del'): 
                                if item_del.text: 
                                    goods_item[name] = [item_del.text]
                                    break

                    if name not in goods_item.keys():
                        goods_item[name] = ['']
                elif name == 'discount_rate':
                    discount_rate = ''
                    for sel in selector:
                        discount_rate = dom.xpath('{}//text()'.format(sel))  
                        if discount_rate: break
                    goods_item[name] =  [discount_rate[0]] if discount_rate else ['TYPE1'] 
                elif name == 'images': 
                    src_url = dom.xpath('{}/@data-src'.format(selector))  
                    if src_url == '' or len(src_url) == 0:
                        data_srcs =  dom.xpath(selector)
                        src_url = []
                        for item in data_srcs: 
                            u = item.attrib.get('src')
                            if u == None or len(u) == 0 or 'javascript:void(0)' in u: u = item.attrib.get('data-thumb') 
                            if u == None or len(u) == 0 or 'javascript:void(0)' in u: u = item.attrib.get('href')
                            if u != None: src_url.append('https://' + urlsafre_decode(page_item['PK']) + u) 
                        
                    goods_item[name] = [ item for item in src_url if item and item.startswith('https:')]
                    goods_item['THUMBNAIL_URL'] = [goods_item[name][0]] if len(goods_item[name]) != 0 else []
                elif name == 'rating_average': 
                    if page_item['PK'] == 'ZGlkb25nbWFuZ28uY29t' and selector:
                        sel = ''.join(dom.xpath('{}//text()'.format(selector)))
                        goods_item[name] = [sel.strip()]
                    elif page_item['PK'] == 'ZGlkb25ndGhvbmdtaW5oLnZu':
                        goods_item[name] = '0/5'
                        goods_item['rating_real'] = False
                    elif selector:
                        sel = dom.xpath('{}'.format(selector))
                        rated = str(len(sel)).strip()  
                        goods_item[name] = [rated,'/','5']
                        goods_item['rating_real'] = True
                    else:
                        goods_item[name] = '0/5'
                        goods_item['rating_real'] = False
                else:
                    goods_item[name] = dom.xpath('{}//text()'.format(selector))

            if page_item['PK'] == 'Y2VsbHBob25lcy5jb20udm4':
                for text in goods_item['name']:
                    if 'Tin đồn'.lower() in text.lower():
                        return None
                for text in goods_item['booking']:
                    if 'Sắp về hàng'.lower() in text.lower():
                        return None
            new_goods_item = pre_handle_goods_item(goods_item, page_item) 
            new_goods_item['CATEGORY'] = page_item['CATEGORY_CUSTOM']
            new_goods_item["URL_KEY"] = urlsafre_decode(page_item["SK"])
            new_goods_item["DOMAIN"] = new_goods_item["PK"]
            new_goods_item['IS_MANY_STORE'] = False         
            new_goods_item['PRICE'] = new_goods_item['PRICE'].replace('đ','').replace('.','').replace(',','')
            new_goods_item['LIST_PRICE'] = new_goods_item['LIST_PRICE'].replace('đ','').replace('.','').replace(',','')
            new_goods_item['DISCOUNT_RATE'] = new_goods_item['DISCOUNT_RATE'].replace('%','').replace(',','')
            if new_goods_item['PRICE'] and new_goods_item['LIST_PRICE']:
                if not new_goods_item['LIST_PRICE'].isnumeric(): 
                    if new_goods_item['PRICE'].isnumeric():
                        new_goods_item['LIST_PRICE'] = new_goods_item['PRICE']
                    else:
                        return None
                price = float(new_goods_item['PRICE']) 
                list_price = float(new_goods_item['LIST_PRICE']) 
                if price == 0 or list_price == 0: return None
                if list_price < price: list_price = price
                if(new_goods_item['DISCOUNT_RATE'] == 'TYPE1'): new_goods_item['DISCOUNT_RATE'] = -1 * int((list_price - price) / list_price * 100)
                new_goods_item['DISCOUNT'] = -1 * int(list_price - price)


            total_attr = len(new_goods_item.keys()) - 8
            for key, value in new_goods_item.items(): 
                if value is None or value == '': count_invalid += 1  
            # if missing too much information, shouldn't save it to db 
            new_goods_item["CONFIDENT_RATE"] = (total_attr-count_invalid) / total_attr
            new_goods_item["IS_CONFIDENT"] = True if (total_attr-count_invalid) / total_attr > 0.5 else False
            return new_goods_item
        # except:
        #     return None



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


def query_all_page_item(scan_kwargs):
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

def get_seller_tiki(obj):
    item = {}
    allowed_attribute = ["name", "link", "logo", "product_id", "price", "store_id"]
    for attr in allowed_attribute:
        res = obj.get(attr, '')
        if res: item[attr.upper()] = res
    return item
    
def handle_tiki_json(site_json):
    item = {} 
    allowed_attribute = ['id','name','url_key','price','list_price','discount','discount_rate','rating_average','review_count',\
                         'thumbnail_url','description','short_description','images','ranks','brand','current_seller','other_sellers',\
                        'specifications','price_comparison']
    for attr in allowed_attribute:
        res = site_json.get(attr,'')
        if res:
            if attr == 'images':
                res = [ image['base_url'] for image in res]
            if attr == 'url_key':
                res = site_json.get('url_path','')
            if attr == 'current_seller':
                res = get_seller_tiki(res)
            if attr == 'other_sellers':
                sellers = []
                for seller in res:
                    sellers.append(get_seller_tiki(seller))
                if len(sellers) != 0: item['IS_MANY_STORE'] = True
                res = sellers
            item[attr.upper()] = res
        else:
            item[attr.upper()] = None
    return item     

def get_all_page_item_unprocessed(allowed_category, allowed_domain):
    categories = glob.glob("{}/*".format(os.path.join(file_dir,'data/raw/2021-07-06'))) 
    list_items = []
    for cate_path in categories:
        print('category', cate_path.split('/')[-1])
        domain_items = glob.glob("{}/*".format(os.path.join(cate_path)))
        if cate_path.split('/')[-1] in allowed_category:
            for domain_path in domain_items:
                if domain_path.split('/')[-1] in allowed_domain:
                    url_items = glob.glob("{}/*".format(os.path.join(domain_path)))
                    print('\tdomain', domain_path.split('/')[-1],'=>', len(url_items), 'items')
                    for url_path in url_items: 
                        with open(os.path.join(url_path, 'index.txt'), 'rb') as f:
                            html_text_compressed = f.read()
                            f.close()
                        with open(os.path.join(url_path, 'index.json')) as f:
                            item = json.load(f)
                            f.close()
                        item["HTML_TEXT_COMPRESSED"] = html_text_compressed
                        item["CATEGORY_CUSTOM"] = cate_path.split('/')[-1]
                        list_items.append(item)
    return list_items

def urlsafre_encode(url):
    return base64.urlsafe_b64encode(url.encode("utf-8")).decode("utf-8").rstrip('=') if url else '' 

def urlsafre_decode(encoded_str):
    return base64.urlsafe_b64decode(encoded_str + '===').decode("utf-8") if encoded_str else ''
 
def extract_item_from_html(): 
    """
        get data from html
    """   

    # allowed_domain = ['ZGllbm1heXhhbmguY29t','dGlraS52bg','dm9zby52bg', 'bmd1eWVua2ltLmNvbQ','ZGllbm1heXhhbmguY29t', 'bWV0YS52bg']
    allowed_category = ['DienThoai']#,'MayGiat', 'TuLanh','Tivi',]
    allowed_domain = [ 
        # 'bmhhbmhhdnVpLmNvbS52bg', # nhanhavui.com.vn
        # 'bWVkaWFtYXJ0LnZu', # mediamart.vn
        # 'c2lldXRoaWdpYWtoby5jb20', # sieuthigiakho.com
        # 'cGljby52bg', # pico.vn
        # 'dmFuY2hpZW4uY29t',   #vanchien.com
        # 'ZGllbm1heXBsdXMuY29t', # dienmayplus.com
        # 'ZGllbm1heXNhaWdvbi5jb20udm4', # dienmaysaigon.com không get được hình
        # # 'ZGllbm1heXRoaWVuaG9hLnZu', # dienmaythienhoa.vn 2 sp
        # 'ZGllbm1heXRoYW5oLmNvbQ', # dienmaythanh.com
        # 'ZGllbm1heXRpbnBoYXQuY29t', # dienmaytinhphat.com
        # 'ZWNvLW1hcnQudm4',  # eco-mart.vn
        # 'ZXNob3BzLnZu', # eshops.vn
        'dGlraS52bg'
    ]

    # igorne_domain= [ 
    #     'bWVkaWFtYXJ0LnZu', #giá liên hệ 
    #     'ZGllbm1heXBsdXMuY29t', #gia liên hệ
    # ]
    page_items = get_all_page_item_unprocessed(allowed_category, allowed_domain)
    print("Found: {} items unprocessed".format(len(page_items)))   
    is_upload_data = False
    count_upload_file = 0
    count_skip_item = 0
    count_not_confident = 0
    count_no_price_item = 0
    count_none_iem = 0
    stat_attrib = {}
    if len(page_items) != 0: 
        for page_item in tqdm(page_items[:]):    
            # extract neccessary information
            # if s3_helper.is_exist_data(page_item) is False:
            new_goods_item = extract_goods_from_page_item(page_item, True, True)
            # print('new_goods_item',new_goods_item)
            # if new_goods_item['PRICE'] == '':
            
            if new_goods_item is not None: 
                # for k,v in new_goods_item.items():
                #     # if k == 'COMMENT' or k == 'GUARANTEE': continue
                #     print(k, end='')
                #     if k == 'URL_KEY': print('\t\t',v)
                #     elif type(v) == str and len(v) > 100: print('\t\t',v[:10])
                #     else: print('\t\t',v)
                # return     
                if new_goods_item['PRICE'] == '': 
                    if new_goods_item['PK'] in igorne_domain:
                        print("SKIP IGORNE DOMAIN") 
                        count_skip_item +=1
                        continue
                    if new_goods_item['IS_CONFIDENT'] == True: 
                        print('IS_CONFIDENT') 
                        print('NAME',new_goods_item['NAME'])
                        print('PRICE',new_goods_item['PRICE'])
                        print('LIST_PRICE',new_goods_item['LIST_PRICE'])
                        print('URL_KEY',new_goods_item['URL_KEY'])
                        count_no_price_item +=1
                        continue
                    if new_goods_item['IS_CONFIDENT'] == False: 
                        print("NOT IS_CONFIDENT") 
                        count_not_confident +=1 
                        continue
                    if new_goods_item['PRICE'] == '' and new_goods_item['LIST_PRICE'] == '' and new_goods_item['DISCOUNT_RATE'] == 'TYPE1':
                        print("SKIP") 
                        count_skip_item +=1
                        continue 
                    print("SKIPddd") 

                    count_no_price_item +=1
                else:
                    if('IMAGES' not in new_goods_item.keys() or len(new_goods_item['IMAGES'])== 0): print('no Image count_upload_file',count_upload_file)
                    if(new_goods_item['IS_CONFIDENT']): 
                        for k, v in new_goods_item.items():
                            if k not in stat_attrib:
                                if type(v) == str and len(v) > 250: stat_attrib[k] = 1
                            else:
                                if type(v) == str and len(v) > 250: stat_attrib[k] += 1
                        
                        if 'COMMENT' in new_goods_item.keys():
                            del new_goods_item['COMMENT']
                        s3_helper.write_handled_data(new_goods_item)
                    # print(new_goods_item)
                    count_upload_file +=1
                    # return 
            else:
                print('No')
                count_none_iem += 1
        # data_finished_dir = os.path.join('data/raw_finished')
        # s3_helper.copy_data_to(data_finished_dir)
        # s3_helper.remove_old_data()
        print('count_not_confident',count_not_confident)
        print('count_skip_item',count_skip_item)
        print('count_no_price_item',count_no_price_item)
        print('count_none_iem',count_none_iem)
        print('count_upload_file',count_upload_file)
        for k,v in stat_attrib.items():
            print(k,':',v)
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


def get_page_item(PK, SK):
    return pages_table.get_item(
        TableName="pcw-dev-PAGES",
        Key={
            "PK":PK,
            "SK":SK
        }).get('Item', False)

def query_goods_item(PK):
    return goods_table.query(
        TableName="pcw-dev-GOODS",
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