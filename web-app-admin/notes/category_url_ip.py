
import string
import random 
import re 
from pprint import pprint
# type: string
# gen_number: integer
# ram_size: integer
# storage_size: integer
# color: string

class ExtractInfoIphone(object):

    @staticmethod
    def extract_gen_number(url):
        regexs = [
            'iphone-(\d+)-pro-max',
            'iphone-(\d+)-pro',
            'iphone-(\d+)-mini',
            'iphone-se',
            'iphone-se(-\d+)',
            'iphone-(\d+)'
        ] 
        for regex in regexs:
            match = re.search(regex, url)
            if match:
                return match.group()
        return ''

    @staticmethod
    def extract_ram_size(url):
        regexs = [
            '(\d+)tb', 
            '(\d+)gb', 
        ] 
        for regex in regexs:
            match = re.search(regex, url)
            if match:
                return match.group()
        return ''


    @staticmethod
    def extract_is_used(url):
        regexs = [
            '-cu',  
        ] 
        for regex in regexs:
            match = re.search(regex, url)
            if match:
                return True
        return False

    @staticmethod
    def extract_info(base_url, name_sp=""):
        base_url = base_url.lower()
        name_sp = name_sp.lower()
        gen_number = ExtractInfoIphone().extract_gen_number(base_url)
        ram_size = ExtractInfoIphone().extract_ram_size(base_url) 
        is_used = ExtractInfoIphone().extract_is_used(base_url)
        if ram_size and gen_number and not is_used:
            return gen_number, ram_size, is_used
        if gen_number and not is_used and ram_size == '' and name_sp != '':
            ram_size = ExtractInfoIphone().extract_ram_size(name_sp) 
            if ram_size and gen_number and not is_used:
                return gen_number, ram_size, is_used
        return None, None, None

    @staticmethod
    def is_candidate_url(base_url, name_sp=""): 
        gen_number, ram_size, _ = ExtractInfoIphone().extract_info(base_url, name_sp)
        if gen_number and ram_size:
            return True
        return False

with open('./notes/data.txt', 'r') as f:
    data = f.read()
    data = data.split('\n')

final_data = []

for i in data:
    url, name_sp = i.split('\t')
    gen_number, ram_size, is_used = ExtractInfoIphone().extract_info(url, name_sp) 
    if ram_size and gen_number and not is_used:
        final_data.append({
            'gen_number': gen_number,
            'ram_size': ram_size,
            'url': i,            
        })
    else:
        print(i)
        # print('[data] =>',gen_number, '\t',ram_size, '\t', is_used,'\t',i) 

group = {}
final_data = list(sorted(final_data, key=lambda x: (x['gen_number'], x['ram_size']), reverse=True))
# for i in final_data: 
#     if '{}#{}'.format(i['gen_number'], i['ram_size']) not in group:
#         group['{}#{}'.format(i['gen_number'], i['ram_size'])] = []
#     group['{}#{}'.format(i['gen_number'], i['ram_size'])].append(i['url'])
#     print('{} \t\t- {} - {}'.format(i['gen_number'], i['ram_size'],i['url']))  

print(len(final_data))
# for key, value in group.items():
#     print('{}'.format(key))
#     pprint(value)
    