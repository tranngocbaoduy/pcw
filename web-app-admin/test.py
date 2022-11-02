import json
import base64
from bs4 import BeautifulSoup
from lxml import etree 

def read_html_page(path):
    try:
        with open(path, 'r') as f:
            return f.read()
    except e as Exception:
        print(e)
    return None 

def get_basic_info(res_info):
    basic_info = {}
    basic_info['name'] = res_info.get('name', '')
    basic_info['description'] = res_info.get('description', '')
    basic_info['url'] = res_info.get('url', '')
    basic_info['image'] = res_info.get('image', '')
    basic_info['brand'] = res_info.get('brand', '')

    if res_info.get('offers'):
        basic_info['price'] = res_info['offers'].get('price', '')
        if basic_info['price'] == '':
            basic_info['price'] = res_info['offers'].get('lowPrice', '')
            basic_info['list_price'] = res_info['offers'].get('highPrice', '')
        else:
            basic_info['list_price'] = basic_info['price']
        
        if res_info['offers'].get('seller'):
            basic_info['seller'] = {
                "name": res_info['offers']['seller'].get('name', ''),
                "url": res_info['offers']['seller'].get('url', ''),
                "image": res_info['offers']['seller'].get('image', ''), 
            }
            if res_info['offers']['seller'].get('aggregateRating'):
                basic_info["seller"]["star"] = res_info['offers']['seller']['aggregateRating'].get('ratingValue', '')
                basic_info["seller"]["review"] = res_info['offers']['seller']['aggregateRating'].get('ratingCount', '')
        
    if res_info.get('aggregateRating'):
        basic_info['star'] = res_info['aggregateRating'].get('ratingValue', '')
        basic_info['review'] = res_info['aggregateRating'].get('ratingCount', '')
        
    return basic_info

def urlsafe_encode(url):
    return (
        base64.urlsafe_b64encode(url.encode("utf-8")).decode("utf-8").rstrip("=")
        if url
        else ""
    )

def get_basic_category(res_info):
    tree_category = res_info.get('itemListElement', [])
    list_category = []
    if tree_category and len(tree_category) != 0: 
        tree_category = sorted(tree_category, key=lambda x: x.get('position', 1), reverse=False)
        print('tree_category',tree_category)
        index = 0
        for category in tree_category: 
            if category.get('position') == 1: 
                index += 1
                continue
            item = category.get('item', None)
            if item == None: continue 
            params = {
                "id": urlsafe_encode(item.get('@id', '')),
                "url": item.get('@id', ''),
                "name": item.get('name', ''),
            }
            if index > 1 and index - 1 <= len(tree_category):
                prev_item = tree_category[index - 1].get('item', None)
                params['parent'] =  urlsafe_encode(prev_item.get('@id', ''))
            
            if index + 1 < len(tree_category):
                next_item = tree_category[index + 1].get('item', None)
                params['child'] =  urlsafe_encode(next_item.get('@id', ''))

            list_category.append(params)
            index += 1
    return list_category


def main():
    path = 'crawler_admin/raw_html/1-C%E1%BA%B7p-B%E1%BB%8Dc-Ng%C3%B3n-Tay-Ch%C6%A1i-Game-Pubg-Si%C3%AAu-M%E1%BB%8Fng-Tho%C3%A1ng-Kh%C3%AD-i.293689217.16575434540/index.html'
    html_page = read_html_page(path) 
    soup = BeautifulSoup(html_page, "html.parser")
    dom = etree.HTML(str(soup))
    tag = dom.getiterator(tag='script')
    basic_info = {}
    for i in tag:
        if i.get('type') == 'application/ld+json':
            res_info = json.loads(i.text)
            if res_info.get('@type') == 'Product': 
                basic_info.update(get_basic_info(res_info)) 
            if res_info.get("@type") == "BreadcrumbList":
                tree_category = get_basic_category(res_info)
                basic_info.update({
                    "tree_category": tree_category,
                    "category": tree_category[-2]
                }) 

    print('basic_info', basic_info)
    # print(tag)
    # name = dom.xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div[1]/span/text()')
    # list_price = dom.xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div[3]/div/div/div/div/div/div/text()')
    # price = dom.xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div[3]/div/div/div/div/div/div/text()')
    # stock = dom.xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div[4]/div/div[3]/div/div[2]/div[2]/div[2]/text()')
    # description = dom.xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[4]/div[2]/div[1]/div[1]/div[2]/text()')
    # review = dom.xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div[2]/div[2]/div[1]/text()')
    # sold = dom.xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div[2]/div[3]/div[1]/text()')
    # voucher = dom.cssselect('.voucher-ticket')
    # location = dom.xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div[4]/div/div[2]/div/div[3]/div[2]/div[1]/div[2]/div[2]/div[2]/div/span/text()')
    # star = dom.xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div[2]/div[1]/div[1]/text()')
    # category = dom.xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[3]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/text()')
    # print('rés', {
    #     "name": name,
    #     "list_price": list_price,
    #     "price": price,
    #     "stock": stock,
    #     "review": review,
    #     "stock": stock,
    #     "sold": sold,
    #     "star": star,
    #     "category": category,
    #     "location": location,
    #     # "voucher": voucher,
    #     "description": description,
    # })

if __name__ == '__main__':
    main()
