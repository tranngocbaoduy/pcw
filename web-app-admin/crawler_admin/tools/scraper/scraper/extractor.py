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
from tools.scraper.scraper.items import ProductItem, RawProductItem
from tools.scraper.scraper.utils import CrawlingHelper, SettingService
from price_parser import Price
from bs4 import BeautifulSoup
from lxml import etree

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
    def handle_extract_information_from_json(response, domain, list_seller):
        base_item = PageItem()
        base_item["url"] = response["url"]
        base_item["base_encoded_url"] = response["base_encoded_url"]
        if len(response["base_encoded_url"]) > 250:
            print(response)
        base_item["domain"] = response["domain"]
        base_item["created_date"] = response["created_date"]
        base_item["is_api"] = response["is_api"]
        base_item["agency"] = response.get("agency", "")

        setting_brand_items = SettingService.get_all_setting_brand_items()
        product_item = Product()
        product_item["id_pcw"] = response["id_pcw"]
        product_item["name"] = response["name"].strip()
        product_item["clean_name"] = ExtractorService.handle_get_clean_name(
            response["name"]
        ).strip()
        product_item["category_code"] = response["category_code"]
        product_item["main_category_code"] = response.get("main_category_code", "NONE")
        product_item["category_code_from_title"] = ExtractorService.handle_get_category(
            response["name"]
        )
        product_item["brand_from_title"] = SettingService.get_brand_from_name(
            response["name"], setting_brand_items
        )

        if domain == "lazada.vn":
            product_item["slug_id"] = response["itemUrl"].replace(
                "//www.lazada.vn/products", ""
            )
            product_item["brand"] = response["brandName"].strip()
            product_item["image"] = [response["image"].strip()]
            if response.get("sellerName", ""):
                product_item["shop_item"] = {
                    "shop_id": response.get("sellerId", ""),
                    "shop_name": response.get("sellerName", ""),
                }
            else:
                product_item["shop_item"] = None
            product_item["price"] = response.get("price", 0)
            product_item["list_price"] = response.get(
                "originalPrice", response.get("price", 0)
            )
            product_item["stock"] = 10 if response["inStock"] else 0
            product_item["historical_sold"] = 0
            product_item["liked_count"] = 0
            product_item["shop_location"] = response.get("location", "Lazada Mall")
            product_item["item_rating"] = {
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
            product_item["product_code"] = ExtractorService.handle_get_code(
                response["name"],
                response["category_code"],
                product_item["brand"].lower(),
            )
            # product_item['content'] = response['short_description'].strip()
            product_item["voucher_info"] = None
            product_item["description"] = response.get("description", [])

        if domain == "tiki.vn":
            official_shop = list(
                filter(
                    lambda x: x.get("id", "") == response.get("shopid", None),
                    list_seller,
                )
            )

            if len(official_shop) == 1:
                official_shop = official_shop[0]
                product_item["shop_item"] = {
                    "shop_id": official_shop.get("id", ""),
                    "shop_name": official_shop.get("seller_name", ""),
                    "shop_logo": official_shop.get("logo", ""),
                    "shop_level": official_shop.get("store_level", "NONE"),
                    "shop_url": official_shop.get("url_slug", ""),
                }
            else:
                official_shop = None
                product_item["shop_item"] = None

            product_item["slug_id"] = "/{}".format(response["url_key"])
            product_item["brand"] = response["brand_name"].strip()
            product_item["image"] = [response["thumbnail_url"].strip()]
            product_item["price"] = response["price"]
            product_item["list_price"] = response["list_price"]
            product_item["stock"] = (
                response["stock_item"]["qty"] if response["stock_item"] else 0
            )
            product_item["historical_sold"] = (
                response["quantity_sold"]["value"] if response["quantity_sold"] else 0
            )
            product_item["liked_count"] = 0
            product_item["shop_location"] = (
                official_shop.get("seller_address", "").split(",")[-1].strip()
                if official_shop and official_shop.get("seller_address", "")
                else "Tiki Trading"
            )
            product_item["item_rating"] = {
                "rating_star": int(response["rating_average"]),
                "rating_count": [
                    response["review_count"],
                    response["review_count"],
                    0,
                    0,
                    0,
                    0,
                ],
                "rcount_with_context": response["review_count"],
                "rcount_with_image": 0,
            }
            product_item["product_code"] = ExtractorService.handle_get_code(
                response["name"],
                response["category_code"],
                product_item["brand"].lower(),
            )
            # product_item['content'] = response['short_description'].strip()
            product_item["voucher_info"] = None
            product_item["description"] = [response.get("short_description", "")]

        if domain == "shopee.vn":
            official_shop = list(
                filter(
                    lambda x: x.get("shopid", "") == response.get("shopid", None),
                    list_seller,
                )
            )
            if len(official_shop) == 1:
                official_shop = official_shop[0]
                product_item["shop_item"] = {
                    "shop_id": official_shop.get("shopid", ""),
                    "shop_name": official_shop.get("name", ""),
                    "shop_level": official_shop.get("store_level", ""),
                }
            else:
                official_shop = None
                product_item["shop_item"] = None

            url_obj = urlparse(response["url"])
            slug_arr = url_obj.path.split(".")
            product_item["slug_id"] = ".".join(slug_arr[:-2])
            product_item["brand"] = response["brand"]
            product_item["image"] = [
                "https://cf.shopee.vn/file/{}".format(image)
                for image in response["images"]
            ]
            product_item["stock"] = response["stock"]
            product_item["item_rating"] = response["item_rating"]
            product_item["historical_sold"] = response["historical_sold"]
            product_item["liked_count"] = response["liked_count"]
            product_item["shop_location"] = response["shop_location"]
            product_item["price"] = int(response["price"]) / 100000
            product_item["list_price"] = int(response["price_max"]) / 100000
            product_item["slug_id"] = response["slug_id"]
            product_item["voucher_info"] = response["voucher_info"]

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
                    product_item["brand"] == 0
                    or product_item["brand"].lower() not in not_allow_brand
                    or len(product_item["brand"]) == 0
                )
                and product_item["brand_from_title"]
                and len(product_item["brand_from_title"]) != 0
            ):
                product_item["brand"] = product_item["brand_from_title"]
            product_item["product_code"] = ExtractorService.handle_get_code(
                response["name"],
                response["category_code"],
                product_item["brand"].lower(),
            )
            product_item["description"] = []

        merged_item = dict()
        merged_item.update(base_item)
        merged_item.update(product_item)

        return merged_item

    @staticmethod
    def handle_extract_information_from_html(html_text, xpath_items):
        parsed_html = BeautifulSoup(html_text, "html.parser")
        dom = etree.HTML(str(parsed_html))

        item = Product()
        for name, selector in xpath_items.items():
            if name == "name":
                content = dom.xpath("{}//text()".format(selector))
                item[name] = ExtractorService.handle_crawl_content(content)
                item["product_code"] = ExtractorService.handle_get_code(content)
                item["category_code"] = ExtractorService.handle_get_category(content)
            elif name == "price" or name == "list_price":
                # many opinion
                item[name] = ExtractorService.handle_get_currency(dom, selector)
            elif name == "image":
                item[name] = ExtractorService.handle_get_list_image(dom, selector)
            else:
                content = dom.xpath("{}//text()".format(selector))
                item[name] = ExtractorService.handle_crawl_content(content)

        item = ExtractorService.handle_compare_list_price_and_price(item)

        return dict(item)

    @staticmethod
    def get_html_from_zip(compress_html):
        return zlib.decompress(compress_html).decode("utf-8")

    @staticmethod
    def get_html_from_path(path):
        with open(path, "r") as f:
            return f.read()

    @staticmethod
    def handle_crawl_content(text):
        return "".join(text).strip().lower()

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
        dict_replace_word = {}
        if category == "ELECTRIC_STOVE":
            list_stop_word = ["papa", "cook"]
            is_allowed_2_digits = False
        elif category == "PHONE":
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
    def handle_get_code(text, category, brand):
        (
            _,
            _,
            _,
            _,
            dict_replace_word,
            allowed_brand,
        ) = ExtractorService.get_config_filter_of_category(category)
        if brand in allowed_brand or len(allowed_brand) == 0:
            text = ExtractorService.replace_word_consistent(
                text.lower(), dict_replace_word
            )
            text = ExtractorService.handle_clean_code(text)
            text = re.sub(" +", " ", text)
            if brand == "apple":
                brand = "iphone"
            split_str_name = text.split(" ")
            if brand in split_str_name:
                index_of_brand = split_str_name.index(brand)
                last_n_word = ExtractorService.get_last_n_word(
                    split_str_name, index_of_brand, category, n=1
                )
                if len(last_n_word) == 0:
                    return "NONE"
                return brand + " " + " ".join(last_n_word)
        return "NONE"

    @staticmethod
    def handle_clean_code(text):
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

        text = text.split(" ")
        response = []
        for t in text:
            unicode_text = t.encode("ascii", errors="ignore").strip().decode("ascii")
            if unicode_text == t:
                response.append(unicode_text)
        return " ".join(response)

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
    def handle_get_clean_code(text):
        text = text.strip().lower().split(" ")
        with open("product_crawler/spiders/setting/common.txt") as f:
            common_words = [f.replace("\n", "").strip() for f in f.readlines()]
        words1 = set(text)
        return " ".join(
            list(filter(lambda x: len(x) > 4, list(words1.difference(common_words))))
        )

    @staticmethod
    def handle_compare_list_price_and_price(item):
        if item["price"] is None and item["list_price"]:
            item["price"] = item["list_price"]
            item["list_price"] = None
        elif (
            item["price"] and item["list_price"] and item["price"] > item["list_price"]
        ):
            item["list_price"], item["price"] = item["price"], item["list_price"]
        return item

    @staticmethod
    def handle_get_list_image(dom, selector_items):
        # CrawlingHelper.log('selector: {}'.format(','.join(selector_items)))
        image_urls = []
        for selector in selector_items:
            try:
                image_parent_element = dom.xpath("{}".format(selector))[0]
                image_element_items = list(image_parent_element.iter("img"))
                for img_element in image_element_items:
                    src = img_element.attrib.get("src")
                    if src:
                        if "https:" not in src:
                            src = "https:{}".format(src)
                        image_urls.append(src)
            except:
                print("not image")
        # CrawlingHelper.log('\n'.join(image_urls))
        return image_urls

    @staticmethod
    def handle_get_currency(dom, selector):
        for sel in selector:
            content = dom.xpath("{}//text()".format(sel))
            price = ExtractorService.get_currency_from_text(content)
            if price:
                return price
        return None

    @staticmethod
    def get_currency_from_text(text):
        price = Price.fromstring("".join(text).strip())
        if price.amount_float and price.amount_float > float(999):
            return price.amount_float
        return None

    @staticmethod
    def handle_get_category(text):
        text = "".join(text).strip().lower()
        file_dir = os.path.join(root_dir, "product_crawler/product_type")
        with open(
            os.path.join(
                root_dir, "product_crawler/spiders/setting/category_code_priority.json"
            )
        ) as f:
            category_code_files = json.load(f)
            f.close()
        product_type_file_dirs = os.listdir(file_dir)
        product_types = []
        for _dir in product_type_file_dirs:
            if ".txt" not in _dir:
                continue
            else:
                product_type = _dir.split(".")[0]
                words2 = [
                    i.replace("\n", "").lower()
                    for i in open(os.path.join(file_dir, _dir)).readlines()
                ]
                is_exist = False
                for word in words2:
                    if word in text:
                        is_exist = True
                        break
                if is_exist:
                    product_types.append(product_type)
        if len(product_types) != 0:
            type_items = []
            for product_type in product_types:
                if product_type in category_code_files.keys():
                    type_items.append(category_code_files[product_type])
            type_items = sorted(type_items, key=lambda x: x["priority"], reverse=True)
            return type_items[0]["code"]
        return "OTHER"

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

    @staticmethod
    def calculate_score(base_item):
        total_score = 0
        # base score
        base_score = 0
        # keys = ['url', 'base_encoded_url', 'stock', 'item_rating', 'domain', 'created_date', 'is_api', 'id_pcw', 'name', 'product_code', 'category_code', 'brand', 'image', 'price', 'list_price', 'content']
        # for key in keys:
        #     if key in base_item.keys() and base_item[key]:
        #         base_score += 1
        # base_score = base_score / len(keys)

        # score for rating
        if (
            base_item["item_rating"]
            and str(base_item["item_rating"]["rating_star"]) != "0"
        ):
            base_score += 2
        if base_item["price"] != base_item["list_price"]:
            base_score += 0.5
        if base_item["historical_sold"] and str(base_item["historical_sold"]) != "0":
            base_score += 0.5
        if base_item["liked_count"] and str(base_item["liked_count"]) != "0":
            base_score += 0.5
        if base_item["stock"] and str(base_item["stock"]) != "0":
            base_score += 0.5
        if base_item["agency"] in ["mall", "tiki", "lazmall"]:
            base_score += 2
        if base_item["agency"] in ["shopee"]:
            base_score += 1

        if (
            base_item["shop_item"] != None
            and base_item["shop_item"].get("store_level", "") == "TRUSTED_STORE"
        ):
            base_score += 6
        elif (
            base_item["shop_item"] != None
            and base_item["shop_item"].get("store_level", "") == "OFFICAL_STORE"
        ):
            if base_item["category_code"] == "FRIDGE":
                base_score += 5
            if base_item["category_code"] == "TELEVISION":
                base_score += 5
            if base_item["category_code"] == "PHONE":
                base_score += 4
        elif base_item["shop_item"] != None:
            if base_item["category_code"] == "FRIDGE":
                base_score += 4
            if base_item["category_code"] == "TELEVISION":
                base_score += 4
            if base_item["category_code"] == "PHONE":
                base_score += 3
        else:
            base_score += 2
        # print(base_score , rating_score , stock_score, (base_score + rating_score + stock_score) / 3)
        return base_score / 12

    @staticmethod
    def make_new_dir(
        init_dir,
        id_pcw,
        init_category_code,
        update_category_code,
        brand_name,
        allowed_category,
        from_dir="data_crawler",
    ):
        _dir_save_data = ""
        # change name file BASE_URL_ENCODED => ID
        init_dir = os.path.join("/".join(init_dir.split("/")[:-1]), id_pcw)
        init_category_code = init_category_code.replace(" ", "_")
        update_category_code = update_category_code.replace(" ", "_")

        if update_category_code in allowed_category:
            # change from data_crawler => data folder
            _dir_save_data = init_dir.replace(from_dir, "data").replace(
                init_category_code, update_category_code
            )

            # add brand name to path
            _dir_save_data = _dir_save_data.replace(
                update_category_code, "{}/{}".format(update_category_code, brand_name)
            )

            if not os.path.exists("/".join(_dir_save_data.split("/")[:-1])):
                os.makedirs("/".join(_dir_save_data.split("/")[:-1]))
            _dir_save_data = "{}.json".format(_dir_save_data)

        return _dir_save_data

    @staticmethod
    def get_config_item(domain, category):
        config = ExtractorService.read_data_json(
            os.path.join(
                root_dir,
                "product_crawler/spiders/setting/{}/{}.json".format(domain, category),
            )
        )

        ALLOWED_DOMAIN = config["ALLOWED_DOMAIN"]
        START_URL = config["START_URL"]
        START_PAGE = config["START_PAGE"]
        CLASS_PARENT = config["CLASS_PARENT"]
        XPATH_ITEMS = {}
        for key, value in config["XPATH_ITEMS"].items():
            XPATH_ITEMS[key.replace("_XPATH", "").lower()] = value

        config["XPATH_ITEMS"] = XPATH_ITEMS
        return config

    # @staticmethod
    # def get_list_seller(domain):
    #     list_seller = []
    #     if domain == 'tiki':
    #         list_seller = ExtractorService.read_data_json(os.path.join(root_dir, 'product_crawler/service/supplier/tiki.json'))
    #     if domain == 'shopee' or domain == 'mall':
    #         list_seller = ExtractorService.read_data_json(os.path.join(root_dir, 'product_crawler/service/supplier/shopee.json'))
    #     list_seller = list(filter(lambda x: x, list_seller))
    #     return list_seller

    # @staticmethod
    # def is_valid_product_of_lazmall(base_item):
    #     categories = base_item.get('categories', [])
    #     if base_item['category_code'] == 'TELEVION':
    #         if 4403 not in categories or 4549 not in categories: return False
    #     if base_item['category_code'] == 'PHONE':
    #         if 4402 not in categories or 4518 not in categories: return False
    #     if base_item['category_code'] == 'FRIDGE':
    #         if 10100871 not in categories or 12625 not in categories: return False
    #     return True

    # @staticmethod
    # def recover_handle_filter_data(domain, allowed_category, data_crawler_dir='data_crawler_shopee'):
    #     # recover from crawler data => filter to save data
    #     setting_brand_items = SettingService.get_all_setting_brand_items()
    #     list_seller = ExtractorService.get_list_seller(domain)
    #     all_item_dirs = CrawlingHelper.get_all_goods_item_dirs(main_dir='product_crawler/{}'.format(data_crawler_dir), allowed_category=allowed_category)
    #     success_item = 0
    #     stat_score = {}
    #     failed_lazmall_item = 0

    #     for _dir in tqdm(all_item_dirs, desc='recover_handle_filter_data {}'.format(data_crawler_dir)):
    #         # if len(_dir) < 240:
    #         # try:
    #             base_item = ExtractorService.read_data_json(os.path.join(_dir, 'data.json'))
    #             # if base_item['domain'] != 'shopee.vn': continue
    #             if base_item['is_api']:
    #                 if domain == 'lazmall' and not (ExtractorService.is_valid_product_of_lazmall(base_item)):
    #                     failed_lazmall_item +=1
    #                     continue

    #                 # read data and classify product by brand
    #                 base_item = ExtractorService.handle_extract_information_from_json(base_item, base_item['domain'], list_seller)
    #                 not_allow_brand = ['nobrand','no brand', 'No brand','No Brand', 0,'0', '', 'none']
    #                 if (base_item['brand'] == 0 or \
    #                     base_item['brand'].lower() in not_allow_brand  or \
    #                     len(base_item['brand']) == 0) and \
    #                     base_item['brand_from_title'] and len(base_item['brand_from_title']) != 0:
    #                     base_item['brand'] = base_item['brand_from_title']

    #                 score = ExtractorService.calculate_score(base_item)
    #                 base_item['score'] = score
    #                 if str(score) not in stat_score.keys():
    #                     stat_score[str(score)] = 1
    #                 else:
    #                     stat_score[str(score)] += 1
    #                 if score >= 0.5 and base_item['brand'].lower() not in not_allow_brand and len(base_item['brand']) != 0 and (base_item['brand']) != '0' :
    #                     _dir_save_data = ExtractorService.make_new_dir(_dir, str(base_item['id_pcw']), base_item['category_code'], base_item['category_code'], base_item['brand'].lower(),from_dir=data_crawler_dir,allowed_category=allowed_category)
    #                     if len(_dir_save_data) != 0:
    #                         success_item += 1
    #                         ExtractorService.write_data_json(_dir_save_data, base_item)
    #                 # else:
    #                     # print('brand', base_item['brand'], base_item['brand_from_title'])
    #             else:
    #                 if base_item['category_code'] in ['NOISE']: continue
    #                 html_text = ExtractorService.get_html_from_path(os.path.join(_dir, 'index.html'))
    #                 if len(html_text) == 0: continue
    #                 if base_item['category_code'] not in allowed_category: continue
    #                 name = base_item['domain'].split('.')[0]
    #                 config_item = ExtractorService.get_config_item(name, base_item['category_code'].lower())
    #                 xpath_items = config_item['XPATH_ITEMS']

    #                 # get old item and new item
    #                 product_item = ExtractorService.handle_extract_information_from_html(html_text, xpath_items)
    #                 base_item['sk'] = '{}#{}#{}'.format(product_item['category_code'], product_item['product_code'], base_item['base_encoded_url'])

    #                 # get brand from name
    #                 brand_name = SettingService.get_brand_from_name(base_item['name'], setting_brand_items)
    #                 if len(brand_name) == 0: continue
    #                 base_item['brand'] = brand_name
    #                 base_item.update(product_item)
    #                 # get dir to save new item
    #                 _dir_save_data = ExtractorService.make_new_dir(_dir, base_item['id_pcw'], base_item['category_code'], product_item['category_code'], brand_name.lower(),from_dir=data_crawler_dir, allowed_category=allowed_category)
    #                 if len(_dir_save_data) != 0 and base_item['price'] and base_item['list_price']:
    #                     success_item += 1
    #                     ExtractorService.write_data_json(_dir_save_data, base_item)
    #         # except:
    #         #     print('Not file', _dir)
    #         #     a=0

    #     CrawlingHelper.log('Add success {} / {} items'.format(success_item, len(all_item_dirs)))
    #     CrawlingHelper.log('Stat score {}'.format(stat_score))
