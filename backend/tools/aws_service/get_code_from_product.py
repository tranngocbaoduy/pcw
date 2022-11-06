import os
import sys
import json
import glob
import tqdm
import base64
import re

from tqdm import tqdm
from json import JSONEncoder
from nlp2category import NLPCategory2Code

file_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(file_dir + "/../..")
sys.path.append(os.path.normpath(root_dir))


class GetCodeFromProduct:
    def __init__(self):
        self.ID2CATE_DICT = {}
        self.CATE2ID_DICT = {}
        self.CATEGORY_ITEM_SET = {}
        self.NEW_CATEGORY_ITEM_SET = {}
        self.SK2ITEM_DICT = {}
        self.SENT2SK_DICT = {}
        self.MODEL = {}
        self.EXCEPTION_BRANDS = [
            "vivo",
            "y1s",
            "a74",
            "y19",
            "y20s",
            "y72",
            "v20",
            "realme",
            "c21y",
            "mitsubishi",
            "xiaomi",
            "poco",
            "x3",
            "nfc",
            "9c",
            "9s",
            "f3",
            "mi",
            "10t",
            "samsung",
            "galaxy",
            "ultra",
            "4g",
            "5g",
            "a02s",
            "a11",
            "a12",
            "a21s",
            "a32",
            "a51",
            "a52",
            "a71",
            "s21",
            "s21+",
            "m11",
            "m12",
            "fe",
            "z",
            "fold2",
            "fold",
            "lg",
            "toshiba",
            "huawei",
            "note",
            "redmi",
            "oppo",
            "reno",
            "reno4",
            "reno5",
            "a15",
            "a15s",
            "a31",
            "a54",
            "a74",
            "a93",
            "a94",
            "nokia",
            "2.4",
            "3.4",
            "4.4",
            "c20",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
            "iphone",
            "plus",
            "pro",
            "promax",
            "max",
            "xr",
            "se",
            "mini",
            "vsmart",
            "active",
            "live",
            "joy",
            "star",
            "aris",
            "oneplus",
            "nord",
            "n10",
        ]

    def load_data(self):
        self.load_id_cate_config()
        self.items = self.get_all_page_item_processed()

    def get_all_page_item_processed(self):
        categories = glob.glob("{}/*".format(os.path.join(file_dir, "data/goods")))
        list_items = []
        for cate_path in categories:
            domain_items = glob.glob("{}/*".format(os.path.join(cate_path)))
            for domain_path in tqdm(domain_items, cate_path.split("/")[-1]):
                url_items = glob.glob("{}/*".format(os.path.join(domain_path)))
                for url_path in url_items:
                    item_paths = glob.glob("{}/*".format(os.path.join(url_path)))
                    with open(os.path.join(item_paths[0])) as f:
                        item = json.load(f)
                        f.close()
                    list_items.append(item)
        return list_items

    def load_id_cate_config(self):
        with open(os.path.join(file_dir, "category_config_custom.json"), "r") as f:
            self.ID2CATE_DICT = json.load(f)

        for k, v in self.ID2CATE_DICT.items():
            for cate in v:
                self.CATE2ID_DICT[cate] = k

    def classify(self):
        for i in self.items:
            self.SK2ITEM_DICT[i["SK"]] = i
            self.SENT2SK_DICT[i["NAME"]] = i["SK"]
        for item in self.items:
            code = self.CATE2ID_DICT[item["CATEGORY"]]
            if code not in self.CATEGORY_ITEM_SET.keys():
                self.CATEGORY_ITEM_SET[code] = [item]
            else:
                self.CATEGORY_ITEM_SET[code].append(item)

    def get_all_item_by_attr(self, id_cate, attr="NAME"):
        items = self.CATEGORY_ITEM_SET[id_cate]
        if attr == "URL":
            return list(map(lambda x: self.urlsafre_decode(x["SK"]), items))
        return list(map(lambda x: x[attr], items))

    def get_longest_sentence(self, sents):
        map_item = list(map(lambda x: len(x), sents))
        max_item = max(map_item)
        return sents[map_item.index(max_item)]

    def remove_open_close_sign(self, text):
        return text.replace("(", "").replace(")", "")

    def build(self):
        print("loading data...")
        self.load_data()
        self.classify()
        print("building...")
        for id_cate in tqdm(self.CATEGORY_ITEM_SET.keys()):
            corpus = self.get_all_item_by_attr(id_cate, attr="NAME")
            corpus_url = self.get_all_item_by_attr(id_cate, attr="URL")
            model = NLPCategory2Code(id_cate, corpus, corpus_url)
            model.build()
            self.MODEL[id_cate] = model
            new_category = []
            for index, sent in enumerate(corpus):
                SK = self.SENT2SK_DICT[sent]
                item = self.SK2ITEM_DICT[SK]
                list_code_product = model.get_code_of_sentence(sent)
                list_code_longest_product = model.get_code_longest_of_sentence(sent)
                list_code = [
                    list_code_product["by_init"],
                    list_code_product["by_name"],
                ]

                list_code_longest = [
                    list_code_longest_product["by_init"],
                    list_code_longest_product["by_name"],
                ]

                list_code = list(sorted(list_code, key=lambda x: len(x), reverse=True))
                list_code_longest = list(
                    sorted(list_code_longest, key=lambda x: len(x), reverse=True)
                )
                piority_code = (
                    list_code_longest
                    + list_code
                    + [list_code_longest_product["by_url"], list_code_product["by_url"]]
                )

                """
                    # find code by rule:
                    if code contain number and letter
                        if len < 5: plus exception word
                        else len < 16: assign for code
                    else:
                        find any word contain letter and number => assign for code
                    else:
                        find any exception word add to code
                    else:
                        get url longest to do code product
                """
                item["LIST_CODE_PRODUCT"] = piority_code
                for code in piority_code:
                    if self.is_contain_both_letter_and_number(code):
                        if (
                            len(
                                self.remove_open_close_sign(
                                    code.replace("GB", "").replace("/", "")
                                )
                            )
                            <= 5
                        ):
                            word_plus_more = []
                            word_gb = []
                            for word_in_name in item["NAME"].split(" "):
                                if (
                                    "GB" in word_in_name
                                    and len(
                                        self.remove_open_close_sign(
                                            word_in_name.replace("GB", "").replace(
                                                "/", ""
                                            )
                                        )
                                    )
                                    <= 4
                                ):
                                    word_gb.append(word_in_name)
                                if word_in_name.lower() in self.EXCEPTION_BRANDS:
                                    word_plus_more.append(
                                        self.remove_open_close_sign(
                                            word_in_name.lower()
                                        )
                                    )

                            if len(word_plus_more) != 0:
                                item["CODE_PRODUCT"] = "-".join(word_plus_more)
                                if len(word_gb) != 0:
                                    item[
                                        "CODE_PRODUCT"
                                    ] += "." + self.remove_open_close_sign(
                                        "-".join(word_gb)
                                    )
                                if code not in item["CODE_PRODUCT"]:
                                    item[
                                        "CODE_PRODUCT"
                                    ] += "." + self.remove_open_close_sign(code)
                                break
                            else:
                                continue
                        elif len(code) > 5 and len(code) < 16:
                            item["CODE_PRODUCT"] = self.remove_open_close_sign(code)
                            break

                if "CODE_PRODUCT" not in item.keys():
                    for code in piority_code:
                        if self.is_contain_both_letter_and_number(code):
                            item["CODE_PRODUCT"] = self.remove_open_close_sign(code)
                            break

                if "CODE_PRODUCT" not in item.keys():
                    word_plus_more = []
                    for word_in_name in item["NAME"].split(" "):
                        if word_in_name.lower() in self.EXCEPTION_BRANDS:
                            word_plus_more.append(
                                self.remove_open_close_sign(word_in_name.lower())
                            )

                    if len(word_plus_more) != 0:
                        item["CODE_PRODUCT"] = "-".join(word_plus_more)
                        flag = False
                        for word_item in word_plus_more:
                            if code.lower() in word_item:
                                flag = True
                        if flag:
                            item["CODE_PRODUCT"] += "." + self.remove_open_close_sign(
                                code
                            )
                        break
                    else:
                        item["CODE_PRODUCT"] = self.get_longest_sentence(
                            piority_code[4:]
                        )
                item["CODE_PRODUCT"] = (
                    item["CODE_PRODUCT"]
                    .replace("/", "-")
                    .replace(".", "-")
                    .replace("(", "-")
                    .replace(")", "-")
                )
                new_category.append(item.copy())
            self.NEW_CATEGORY_ITEM_SET[id_cate] = new_category

    def is_contain_both_letter_and_number(self, text):
        rx_number = re.compile("\d+")
        rx_letter = re.compile("[a-zA-Z]+")
        return (
            True
            if len(rx_number.findall(text)) != 0 and len(rx_letter.findall(text)) != 0
            else False
        )

    def urlsafre_encode(self, url):
        return (
            base64.urlsafe_b64encode(url.encode("utf-8")).decode("utf-8").rstrip("=")
            if url
            else ""
        )

    def urlsafre_decode(self, encoded_str):
        return (
            base64.urlsafe_b64decode(encoded_str + "===").decode("utf-8")
            if encoded_str
            else ""
        )
