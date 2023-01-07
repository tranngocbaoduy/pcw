
import string
import random 

def id_generator(size=12):
    chars= string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for x in range(size))

print('id_generator',id_generator())
print('id_generator',id_generator())
print('id_generator',id_generator())
print('id_generator',id_generator())
print('id_generator',id_generator())
print('id_generator',id_generator())
print('id_generator',id_generator())

import re
from urllib.parse import urljoin, urlparse

def get_url_formatted(base_url):
    base_url_formatted = base_url
    if ('index.html' in base_url):
        base_url_formatted = re.sub(r'(index\.html(\?.*)*$)', '', base_url)
    elif ('.html' in base_url):
        base_url_formatted = re.sub(r'(\.html(\?.*)*$)', '', base_url)
        temp = base_url_formatted.split('/')
        base_url_formatted = '/'.join(temp[:-1])
    return base_url_formatted

def get_clean_url(url):
    o = urlparse(url)
    return o.scheme + "://" + o.netloc + o.path


print(get_url_formatted('http://127.0.0.1:8000/#/crawler/sitemap/'))
print(get_url_formatted('https://www.geeksforgeeks.org/slugfield-django-models/'))
print(get_url_formatted('https://www.geeksforgeeks.org/slugfield-django-models/index.html'))
print(get_url_formatted('https://bachlongmobile.com/dien-thoai.html'))
print(get_url_formatted('https://bachlongmobile.com/index.html'))


print(get_clean_url('http://127.0.0.1:8000/#/crawler/sitemap/'))
print(get_clean_url('https://www.geeksforgeeks.org/slugfield-django-models/'))
print(get_clean_url('https://www.geeksforgeeks.org/slugfield-django-models/index.html'))
print(get_clean_url('https://bachlongmobile.com/dien-thoai.html'))
print(get_clean_url('https://bachlongmobile.com/index.html'))