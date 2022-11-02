import os
import sys
import datetime
import json
import base64
import re
import time
import random
import uuid

from decimal import *
from urllib.parse import urlparse
from json import JSONEncoder
from pprint import pprint
from tqdm import tqdm
from price_parser import Price
from bs4 import BeautifulSoup
from lxml import etree
from django.forms.models import model_to_dict
from modules.crawler.handlers.utils import SettingService, CrawlingHelper
from pyvi import ViTokenizer, ViPosTagger

file_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(file_dir + "/..")
sys.path.append(os.path.normpath(root_dir))


class Encoder(JSONEncoder):
    def default(self, o):
        try:
            return o.__dict__
        except:
            return float(o)


class ExtractorService(object):
    @staticmethod
    def update_item_db(new_item, old_item, model):
        keys = model._meta.get_fields()
        old_item = model_to_dict(old_item)
        for key in keys:
            if new_item.get(key, "") != old_item.get(key, ""):
                old_item[key] = new_item[key]
        return old_item

    @staticmethod
    def handle_brand_name(brand, product_name):
        setting_brand_items = SettingService.get_all_setting_brand_items()
        brand_from_title = SettingService.get_brand_from_name(
            product_name, setting_brand_items
        )
        if brand == brand_from_title:
            return brand
        if brand == "" and brand_from_title != "":
            return brand_from_title
        if not brand and brand_from_title != "":
            return brand_from_title
        return brand

    @staticmethod
    def handle_get_slug_id_from_name(name):
        slug_id = "/" + CrawlingHelper.no_accent_vietnamese(name)
        slug_id = slug_id.replace("[", "(")
        slug_id = slug_id.replace("]", ")")
        slug_id = slug_id.replace("-", "")
        slug_id = slug_id.replace(" ", "-")
        return slug_id

    @staticmethod
    def handle_extract_information_from_json(response):

        domain = response.get("domain", " ")
        agency = response.get("agency", " ")
        seller = response.get("seller", None)
        tree_category = response.get("tree_category", None)

        base_item = dict() 
        base_item["name"] = response.get("name", "").strip()
        base_item["url"] = response.get("url", "")
        base_item["domain"] = domain
        base_item["agency"] = agency
        if seller: base_item["seller"] = seller
        if tree_category: base_item["tree_category"] = tree_category
        base_item["clean_name"] = ExtractorService.handle_get_clean_name(
            response.get("name", "")
        ).strip()
        base_item["category"] = response.get("category", "")
        base_item["category_code"] = response.get("category_code", "")
        base_item["brand"] = ExtractorService.handle_brand_name(
            response.get("brand", ""), response.get("name", "")
        )
        base_item["product_code"] = ExtractorService.handle_get_code(
            response.get("name", ""),
            response.get("category_code", ""),
            base_item["brand"].lower(),
        )
        base_item["image"] = json.dumps(response.get("image", []))
        base_item["slug_id"] = ExtractorService.handle_get_slug_id_from_name(
            response.get("name", "")
        )
        base_item["price"] = response.get("price", "")
        base_item["list_price"] = response.get("list_price", "")
        base_item["scraper_type"] = response.get("scraper_type", "")

        if domain == "lazada.vn":
            base_item["slug_id"] = response.get("itemUrl", "").replace(
                "//www.lazada.vn/products", ""
            )
            base_item["brand"] = response.get("brandName", "").strip()
            base_item["image"] = [response.get("image", "").strip()]
            if response.get("sellerName", ""):
                base_item["shop"] = {
                    "shop_id": response.get("sellerId", ""),
                    "shop_name": response.get("sellerName", ""),
                }
            else:
                base_item["shop"] = None
            base_item["price"] = response.get("price", 0)
            base_item["list_price"] = response.get(
                "originalPrice", response.get("price", 0)
            )
            base_item["stock"] = 10 if response.get("inStock", "") else 0
            base_item["historical_sold"] = 0
            base_item["liked_count"] = 0
            base_item["item_rating"] = {
                "rating_star": int(Decimal(response.get("ratingScore", 0))),
                "rating_count": [
                    int(response.get("review", 0) if response.get("review", 0) else 0),
                    int(response.get("review", 0) if response.get("review", 0) else 0),
                    0,
                    0,
                    0,
                    0,
                ],
                "rcount_with_context": int(
                    response.get("review", 0) if response.get("review", 0) else 0
                ),
                "rcount_with_image": 0,
            }
            # base_item['content'] = response.get('short_description',"").strip()
            # base_item['voucher_info'] = None
            base_item["description"] = response.get("description", [])

        if domain == "tiki.vn":
            official_shop = (
                []
            )  # list(filter(lambda x: x.get('id', '') == response.get('shopid', None) , list_seller))

            if len(official_shop) == 1:
                official_shop = official_shop[0]
                base_item["shop"] = {
                    "shop_id": official_shop.get("id", ""),
                    "shop_name": official_shop.get("seller_name", ""),
                    "shop_logo": official_shop.get("logo", ""),
                    "shop_level": official_shop.get("store_level", "NONE"),
                    "shop_url": official_shop.get("url_slug", ""),
                }
            else:
                official_shop = None
                base_item["shop"] = None

            base_item["slug_id"] = "/{}".format(response.get("url_key", ""))
            base_item["brand"] = response.get("brand_name", "").strip()
            base_item["image"] = [response.get("thumbnail_url", "").strip()]
            base_item["price"] = response.get("price", "")
            base_item["list_price"] = response.get("list_price", "")
            base_item["stock"] = (
                response.get("stock_item", "")["qty"]
                if response.get("stock_item", "")
                else 0
            )
            base_item["historical_sold"] = (
                response.get("quantity_sold", "")["value"]
                if response.get("quantity_sold", "")
                else 0
            )
            base_item["liked_count"] = 0
            base_item["item_rating"] = {
                "rating_star": int(response.get("rating_average", "")),
                "rating_count": [
                    response.get("review_count", ""),
                    response.get("review_count", ""),
                    0,
                    0,
                    0,
                    0,
                ],
                "rcount_with_context": response.get("review_count", ""),
                "rcount_with_image": 0,
            }
            # base_item['content'] = response.get('short_description',"").strip()
            # base_item['voucher_info'] = None
            base_item["description"] = [response.get("short_description", "")]

        if domain == "1shopee.vn":
            official_shop = list(
                filter(
                    lambda x: x.get("shopid", "") == response.get("shopid", None),
                    list_seller,
                )
            )
            if len(official_shop) == 1:
                official_shop = official_shop[0]
                base_item["shop"] = {
                    "shop_id": official_shop.get("shopid", ""),
                    "shop_name": official_shop.get("name", ""),
                    "shop_level": official_shop.get("store_level", ""),
                }
            else:
                official_shop = None
                base_item["shop"] = None

            url_obj = urlparse(response.get("url", ""))
            slug_arr = url_obj.path.split(".")
            base_item["slug_id"] = ".".join(slug_arr[:-2])
            base_item["brand"] = response.get("brand", "")
            base_item["image"] = [
                "https://cf.shopee.vn/file/{}".format(image)
                for image in response.get("images", "")
            ]
            base_item["stock"] = response.get("stock", "")
            base_item["item_rating"] = response.get("item_rating", "")
            base_item["historical_sold"] = response.get("historical_sold", "")
            base_item["liked_count"] = response.get("liked_count", "")
            base_item["price"] = int(response.get("price", "")) / 100000
            base_item["list_price"] = int(response.get("price_max", "")) / 100000
            base_item["slug_id"] = response.get("slug_id", "")
            # base_item['voucher_info'] = response.get('voucher_info',"")

            not_allow_brand = [
                "nobrand",
                "no brand",
                "No brand",
                "No Brand",
                0,
                "0",
                "",
                "none",
            ]
            if (
                (
                    base_item["brand"] == 0
                    or base_item["brand"].lower() not in not_allow_brand
                    or len(base_item["brand"]) == 0
                )
                and base_item["brand_from_title"]
                and len(base_item["brand_from_title"]) != 0
            ):
                base_item["brand"] = base_item["brand_from_title"]

            base_item["description"] = []

        return base_item

    @staticmethod
    def remove_string_in_splash(text):
        if "(" in text and ")" in text:
            start_index = text.index("(")
            end_index = text.index(")")
            remove_str = text[start_index : end_index + 1]
            text = text.replace(remove_str, "")
        return text

    @staticmethod
    def remove_string_in_square_splash(text):
        if "[" in text and "]" in text:
            start_index = text.index("[")
            end_index = text.index("]")
            remove_str = text[start_index : end_index + 1]
            text = text.replace(remove_str, "")
        return text

    @staticmethod
    def handle_get_clean_name(text):
        text = "".join(text).strip().lower()
        text = re.sub(
            "/[^a-z0-9A-Z_ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂưăạảấầẩẫậắằẳẵặẹẻẽềềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễếệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ]/u",
            "",
            text,
        )
        text = re.sub(" +", " ", text)
        count = 0
        while count < 2:
            text = ExtractorService.remove_string_in_splash(text)
            text = ExtractorService.remove_string_in_square_splash(text)
            count += 1
        text = re.sub("[\[\]\-\/\\!,*)@#%(&$_?.^]\,", " ", text)
        return text

    @staticmethod
    def is_large_2_digits_and_not_is_number(text):
        return len(text) > 2 and not text.isnumeric()

    @staticmethod
    def get_config_filter_of_category(category):
        remove_word = ["/intel", "/", "-"]
        list_keep_word = []
        allowed_brand = []
        list_stop_word = []
        is_allowed_2_digits = False
        dict_replace_word = {}
        if category == "ELECTRIC_STOVE":
            list_stop_word = ["papa", "cook"]
            is_allowed_2_digits = False
        elif category == "Phone":
            list_stop_word = [
                "galaxy",
                "-",
                "iphone",
                "redmi",
                "fullbox",
                "pixel",
                "z",
                "rog",
                "phone",
                "gaming",
                "reno",
                "note",
                "xperia",
            ]
            is_allowed_2_digits = True
            list_keep_word = ["pro", "promax", "reno", "note", "z", "redmi", "xperia"]
            dict_replace_word = {
                " reno 4 ": " reno4 ",
                " reno 5 ": " reno5 ",
                " reno 6 ": " reno6 ",
                " reno 6z ": " reno6 z ",
                " reno 7 ": " reno7 ",
                " reno 7z ": " reno7 z ",
                " reno 8 ": " reno8 ",
                " reno 9 ": " reno9 ",
                " reno 10 ": " reno10 ",
                " flip 2 ": " flip2 ",
                " flip 3 ": " flip3 ",
                " flip 4 ": " flip4 ",
                " flip 5 ": " flip5 ",
                " fold 2 ": " fold2 ",
                " fold 3 ": " fold3 ",
                " fold 4 ": " fold4 ",
                " fold 5 ": " fold5 ",
                " ss galaxy ": " samsung galaxy ",
                " điện thoại ss ": " điện thoại samsung ",
                " điện thoại galaxy ": " điện thoại samsung galaxy ",
                " pro max ": " promax ",
                " ip ": " iphone ",
                " pixel 6pro ": " pixel 6 pro ",
                " xs max ": " xsmax ",
            }
            allowed_brand = [
                "apple",
                "samsung",
                "xiaomi",
                "oppo",
                "sony",
                "vivo",
                "asus",
                # 'lenovo', 'huawei',  'google', 'microsoft', 'vsmart',
                # 'lp', 'realme', 'sony', 'vivo'
            ]
        elif category == "FRIDGE":
            list_stop_word = [
                "inverter",
                "side",
                "by",
                ",",
                "mini",
                "lan",
                "multidoor",
                "twin",
                "multi",
                "hai",
                "door",
                "nha",
                "dung",
                "cao",
                "sinh",
                "90%",
                "lanh",
                "zin",
                "electric",
                "qua",
                "motor",
                "cho.",
                "in",
                "cho",
                "hcm",
                "13hn",
                "553/515",
                "dc8v",
            ]
            list_keep_word = []
            allowed_brand = [
                "aqua",
                "alaska",
                "casper",
                "bosch",
                "electrolux",
                "funiki",
                "hitachi",
                "panasonic",
                "samsung",
                "sanyo",
                "sharp",
                "toshiba",
                #    'kaff', 'kamegara', 'kangaroo', 'kemin', 'lg', 'lock&lock', 'malloca', 'midea',
                #    'misubis', 'mitsubishi', 'oem', 'sanaky', 'suka', 'sumikura', 'tiross','tupperware', 'whirlpool', 'xiaomi',
                #    'akashi', 'amoi', 'ata', 'bases', 'bebe', 'beko', 'brother',
                #    'carrier', 'caso', 'china','daewoo', 'darling','dkw', 'goodlife', 'hafele',
            ]
            dict_replace_word = {
                " sl 16c3 ": " sl-16c3 ",
                "/sv ": " ",
                ".model2022": "",
                ".model2020": "",
                ".model2021": "",
                ".model2019": "",
                ".new100%": "",
                ".fullbox": "",
                ".md2019": "",
                ".md2020": "",
                ".md2021": "",
                ".md2022": "",
            }
            is_allowed_2_digits = False
        elif category == "LAPTOP" or category == "COMPUTER":
            list_stop_word = [
                "aspire",
                "digital",
                "cooling",
                "swift",
                "travelmate",
                "plus",
                "x",
                "b3",
                "gaming",
                "macbook",
                "mac",
                "vivobookslate",
                "vivobook",
                "zenbook",
                "flip",
                "oled",
                "evo",
                "tuf",
                "expertbook",
                "f15",
                "14x",
                "15x",
                "rog",
                "strix",
                "dash",
                "15s",
                "14s",
                "essential",
                "notebook",
                "core",
                "340s",
                "intel",
                "probook",
                "x360",
                "gram",
                "modern",
                "series",
                "ship",
                "1tr5",
            ]
            is_allowed_2_digits = True
        elif category == "TELEVISION":
            list_stop_word = [
                "inch",
                "led",
                "wifi",
                "-",
                "crystal",
                "hd",
                "uhd",
                "smart",
                "tv",
                "tivi",
                "android",
                "model",
                "10.0",
                "9.0",
                "the",
                "qled",
                "neo",
                "ltv",
                "full",
                "inchsmart",
                "khung",
                "fhd",
                "serif",
                "frame",
                "mini",
                "freestyle",
                "islim",
                "series",
                "thanh",
                "new",
                "udh",
                "oled",
            ]
            allowed_brand = [
                "aqua",
                "asanzo",
                "casper",
                "tcl",
                "coocaa",
                "samsung",
                "sharp",
                "sony",
                "lg",
                "panasonic",
                "philips",
                #  'darling', 'ffalcon',  'tvb',  'xiaomi',
            ]
            dict_replace_word = {
                "kxxv": "",
                " tv ": " tivi ",
                "/z": "",
                "/s": "",
                '"': "",
                "''": "",
                ".fullbox": "",
                ".model2022": "",
                ".model2020": "",
                ".model2021": "",
                ".model2019": "",
                ".new100%": "",
                ".fullbox": "",
                ".md2019": "",
                ".md2020": "",
                ".md2021": "",
                ".md2022": "",
                "-dienmaysieure.net": "",
            }
            is_allowed_2_digits = False
        elif category == "WATCH_MAN" or category == "WATCH_WOMAN":
            list_stop_word = []
            is_allowed_2_digits = False
        return (
            list_stop_word,
            is_allowed_2_digits,
            remove_word,
            list_keep_word,
            dict_replace_word,
            allowed_brand,
        )

    @staticmethod
    def replace_word_consistent(text, dict_replace_word):
        for key, value in dict_replace_word.items():
            if key in text:
                text = text.replace(key, value)
        return text

    @staticmethod
    def is_word_valid(text, category):
        if category == "FRIDGE" and (
            re.match(r"[0-9]+l", text)
            or re.match(r"[0-9]+%", text)
            or re.match(r"[0-9]+v", text)
            or re.match(r"[0-9]+[0-9]+", text)
            or re.match(r"[0-9]+.[0-9]+cm", text)
            or re.match(r"[0-9]+.[0-9]+w", text)
        ):
            return False
        if category == "PHONE" and re.match(r"[0-9]+4310mah", text):
            return False
        if category == "TELEVISION" and (
            re.match(r"[0-9]+inch", text)
            or re.match(r"[0-9]+k", text)
            or re.match(r"pro[0-9]+", text)
        ):
            return False
        return True

    @staticmethod
    def get_last_n_word(list_text, from_index, category, n=3):
        (
            list_stop_word,
            is_allowed_2_digits,
            remove_word,
            list_keep_word,
            dict_replace_word,
            _,
        ) = ExtractorService.get_config_filter_of_category(category)
        last_n_word = []
        from_index += 1
        count = 0
        check = False
        for i, text in enumerate(list_text):
            text = text.replace(",", "")
            for k in remove_word:
                len_k = len(k)
                start_index = len(text) - len_k
                end_index = len(text)
                if len(text) > len_k and text[start_index:] == k:
                    text = text[: start_index - 1]
            if i == from_index:
                from_index += 1
                if text == "rog":
                    check = True
                if text not in list_stop_word:
                    if not ExtractorService.is_word_valid(text, category):
                        continue
                    if is_allowed_2_digits:
                        last_n_word.append(text)
                        count += 1
                    else:
                        if ExtractorService.is_large_2_digits_and_not_is_number(text):
                            last_n_word.append(text)
                            count += 1

                if count == n:
                    break

        for keep_word in list_keep_word:
            if keep_word in list_text[:from_index]:
                last_n_word.insert(0, keep_word)
            if keep_word in list_text[from_index:]:
                last_n_word.append(keep_word)
        # if check == True: print('-', k, list_text, ' - ', last_n_word)
        # if k == True: print('-', k, list_text, ' - ', last_n_word)
        return last_n_word

    @staticmethod
    def get_stop_word(category):
        with open(os.path.join(file_dir,'stop_word/common.txt'), 'r') as f:
            common_stop_word =  f.read().split('\n')
        stop_word_of_category_dir = os.path.join(file_dir,'stop_word/{}.txt'.format(category))
        category_stop_word = []
        if os.path.isfile(stop_word_of_category_dir):
            with open(stop_word_of_category_dir, 'r') as f2:
                category_stop_word = f2.read().split('\n') 
        else:
            with open(stop_word_of_category_dir, 'w') as f:
                f.write('')
        return common_stop_word + category_stop_word

    @staticmethod
    def get_keep_word(category):
        with open(os.path.join(file_dir,'keep_word/common.txt'), 'r') as f:
            common_keep_word =  f.read().split('\n')
        keep_word_of_category_dir = os.path.join(file_dir,'keep_word/{}.txt'.format(category))
        category_keep_word = []
        if os.path.isfile(keep_word_of_category_dir):
            with open(keep_word_of_category_dir, 'r') as f2:
                category_keep_word = f2.read().split('\n') 
        else:
            with open(keep_word_of_category_dir, 'w') as f:
                f.write('') 
        return common_keep_word + category_keep_word

    @staticmethod
    def handle_get_code(text, category, brand):
        NUMBER_WORD_KEEPER = 2
        STOP_WORD = ExtractorService.get_stop_word(category)
        KEEP_WORD = ExtractorService.get_keep_word(category)
        text = ExtractorService.handle_get_clean_name(text)
        sents, postagging = ViPosTagger.postagging(ViTokenizer.tokenize(u"{}".format(text)))
        final_code = [brand] 
        for index, pos in enumerate(postagging):
            tags = sents[index].split('_')
            flag = True
            for m in tags:
                if m in STOP_WORD:
                    flag = False
            if sents[index] and sents[index] != '':
                if sents[index] in KEEP_WORD: 
                    final_code.append(sents[index])
                elif (pos == 'N' or pos == 'V' or (pos == 'M' and len(pos) <= 2)) and flag and sents[index] not in final_code: 
                    final_code.append(sents[index]) 
        if NUMBER_WORD_KEEPER < len(final_code) and final_code[NUMBER_WORD_KEEPER].isnumeric(): return " ".join(final_code[:NUMBER_WORD_KEEPER + 1])
        if len(final_code) != 1: return " ".join(final_code[:NUMBER_WORD_KEEPER])
        return "NONE"

    @staticmethod
    def no_accent_vietnamese(s):
        s = re.sub(r"[àáạảãâầấậẩẫăằắặẳẵ]", "a", s)
        s = re.sub(r"[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]", "A", s)
        s = re.sub(r"[èéẹẻẽêềếệểễ]", "e", s)
        s = re.sub(r"[ÈÉẸẺẼÊỀẾỆỂỄ]", "E", s)
        s = re.sub(r"[òóọỏõôồốộổỗơờớợởỡ]", "o", s)
        s = re.sub(r"[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]", "O", s)
        s = re.sub(r"[ìíịỉĩ]", "i", s)
        s = re.sub(r"[ÌÍỊỈĨ]", "I", s)
        s = re.sub(r"[ùúụủũưừứựửữ]", "u", s)
        s = re.sub(r"[ƯỪỨỰỬỮÙÚỤỦŨ]", "U", s)
        s = re.sub(r"[ỳýỵỷỹ]", "y", s)
        s = re.sub(r"[ỲÝỴỶỸ]", "Y", s)
        s = re.sub(r"[Đ]", "D", s)
        s = re.sub(r"[đ]", "d", s)
        return s 
        
    @staticmethod
    def read_data_json(path):
        with open(path, "r") as f:
            data = json.load(f)
            return data

    @staticmethod
    def write_data_json(path, data):
        with open(path, "w", encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=True, indent=4, cls=Encoder)
            f.close()
 