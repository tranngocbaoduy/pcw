# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class PageInfoItem(Item):
    URL = Field()
    encoded_base_url = Field()
    title = Field()
    meta = Field() 
    id = Field() 
    pass

class ProductInfoItem(Item):
    URL = Field()
    encoded_base_url = Field()
    title = Field()
    meta = Field()  
    description = Field()
    price = Field()
    name = Field()
    list_price = Field()
    category = Field() 
    list_image = Field() 
    pass


# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import json
from json import JSONEncoder


class RawProductItem(scrapy.Item):
    url = scrapy.Field()
    sk = scrapy.Field()
    base_encoded_url = scrapy.Field()
    slug_id = scrapy.Field()
    voucher_info = scrapy.Field()
    html_text_compressed = scrapy.Field()
    domain = scrapy.Field()
    agency = scrapy.Field()
    xpath = scrapy.Field()
    is_api = scrapy.Field()
    shopid = scrapy.Field()
    created_date = scrapy.Field()


class ProductItem(scrapy.Item):
    id_pcw = scrapy.Field()
    name = scrapy.Field()
    clean_name = scrapy.Field()
    product_code = scrapy.Field()
    category_code = scrapy.Field()
    main_category_code = scrapy.Field()
    category_code_from_title = scrapy.Field()
    image = scrapy.Field()
    seller_name = scrapy.Field()
    brand = scrapy.Field()
    brand_from_title = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    historical_sold = scrapy.Field()
    liked_count = scrapy.Field()
    shop_location = scrapy.Field()
    item_rating = scrapy.Field()
    list_price = scrapy.Field()
    content = scrapy.Field()
    slug_id = scrapy.Field()
    voucher_info = scrapy.Field()
    shop_item = scrapy.Field()
    description = scrapy.Field()


# subclass JSONEncoder
class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
