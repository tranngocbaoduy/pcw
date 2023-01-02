import urllib
import requests
from pprint import pprint
from gse import GoogleSearchEngine 

query = "Iphone 14 pro" 

allowed_sites = [
    # "https://fptshop.com.vn/",
    "https://topzone.vn/",
    "https://mac24h.vn/",
    "https://bachlongmobile.com/",
    "https://cellphones.com.vn/",
    "https://www.thegioididong.com/",
    # "https://laptopvang.com/",
    "https://viettelstore.vn/",
] 

# for site in allowed_sites:
#     gs = GoogleSearchEngine(site)
#     url = gs.get_url_search(query)
#     results = gs.get_search_results(url)
#     pprint(results)


from urllib.parse import urlencode, urlparse
o = urlparse(url)
url_without_query_string = o.scheme + "://" + o.netloc + o.path
print('url_without_query_string',url_without_query_string)