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