

import pprint

import asyncio
from pyppeteer import launch
from urllib.parse import urlparse
from search_engine_parser.core.engines.bing import Search as BingSearch
from search_engine_parser.core.engines.google import Search as GoogleSearch
from search_engine_parser.core.engines.yahoo import Search as YahooSearch
# AIzaSyCWxmH07ZSIbeD-WIjzctN96IbJj9lWz90
async def main(url):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto(url)
    await page.screenshot({'path': 'example.png'})


    xpath_name =  '/html/body/section/div[1]/div/aside[2]/h1'
    xpath_price = '/html/body/section/div[1]/div/aside[2]/strong'
    xpath_list_price = '/html/body/section/div[1]/div/aside[2]/div[2]/div/p'

    names = await page.xpath(xpath_name)
    prices = await page.xpath(xpath_price)
    list_prices = await page.xpath(xpath_list_price)

    name = await page.evaluate("e => e.innerText", names[0])
    price = await page.evaluate("e => e.innerText", prices[0])
    # list_price = await page.evaluate("e => e.innerText", list_prices[0])


    print('name',name)
    print('price',price)
    print('list_price',list_price)

    await browser.close()

def get_domain(url):
    domain = urlparse(url).netloc
    return ('.'.join(domain.split('.')[-2:]))

def get_search_results(search_term):
    search_args = (search_term, 1)
    gsearch = GoogleSearch() 
    gresults = gsearch.search(*search_args,  hl="vi") 
    
    for result in gresults: 
        result['domain'] = get_domain(result['links'])
    
    ALLOWED_DOMAINS = [
        # 'apple.com',
        'topzone.vn',
        # 'uscom.vn',
        # 'mainguyen.vn',
        # 'shopdunk.com',
        # 'ionevn.vn',
        # 'thegioididong.com',
        # 'didongviet.vn',
        # 'anhducdigital.vn',
        # 'websosanh.vn',
    ]

    gresults = list(filter(lambda x: x['domain'] in ALLOWED_DOMAINS, gresults)) 
    asyncio.get_event_loop().run_until_complete(main(gresults[0]['links']))


search_term = 'Apple Watch Ultra GPS + Cellular 49mm size M/L'

get_search_results(search_term)