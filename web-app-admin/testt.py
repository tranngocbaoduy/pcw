from gse import Response, GoogleSearchEngine, HTMLObject
from pprint import pprint
import uuid
import os

gse = GoogleSearchEngine()

search_term = "Iphone 14 pro 256GB"

allowed_sites = [
    # "https://fptshop.com.vn/",
    "https://topzone.vn/",
    "https://mac24h.vn/",
    "https://bachlongmobile.com/",
    "https://cellphones.com.vn/",
    "https://www.thegioididong.com/",
    "https://laptopvang.com/",
    "https://viettelstore.vn/",
]
 
for site_search in allowed_sites:
    url = gse.get_url_search(search_term=search_term, num=1, site_search=site_search)
    items = gse.get_search_results(url)
    print("[LEN] =>", len(items)) 
    for k in items: 
        print(k.link)
        h = HTMLObject(k.link)
        html_text = h.get_content()

        data_crawler_file_dir = "html/{}/{}".format(k.domain,k.base_encoded_url)
        if not os.path.exists(data_crawler_file_dir):
            os.makedirs(data_crawler_file_dir)
        with open("{}/index.html".format(data_crawler_file_dir), "w") as f:
            f.write(html_text)
            f.close()