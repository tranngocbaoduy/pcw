import itertools

def get_combination_words(sentence):
    words = sentence.split(' ')
    len_words = len(words)
    result = [] 
    for n in range(1, len_words):
        for res in itertools.combinations(words, n):
            result.append(" ".join(res))  
    print(result) 

# get_combination_words('iphone 14 256GB')

import re
from price_parser import Price
def get_currency_from_text(text):
    # text = re.sub(r"[{}\\*/.]", "", text)
    price = Price.fromstring("".join(text).strip())
    if price.amount_float and price.amount_float > float(999):
        return price.amount_float
    return None

print(get_currency_from_text('34.820.000₫ *'))


from decimal import *

p1 = Decimal(45990000)
p2 = Decimal(49990000)
if p1 and p1 > 0 and p2 and p2  > 0:
    if p1 * 2 < p2:
        p2 = p1
        discount_rate = 0
    else:
        discount_rate = 100 - int(Decimal(p1) / Decimal(p2) * 100)

print(discount_rate)
print(45990000 / 49990000 * 100)